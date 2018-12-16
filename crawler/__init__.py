import abc
import queue
import threading

from selenium.webdriver.remote.webdriver import WebDriver
from typing import NamedTuple


class Metric(NamedTuple):
    pass


class ClimaTempoMetric(Metric):
    city: str
    state: str
    month: str
    min_temp: int
    max_temp: int
    rain: int


class Extractor(abc.ABC):

    def __init__(self, driver):
        self.driver = driver

    @abc.abstractmethod
    def extract(self, url):
        pass


class ClimaTempoMetricExtractor(Extractor):

    def extract(self, url):
        metric = ClimaTempoMetric()
        metric.city = url
        return metric


class Worker(threading.Thread):

    def __init__(self, extractor, input_queue, output_queue):
        threading.Thread.__init__(self)
        self.extractor = extractor
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.setDaemon(True)
        self.start()

    def run(self):
        url: str = self.input_queue.get()
        metric = self.extractor.extract(url)
        self.output_queue.put(metric)
        self.input_queue.task_done()


class Crawler:

    def __init__(self, extractor, concurrency=5):
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        for _ in range(concurrency):
            Worker(extractor, self.input_queue, self.output_queue)

    def crawl(self, urls):
        for url in urls:
            self.input_queue.put(url)
        self.input_queue.join()

    def metrics(self):
        try:
            while self.output_queue.not_empty:
                metric = self.output_queue.get_nowait()
                yield metric
        except queue.Empty:
            pass
