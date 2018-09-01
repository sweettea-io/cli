import click
from sweettea import log
from sweettea.utils import auth


@click.command()
def logout():
  """
  Logout of SweetTea.

  Ex: $ st logout
  """
  # Remove authed session from netrc.
  auth.delete()
  log('Successfully logged out.')