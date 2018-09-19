from . import config
from sweettea.definitions import *


def write_placeholders():
  config.unmarshal({
    'training': {
      'buildpack': train_buildpacks[0],
      'dataset': {
        'fetch': 'mod1.mod2:fetch_dataset_func_name',
        'prepro': 'mod1.mod2:preprocess_dataset_func_name'
      },
      'train': 'mod1.mod2:train_func_name',
      'test': 'mod1.mod2:test_func_name',
      'eval': 'mod1.mod2:eval_func_name',
      'model': {
        'path': 'rel/path/to/model/dest',
        'upload_criteria': 'always'
      }
    },
    'hosting': {
      'buildpack': api_buildpacks[0],
      'predict': 'mod1.mod2:predict_func_name',
      'model': {
        'path': 'rel/path/to/model/source',
      }
    }
  })

