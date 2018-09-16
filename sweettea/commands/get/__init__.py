import click
from sweettea.resources import project
from sweettea.utils.auth import auth_required

sub_commands = [
  project.get
]


@click.group()
def get():
  """
  Get a SweetTea resource.

  Currently supported resources:

  * project
  """
  # Must be logged in to perform any get commands.
  auth_required()
  pass


[get.add_command(c) for c in sub_commands]
