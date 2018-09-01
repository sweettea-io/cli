import click
from sweettea import log
from sweettea.definitions import auth_header_name
from sweettea.utils import auth
from sweettea.utils.api import api


@click.command()
@click.option('--email', '-e')
@click.option('--password', '-p')
def login(email, password):
  """
  Login as a SweetTea user.

  If --email (-e) and --password (-p) are not provided as options,
  the user will be prompted for these values.

  Ex: $ st login
  """
  log('Enter your SweetTea credentials:')

  # Prompt user for username unless already provided.
  email = (email or click.prompt('Email')).strip()

  # Can't proceed without email...
  if not email:
    log('SweetTea email is required.')
    return

  # Prompt user for password unless already provided.
  pw = (password or click.prompt('SweetTea Password', hide_input=True)).strip()

  # Can't proceed without password...
  if not pw:
    log('SweetTea password is required.')
    return

  # Construct API payload.
  payload = {
    'email': email,
    'password': pw,
  }

  try:
    # Request auth from SweetTea API.
    resp = api.post('/user/auth', payload=payload, log_on_error=False, exit_on_error=False)
  except KeyboardInterrupt:
    return

  # Log the error if the login failed.
  if not resp.ok:
    log('Authentication failed.')
    return

  # Get the user session token from the response headers.
  session_token = resp.headers.get(auth_header_name)

  # Create a new authed session in netrc with the session token as the password.
  auth.create(password=session_token)

  log('Logged in as {}.'.format(email))
