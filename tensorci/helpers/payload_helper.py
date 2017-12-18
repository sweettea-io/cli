from team_helper import current_team
from tensorci.proj_config.config_file import ConfigFile


# TODO: Rename this and just make a config reader or something
def team_prediction_payload(include_repo=False, include_model_ext=False):
  # Read current team from netrc and fail if not there.
  curr_team = current_team(required=True)

  # Load config file from disk into our ConfigFile model.
  config = ConfigFile().load()

  # Return if config file not valid.
  # TODO: add config validation for model file string
  if not config.validate():
    exit(1)

  # Construct api payload and return it
  payload = {
    'team_slug': curr_team,
    'prediction_slug': config.name.value,
  }

  if include_repo:
    payload['git_repo'] = config.repo.value

  if include_model_ext:
    payload['model_ext'] = config.model.value.split('.').pop()

  return payload