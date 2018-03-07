from .tosneet_spider import TosneetSpider


class SkillsSpider(TosneetSpider):
    name = "skills"
    start_urls = [
        'https://tos.neet.tv/skills?f=1',
    ]

    def _parse_row(self, row, headers):
        data = super()._parse_row(row, headers)
        data['img'] = row.css('td img::attr(src)').extract_first()
        return data
