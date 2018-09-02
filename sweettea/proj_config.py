from sweettea.definitions import *
from sweettea.utils.config.config_file import ConfigFile
from sweettea.utils.config.config_key import ConfigKey
from sweettea.utils.config.config_map import ConfigMap
from sweettea.utils.file_util import config_file_path

MODEL_UPLOAD_CRITERIA_ALWAYS = 'always'
MODEL_UPLOAD_CRITERIA_EVAL = 'eval'


def validate_training_bp(val):
  return val in train_buildpacks


def validate_hosting_bp(val):
  return val in api_buildpacks


def validate_model_path(val):
  return bool(val) and not val.startswith('/')


def validate_model_upload_criteria(val):
  return val in {MODEL_UPLOAD_CRITERIA_ALWAYS, MODEL_UPLOAD_CRITERIA_EVAL}


config = ConfigFile(path=config_file_path(), config=ConfigMap(key_order=('training', 'hosting'), value={
  'training': ConfigMap(key_order=('buildpack', 'dataset', 'train', 'test', 'eval', 'model'), value={
    'buildpack': ConfigKey(required=True, custom_validation=validate_training_bp),
    'dataset': ConfigMap(key_order=('fetch', 'prepro'), value={
      'fetch': ConfigKey(validation='mod_function'),
      'prepro': ConfigKey(validation='mod_function')
    }),
    'train': ConfigKey(required=True, validation='mod_function'),
    'test': ConfigKey(validation='mod_function'),
    'eval': ConfigKey(validation='mod_function'),
    'model': ConfigMap(key_order=('path', 'upload_criteria'), value={
      'path': ConfigKey(required=True, custom_validation=validate_model_path),
      'upload_criteria': ConfigKey(required=True, custom_validation=validate_model_upload_criteria)
    })
  }),
  'hosting': ConfigMap(key_order=('buildpack', 'predict', 'model'), value={
    'buildpack': ConfigKey(required=True, custom_validation=validate_hosting_bp),
    'predict': ConfigKey(required=True, validation='mod_function'),
    'model': ConfigMap(value={
      'path': ConfigKey(required=True, custom_validation=validate_model_path),
    })
  })
}))