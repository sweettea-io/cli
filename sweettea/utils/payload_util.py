from sweettea.utils import gitconfig


def project_payload(pl=None, key='projectNsp'):
  pl = pl or {}
  pl[key] = gitconfig.get_remote_nsp()
  return pl
