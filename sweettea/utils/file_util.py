"""
Utility methods related to files or their respective paths
"""
import json
import mimetypes
import os
import shutil
import yaml
import zipfile
from clint.textui.progress import Bar as ProgressBar
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from sweettea.definitions import config_file_name, default_mime_type
from sweettea import log

JSON_EXT = 'json'
YAML_EXT = 'yaml'
ENV_EXT = 'env'


def is_json_file(path):
  return path.endswith('.{}'.format(JSON_EXT))


def is_yaml_file(path):
  return path.endswith('.{}'.format(JSON_EXT))


def is_env_file(path):
  return path.endswith('.{}'.format(JSON_EXT))


def file_ext(path):
  comps = path.rsplit('/', 1).pop().rsplit('.', 1)

  if len(comps) == 1:
    return ''

  return comps[1]


def json_load(path):
  with open(path) as f:
    return json.load(f)


def yaml_load(path):
  with open(path) as f:
    return yaml.load(f)


def config_file_path():
  return os.path.join(os.getcwd(), config_file_name)


def create_model_save_path(path, download_ext):
  """
  Create path to save a model to.
  Validate the provided and desired extensions are compatible.

  :param str path: Desired model path (either filename or directory)
  :param str download_ext: File extension of downloaded model content
  :return: Path to save model to.
  :rtype: str
  """
  archive = 'zip'  # All model folders should be downloaded as zip files.

  # Check if the specified model path is a directory
  is_dir = path.endswith('/') or ('.' not in path.split('/').pop())

  # Ensure downloaded file is a zip file if model path is a directory
  if is_dir:
    if download_ext != archive:
      log('Can\'t download model -- Specified model path was a directory, '
          'but downloaded model not a {} file.'.format(archive))
      exit(1)

    save_to = '.'.join((path.rstrip('/'), archive))
  else:
    ext = path.split('/').pop().split('.').pop()

    # If model is a file (not a dir), ensure its ext matches the downloaded file ext.
    if ext != download_ext:
      log('Can\'t donwload model -- Expected type: {}; Actual type: {}'.format(ext, download_ext))
      exit(1)

    save_to = path

  return save_to


def upsert_parent_dirs(filepath):
  """
  Similar to os.makedirs, but ignores filename and doesn't raise an error when
  a directory is already in existence...it just skips it.

  :param str filepath: File path to upsert all parent directories for
  """
  comps = [c for c in filepath.split('/') if c]
  comps.pop()

  if filepath.startswith('/'):
    path = '/'
  else:
    path = ''

  for dir in comps:
    path += (dir + '/')

    if not os.path.exists(path):
      try:
        os.mkdir(path)
      except:
        pass


def extract_in_place(archive_path):
  """
  Unpack a zipfile in place and remove it upon completion.

  Ex:
    extract_in_place('path/to/archive.zip')
    # => creates 'path/to/archive/' directory

  :param str archive_path: Path to zipfile
  :return: Path to directory where zipfile contents were extracted
  :rtype: str
  """
  # Comments using values from example of archive_path='/path/to/model.zip
  filename_w_ext = archive_path.split('/').pop()        # model.zip
  ext = filename_w_ext.split('.').pop()                 # zip
  extract_dir = archive_path[:-(len(ext) + 1)]          # /path/to/model

  # Remove the destination dir if it already exists
  if os.path.exists(extract_dir) and os.path.isdir(extract_dir):
    shutil.rmtree(extract_dir)

  # Unpack the archive
  archive = zipfile.ZipFile(archive_path)
  archive.extractall(extract_dir)
  archive.close()

  # Remove the archive file
  os.remove(archive_path)

  return extract_dir


def zip_dir(src_dir, dest_zip_file_path):
  path = src_dir.rstrip('/') + '/'

  # Ensure path exists.
  if not os.path.exists(path):
    log('No directory found at {}'.format(path))
    exit(1)

  # Upsert parent directories of destination zip path.
  os.makedirs(os.path.dirname(dest_zip_file_path), exist_ok=True)

  # Create new zip file.
  zf = zipfile.ZipFile(dest_zip_file_path, 'w', zipfile.ZIP_DEFLATED)

  try:
    # Walk over all tree contents of path
    contents = os.walk(path)

    # For each file and sub-dir inside source directory, write it into the zip file.
    for root, dirs, files in contents:
      for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        zf.write(dir_path, dir_path.replace(path, '', 1))

      for file_name in files:
        file_path = os.path.join(root, file_name)
        zf.write(file_path, file_path.replace(path, '', 1))

  except BaseException as e:
    # Exit anytime an error occurs.
    log('Error occurred while zipping directory: {}'.format(e))
    exit(1)
  finally:
    # Always close zipfile.
    zf.close()


def new_file_uploader(path, name='file', completion_msg='Done!', **kwargs):
  # Get file extension from path.
  ext = file_ext(path)

  # Append extension to name if extension is not empty.
  if ext:
    name = name + '.' + ext

  # Guess mime type from file path.
  mime_type = mimetypes.guess_type(path)[0] or default_mime_type

  # Create payload for uploading with file info attached.
  payload = kwargs
  payload['file'] = (name, open(path, 'rb'), mime_type)
  payload['ext'] = ext

  # Create a multipart encoder.
  encoder = MultipartEncoder(fields=payload)

  # Create progress callback, specifying message to show when upload completes.
  callback = file_upload_callback(encoder, completion_msg=completion_msg)

  # Return monitor for the encoder so we can track upload progress.
  return MultipartEncoderMonitor(encoder, callback)


def file_upload_callback(encoder, completion_msg=None):
  """
  Create a progress callback function for a multi-part file upload

  :param encoder:
    Multipart file encoder
    :type: requests_toolbelt.multipart.encoder.MultipartEncoder
  :param str completion_msg:
    Log to display when the file upload has completed
  :return: Upload progress callback function
  :rtype: function
  """
  # Create a progress bar with the given size, specifying which character to show for progress.
  bar = ProgressBar(expected_size=encoder.len, filled_char='=')

  # Function to be called as the upload progresses
  def callback(monitor):
    # If upload has completed...
    if monitor.bytes_read == encoder.len:
      # Hacking around this callback being called twice when completed.
      if not hasattr(monitor, 'finished'):
        setattr(monitor, 'finished', True)

        # Show upload progress.
        bar.show(monitor.bytes_read)

        # Display completion log if provided.
        if completion_msg:
          log(completion_msg)
    else:
      # Show upload progress.
      bar.show(monitor.bytes_read)

  return callback


class ProgressDownloadStream(object):
  """
  Progress bar buffer class that can monitor a file download by displaying
  progress to the user while also writing to the desired file.

  Basic usage:

    download_stream = ProgressDownloadStream(stream=api_response_obj,
                                             expected_size=total_file_bytes)

    download_stream.stream_to_file(desired_file_path)

  """

  def __init__(self, stream=None, expected_size=None, chunk_size=512):
    """
    :param stream:
      Streaming API response object returned by the 'requests' library
      :type: requests.Response
    :param int expected_size:
      Total size of file being downloaded (in bytes)
    :param int chunk_size:
      Chunk size to use when iterating over streamed response content
    """
    self.stream = stream
    self.prog_bar = ProgressBar(expected_size=expected_size, filled_char='=')
    self.progress = 0
    self.chunk_size = chunk_size

  def stream_to_file(self, path):
    """
    Download file to given path and display progress to user

    :param str path: Desired file path
    """
    # Using default state of files being overwritten for now
    if os.path.exists(path):
      os.remove(path)

    # Stream downloaded contents to file and show progress
    with open(path, 'wb') as f:
      for chunk in self.stream.iter_content(chunk_size=self.chunk_size):
        f.write(chunk)
        self.progress += int(len(chunk))
        self.prog_bar.show(self.progress)