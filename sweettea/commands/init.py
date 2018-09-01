import click
import os
from sweettea import log
from sweettea.definitions import *
from sweettea.helpers.file_helper import config_file_path
from sweettea.proj_config.config_file import ConfigFile
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

  # Find this git project's remote url from inside '.git/config'
  git_repo = gitconfig.get_remote_url()

  try:
    # Register the git repository as a SweetTea project.
    api.post('/project', payload={'nsp': git_repo})
  except KeyboardInterrupt:
    return
  
  # Create a ConfigFile instance with default placeholder values for the user.
  config = ConfigFile(
    training=dict(
      buildpack=train_buildpacks[0],
      train='mod1.mod2.train_func_name',
      test='mod1.mod2.test_func_name',
      eval='mod1.mod2.eval_func_name',
      model=dict(
        path='rel/path/to/model/dest',
        upload_criteria='always'
      )
    ),
    hosting=dict(
      buildpack=api_buildpacks[0],
      predict='mod1.mod2.predict_func_name',
      model=dict(
        path='rel/path/to/model/source'
      )
    )
  )

  # Write the config file to the user's project.
  config.save()

  log('Initialized new SweetTea project.\n' +
      'Generated new config file at {}'.format(config.FILE_NAME))
