import click
from team import team
from dataset import dataset


@click.group()
def create():
  pass


create.add_command(team)
create.add_command(dataset)