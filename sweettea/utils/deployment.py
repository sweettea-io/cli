"""
Utility file exposing a consolidated 'deploy' method used by the following commands:

  $ tensorci train
  $ tensorci serve
  $ tensorci push

"""
# from sweettea.proj_config.config_file import ConfigFile
from sweettea.utils import gitconfig
from sweettea.utils.api import api
from sweettea.utils.auth import auth_required

# TODO: Remove this file
def deploy(action=None):
  """
  Perform a training deploy, API deploy, or both.

  :param str action:
    Deploy action to take.
    Supported values:
      - 'train'
      - 'serve'
      - 'push'
  """
  # Must already be logged in to perform this command.
  auth_required()

  # # Load config file from disk into our ConfigFile model.
  # config = ConfigFile().load()
  #
  # # Return if config file not valid.
  # if not config.is_valid():
  #   exit(1)

  # Find this git project's remote url namespace from inside .git/config
  git_repo_nsp = gitconfig.get_remote_nsp()

  # Create deploy payload.
  payload = {'project_nsp': git_repo_nsp}

  # Perform the deployment with a streaming response.
  resp = api.post('/deployment/{}'.format(action), payload=payload, stream=True)

  # Stream the response logs.
  resp.log_stream()