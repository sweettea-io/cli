import click
from tensorci import log


@click.command()
@click.option('--prediction', '-p', help='prediction model belongs to')
def model(prediction):
  log('Getting model for prediction {}...'.format(prediction))