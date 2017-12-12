import click
from tensorci import log
from tensorci.utils import auth
from tensorci.utils.api import api, ApiException
from tensorci.definitions import auth_header_name


@click.command()
@click.option('--email', '-e')
@click.option('--password', '-p')
def login(email, password):
  """
  Log in as a TensorCI user. Request responds with api token that can be used for
  future authed requests to TensorCI API. Email and API token are stored in netrc file.

  :param email: str (required)
  :param password: str (required)
  """
  log('Enter your TensorCI credentials:')

  # Prompt user for email unless already provided
  email = (email or click.prompt('Email')).strip()

  # Can't proceed without email :/
  if not email:
    log('Email is required.')
    return

  # Prompt user for password unless already provided
  pw = (password or click.prompt('Password', hide_input=True)).strip()

  # Can't proceed without email :/
  if not pw:
    log('Password is required.')
    return

  # Construct API payload
  payload = {'email': email, 'password': pw}

  try:
    # Make login request and get both response body and response headers
    resp, headers = api.post('/user/login', payload=payload, return_headers=True)
  except ApiException:
    log('Authentication failed.')
    return

  # Get the user_token provided in the response headers
  user_token = headers.get(auth_header_name)

  # Create a new authed session in netrc with the user_token as the password
  auth.create(email=email, password=user_token)

  log('Logged in as {}'.format(email))