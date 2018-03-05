from .tosneet_spider import TosneetSpider


class ItemsSpider(TosneetSpider):
    name = "items"
    start_urls = [
        'https://tos.neet.tv/items?f=1',
    ]

    def scrape_page(self, response):
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
