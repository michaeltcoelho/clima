from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from clima import Crawler, Scraper
from clima.scrapers import climatempo


def test_dummy_crawler():

    class DummyScraper(Scraper):
        def scrape(self, url):
            return url

    urls = ['http://example.org/%s' % num for num in range(3)]

    crawler = Crawler(DummyScraper(driver=None))
    crawler.crawl(urls)
    assert list(crawler.iterdata()) == urls


def test_climatempo_scraper(mock_loader):
    class DummyClimaTempoDriver:
        def __init__(self):
            self.page_source = ''

        def get(self, url):
            self.page_source = mock_loader('climatempo/araraquara-sp.txt')

        def quit(self):
            pass

    url = 'https://www.climatempo.com.br/climatologia/397/araraquara-sp'
    scraper = climatempo.ClimaTempoMetricScraper(driver=DummyClimaTempoDriver())
    climatempo_metric = scraper.scrape(url)
    assert climatempo_metric.city == 'Araraquara'
    assert climatempo_metric.state == 'SP'
    assert climatempo_metric.min_temp == '20'
    assert climatempo_metric.max_temp == '28'
    assert climatempo_metric.rain == '224'
