import os
from sweettea import log
from sweettea.definitions import tmp_model_archive_path
from sweettea.utils.file_util import zip_dir


def upload_ready_model_path(path):
  # Ensure specified model path exists.
  if not os.path.exists(path):
    log('No model file or directory found at "{}".'.format(path))
    exit(1)

  # If path is to a file, return the absolute file path.
  if not os.path.isdir(path):
    return os.path.abspath(path)

  # If path is a directory, compress it into a zipfile inside st tmp storage.
  zip_dir(path, tmp_model_archive_path)

  # Return path to compressed model file.
  return tmp_model_archive_path
