import click
from tensorci.helpers.auth_helper import auth_required


@click.command()
def train():
  auth_required()

  pass