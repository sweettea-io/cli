import click
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.utils import auth
from slugify import slugify
from tensorci.utils.api import api, ApiException


@click.command(name='use-team')
@click.argument('name')
def use_team(name):
  """
  Sets the current team.

  Ex: tensorci use-team myteam
  """
  # Require authed user
  auth_required()

  # Slugify the name input
  team_slug = slugify(name, separator='-', to_lower=True)

  try:
    # Get list of teams from API
    resp = api.get('/teams')
    teams = resp.get('data')
  except ApiException as e:
    log(e.message)
    return

  # Tell the user if he doesn't have any teams associated with his account.
  if not teams:
    log("You currently don't have any TensorCI teams to use.\n"
        "You can create one with 'tensorci create team NAME'.")
    return

  # Curate list of team slugs
  team_slugs = [t.get('slug') for t in teams]

  # If team requested doesn't exist for this user's account, tell the user and return.
  if team_slug not in team_slugs:
    log("You currently don't have a team named '{}'.".format(team_slug))
    return

  # Set team associated with authed session in netrc file
  auth.set_team(team_slug)

  log('Set current team to {}.'.format(name))