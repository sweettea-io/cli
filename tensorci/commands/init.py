import os
import click
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.helpers.team_helper import current_team
from tensorci.utils import gitconfig
from tensorci.proj_config.config_file import ConfigFile
from slugify import slugify


@click.command()
@click.option('--name', '-n')
def init(name):
  # Require authed user.
  auth_required()

  # Create a ConfigFile class instance from the config file.
  config = ConfigFile()

  # If the current directory already has a config file, tell them and exit.
  if os.path.exists(config.path):
    log('Project already initialized.')
    return

  # Prompt user for prediction name unless already provided
  pred_name = (name or click.prompt('Prediction Name')).strip()

  # Can't proceed without a prediction name :/
  if not pred_name:
    log('Prediction Name is required.')
    return

  # Find this git project's remote url from inside .git/config
  git_repo, err = gitconfig.get_remote_url()

  # Error out if the remote git url couldn't be found.
  if err:
    log(err)
    return

  # Slugify the name for them.
  pred_name = slugify(pred_name, separator='-', to_lower=True)

  # Add values to the config instance representing the config file
  # (use placeholders for the keys not requested by prompting the user).
  config.set_value('name', pred_name)
  config.set_value('repo', git_repo)
  config.set_value('model', 'path/to/model/file')
  config.set_value('prepro_data', 'module1.module2:function')
  config.set_value('train', 'module1.module2:function')
  config.set_value('test', 'module1.module2:function')
  config.set_value('predict', 'module1.module2:function')

  # Write the config file to the user's project.
  config.save()

  log('Initialized new TensorCI prediction: {}.\n\n'
      'Generated new config file at {}'.format(pred_name, config.NAME))