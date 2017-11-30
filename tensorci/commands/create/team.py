import click
from tensorci import log


@click.command()
@click.argument('name')
def team(name):
  log('Creating team {}...'.format(name))