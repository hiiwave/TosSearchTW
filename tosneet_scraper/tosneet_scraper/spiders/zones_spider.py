from .tosneet_spider import TosneetSpider


class ZonesSpider(TosneetSpider):
    name = "zones"
    start_urls = [
        'https://tos.neet.tv/zones',
    ]
