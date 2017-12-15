import click
from tensorci.utils.deployment import deploy


@click.command()
def serve():
  deploy(action='api')