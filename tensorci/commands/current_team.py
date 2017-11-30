import click
from tensorci.utils import auth


@click.command(name='current-team')
def current_team():
  """
  Prints current team in use by the CLI.

  :return: None
  """
  auth_required()

  curr_team = auth.get_team()

  if not curr_team:
    log("No team is currently in use. Use 'tensorci use-team NAME' to set a team as the current team.")
    return

  log('Current team: {}'.format(curr_team))