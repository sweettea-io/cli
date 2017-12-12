from tensorci import log
from tensorci.utils.auth import authed


def current_team(required=False):
  # Read current team from netrc
  curr_team = auth.get_team()

  if not curr_team and required:
    log("You must be actively using one of your teams before running this command.\n"
        "Use 'tensorci use-team NAME' to set a team as your current team.")
    exit(1)

  return curr_team