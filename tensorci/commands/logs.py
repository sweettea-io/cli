import click
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.utils.api import api
from tensorci.utils import gitconfig


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

  # Find this git project's remote url from inside .git/config
  git_repo, err = gitconfig.get_remote_url()

  # Error out if the remote git url couldn't be found.
  if err:
    log(err)
    return

  # Built the payload.
  payload = {
    'git_url': git_repo,
    'follow': str(follow).lower()  # 'true' or 'false' --> will be converted into query param anyways
  }

  try:
    # Get the logs for this deployment.
    resp = api.get('/deployment/logs', payload=payload, stream=follow)
  except KeyboardInterrupt:
    return

  # Log the error if the request failed.
  if not resp.ok:
    resp.log_error()
    return

  if follow:
    # Streaming log response
    resp.log_stream()
  else:
    # JSON dump of logs
    logs = resp.json.get('logs')

    if logs:
      log('\n'.join(logs))