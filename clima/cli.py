import click

from clima import Crawler
from clima.scrapers.ibge import CityScraper

STATES = [
    'AC', 'AL', 'AM', 'AP',
    'BA', 'CE', 'DF', 'ES',
    'GO', 'MA', 'MG', 'MS',
    'MT', 'PA', 'PB', 'PE',
    'PI', 'PR', 'RJ', 'RN',
    'RO', 'RR', 'RS', 'SC',
    'SE', 'SP', 'TO',
]


@click.group()
def clima():
    pass


@clima.command()
def init():
    click.echo('Loading cities...')
    city_crawler = Crawler(CityScraper(driver=None), concurrency=10)
    city_crawler.crawl(['https://cidades.ibge.gov.br/' for x in range(10000)])
