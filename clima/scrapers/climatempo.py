import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

from clima import Scraper, Metric

__all__ = [
    'ClimaTempoMetric', 'ClimaTempoMetricScraper',
    'GoogleClimaTempoCityLinkScraper',
]


@dataclass
class ClimaTempoMetric(Metric):
    city: str
    state: str
    month: str
    min_temp: int
    max_temp: int
    rain: int


class ClimaTempoMetricScraper(Scraper):
    """Scrapes data from https://www.climatempo.com.br/."""

    def scrape(self, url):
        driver = self.get_driver()
        climatempo_city_page = self.get_city_page_source(driver, url)
        climatempo_city_data = self.get_weather_data_from_city_page_source(
            climatempo_city_page)
        driver.quit()
        metric = ClimaTempoMetric(**climatempo_city_data)
        return metric

    def get_city_page_source(self, driver, url):
        print(f'Fetching Climatempo at {url}')
        driver.get(url)
        return driver.page_source

    def get_weather_data_from_city_page_source(self, page_source):
        page = BeautifulSoup(page_source, 'html.parser')
        table_attrs = {
            'class': 'left top20 small-12 border-none',
        }
        table = page.find('table', attrs=table_attrs)

        metric_trs = table.find_all('tr')
        last_month_measured_weather_tr = metric_trs[-1]
        last_mesured_month_metric_tds = last_month_measured_weather_tr\
            .find_all('td')

        city_name_p = page.find('p', attrs={'data-reveal-id': 'geolocation'})
        city_name_span = city_name_p.find_all('span')[1]

        city_name, city_state = city_name_span.text\
            .replace(' ', '')\
            .split('-')
        clean_temp = lambda temp: re.sub(r'\W+', '', temp)

        return {
            'city': city_name,
            'state': city_state,
            'month': last_mesured_month_metric_tds[0].text,
            'min_temp': clean_temp(last_mesured_month_metric_tds[1].text),
            'max_temp': clean_temp(last_mesured_month_metric_tds[2].text),
            'rain': last_mesured_month_metric_tds[3].text,
        }


class GoogleClimaTempoCityLinkScraper(Scraper):
    """Scrapes climatempo weather city link on google."""

    def scrape(self, url):
        driver = self.get_driver()
        google_page_source = self.get_page_source(driver, url)
        climatempo_city_link = self.get_climatempo_city_link(
            url, google_page_source)
        print(f'Closing driver for url at {url}')
        driver.quit()
        return climatempo_city_link

    def get_page_source(self, driver, url):
        print(f'Fetching page at {url}...')
        driver.get(url)
        return driver.page_source

    def get_climatempo_city_link(self, url, page_source):
        page = BeautifulSoup(page_source, 'html.parser')
        climatempo_link_tag = page.select_one('a[href*=/url?q=https://www.climatempo.com.br/climatologia/]')
        if climatempo_link_tag is None:
            print(f'City not found on google at {url}')
            return ''
        climatempo_link = self.get_climatempo_link_from_tag(
            climatempo_link_tag)
        return climatempo_link

    def get_climatempo_link_from_tag(self, tag):
        match = re.search(r'(?P<url>https?://[^\s]+)', tag['href'])
        if match is not None:
            climatempo_link = match.group('url')
            climatempo_link = climatempo_link.split('&')[0]
            return climatempo_link
        return ''
