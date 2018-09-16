import click
from sweettea.definitions import default_model_name

MODEL_CMD = 'model'


@click.command(name=MODEL_CMD)
@click.option('--name', '-n', default=default_model_name)
@click.option('--path', required=True)
def upload(name, path):
  pass


@click.command(name=MODEL_CMD)
def download():
  pass
