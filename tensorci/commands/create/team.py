import click
from tensorci import log, auth_required
from tensorci.utils import auth
from tensorci.utils.api import api, ApiException
from slugify import slugify


@click.command()
@click.argument('name')
def team(name):
  auth_required()

  try:
    api.post('/team', {'name': name})
  except ApiException as e:
    log(e.message)
    return

  log('Successfully created team {}.'.format(name))

  team_slug = slugify(name, separator='-', to_lower=True)
  auth.set_team(team_slug)

  log('Switched current team to {}.'.format(name))