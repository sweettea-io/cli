import click
import os
from sweettea import log
from sweettea.definitions import *
from sweettea.helpers.file_helper import config_file_path
from sweettea.proj_config import config
from sweettea.utils import gitconfig
from sweettea.utils.api import api
from sweettea.utils.auth import auth_required


@click.command()
def init():
  """
  Create a new SweetTea project.

  This command will fail if the current working directory is not the base
  of a git repository.

  Upon success, a new config file named .sweettea.yml will be created in
  the current working directory.

  Ex: $ st init
  """
  # Must already be logged in to perform this command.
  auth_required()

  # If the current directory already has a config file, tell the user and exit.
  if os.path.exists(config_file_path()):
    log('SweetTea project already exists for this directory.')
    return

  # Find this git project's remote url namespace from inside .git/config
  git_repo_nsp = gitconfig.get_remote_nsp()

  try:
    # Register the git repository as a SweetTea project.
    api.post('/project', payload={'nsp': git_repo_nsp})
  except KeyboardInterrupt:
    return

  # Unmarshal placeholder values into the SweetTea config file for the user to start with.
  config.unmarshal({
    'training': {
      'buildpack': train_buildpacks[0],
      'dataset': {
        'fetch': 'mod1.mod2:fetch_dataset_func_name',
        'prepro': 'mod1.mod2:preprocess_dataset_func_name'
      },
      'train': 'mod1.mod2:train_func_name',
      'test': 'mod1.mod2:test_func_name',
      'eval': 'mod1.mod2:eval_func_name',
      'model': {
        'path': 'rel/path/to/model/dest',
        'upload_criteria': 'always'
      }
    },
    'hosting': {
      'buildpack': api_buildpacks[0],
      'predict': 'mod1.mod2:predict_func_name',
      'model': {
        'path': 'rel/path/to/model/source',
      }
    }
  })

  # Save the placeholder config file to disk.
  config.save()

  log('Initialized new SweetTea project.\n' +
      'Generated new config file at {}'.format(config_file_name))
