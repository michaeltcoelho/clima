import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

from clima import Scraper, Metric

__all__ = ['ClimaTempoMetric', 'ClimaTempoMetricScraper']


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
        city_page_source = self.get_city_page_source(url)
        city_weather_data = self.get_weather_data_from_city_page_source(city_page_source)
        self.driver.quit()
        metric = ClimaTempoMetric(**city_weather_data)
        return metric

    def get_city_page_source(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def get_weather_data_from_city_page_source(self, page_source):
        page = BeautifulSoup(page_source, 'html.parser')
        table = page.find('table', attrs={'class': 'left top20 small-12 border-none'})
        trs = table.find_all('tr')
        current_month_tr = trs[-1]
        tds = current_month_tr.find_all('td')

        city_name_p = page.find('p', attrs={'data-reveal-id': 'geolocation'})
        city_name_span = city_name_p.find_all('span')[1]

        city_name, city_state = city_name_span.text.replace(' ', '').split('-')
        clean_temp = lambda temp: re.sub(r'\W+', '', temp)
        return {
            'city': city_name,
            'state': city_state,
            'month': tds[0].text,
            'min_temp': clean_temp(tds[1].text),
            'max_temp': clean_temp(tds[2].text),
            'rain': tds[3].text,
        }


class ClimaTempoCityScraper(Scraper):
    pass
