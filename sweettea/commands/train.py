import click
from sweettea.utils.deployment import deploy


@click.command()
def train():
  """
  Train a model on the SweetTea Train Cluster.

  The master branch of your current project's remote git repository will be deployed
  to the SweetTea Train Cluster, where the following functions specified in
  .sweettea.yml will be executed (in order):

  1. training.dataset.fetch (if provided)
  2. training.dataset.prepro (if provided)
  3. training.train
  4. training.test (if provided)
  5. training.eval (if provided)

  Ex: st train
  """
  try:
    pass
    # deploy(action='train')
  except KeyboardInterrupt:
    return