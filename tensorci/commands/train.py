import click
from tensorci.utils.deployment import deploy


@click.command()
def train():
  deploy(action='train', include_repo=True)