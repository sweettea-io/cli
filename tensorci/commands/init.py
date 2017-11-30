import click
from tensorci import log, auth_required


@click.command()
def init():
  auth_required()
  log('Heard init...')