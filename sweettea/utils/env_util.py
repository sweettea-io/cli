import os
import re
from sweettea import log
from sweettea.utils.file_util import *


def parse_cmd_envs(env_file_path=None, env_options=None):
  envs = {}

  # First read in envs from file if provided.
  if env_file_path:
    envs = env_dict_from_file(env_file_path)

  # Then add other custom envs that were provided as options.
  if env_options:
    for k, v in env_dict_from_options(env_options):
      envs[k] = v

  return envs


def env_dict_from_file(path):
  # Ensure env file exists at provided path.
  if not os.path.exists(path):
    log('No env file found at "{}".'.format(path))
    exit(1)

  file_name_with_ext = path.rsplit('/', 1).pop()

  # JSON env file
  if is_json_file(file_name_with_ext):
    return valid_env_dict(json_load(path))

  # YAML env file
  elif is_yaml_file(file_name_with_ext):
    return valid_env_dict(yaml_load(path))

  # ENV env file
  elif is_env_file(file_name_with_ext):
    return read_env_envs(path)

  # UNSUPPORTED env file
  else:
    log('Unsupported env file type "{}". Supported file types are .{}, .{}, and .{}'.format(
      file_ext(file_name_with_ext), JSON_EXT, YAML_EXT, ENV_EXT))
    exit(1)


def valid_env_dict(content):
  # JSON content must just be a simple dict of key:val entries.
  if type(content) != dict:
    log('Invalid env file -- file must only contain a map of key:val entries.')
    exit(1)

  # Create a new dict, with all values stringified.
  envs = {}
  for key, val in content.iteritems():
    validate_env_val_type(val)
    envs[key] = str(val)

  return envs


def validate_env_val_type(val):
  if type(val) not in (str, bool, int, float):
    log('Invalid value in JSON env file -- {} is not of type str, bool, int, or float.')
    exit(1)


def read_env_envs(path):
  # Read env file in as text and split by newlines
  with open(path) as f:
    content = [line.strip() for line in f.read().split('\n')]

  return {k: v for k, v in [parse_env_line(line) for line in content]}


def env_dict_from_options(options):
  return {k: v for k, v in [parse_env_option(opt) for opt in options]}


def parse_env_option(option):
  comps = option.split('=', 1)

  if len(comps) != 2:
    log('Invalid env option "{}". Must be in the format "key=value".'.format(option))
    exit(1)

  return comps


def parse_env_line(line):
  # Supported regex patterns for parsing an env var from a line of text.
  export_match = re.match('^export (.*)=\"(.*)\"', line)
  key_equals_val_match = re.match('(.*)=(.*)', line)

  if export_match:
    return parse_env_line_match(export_match, line)

  if key_equals_val_match:
    return parse_env_line_match(key_equals_val_match, line)

  env_line_parse_err(line)


def parse_env_line_match(match, line):
  groups = [g for g in match.groups() if g]

  if len(groups) != 2:
    env_line_parse_err(line)

  return groups


def env_line_parse_err(line):
  log('Error parsing env var from line "{}".'.format(line))
  exit(1)
