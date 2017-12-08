import click
from tensorci import log, auth_required
from tensorci.utils import auth
from tensorci.utils.api import api, ApiException
from tensorci.proj_config.config_file import ConfigFile


@click.command()
def push():
  auth_required()

  # Read current team from netrc
  curr_team = auth.get_team()

  # Require current team to be specified
  if not curr_team:
    log("You must be actively using one of your teams before deploying a prediction.\n"
        "Use 'tensorci use-team NAME' to set a team as your current team.")
    return

  # Load config file from disk into our ConfigFile model
  config = ConfigFile()
  config.load()

  # Return if config file not valid
  if not config.validate():
    return

  payload = {
    'team_slug': curr_team,
    'prediction_slug': config.name.value,
    'git_repo': config.repo.value
  }

  # Make deploy
  resp = api.post('/deployment', payload=payload, stream=True)

  # Handle error cases
  if resp.status_code != 200:
    handle_push_error(resp)
    return

  if resp.headers.get('Content-Type') == 'application/json':
    handle_non_stream_resp(resp)
  else:
    handle_stream_resp(resp)


def handle_push_error(resp):
  try:
    data = resp.json() or {}
    error = data.get('error')
  except:
    error = None

  if error:
    log(error)
  else:
    log('Unknown error occured with status code {}'.format(resp.status_code))


def handle_stream_resp(resp):
  for line in resp.iter_lines(chunk_size=10):
    if line:
      log(line)


def handle_non_stream_resp(resp):
  try:
    data = resp.json() or {}
  except:
    data = {}

  up_to_date = data.get('up_to_date')

  if up_to_date is True:
    log('Everything up to date.')
  else:
    log('Unknown response: {}'.format(data or resp.content))