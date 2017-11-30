import click
from tensorci import log, auth_required


@click.command()
@click.argument('name')
def team(name):
  auth_required()
  log('Creating team {}...'.format(name))