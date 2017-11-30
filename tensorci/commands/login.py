import click
from tensorci import log


@click.command()
def login():
  log('Logging in...')