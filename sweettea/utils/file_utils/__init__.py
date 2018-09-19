import os
import json
import mimetypes
import shutil
import yaml
import zipfile
from sweettea import log
from sweettea.definitions import default_mime_type

JSON_EXT = 'json'
YAML_EXT = 'yaml'
ENV_EXT = 'env'


def is_json_file(path):
  return path.endswith('.{}'.format(JSON_EXT))


def is_yaml_file(path):
  return path.endswith('.{}'.format(JSON_EXT))


def is_env_file(path):
  return path.endswith('.{}'.format(JSON_EXT))


def json_load(path):
  with open(path) as f:
    return json.load(f)


def yaml_load(path):
  with open(path) as f:
    return yaml.load(f)


def get_file_ext(path):
  comps = path.rsplit('/', 1).pop().rsplit('.', 1)

  if len(comps) == 1:
    return ''

  return comps[1]


def get_mime_type(path):
  return mimetypes.guess_type(path)[0] or default_mime_type


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


def extract_zip(archive_path, destination_dir_path):
  # Upsert parent directory of extracted destination path.
  upsert_parent_dirs(destination_dir_path.rstrip('/'))

  # Remove the entire destination dir if it already exists.
  if os.path.exists(destination_dir_path) and os.path.isdir(destination_dir_path):
    shutil.rmtree(destination_dir_path)

  # Extract archive into desired destination.
  with zipfile.ZipFile(archive_path) as archive:
    archive.extractall(destination_dir_path)
