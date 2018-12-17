import abc
import queue
import threading
from dataclasses import dataclass


@dataclass
class Metric:
    """Metric base data class."""


class Scraper(abc.ABC):
    """Abstract class for specific scraper classes."""

    def __init__(self, driver):
        self.driver = driver

    @abc.abstractmethod
    def scrape(self, url):
        """Method responsible for scraping data from a :param url
        and returna python-like datastructure.
        """


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
            print(f'No more data available :)')