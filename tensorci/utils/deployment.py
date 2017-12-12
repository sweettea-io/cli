from tensorci.helpers.auth_helper import auth_required
from tensorci.utils.api import api
from tensorci.helpers.deploy_helper import *


def deploy(action=None, with_repo=True):
  # Require authed user
  auth_required()

  # Get our deploy payload
  payload = curate_deploy_payload(with_repo=with_repo)

  # Perform the deploy with a streaming response
  resp = api.post('/deployment/{}'.format(action), payload=payload, stream=True)

  # If initial request failed, handle the JSON response accordingly
  if resp.status_code != 200:
    handle_deploy_error(resp)
    return

  # If request succeeded but responded with JSON, parse and log the response
  if resp.headers.get('Content-Type') == 'application/json':
    handle_deploy_json_success(resp)
    return

  # Handle the real-time log stream response
  handle_deploy_stream_success(resp)