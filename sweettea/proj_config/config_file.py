import os
import yaml
from collections import OrderedDict
from sweettea.helpers.file_helper import config_file_path
from sweettea import log
from sweettea.definitions import *
from sweettea.proj_config.config_key import ConfigKey
from sweettea.proj_config.config_map import ConfigMap


class ConfigFile(object):
  """
  Serves as an interface to the .sweettea.yml config file.
  Contains methods to read/write the config file to disk, as well as validate its contents.

  Basic usage:

    config = ConfigFile()

  Or load the file immediately in a chained manner:

    config = ConfigFile().load()

  """
  FILE_NAME = config_file_name
  UPLOAD_CRITERIA_ALWAYS = 'always'
  UPLOAD_CRITERIA_EVAL = 'eval'
  TRAINING = 'training'
  HOSTING = 'hosting'

  def __init__(self, path=None, training=None, hosting=None):
    """
    The initialization params represent the keys of the config file:

    :param dict(str: str|dict) training: Training config
    :param dict(str: str|dict) hosting: Hosting config
    """
    # Config file path.
    self.path = path or config_file_path()
    self._unmarshal_dict(training=training, hosting=hosting)

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
      config = yaml.load(f)

    # Unmarshal main config sections into this class.
    self._unmarshal_dict(training=config.get(self.TRAINING),
                         hosting=config.get(self.HOSTING))

    return self

  def save(self):
    """Write this class's key-val pairs to disk inside the config file"""
    with open(self.path, 'w+') as f:
      yaml.dump(self._as_ordered_dict(), f, default_flow_style=False)

  def is_valid(self):
    """
    Validate each of the config file's key-val pairs

    :return: Whether the config file is valid or not
    :rtype: bool
    """
    # File has to exist in order to be valid...
    if not os.path.exists(self.path):
      log('A {} config file must exist before running this command.\n'.format(self.FILE_NAME) +
          'Run \'st init\' to initialize your project and create this file.')
      return False

    for k, v in self.config.items():
      if not v.is_valid():
        return False

    return True

  def abs_model_path(self, section):
    """
    Construct an absolute path from the specified 'model' key's relative path

    returns: model's would-be absolute path
    :rtype: str
    """
    if section not in (self.TRAINING, self.HOSTING):
      return None

    # Fetch raw model path value from desired config section.
    model = (getattr(self, section).get_value() or {}).get('model', {}).get('path')

    # Construct and return an absolute path using the current working directory.
    return os.path.join(os.getcwd(), model)

  def _as_ordered_dict(self):
    """
    Creates an ordered dict from the config's key-val pairs.

    :return: 'OrderedDict' of config's key-val pairs.
    :rtype: collections.OrderedDict
    """
    d = OrderedDict()

    # Add keys in the order we want them.
    d[self.TRAINING] = self.training.get_value()
    d[self.HOSTING] = self.hosting.get_value()

    return d

  @staticmethod
  def _model_path_validation(val):
    """
    Custom validation method for the 'model' key

    :return: If the 'model' key is valid
    :rtype: bool
    """
    # Ensure model path is a relative path
    return bool(val) and not val.startswith('/')

  @staticmethod
  def _training_buildpack_validation(val):
    return val in train_buildpacks

  @staticmethod
  def _hosting_buildpack_validation(val):
    return val in api_buildpacks

  def _upload_criteria_validation(self, val):
    return val in (self.UPLOAD_CRITERIA_ALWAYS, self.UPLOAD_CRITERIA_EVAL)

  def _unmarshal_dict(self, training=None, hosting=None):
    # Establish attributes for each config file key (represented as either the ConfigMap or ConfigKey class).
    training = training or {}
    hosting = hosting or {}
    dataset = training.get('dataset', {})
    training_model = training.get('model', {})
    hosting_model = hosting.get('model', {})

    # Configure buildpacks.
    training_buildpack_val = ConfigKey(value=training.get('buildpack'),
                                       custom_validation=self._training_buildpack_validation,
                                       required=True)

    hosting_buildpack_val = ConfigKey(value=hosting.get('buildpack'),
                                      custom_validation=self._hosting_buildpack_validation,
                                      required=True)

    # Configure dataset section.
    dataset_val = ConfigMap(value=dict(
      fetch=ConfigKey(value=dataset.get('fetch'), validation='mod_function'),
      prepro=ConfigKey(value=dataset.get('prepro'), validation='mod_function')
    ), key_order=(
      'fetch',
      'prepro'
    ))

    # Configure ML actions functions.
    train_val = ConfigKey(value=training.get('train'), validation='mod_function', required=True)
    test_val = ConfigKey(value=training.get('test'), validation='mod_function')
    eval_val = ConfigKey(value=training.get('eval'), validation='mod_function')
    predict_val = ConfigKey(value=hosting.get('predict'), validation='mod_function', required=True)

    # Configure model sections
    training_model_val = ConfigMap(value=dict(
      path=ConfigKey(value=training_model.get('path'),
                     custom_validation=self._model_path_validation,
                     required=True),
      upload_criteria=ConfigKey(value=training_model.get('upload_criteria'),
                                custom_validation=self._upload_criteria_validation,
                                required=True),
    ), key_order=(
      'path',
      'upload_criteria'
    ))

    hosting_model_val = ConfigMap(value=dict(
      path=ConfigKey(value=hosting_model.get('path'), custom_validation=self._model_path_validation, required=True),
    ))

    # Configure main sections of config file (training and hosting).
    self.training = ConfigMap(value=dict(
      buildpack=training_buildpack_val,
      dataset=dataset_val,
      train=train_val,
      test=test_val,
      eval=eval_val,
      model=training_model_val
    ), key_order=(
      'buildpack',
      'dataset',
      'train',
      'test',
      'eval',
      'model'
    ))

    self.hosting = ConfigMap(value=dict(
      buildpack=hosting_buildpack_val,
      predict=predict_val,
      model=hosting_model_val,
    ), key_order=(
      'buildpack',
      'predict',
      'model'
    ))

    # Store all config info inside config attribute.
    self.config = dict(training=self.training,
                       hosting=self.hosting)


def _setup_yaml():
  """Allow yaml library to save our data as an ordered dict"""
  represent_dict_order = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
  yaml.add_representer(OrderedDict, represent_dict_order)


_setup_yaml()
