import click
from tensorci import log


@click.command()
def push():
  log('Heard push...')