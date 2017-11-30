import click
from tensorci import log, auth_required


@click.command()
def push():
  auth_required()
  log('Heard push...')