import click
from sweettea import log
from sweettea.utils import gitconfig
from sweettea.utils.api import api
from sweettea.utils.auth import auth_required


@click.command()
@click.option('--follow', '-f', is_flag=True)
def logs(follow):
  """
  Show logs from the latest training session.

  Includes logs from preprocessing, training, and testing steps.

  If the --follow (-f) option is provided, the logs will be streamed
  and followed in real-time.

  Ex: tensorci logs -f
  """
  # Must already be logged in to perform this command.
  auth_required()

  # Find this git project's remote url namespace from inside .git/config
  git_repo_nsp = gitconfig.get_remote_nsp()

  # Built the payload.
  payload = {
    'project_nsp': git_repo_nsp,
    'follow': str(follow).lower()  # 'true' or 'false' --> will be converted into query param anyways
  }

  try:
    # Get the logs for this deployment.
    resp = api.get('/deployment/logs', payload=payload, stream=follow)
  except KeyboardInterrupt:
    return

  if follow:
    # Streaming log response
    resp.log_stream()
  else:
    # JSON dump of logs
    logs = resp.json.get('logs')

    if logs:
      log('\n'.join(logs))