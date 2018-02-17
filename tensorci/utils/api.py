import os
from abstract_api import AbstractApi, ApiException
from tensorci.config import config
from tensorci.definitions import auth_header_name
from tensorci.utils.auth import get_password

# Configure our TensorCI API client
api = AbstractApi(base_url=config.API_URL,
                  auth_header_name=auth_header_name,
                  auth_header_val_getter=get_password)