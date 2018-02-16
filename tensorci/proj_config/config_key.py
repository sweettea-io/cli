import re
from slugify import slugify
from importlib import import_module


class ConfigKey(object):
  """
  Class representation of a yaml file's key-value pair.
  Contains methods for setting the key's value, as well as validating its value.

  Basic usage:

    self.my_key = ConfigKey(value='initial value', required=True)

  """

  def __init__(self, value=None, required=False, validation='truthy'):
    """
    :param str value: Value to set for this key
    :param bool required: Is this key's validation required to pass?
    :param validation:
      String name of validation function to use when 'validate' is called, or,
      your own custom validation function.

      Multiple types supported:
        - str
        - function
        - instancemethod

      default: 'truthy'
    """
    self.value = value
    self.required = required
    self.validation = validation

  def set_value(self, val):
    """Set the value for this key"""
    self.value = val

  def validate(self):
    """
    Validate this class's 'value' attribute

    :returns: Whether the value is considered "valid".

    """
    # If value isn't required and also isn't specified, it's automatically valid.
    if not self.required and not self.value:
      return True

    # If value is required but not provided, it's automatically invalid.
    if self.required and not self.value:
      return False

    # If our validation attr is callable, call it.
    if type(self.validation).__name__ in ('function', 'instancemethod'):
      return self.validation()

    # If non-supported validation string provided, fallback to 'truthy' validation.
    if not hasattr(self, self.validation):
      self.validation = 'truthy'

    # Call the supported validator.
    return getattr(self, '{}_validator'.format(self.validation))()

  # --- Validators ---

  def truthy_validator(self):
    """
    :return: Whether this class's 'value' attribute is truthy.
    :rtype: bool
    """
    return bool(self.value)

  def slug_validator(self):
    """
    :return: Whether this class's 'value' attribute is equal to its slug counterpart.
    :rtype: bool
    """
    return self.value == slugify(self.value, separator='-', to_lower=True)

  def url_validator(self):
    """
    :return: Whether this class's 'value' attribute is a valid url.
    :rtype: bool
    """
    url_regex = re.compile(
      r'^(?:http)s?://'  # http:// or https://
      r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
      r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
      r'(?::\d+)?'  # optional port
      r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(url_regex, self.value) is not None

  def mod_function_validator(self):
    """
    :return:
      Whether this class's 'value' attribute is a valid function path.
      Path must follow the 'module1.module2.moduleN:function_name' format.

      Valid example: 'src.main:train'

    :rtype: bool
    """
    # Split the path into modules/function_name
    module_str, func_str = self.value.split(':')

    if not module_str:
      return False

    if not func_str:
      return False

    try:
      # Ensure the provided module actually exists and can be imported
      module = import_module(module_str)
    except KeyboardInterrupt:
      exit(0)
    except:
      return False

    # Module must actually exist
    if not module:
      return False

    # Function must exist on module
    if not hasattr(module, func_str):
      return False

    func = getattr(module, func_str)

    # Ensure function is actually of type 'function'.
    # 'instancemethod' type is not supported as of now.
    return type(func).__name__ == 'function'