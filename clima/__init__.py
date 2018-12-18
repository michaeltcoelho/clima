import abc
import pathlib
import pprint
import queue
import threading
from dataclasses import dataclass

import huepy as hue
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


DRIVERS_PATH = pathlib.Path(__file__).parent / 'drivers'


@dataclass
class Metric:
    """Metric base data class."""


class Scraper(abc.ABC):
    """Abstract class for specific scraper classes."""

    def __init__(self, driver_name):
        self.driver_name = driver_name

    def get_driver(self):
        return DriverFactory.get_driver(self.driver_name)

    @abc.abstractmethod
    def scrape(self, url):
        """Method responsible for scraping data from a :param url
        and return a python-like datastructure.
        """


class DriverNotImplemented(RuntimeError):
    pass


class Driver(abc.ABC):

    @abc.abstractstaticmethod
    def get_driver():
        pass


class PhanthomJSDriver(Driver):

    def get_driver():
        driver_binary = DRIVERS_PATH / 'phantomjs'
        driver = webdriver.PhantomJS(driver_binary)
        return driver


class DriverFactory:

    @staticmethod
    def get_driver(driver_name):
        if driver_name == 'phantomjs':
            return PhanthomJSDriver.get_driver()
        raise DriverNotImplemented


class AsyncScraperRunner(threading.Thread):
    """Allows running a :class Scraper based class
    in a daemon thread.
    """

    def __init__(self, scraper, input_queue, output_queue):
        threading.Thread.__init__(self)
        self.scraper = scraper
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.setDaemon(True)
        self.start()

    # TODO: better exception handling
    def run(self):
        """Thread run method."""
        try:
            while self.input_queue.not_empty:
                url = self.input_queue.get(timeout=1)
                data = self.scraper.scrape(url)
                self.output_queue.put(data)
                self.input_queue.task_done()
        except queue.Empty:
            pass
        except WebDriverException as err:
            print(hue.red(str(err)))
            self.input_queue.task_done()


class Crawler:
    """Crawler is responsible for receiving a :class Scrape based class
    instance and spawn :class AsyncScraperRunner thread.

    Arguments:
        - scraper: A :class Scraper based class instance.
        - concurrency: The number of concurrent threads available
        for running :param scraper.
    """

    def __init__(self, scraper, concurrency=1):
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        for _ in range(concurrency):
            AsyncScraperRunner(scraper, self.input_queue, self.output_queue)

    def crawl(self, urls):
        """Receives a list of urls for scraping from and head them to
        a queue.
        """
        for url in urls:
            self.input_queue.put(url)
        self.input_queue.join()

    def iterdata(self):
        """Yield each data from the output queue."""
        try:
            while self.output_queue.not_empty:
                data = self.output_queue.get_nowait()
                yield data
        except queue.Empty:
            print(hue.yellow('No more data available :)'))
