import click
from sweettea.commands.get.model import model


@click.group()
def get():
  """
  Get a TensorCI resource.

  Currently supported resources:

  * model
  """
  pass

get.add_command(model)