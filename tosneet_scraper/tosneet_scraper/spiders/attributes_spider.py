from .tosneet_spider import TosneetSpider


class AttributesSpider(TosneetSpider):
    name = "attributes"
    start_urls = [
        'https://tos.neet.tv/attributes?f=1',
    ]

    def _parse_row(self, row, headers):
        data = super()._parse_row(row, headers)
        data['img'] = row.css('td img::attr(src)').extract_first()
        return data
