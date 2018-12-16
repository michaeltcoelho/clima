from crawler import Crawler, ClimaTempoMetricExtractor, ClimaTempoMetric


def test_crawler():
    crawler = Crawler(
        ClimaTempoMetricExtractor(driver=None)
    )
    crawler.crawl([1, 2, 3])
    print(crawler.metrics())
