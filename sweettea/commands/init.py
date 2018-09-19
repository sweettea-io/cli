import click
from sweettea import log
from sweettea.definitions import *
from sweettea.utils import project_config
from sweettea.utils.api import api
from sweettea.utils.auth import auth_required
from sweettea.utils.payload_util import project_payload
from sweettea.utils.project_config.helpers import write_placeholders


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
  if os.path.exists(project_config.file_path()):
    log('SweetTea project already exists for this directory.')
    return

  try:
    # Register the git repository as a SweetTea project.
    api.post('/project', payload=project_payload(key='nsp'))
  except KeyboardInterrupt:
    return

  # Unmarshal placeholder values into SweetTea config file for user to start with.
  write_placeholders()
  project_config.config.save()

  log('Initialized new SweetTea project.\n' +
      'Generated new config file at {}'.format(config_file_name))
