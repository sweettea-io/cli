import click
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from sweettea import log
from sweettea.definitions import default_model_name, default_mime_type
from sweettea.utils import file_util, model_util
from sweettea.utils.api import api
from sweettea.utils.multipart_request_util import create_callback
from sweettea.utils.payload_util import project_payload

MODEL_CMD = 'model'


@click.command(name=MODEL_CMD)
@click.option('--name', '-n', default=default_model_name)
@click.option('--path', required=True)
def upload(name, path):
  # Get exact model path to upload from provided path (if path is directory, it is compressed first).
  model_path = model_util.upload_ready_model_path(path)

  # Name of file used in upload attachment.
  upload_file_key = 'model'

  # Get the file extension for the model file.
  model_ext = file_util.file_ext(model_path)

  # Add model extension to upload file key (if exists).
  if model_ext:
    upload_file_key = '.'.join((upload_file_key, model_ext))

  # Get model's mime type based on its final file path.
  model_mime_type = mimetypes.guess_type(model_path)[0] or default_mime_type

  # Create payload.
  payload = project_payload({
    'name': name,
    'ext': model_ext,
    'file': (upload_file_key, open(model_path, 'rb'), model_mime_type)
  })

  # Create a multipart encoder.
  encoder = MultipartEncoder(fields=payload)

  # Create progress callback, specifying message to show when upload completes.
  callback = create_callback(encoder, completion_log='\nUploading model...')

  # Create a monitor for the encoder so we can track upload progress.
  monitor = MultipartEncoderMonitor(encoder, callback)

  # Set the request Content-Type to the multipart encoder's content type.
  headers = {'Content-Type': monitor.content_type}

  try:
    # Upload the model.
    api.post('/model', headers=headers, mp_upload_monitor=monitor)
  except KeyboardInterrupt:
    return

  # TODO: Make this message more verbose, displaying the model version created.
  log('Successfully uploaded model.')


@click.command(name=MODEL_CMD)
def download():
  pass
