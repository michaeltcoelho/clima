import click

@click.group()
def clima():
    pass


@clima.command()
def init():
    click.echo('Loading cities...')
