import click
from sweettea.utils.auth import auth_required

sub_commands = [

]


@click.group()
def update():
  """
  Update a SweetTea resource.

  Currently supported resources:

  * ...
  """
  # Must be logged in to perform any update commands.
  auth_required()
  pass


[update.add_command(c) for c in sub_commands]
