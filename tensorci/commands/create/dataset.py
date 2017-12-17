import click
import os
from tensorci import log
from tensorci.helpers.auth_helper import auth_required
from tensorci.helpers.payload_helper import team_prediction_payload
from tensorci.utils.api import api, ApiException
from slugify import slugify
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor


@click.command()
@click.option('--name', '-n')
@click.option('--file', '-f', required=True)
def dataset(name, file):
  # Require authed user
  auth_required()

  # Start building our payload
  payload = team_prediction_payload()

  # If dataset name specified, slugify it.
  if name:
    dataset_slug = slugify(name, separator='-', to_lower=True)
  else:
    # Default dataset slug is just prediction slug.
    dataset_slug = payload['prediction_slug']

  payload['dataset_slug'] = dataset_slug

  # Make sure file actually exists
  if not os.path.exists(file):
    log('No file found at path {}'.format(file))
    return

  # Require dataset file to be JSON
  if not file.endswith('.json'):
    log('Dataset must be a JSON file (i.e. dataset.json)')
    return

  # Add file to payload
  payload['file'] = ('dataset.json', open(file, 'rb'), 'application/json')

  # Create a multipart encoder
  encoder = MultipartEncoder(fields=payload)

  # Create a monitor for the encoder so we can track upload progress
  monitor = MultipartEncoderMonitor(encoder, monitor_upload)

  try:
    resp = api.post('/dataset',
                    data=monitor,
                    headers={'Content-Type': monitor.content_type},
                    mp_upload=True)
  except ApiException as e:
    log(e.message)
    return

  print resp.__dict__

  log('Successfully created dataset {}.'.format(dataset_slug))


def monitor_upload(monitor):
  pass