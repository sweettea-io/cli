import yaml
import os


class ConfigFile(object):
  NAME = '.tensorci.yml'

  def __init__(self, path=None, name=None, repo=None, model=None,
               create_dataset=None, train=None, test=None, predict=None):

    # Config file path
    self.path = path or '{}/{}'.format(os.getcwd(), self.NAME)

    # Config file keys
    self.name = ConfigKey(value=name, required=True, validation='slug')
    self.repo = ConfigKey(value=repo, required=True, validation='url')
    self.model = ConfigKey(value=model, required=True, validation='truthy')
    self.create_dataset = ConfigKey(value=create_dataset, required=True, validation='mod_function')
    self.train = ConfigKey(value=train, required=True, validation='mod_function')
    self.test = ConfigKey(value=test, required=False, validation='mod_function')
    self.predict = ConfigKey(value=predict, required=True, validation='mod_function')

    self.config = dict(name=self.name,
                     repo=self.repo,
                     model=self.model,
                     create_dataset=self.create_dataset,
                     train=self.train,
                     test=self.test,
                     predict=self.predict)

  def load(self):
    if not os.path.exists(self.path):
      return

    with open(self.path, 'r') as f:
      file_config = yaml.load(f)

    for k, v in file_config.items():
      if k in self.config:
        self.config[k].set_value(v)

  def as_dict(self):
    return {k: v.value for k, v in self.config.items()}

  def save(self):
    with open(self.path, 'w+') as f:
      f.write(yaml.dumps(self.as_dict()))

  def validate(self):
    [v.validate() for v in self.config.values()]