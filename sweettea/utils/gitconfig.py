"""
Utility for interacting with the git repo of the current working directory
"""
import git
import os
from sweettea import log
from urllib.parse import urlparse


def get_remote_nsp(remote='origin', required=True):
  """
  Read the git url for the given remote from the .git/config
  file of the current working directory and return the combined host+path from
  that url, without the .git extension if included in the path

  Ex: If the git url is 'https://github.com/team/project.git',
      the return value will be 'github.com/team/project'

  :param str remote: Git remote to look for
  :param bool required: Should the program exit if the url for this remote isn't found?
  :return: The combined host+path of the discovered git url
  :rtype: str
  """
  # Handle case where git remote url isn't found. What to do depends
  # on whether this url is required to exist or not...
  def handle_not_found(err):
    if not required:
      return None
    log(err)
    exit(1)

  # Path to .git/ folder inside current working directory.
  git_path = os.path.join(os.getcwd(), '.git')

  # Ensure cwd is a git repository.
  is_git_repo = os.path.exists(git_path) and os.path.isdir(git_path)

  if not is_git_repo:
    return handle_not_found('Current project is not a git repository.')

  # git config default path.
  config_path = os.path.join(git_path, 'config')

  if not os.path.exists(config_path):
    return handle_not_found('.git/config file missing.')

  try:
    # Parse the git config file.
    config = git.GitConfigParser([config_path], read_only=True)
  except KeyboardInterrupt:
    exit(0)
  except BaseException:
    return handle_not_found('Error parsing .git/config file.')

  try:
    # Get the url for the given remote
    url = config.get_value('remote "{}"'.format(remote), 'url')
  except KeyboardInterrupt:
    exit(0)
  except BaseException:
    return handle_not_found('Error determining remote origin url...make sure you have a git remote origin set up.')

  # Split url into components.
  url_comps = urlparse(str(url))
  host = url_comps.netloc
  path = url_comps.path

  if path.endswith('.git'):
    path = path[:-4]

  return host + path
