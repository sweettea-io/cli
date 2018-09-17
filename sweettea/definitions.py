"""
Frequently-used constants
"""
import os

auth_header_name = 'Sweet-Tea-Api-Token'

config_file_name = '.sweettea.yml'

train_buildpacks = [
  'python-train'
]

api_buildpacks = [
  'python-websocket-api',
  'python-json-api'
]

default_model_name = 'default'

st_tmp_dir = '/tmp/st'

default_archive_fmt = 'zip'

tmp_model_archive_path = os.path.join(st_tmp_dir, 'model.{}'.format(default_archive_fmt))

default_mime_type = 'text/plain'
