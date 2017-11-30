import click
from tensorci import log


@click.command()
def init():
  log('Heard init...')