import click
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.utils import auth
from tensorci.utils.api import api, ApiException
from slugify import slugify


@click.command()
@click.argument('name')
def team(name):
  """
  Create a TensorCI team.

  The current team will be set to this team upon successful creation.

  Ex: tensorci create team myteam
  """
  auth_required()

  try:
    api.post('/team', payload={'name': name})
  except ApiException as e:
    log(e.message)
    return

  log('Successfully created team {}.'.format(name))

  team_slug = slugify(name, separator='-', to_lower=True)
  auth.set_team(team_slug)

  log('Set current team to {}.'.format(name))