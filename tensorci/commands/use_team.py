import click
from tensorci import log


@click.command(name='use-team')
@click.argument('team')
def use_team(team):
  log('Switched to team: {}.'.format(team))