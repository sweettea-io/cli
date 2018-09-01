from collections import OrderedDict


class ConfigMap(object):

  def __init__(self, value=None, key_order=None):
    """
    :param dict(str: ConfigKey|ConfigMap) value: Dictionary representation of a map section of a config file.
    """
    self.value = value
    self.key_order = key_order or ()

  def get_value(self):
    if not self.value:
      return None

    value = {}
    for k, v in self.value.items():
      val = v.get_value()

      if val is not None:
        value[k] = val

    if not self.key_order:
      return value

    return self._as_ordered_dict(value)

  def is_valid(self):
    """
    Validate each of the key-val pairs inside this ConfigMap.

    :return: Whether the config map is valid or not
    :rtype: bool
    """
    for k, v in self.value.items():
      if not v.is_valid():
        return False

    return True

  def _as_ordered_dict(self, value):
    d = OrderedDict()

    for key in self.key_order:
      val = value.get(key)

      if val is not None:
        d[key] = val

    return d
