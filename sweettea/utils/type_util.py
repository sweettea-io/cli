import sys


def get_filesystem_encoding():
  return sys.getfilesystemencoding() or sys.getdefaultencoding()


def to_str(value):
  """Converts a value into a valid string."""
  if isinstance(value, bytes):
    try:
      return value.decode(get_filesystem_encoding())
    except UnicodeError:
      return value.decode('utf-8', 'replace')

  return str(value)