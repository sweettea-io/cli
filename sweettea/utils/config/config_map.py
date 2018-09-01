from collections import OrderedDict


class ConfigMap(object):

  def __init__(self, value=None, key_order=()):
    """
    :param dict(str: ConfigKey|ConfigMap) value: dict representation of a map section of a config file
    :param tuple key_order: Key order to use when saving as an ordered dict
    """
    self.value = value
    self.key_order = key_order

  def unmarshal(self, cfg):
    for key, val in cfg.items():
      if key in self.value:
        self.value[key].unmarshal(val)

  def get_value(self):
    if not self.value:
      return None

    # Create unordered key-val map of data.
    data = {}
    for k, v in self.value.items():
      val = v.get_value()

      if val is not None:
        data[k] = val

    # If no key order specified, return unordered dict.
    if not self.key_order:
      return data

    return self.as_ordered_dict(data)

  def as_ordered_dict(self, data):
    d = OrderedDict()

    for key in self.key_order:
      val = data.get(key)

      if val is not None:
        d[key] = val

    return d

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
