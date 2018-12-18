import codecs
import json
import urllib3

import beautifultable
import click
import huepy as hue
from selenium import webdriver

from clima import Crawler
from clima.scrapers.climatempo import (
    ClimaTempoMetricScraper, GoogleClimaTempoCityLinkScraper,
    ClimaTempoMetric,
)
from clima.utils import sanitize_string


def fetch_cities_json():
    click.echo(hue.yellow('Fetching cities json...'))
    json_url = 'https://raw.githubusercontent.com/michaeltcoelho/'\
        'Municipios-Brasileiros/master/municipios_brasileiros.json'
    http = urllib3.PoolManager()
    response = http.request('GET', json_url)
    data = json.loads(response.data.decode('utf-8-sig'))
    click.echo(hue.yellow('Cities json fetched...'))
    return data


def get_google_search_cities_links(limit):
    cities_data = fetch_cities_json()
    links = []
    for city_data in cities_data[:limit]:
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


@clima.command(
    help='Display the first 100 brazilian cities in alphabetical order.'
)
@click.option('--concurrency', type=int, default=5)
def show(concurrency):
    cities_links = get_google_search_cities_links(limit=100)

    google_climatempo_scraper = GoogleClimaTempoCityLinkScraper(driver_name='phantomjs')
    google_climatempo_crawler = Crawler(
        scraper=google_climatempo_scraper,
        concurrency=concurrency)
    google_climatempo_crawler.crawl(cities_links)

    climatempo_links = google_climatempo_crawler.iterdata()

    climatempo_metric_scraper = ClimaTempoMetricScraper(driver_name='phantomjs')
    climatempo_metric_crawler = Crawler(
        scraper=climatempo_metric_scraper,
        concurrency=concurrency)
    climatempo_metric_crawler.crawl(climatempo_links)

    climatempo_metrics = climatempo_metric_crawler.iterdata()

    table = beautifultable.BeautifulTable(max_width=120)
    table.column_headers = [
        'City', 'State', 'Month',
        'Min. Temp. (˚C)', 'Max. Temp. (˚C)',
        'Rain (mm)',
    ]
    for metric in climatempo_metrics:
        table.append_row([
            metric.city, metric.state,
            metric.month, metric.min_temp,
            metric.max_temp, metric.rain,
        ])
    print(table)
