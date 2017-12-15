from tensorci.helpers.auth_helper import auth_required
from tensorci.utils.api import api
from tensorci.helpers.dynamic_response_helper import handle_dynamic_log_response
from tenosrci.helpers.payload_helper import team_prediction_payload


def deploy(action=None, include_repo=True):
  # Require authed user
  auth_required()

  # Get our deploy payload
  payload = team_prediction_payload(include_repo=include_repo)

  # Perform the deploy with a streaming response
  resp = api.post('/deployment/{}'.format(action), payload=payload, stream=True)

  # Handle response
  handle_dynamic_log_response(resp)