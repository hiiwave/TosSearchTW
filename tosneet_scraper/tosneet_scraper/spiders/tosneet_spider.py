import scrapy
from abc import ABCMeta, abstractmethod


class TosneetSpider(scrapy.Spider, metaclass=ABCMeta):
    name = "TBD"
    start_urls = [
        'TBD',
    ]

    # Override
    def parse(self, response):
        yield from self._scrape_page(response)

        next_page = response.css('.pagination').xpath(
            ".//a[text()='›']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def _scrape_page(self, res):
        headers = self._get_tableheader(res)
        for row in res.css('.results-table tbody tr'):
            yield self._parse_row(row, headers)

    def _get_tableheader(self, res):
        thead = res.css('.results-table > thead > tr')[0]
        headers = [tr.xpath('text()').extract_first() for tr in thead.css('th')]
        # Hardcode null header name as 'img'
        headers = [h if h else 'img' for h in headers]
        return headers

    # Could be overriden
    def _parse_row(self, row, headers):
        data = {}
        for i, head in enumerate(headers):
            data[head] = row.css('td:nth-child({})::text'.format(i + 1))
        data = {key: value.extract_first() for key, value in data.items()}
        # Set ClassID as speical attribute
        data['ClassID'] = row.css('td a::text').extract_first()
        return data
