"""
TensorCI API client
"""
import os
from sweettea.config import config
from sweettea.definitions import auth_header_name
from sweettea.utils.abstract_api import AbstractApi
from sweettea.utils.auth import get_password

# Configure a TensorCI API client
api = AbstractApi(base_url=config.API_URL,
                  auth_header_name=auth_header_name,
                  auth_header_val_getter=get_password)