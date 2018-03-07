# Tos Search Gadget
This is a search gadget for [Tree of Savior](https://treeofsavior.com/page/main/)  game.

## Features:
* Support Chinese(zh-tw) / English
* Support typeahead(autocomplete)
* Link search result to [tosgbase](https://tos.neet.tv/)

## Demo:
https://hiiwave.github.io/TosSearchTW/frontend/index.html

## Screenshot:

Search by English          |  Search by Chinese
:-------------------------:|:-------------------------:
![search_en](./demo/search_en.png)  |  ![search_tw](./demo/search_tw.png)

------

## Developer Note
This project is composed of three parts:

1. [Scraper (`tosneet_scraper/`)](./tosneet_scraper/):
Extract data (item list, npc list, .etc) from tosgbase.
Implemeneted by [scrapy](https://scrapy.org/).

2. [Dictionary (`tos_dictionary/`)](./tos_dictionary/):
Merge scraped data, append zh-tw language, and export a lookup table. Implemented by [pandas](http://pandas.pydata.org/).
The language mapping file is exported from project [Tos-Translator](https://github.com/hiiwave/Tos-Translater).

3. [Frontend (`frontend/`)](./frontend/):
The web interface of this gadget. Implemented by [typeahead.js](https://github.com/twitter/typeahead.js).

Please refer to `README.md` in these subfolders for more details.


## Known Issues:
* Some suggestions fail to show when they include spaces *and* there are longer words including them;
for example the word "Swordsman Master" does not show due to the existence of "Swordsman Master Costume".
In this case you could still type "Swordsman Master" and click search button to get the result.
It seems to be a *typeahead.js* issue, see [this](https://github.com/twitter/typeahead.js/issues/238) or [this](https://github.com/twitter/typeahead.js/issues/1198) for more details.


## Contribution
Any issue reporting or pull request is welcome.


## LICENSE
[MIT](LICENSE)
