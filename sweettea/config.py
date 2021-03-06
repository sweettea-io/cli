import os


class Config:
  """
  Internal config class for storing any non-environment-variable config information
  """
  def __init__(self):
    self.DEBUG = os.environ.get('DEBUG', True)
    self.DOMAIN = os.environ.get('DOMAIN', 'api.sweettea.io')
    self.API_VERSION = os.environ.get('API_VERSION', 'v1')
    self.API_URL = os.environ.get('API_URL', 'https://{}/{}'.format(self.DOMAIN, self.API_VERSION))

config = Config()