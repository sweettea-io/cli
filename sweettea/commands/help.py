import click


@click.command()
def help():
  """
  Display global CLI help message
  """
  from sweettea.main import cli
  cli('--help')