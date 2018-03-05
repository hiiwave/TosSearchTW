import scrapy
from abc import ABCMeta, abstractmethod


class TosneetSpider(scrapy.Spider, metaclass=ABCMeta):
    @abstractmethod
    def scrape_page(self, response):
        pass

    def parse(self, response):
        yield from self.scrape_page(response)

        next_page = response.css('.pagination').xpath(
            ".//a[text()='›']/@href").extract()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
