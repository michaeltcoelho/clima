import codecs
import json

import click
from selenium import webdriver

from clima import Crawler
from clima.scrapers.climatempo import (
    ClimaTempoMetricScraper, GoogleClimaTempoCityLinkScraper,
)
from clima.utils import sanitize_string


def get_cities():
    data = codecs.open('./clima/data/cities.json', 'r', 'utf-8-sig')
    return json.load(data)


def get_google_city_search_links():
    cities_data = get_cities()
    links = []
    for city_data in cities_data[:100]:
        city_name = sanitize_string(city_data['nome_municipio'])
        city_state = city_data['uf']
        search_qs = '+'.join([
            'climatempo', 'climatologia',
            city_name, city_state
        ])
        url = f'https://www.google.com.br/search?q={search_qs}'
        links.append(url)
    return links


@click.group()
def clima():
    pass


@clima.command()
def show():
    click.echo('Loading cities...')

    cities_links = get_google_city_search_links()

    google_climatempo_scraper = GoogleClimaTempoCityLinkScraper(driver_name='phantomjs')
    google_climatempo_crawler = Crawler(scraper=google_climatempo_scraper, concurrency=10)
    google_climatempo_crawler.crawl(cities_links)

    climatempo_links = google_climatempo_crawler.iterdata()

    climatempo_metric_scraper = ClimaTempoMetricScraper(driver_name='phantomjs')
    climatempo_metric_crawler = Crawler(scraper=climatempo_metric_scraper, concurrency=10)
    climatempo_metric_crawler.crawl(climatempo_links)

    climatempo_metrics = climatempo_metric_crawler.iterdata()
