import click
from sweettea.utils.auth import auth_required

sub_commands = [

]


@click.group()
def delete():
  """
  Delete a SweetTea resource.

  Currently supported resources:

  * ...
  """
  # Must be logged in to perform any delete commands.
  auth_required()
  pass


[delete.add_command(c) for c in sub_commands]
