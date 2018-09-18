import click
from sweettea import log
from sweettea.definitions import default_model_name
from sweettea.utils.api import api
from sweettea.utils.file_util import new_file_uploader
from sweettea.utils.model_util import upload_ready_model_path

MODEL_CMD = 'model'


@click.command(name=MODEL_CMD)
@click.option('--name', '-n', default=default_model_name)
@click.option('--path', required=True)
def upload(name, path):
  # Get exact model path to upload from provided path (if directory, it's compressed first).
  model_path = upload_ready_model_path(path)

  # Create model uploader.
  uploader = new_file_uploader(model_path, completion_msg='\nUploading model...', name=name)

  try:
    api.post('/model', headers={'Content-Type': uploader.content_type}, mp_upload_monitor=uploader)
  except KeyboardInterrupt:
    return

  log('Successfully uploaded model.')


@click.command(name=MODEL_CMD)
def download():
  pass
