import os
from abstract_api import AbstractApi, ApiException
from tensorci import config

api = AbstractApi(base_url=config.API_URL,
                  auth_header_name='TensorCI-Api-Token',
                  auth_header_value=get_token)