import yaml
import os
from collections import OrderedDict
from config_key import ConfigKey
from tensorci import log


class ConfigFile(object):
  NAME = '.tensorci.yml'

  def __init__(self, path=None, name=None, repo=None, model=None,
               prepro_data=None, train=None, test=None, predict=None):

    # Config file path
    self.path = path or '{}/{}'.format(os.getcwd(), self.NAME)

    # Config file keys
    self.name = ConfigKey(value=name, required=True, validation='slug')
    self.repo = ConfigKey(value=repo, required=True, validation='url')
    self.model = ConfigKey(value=model, required=True, validation='truthy')
    self.prepro_data = ConfigKey(value=prepro_data, required=True, validation='mod_function')
    self.train = ConfigKey(value=train, required=True, validation='mod_function')
    self.test = ConfigKey(value=test, required=False, validation='mod_function')
    self.predict = ConfigKey(value=predict, required=True, validation='mod_function')

    self.config = dict(name=self.name,
                       repo=self.repo,
                       model=self.model,
                       prepro_data=self.prepro_data,
                       train=self.train,
                       test=self.test,
                       predict=self.predict)

  def as_ordered_dict(self):
    d = OrderedDict()
    d['name'] = self.name.value
    d['repo'] = self.repo.value
    d['model'] = self.model.value
    d['prepro_data'] = self.prepro_data.value
    d['train'] = self.train.value
    d['test'] = self.test.value
    d['predict'] = self.predict.value
    return d

  def load(self):
    if not os.path.exists(self.path):
      return

    with open(self.path, 'r') as f:
      file_config = yaml.load(f)

    for k, v in file_config.items():
      self.set_value(k, v)

    return self

  def abs_model_path(self):
    return os.path.join(os.getcwd(), self.model.value)

  def set_value(self, key, val):
    if key in self.config:
      self.config[key].set_value(val)

  def save(self):
    # Write the yaml information
    with open(self.path, 'w+') as f:
      yaml.dump(self.as_ordered_dict(), f, default_flow_style=False)

    # Doublespace everything (personal pref)
    with open(self.path) as f:
      content = f.read()

    with open(self.path, 'w+') as f:
      f.write(content.replace('\n', '\n\n').strip())

  def validate(self):
    invalid_keys = []

    for k, v in self.config.items():
      if not v.validate():
        invalid_keys.append(k)

    if invalid_keys:
      log('Invalid config keys: {}'.format(', '.join(invalid_keys)))

    return len(invalid_keys) == 0


def setup_yaml():
  represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
  yaml.add_representer(OrderedDict, represent_dict_order)

setup_yaml()