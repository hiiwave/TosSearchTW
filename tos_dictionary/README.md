## Part 2: Dictionary (`tos_dictionary/`)

Merge scraped data, append zh-tw language, and export a lookup table. Implemented by [pandas](http://pandas.pydata.org/).

The language mapping file is exported from project [Tos-Translator](https://github.com/hiiwave/Tos-Translater).

### Usage:
1. Prepare latest language mapping (langmap) files into `langmap`. The langmap files could be exported from [Tos-Translator](https://github.com/hiiwave/Tos-Translater) by function `matcher.export('tw', 'map', output_path / 'langmap')`.

1. `python langmap_merge.py`: to merge langmap files into single file `langmap/merged.tsv`.

1. `python dictionary_gen.py`: export lookup table onto `output/result_list.json` and `output/tables_en.json`.