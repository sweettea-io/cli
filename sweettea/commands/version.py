import click
from sweettea import log
from sweettea.version import version as v


@click.command()
def version():
  """
  Show the current CLI version.

  Ex: $ st version
  """
  log(v)
