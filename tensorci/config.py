import os
from utils.env import env


class Config:
  DEBUG = True


class ProdConfig(Config):
  DEBUG = False

  def __init__(self):
    API_URL = os.environ.get('API_URL') or 'http://app.tensorci.com/api'


class StagingConfig(Config):
  DEBUG = False

  def __init__(self):
    API_URL = os.environ.get('API_URL') or 'http://app.staging.tensorci.com/api'


class DevConfig(Config):
  def __init__(self):
    API_URL = os.environ.get('API_URL') or 'http://app.dev.tensorci.com/api'


class TestConfig(Config):
  def __init__(self):
    API_URL = os.environ.get('API_URL') or 'http://localhost/api'


def get_config():
  config_class = globals().get('{}Config'.format(env().capitalize()))
  return config_class()