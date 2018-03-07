from .tosneet_spider import TosneetSpider


class NpcsSpider(TosneetSpider):
    name = "npcs"
    start_urls = [
        'https://tos.neet.tv/npcs?f=1',
    ]
