import click


@click.group()
def clima():
    pass


@clima.command()
def load():
    click.echo('Loading data...')
