from team_helper import current_team
from tensorci.utils import auth
from tensorci.proj_config.config_file import ConfigFile
from tensorci.definitions import tci_keep_alive


def curate_deploy_payload(with_repo=True):
  # Read current team from netrc and fail if not there
  curr_team = current_team(required=True)

  # Load config file from disk into our ConfigFile model
  config = ConfigFile().load()

  # Return if config file not valid
  if not config.validate():
    exit(1)

  payload = {
    'team_slug': curr_team,
    'prediction_slug': config.name.value,
  }

  if with_repo:
    payload['git_repo'] = config.repo.value

  return payload


def handle_deploy_error(resp):
  try:
    data = resp.json() or {}
    error = data.get('error')
  except:
    error = None

  if error:
    log(error)
  else:
    log('Unknown error occured with status code {}'.format(resp.status_code))


def handle_deploy_json_success(resp):
  try:
    data = resp.json() or {}
  except:
    data = {}

  up_to_date = data.get('up_to_date')

  if up_to_date is True:
    log('Everything up to date.')
  else:
    log('Unknown response: {}'.format(data or resp.content))


def handle_deploy_stream_success(resp):
  try:
    for line in resp.iter_lines(chunk_size=10):
      if line and line != tci_keep_alive:
        log(line)
  except BaseException as e:
    log('Encountered error while parsing logs: {}'.format(e.message))