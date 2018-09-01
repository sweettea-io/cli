import os


class Config:
  """
  Config class for storing any non-environment-variable config information
  """
  def __init__(self):
    self.DEBUG = os.environ.get('DEBUG', True)
    self.API_URL = os.environ.get('API_URL', 'https://api.sweettea.io')

config = Config()