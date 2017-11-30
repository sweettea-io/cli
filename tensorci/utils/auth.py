from tinynetrc import Netrc
from tensorci.definitions import auth_header_name
from tensorci.config import config


def login(email=None, password=None):
  netrc = Netrc()

  # delete old creds
  logout(netrc)

  # upsert new creds
  netrc[config.DOMAIN]['login'] = email
  netrc[config.DOMAIN]['password'] = password

  # save dat bish
  netrc.save()


def logout(netrc=None):
  netrc = netrc or Netrc()

  if config.DOMAIN in netrc.keys():
    del netrc[config.DOMAIN]
    netrc.save()


def set_team(team):
  netrc = Netrc()
  assert config.DOMAIN in netrc.keys()
  netrc[config.DOMAIN]['account'] = team
  netrc.save()


def authed():
  creds = get_creds()
  return creds.get('login') and creds.get('password')


def get_email():
  return get_creds.get('login')


def get_team():
  return get_creds.get('account')


def get_password():
  return get_creds.get('password')


def get_creds():
  return Netrc().get(config.DOMAIN)