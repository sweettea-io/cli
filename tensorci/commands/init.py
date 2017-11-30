import click
from tensorci import log, auth_required
from tensorci.utils import auth


@click.command()
# TODO: use --name as option and prompt for it. Then pull github repo from .git and fail if not a git project
def init():
  auth_required()

  curr_team = auth.get_team()

  if not curr_team:
    log("You must be actively using one of your teams before creating a new prediction.\n"
        "Use 'tensorci use-team NAME' to set one of your teams as the current team.")
    return

  pred_name = click.prompt('Prediction Name').strip()

  if not pred_name:
    log('Prediction Name is required.')
    return

  # if not git_repo:
  #   log('Git Repo URL is required.')
  #   return



  log('Heard init...')