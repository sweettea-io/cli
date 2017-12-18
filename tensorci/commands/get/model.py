import click
import os
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.helpers.dynamic_response_helper import handle_error
from tensorci.helpers.payload_helper import team_prediction_payload
from tensorci.utils.api import api, ApiException
from requests_toolbelt.downloadutils import stream


# TODO: add -o --output option to save the model there
@click.command()
def model():
  # Require authed user
  auth_required()

  # Build our payload
  payload = team_prediction_payload(include_model=True)
  model_path = payload.pop('model')

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

  cwd = os.getcwd()
  full_model_path = '{}/{}'.format(cwd, model_path)

  file_path_comps = full_model_path.split('/')
  file_with_ext = file_path_comps.pop()
  dirname = '/'.join(file_path_comps)

  file_name_comps = file_with_ext.split('.')
  file_ext = file_name_comps.pop()
  file_name = '.'.join(file_name_comps)

  # Create the model file's directory if it doesn't exist yet
  if dirname and not os.path.exists(dirname):
    os.makedirs(dirname)

  save_to = full_model_path

  # If the model file already exists
  if os.path.exists(full_model_path):
    # Modify the name of the file so there are no conflicts (i.e. add a number to the end of it)
    files_with_same_ext = {n: True for n in os.listdir(dirname) if n.endswith('.{}'.format(file_ext))}

    i = 1
    while True:
      i += 1
      numbered_file_name = '{}{}.{}'.format(file_name, i, file_ext)

      # if numbered file name hasn't been take yet, use that name.
      if not files_with_same_ext.get(numbered_file_name):
        save_to = '{}/{}'.format(dirname, numbered_file_name)
        break

  try:
    # TODO: add prog bar
    # Stream the response to a file
    stream.stream_response_to_file(resp, path=save_to)
  except BaseException as e:
    log('Error streaming model file to path {} with error: {}'.format(save_to, e))
    return

  log('Successfully fetched trained model.')