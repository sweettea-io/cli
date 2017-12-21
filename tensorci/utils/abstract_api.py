import requests
from tensorci import log


class ApiException(BaseException):

  def __init__(self, status=None, code=None, error=None):
    self.status = status
    self.code = code
    self.error = error
    self.message = 'Request returned error: {}'.format(self.error)


class AbstractApi(object):

  def __init__(self, base_url=None, base_headers=None, auth_header_name=None, auth_header_value=None):
    self.base_url = base_url
    self.base_headers = base_headers or {}
    self.auth_header_name = auth_header_name
    self.auth_header_value = auth_header_value

  def get(self, route, **kwargs):
    return self.make_request('get', route, **kwargs)

  def post(self, route, **kwargs):
    return self.make_request('post', route, **kwargs)

  def put(self, route, **kwargs):
    return self.make_request('put', route, **kwargs)

  def delete(self, route, **kwargs):
    return self.make_request('delete', route, **kwargs)

  def make_request(self, method, route, payload=None, headers=None,
                   return_headers=False, stream=False, data=None, mp_upload=False):

    # Get the proper method (get, post, put, or delete)
    request = getattr(requests, method)

    # Build up headers: base_headers --> auth_headers --> custom_headers
    all_headers = self.base_headers

    if self.auth_header_name and self.auth_header_value is not None:
      if type(self.auth_header_value).__name__ == 'function':
        all_headers[self.auth_header_name] = self.auth_header_value()
      else:
        all_headers[self.auth_header_name] = self.auth_header_value

    if headers:
      for k, v in headers.items():
        all_headers[k] = headers[k]

    # Build up args for the request
    args = {'headers': all_headers}

    if method in ['get', 'delete']:
      args['params'] = payload or {}
    else:
      if mp_upload:
        args['data'] = data
      else:
        args['json'] = payload or {}

    args['stream'] = stream

    # Make the request
    try:
      response = request(self.base_url + route, **args)
    except KeyboardInterrupt:
      exit(0)
    except BaseException as e:
      log('Unknown Error while making request: {}'.format(e))
      exit(1)

    if stream or mp_upload:
      return response

    # Return the JSON response
    return self.handle_response(response, return_headers)

  @staticmethod
  def handle_response(response, return_headers):
    try:
      json = response.json() or {}
    except KeyboardInterrupt:
      exit(0)
    except:
      json = {}

    if response.status_code in (200, 201):
      if return_headers:
        return json, response.headers

      return json
    else:
      raise ApiException(status=response.status_code,
                         code=json.get('code'),
                         error=json.get('error'))