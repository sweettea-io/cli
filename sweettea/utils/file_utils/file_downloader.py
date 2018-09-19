import os
from clint.textui.progress import Bar as ProgressBar
from sweettea import log
from sweettea.definitions import default_archive_fmt, tmp_model_archive_path
from sweettea.utils.file_utils import get_file_ext, upsert_parent_dirs, extract_zip


class FileDownloader(object):

  def __init__(self, api, default_name='file', default_file_type_header='Sweet-Tea-File-Type'):
    self.api = api
    self.default_name = default_name
    self.default_file_type_header = default_file_type_header

  def download(self, api_route, dest_path, payload=None, file_type_header=None, extract_archives=True):
    """
    Download a file from the SweetTea API

    * If the destination path has no file extension, it is assumed to be a directory.

    Potential success outcomes:

      - Destination path is a file:
        --> the file is saved at the destination path, as long as file types match

      - Destination path is a directory, the fetched file is an archive, and extract_archives is true:
        --> the archive will be extracted *as* this directory

      - Destination path is a directory and (the fetched file is an archive but extract_archives is false) or
        (the fetched file is not an archive):
        --> the file will be saved inside of the destination directory
    """
    resp = None
    payload = payload or {}
    file_type_header = file_type_header or self.default_file_type_header

    try:
      # Fetch the file from the API.
      resp = self.api.get(api_route, payload=payload, stream=True)
    except KeyboardInterrupt:
      exit()

    # Extract further info about the downloaded file.
    file_ext, file_is_archive = self._analyze_response_file(resp, file_type_header)

    # Calculate the final path to save downloaded file at.
    save_to, extract_to = self._calc_final_dest(
      dest_path,
      file_ext,
      file_is_archive,
      extract_archives,
      payload.get('name') or self.default_name
    )

    # Stream file to save path.
    self._stream_to_path(save_to, resp.response_obj, int(resp.headers.get('Content-Length')))

    # If no archive extraction needed, just return the path at which the file was saved.
    if not extract_to:
      return save_to

    # Extract archive to final destination.
    extract_zip(save_to, extract_to)

    return extract_to

  def _stream_to_path(self, path, stream, expected_size):
    # Ensure all parent dirs of desired save path exist.
    upsert_parent_dirs(path)

    try:
      ProgressDownloadStream(stream=stream, expected_size=expected_size).stream_to_file(path)
    except KeyboardInterrupt:
      exit()
    except BaseException as e:
      log('\nError downloading file to path "{}" with error: {}.'.format(path, e))
      exit()

  def _calc_final_dest(self, dest_path, actual_ext, is_archive, extract_archives, default_file_name):
    # Extract further info about the desired destination path.
    dest_ext, dest_is_dir = self._analyze_destination(dest_path)

    # If destination path is a file, validate file types match and return final path info.
    if not dest_is_dir:
      self._validate_file_types_match(dest_ext, actual_ext)
      return dest_path, None

    # For archives that need to be extracted, save them to temp storage and
    # use dest path as extraction destination.
    if is_archive and extract_archives:
      return tmp_model_archive_path, dest_path

    # For files with destination directories, save the file inside of that directory with the default name.
    return os.path.join(dest_path, default_file_name + '.' + actual_ext), None

  @staticmethod
  def _analyze_destination(path):
    ext = get_file_ext(path)
    is_dir = path.endswith('/') or ext == ''
    return ext, is_dir

  @staticmethod
  def _analyze_response_file(resp, file_type_header):
    ext = resp.headers.get(file_type_header)
    is_archive = ext == default_archive_fmt
    return ext, is_archive

  @staticmethod
  def _validate_file_types_match(expected_ext, actual_ext):
    if actual_ext != expected_ext:
      log('File type mismatch error -- can\'t save a "{}" file as a "{}".'.format(actual_ext, expected_ext))
      exit()


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