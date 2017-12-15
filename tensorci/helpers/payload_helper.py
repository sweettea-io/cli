from team_helper import current_team
from tensorci.proj_config.config_file import ConfigFile


def team_prediction_payload(include_repo=False):
  # Read current team from netrc and fail if not there.
  curr_team = current_team(required=True)

  # Load config file from disk into our ConfigFile model.
  config = ConfigFile().load()

  # Return if config file not valid.
  if not config.validate():
    exit(1)

  # Construct api payload and return it
  payload = {
    'team_slug': curr_team,
    'prediction_slug': config.name.value,
  }

  if include_repo:
    payload['git_repo'] = config.repo.value

  return payload