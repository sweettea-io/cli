"""
Helper methods related to user authorization
"""
from tensorci import log
from tensorci.utils.auth import authed


def auth_required():
  """Check if user is logged in and exit if not"""
  if not authed():
    log('You must be logged in to perfom that action.\n'
        'Use \'tensorci login\' if you already have an account, or visit '
        'https://tensorci.com to create a new account.')
    exit(1)