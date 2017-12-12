from tensorci import log
from tensorci.utils.auth import get_team


def current_team(required=False, error_msg=None):
  # Read current team from netrc
  curr_team = get_team()

  if not curr_team and required:
    error_msg = error_msg or "You must be actively using one of your teams before running this command.\n" \
                             "Use 'tensorci use-team NAME' to set a team as your current team."

    log(error_msg)
    exit(1)

  return curr_team