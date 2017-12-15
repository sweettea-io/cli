import click
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.utils.api import api
from tensorci.helpers.dynamic_response_helper import handle_dynamic_log_response
from tensorci.helpers.payload_helper import team_prediction_payload


@click.command()
@click.option('--follow', '-f', is_flag=True)
def logs(follow):
  # Require authed user
  auth_required()

  # Format our payload
  payload = team_prediction_payload()
  payload['follow'] = follow

  # Perform the deploy with a streaming response
  resp = api.get('/deployment/logs', payload=payload, stream=True)

  # Handle response
  logs = handle_dynamic_log_response(resp)

  # If logs were sent back in a non-streaming response (just JSON),
  # iterate over them and log each line
  if not follow and logs:
    for line in logs:
      log(line)