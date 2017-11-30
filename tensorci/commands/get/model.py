import click
from tensorci import log, auth_required


@click.command()
@click.option('--prediction', '-p', help='prediction model belongs to')
def model(prediction):
  auth_required()
  log('Getting model for prediction {}...'.format(prediction))