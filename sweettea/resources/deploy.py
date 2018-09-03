import click
from sweettea.definitions import default_model_name
from sweettea.utils.api import api
from sweettea.utils.env_util import parse_cmd_envs
from sweettea.utils.payload_util import project_payload

DEPLOY_CMD = 'deploy'


@click.command(name=DEPLOY_CMD)
@click.option('--name', '-n', required=True)
@click.option('--cluster', '-c', required=True)
@click.option('--model', '-m', default=default_model_name)
@click.option('--sha')
@click.option('--env-file')
@click.option('--env', multiple=True)
def create(name, cluster, model, sha, env_file, env):
  """
  Host model predictions from an API.

  The master branch of your current project's remote git repository will be deployed
  to the specified SweetTea API Cluster, where the specified model will be fetched from
  cloud storage and used to host predictions behind a generated API endpoint.

  Ex: $ st create deploy --name my-deploy --cluster my-cluster --model my-model
  """
  # Create map of custom environment variables to use with this train job.
  envs = parse_cmd_envs(env_file_path=env_file, env_options=env)

  # Create payload.
  payload = project_payload({
    'name': name,
    'apiCluster': cluster,
    'model': model,
    'sha': sha,
    'envs': envs
  })

  try:
    # Create the deploy.
    resp = api.post('/deploy', payload=payload, stream=True)
  except KeyboardInterrupt:
    return

  # Stream the response logs.
  resp.log_stream()
