import scrapy


class ItemsSpider(scrapy.Spider):
    name = "items"
    start_urls = [
        'https://tos.neet.tv/items?f=1',
    ]

    def parse(self, response):
        # Get Table header
        # thead = response.css('.results-table thead tr')[0]
        # heads = ['img'] + [tr.extract() for tr in thead.css('th::text')]

        for row in response.css('.results-table tbody tr'):
            data = {
                'img': row.css('td img::attr(src)'),
                'ClassID': row.css('td a::text'),
                'Name': row.css('td:nth-child(3)::text'),
                'Type': row.css('td:nth-child(4)::text'),
                'Grade': row.css('td .item-grade::attr(data-tip)'),
                'Req. Lvl': row.css('td:nth-child(6)::text')
            }
            data = {key: value.extract_first() for key, value in data.items()}
            yield data

        next_page = response.css('.pagination').xpath(
            ".//a[text()='›']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
