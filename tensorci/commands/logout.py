import click
from tensorci import log
from tensorci.utils import auth


@click.command()
def logout():
  auth.delete()
  log('Successfully logged out.')