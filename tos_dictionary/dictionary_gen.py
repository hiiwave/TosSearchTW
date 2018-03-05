import pandas as pd
from pathlib import Path
import functools


class NeetReader():
    def __init__(self, path_neet):
        self.path_neet = Path(path_neet)

    def read(self):
        neettables = {}
        neetnames = ['items']
        for name in neetnames:
            path = self.path_neet / (name + '.json')
            df = pd.read_json(path, orient='records')
            neettables[name] = df
        return neettables


class DictionaryGenerator():
    def __init__(self, path_neet, path_langmap):
        self.neettables = NeetReader(path_neet).read()
        self.path_langmap = Path(path_langmap)
        self.langmap = pd.DataFrame()

    def read_langmap(self):
        self.langmap = pd.read_csv(
            self.path_langmap, sep='\t',
            names=['tw', 'en', 'korean'],
            usecols=[0, 1, 2],
            error_bad_lines=False)

    def run(self):
        self.read_langmap()
        self.merge()
        return self.neettables

    def merge(self):
        for key, table in self.neettables.items():
            self.neettables[key] = pd.merge(
                table, self.langmap,
                left_on='Name', right_on='en', how='inner')

    def to_json(self, df, path, **kwargs):
        print("Output " + str(path))
        with path.open('w', encoding='utf-8') as file:
            df.to_json(file, force_ascii=False, ** kwargs)

    def export_dictionary(self, output='output/'):
        tables = [table for _, table in self.neettables.items()]
        tables = [df[['tw', 'en']] for df in tables]
        langmap = functools.reduce(pd.concat, tables)
        langmap = langmap.drop_duplicates(subset=['tw'])
        dictionary = langmap.set_index('tw')
        if output is not None:
            self.to_json(langmap['tw'], Path(output) / 'names_tw.json',
                         orient='values')
            self.to_json(langmap['en'], Path(output) / 'names_en.json',
                         orient='values')
            self.to_json(dictionary, Path(output) / 'dictionary.json',
                         orient='index')
        return dictionary


if __name__ == '__main__':
    dictgen = DictionaryGenerator(
        '../tosneet_scraper/', './langmap/merged.tsv')
    dictgen.run()
    dictgen.export_dictionary()
