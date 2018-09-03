import click
import json
from sweettea.definitions import default_model_name
from sweettea.utils.api import api
from sweettea.utils.auth import auth_required
from sweettea.utils.env_util import parse_cmd_envs
from sweettea.utils.payload_util import project_payload


@click.command()
@click.option('--model', '-m', default=default_model_name)
@click.option('--sha')
@click.option('--env-file')
@click.option('--env', multiple=True)
def train(model, sha, env_file, env):
  """
  Train a model on the SweetTea Train Cluster.

  The master branch of your current project's remote git repository will be deployed
  to the SweetTea Train Cluster, where the following functions specified in
  .sweettea.yml will be executed (in order):

  1. training.dataset.fetch (if provided)\n
  2. training.dataset.prepro (if provided)\n
  3. training.train\n
  4. training.test (if provided)\n
  5. training.eval (if provided)\n

  Ex: $ st train --model my-model
  """
  # Must already be logged in to perform this command.
  auth_required()

  # Create map of custom environment variables to use with this train job.
  envs = parse_cmd_envs(env_file_path=env_file, env_options=env)

  # Create payload.
  payload = project_payload({
    'modelName': model,
    'sha': sha,
    'envs': json.dumps(envs)
  })

  try:
    # Create the train job.
    resp = api.post('/train_job', payload=payload, stream=True)
  except KeyboardInterrupt:
    return

  # Stream the response logs.
  resp.log_stream()
