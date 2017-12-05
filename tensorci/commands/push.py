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

  try:
    resp = api.post('/deployment', payload=payload)
  except ApiException as e:
    log(e.message)
    return

  if resp.get('up_to_date'):
    log('Everything up to date.')
    return

  # TODO: open a socket and pipe logs here instead
  log('Successfully deployed prediction.')