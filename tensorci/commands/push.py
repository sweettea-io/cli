import click
from tensorci.utils.deployment import deploy


@click.command()
def push():
  deploy(action='push')