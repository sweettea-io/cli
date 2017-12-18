import click
import os
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.helpers.dynamic_response_helper import handle_error
from tensorci.helpers.payload_helper import team_prediction_payload
from tensorci.utils.api import api, ApiException
from requests_toolbelt.downloadutils import stream
from tensorci.helpers.file_helper import break_file, add_ext, filenames_with_ext


@click.command()
@click.option('--output', '-o')
def model(output):
  # Require authed user
  auth_required()

  # Build our payload
  payload = team_prediction_payload()

  try:
    # Make streaming request
    resp = api.get('/prediction/model', payload=payload, stream=True)
  except ApiException as e:
    log(e.message)
    return

  # Handle error if request not successful
  if resp.status_code != 200:
    handle_error(resp)
    return

  # if output file was specified, create the absolute path from that
  if output:
    if output.startswith('/'):  # already abs path
      model_path = output
    else:  # create abs path from cwd
      model_path = os.path.join(os.getcwd(), output)
  else:
    # Load our config file
    config = ConfigFile().load()

    # Get the model file's absolute path based on cwd
    model_path = config.abs_model_path()

  # Get components of model_path
  direc, filename, ext = break_file(model_path)

  # Set ext to what type of file was fetched (only if output not specified)
  if not output:
    ext = resp.headers.get('Model-File-Type') or ext

  # Join filename with ext now that ext is solidified
  filename_w_ext = add_ext(filename, ext)

  # Create the model file's directory if it doesn't exist yet
  if direc and not os.path.exists(direc):
    os.makedirs(direc)

  # Path we're gonna save model to
  save_to = os.path.join(direc, filename_w_ext)

  # If the model file already exists, modify it with a number on the end to prevent overwriting.
  if os.path.exists(model_path):
    # Get a map of files in the directory that have the same ext as our desired save_to path.
    files_with_same_ext = filenames_with_ext(direc, ext)

    # Iterate until <filename><i>.<ext> is available, then create new save_to with that.
    i = 1
    while True:
      i += 1
      numbered_filename = add_ext('{}{}'.format(filename, i), ext)

      # if numbered file name hasn't been taken yet, use that name.
      if not files_with_same_ext.get(numbered_filename):
        save_to = os.path.join(direc, numbered_filename)
        break

  try:
    # TODO: add prog bar:
    # # Get total bytes from resp
    # bar = ProgressBar(expected_size=<total_bytes>, filled_char='=')
    # b = io.BytesIO()
    # # Set some callback on b, involving bar.show(bytes_read)
    # stream.stream_response_to_file(resp, path=b)

    # Stream the response into our desired file path.
    stream.stream_response_to_file(resp, path=save_to)
  except BaseException as e:
    log('Error streaming model file to path {} with error: {}'.format(save_to, e))
    return

  log('Successfully fetched trained model.')