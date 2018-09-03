import click
from sweettea.resources import deploy
from sweettea.utils.auth import auth_required

sub_commands = [
  deploy.create
]


@click.group()
def create():
  """
  Create a SweetTea resource.

  Currently supported resources:

  * deploy
  """
  # Must be logged in to perform any create commands.
  auth_required()
  pass

[create.add_command(c) for c in sub_commands]
