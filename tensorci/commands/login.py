import click
from tensorci import log
from tensorci.utils import auth


@click.command()
@click.option('--email', '-e', prompt=True)
@click.option('--password', '-p', prompt=True, hide_input=True)
def login(email, password):
   email = email.strip()
   pw = password.strip()

   if not email:
      log('Email is required.')
      return

   if not pw:
      log('Password is required.')
      return

