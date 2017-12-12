import click
from tensorci.helpers.auth_helper import auth_required
from tensorci.helpers.team_helper import current_team
from tensorci import log


@click.command(name='current-team')
def current_team():
  """
  Prints current team in use by the CLI.
  """
  # Require authed user.
  auth_required()

  # Read current team from netrc and fail if not there.
  curr_team = current_team(required=True, error_msg="No team is currently in use.\n"
                                                    "Use 'tensorci use-team NAME' "
                                                    "to set a team as your current team.")

  log('Current team: {}'.format(curr_team))