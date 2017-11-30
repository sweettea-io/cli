import click
from commands import all_cmds


@click.group()
def cli():
  pass


# Add all commands to the CLI
[cli.add_command(cmd) for cmd in all_cmds]