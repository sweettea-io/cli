import click


@click.command(name='use-team')
@click.argument('team')
def use_team(team):
  click.echo('Switched to team: {}.'.format(team))