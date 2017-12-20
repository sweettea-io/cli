import click
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.utils.api import api
from tensorci.helpers.dynamic_response_helper import handle_dynamic_log_response
from tensorci.helpers.payload_helper import team_prediction_payload


@click.command()
@click.option('--follow', '-f', is_flag=True)
def logs(follow):
  """
  Show logs from the latest training session.

  Includes logs from preprocessing, training, and testing steps.

  If the --follow (-f) option is provided, the logs will be streamed
  and followed in real-time.

  Ex: tensorci logs -f
  """
  # Require authed user
  auth_required()

  # Format our payload
  payload = team_prediction_payload()
  payload['follow'] = str(follow).lower()

  # Perform the deploy with a streaming response
  resp = api.get('/deployment/logs', payload=payload, stream=True)

  # Handle response
  parsed_resp = handle_dynamic_log_response(resp)

  # If logs were sent back in a non-streaming response (just JSON),
  # just print the log dump
  if not follow and parsed_resp.get('logs'):
    log('\n'.join(parsed_resp.get('logs')))