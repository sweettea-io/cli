"""
Utility methods related to all-things URL
"""
import re


def is_valid_url(url):
  """
  Check if a URL is a valid http/https url.

  :param str url: Url to validate
  :return: Whether the url is valid
  :rtype: bool
  """
  url_regex = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

  return re.match(url_regex, url) is not None
