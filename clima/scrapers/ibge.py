from dataclasses import dataclass

from bs4 import BeautifulSoup

from clima import Scraper, Metric

__all__ = ['City', 'CityScraper']


@dataclass
class City(Metric):
    name: str


class CityScraper(Scraper):
    def scrape(self, url):
        pass
