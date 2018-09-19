import os
import yaml
from collections import OrderedDict


class ConfigFile(object):
  """
  Serves as an interface to a yaml config file.
  Contains methods to read/write the config file to disk, as well as validate its contents.

  Basic usage:

    config = ConfigFile()

  Or load the file immediately in a chained manner:

    config = ConfigFile().load()

  """
  def __init__(self, path='', config=None):
    self.path = path
    self.file_name = path.rsplit('/', 1)
    self.config = config

  def unmarshal(self, cfg):
    """
    Load values into config fields from dictionary.

    :param dict cfg: Dictionary contents to unmarshal into self.config
    """
    self.config.unmarshal(cfg)

  def load(self):
    """
    Load the config file from disk, and for each key-val pair,
    assign the value to this class's key attribute counterpart.

    :return: self
    """
    # Return early if config file doesn't exist.
    if not os.path.exists(self.path):
      return self

    # Load the yaml config file from disk.
    with open(self.path, 'r') as f:
      cfg = yaml.load(f)

    self.unmarshal(cfg)

    return self

  def save(self):
    """Write this class's key-val pairs to disk inside the config file"""
    with open(self.path, 'w+') as f:
      yaml.dump(self.get_value(), f, default_flow_style=False)

  def get_value(self):
    return self.config.get_value()

  def is_valid(self):
    """
    Validate each of the config file's key-val pairs

    :return: Whether the config file is valid or not
    :rtype: bool
    """
    return self.config.is_valid()


def _setup_yaml():
  """Allow yaml library to save our data as an ordered dict"""
  dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
  yaml.add_representer(OrderedDict, dict_order)


_setup_yaml()
