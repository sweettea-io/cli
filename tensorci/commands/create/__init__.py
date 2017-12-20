import click
from team import team
from dataset import dataset


@click.group()
def create():
  """
  Create a TensorCI resource.

  Currently supported resources:

  * team

  * dataset
  """
  pass


create.add_command(team)
create.add_command(dataset)