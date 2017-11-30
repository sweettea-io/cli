import os
from abstract_api import AbstractApi, ApiException
from tensorci.config import confgi
from tensorci.definitions import auth_header_name

api = AbstractApi(base_url=config.API_URL,
                  auth_header_name=auth_header_name,
                  auth_header_value=get_token)