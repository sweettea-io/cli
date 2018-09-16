import click
from sweettea.resources import model
from sweettea.utils.auth import auth_required

sub_commands = [
  model.upload,
]


@click.group()
def upload():
  """
  Upload a SweetTea resource.

  Currently supported resources:

  * model
  """
  # Must be logged in to perform any upload commands.
  auth_required()
  pass

[upload.add_command(c) for c in sub_commands]
