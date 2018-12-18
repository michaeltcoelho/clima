import pytest
from unittest import mock

from selenium import webdriver

from clima import (
    Crawler, Scraper, DriverNotImplemented, DriverFactory,
    PhanthomJSDriver,
)
from clima.scrapers import climatempo
from clima.utils import sanitize_string


def test_dummy_crawler():

    class DummyScraper(Scraper):
        def scrape(self, url):
            return url

    urls = ['http://example.org/%s' % num for num in range(3)]

    crawler = Crawler(DummyScraper(driver_name=None))
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

    def get_driver():
        return DummyClimaTempoDriver()

    url = 'https://www.climatempo.com.br/climatologia/397/araraquara-sp'
    scraper = climatempo.ClimaTempoMetricScraper(driver_name='')
    scraper.get_driver = get_driver
    climatempo_metric = scraper.scrape(url)
    assert climatempo_metric.city == 'Araraquara'
    assert climatempo_metric.state == 'SP'
    assert climatempo_metric.min_temp == '20'
    assert climatempo_metric.max_temp == '28'
    assert climatempo_metric.rain == '224'


def test_sanitize_string():
    assert 'Albania' == sanitize_string('Albânia')
    assert 'Ribeirao Preto' == sanitize_string('Ribeirão Preto')
    assert 'test' == sanitize_string('test')


@mock.patch('clima.PhanthomJSDriver.get_driver')
def test_driver_factory(mocked_phanthomjsdriver_get_driver):
    mocked_phanthomjsdriver_get_driver.return_value = mock.Mock(webdriver.PhantomJS)
    assert isinstance(DriverFactory.get_driver('phantomjs'), webdriver.PhantomJS)
    with pytest.raises(DriverNotImplemented):
        DriverFactory.get_driver('chrome')
