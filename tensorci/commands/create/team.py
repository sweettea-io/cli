import click


@click.command()
@click.argument('name')
def team(name):
  click.echo('Creating team {}...'.format(name))