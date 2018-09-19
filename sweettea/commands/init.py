import click
from sweettea import log, proj_config
from sweettea.definitions import *
from sweettea.utils import config_util
from sweettea.utils.api import api
from sweettea.utils.auth import auth_required
from sweettea.utils.payload_util import project_payload


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
  if os.path.exists(proj_config.file_path()):
    log('SweetTea project already exists for this directory.')
    return

  try:
    # Register the git repository as a SweetTea project.
    api.post('/project', payload=project_payload(key='nsp'))
  except KeyboardInterrupt:
    return

  # Unmarshal placeholder values into SweetTea config file for user to start with.
  config_util.write_placeholders()
  proj_config.config.save()

  log('Initialized new SweetTea project.\n' +
      'Generated new config file at {}'.format(config_file_name))
