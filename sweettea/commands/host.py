import click
from sweettea.utils.deployment import deploy


@click.command()
def host():
  """
  Host model predictions from an API.

  The payload included with a request to this hosted model will be passed
  to the 'predict' function specified in .sweettea.yml.

  A client_id and client_secret are generated to secure this endpoint,
  both of which belong to this SweetTea project.

  Ex: $ st host
  """
  try:
    deploy(action='api')
  except KeyboardInterrupt:
    return