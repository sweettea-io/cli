import click
from sweettea import log
from sweettea.definitions import default_model_name
from sweettea.utils.api import api
from sweettea.utils.file_utils.file_downloader import FileDownloader
from sweettea.utils.file_utils.file_uploader import FileUploader
from sweettea.utils.model_util import get_upload_ready_model_path
from sweettea.utils.payload_util import project_payload

MODEL_CMD = 'model'


@click.command(name=MODEL_CMD)
@click.option('--name', '-n', default=default_model_name)
@click.option('--path', '-i', required=True)
def upload(name, path):
  FileUploader(api).upload(
    '/model',
    get_upload_ready_model_path(path),
    payload=project_payload({'name': name}),
    completion_msg='\nUploading model...'
  )

  log('Successfully uploaded model.')


@click.command(name=MODEL_CMD)
@click.option('--name', '-n', default=default_model_name)
@click.option('--path', '-o', required=True)
def download(name, path):
  FileDownloader(api).download(
    '/model',
    path,
    payload=project_payload({'model': name})
  )

  log('\nSaved model at "{}".'.format(path))
