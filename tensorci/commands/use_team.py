import click
from tensorci import log, auth_required


@click.command(name='use-team')
@click.argument('team')
def use_team(team):
  auth_required()
  log('Switched to team: {}.'.format(team))