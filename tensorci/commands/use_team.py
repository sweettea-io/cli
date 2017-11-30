import click
from tensorci import log, auth_required
from tensorci.utils import auth


@click.command(name='use-team')
@click.argument('name')
def use_team(name):
  """
  Switches current team to desired team by name.

  :param team: str (required)
  :return:
  """
  auth_required()

  team_slug = slugify(name, separator='-', to_lower=True)
  auth.set_team(team_slug)

  log('Switched current team to {}.'.format(name))