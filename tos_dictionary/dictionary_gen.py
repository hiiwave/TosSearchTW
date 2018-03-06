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
        self.resulttable = pd.DataFrame()

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
        print("Start merging..")
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
        tables = [df[['tw', 'en', 'ClassID']] for df in tables]
        resulttable = functools.reduce(pd.concat, tables)
        resulttable = resulttable.drop_duplicates(subset=['tw'])
        resulttable = resulttable.drop_duplicates(subset=['en'])
        self.resulttable = resulttable
        # self.export_list(resulttable, output)
        self.export_table(resulttable, output)
        
    def export_list(self, result, output):
        self.to_json(result['tw'], Path(output) / 'names_tw.json',
                     orient='values')
        self.to_json(result['en'], Path(output) / 'names_en.json',
                     orient='values')

    def export_table(self, result, output):
        self.to_json(result, Path(output) / 'result_table.json',
                     orient='records')
        # dictionary = result.set_index('en')
        # self.to_json(dictionary, Path(output) / 'tables_en.json',
        #              orient='index')
        # dictionary = result.set_index('tw')
        # self.to_json(dictionary, Path(output) / 'tables_tw.json',
        #              orient='index')


if __name__ == '__main__':
    dictgen = DictionaryGenerator(
        '../tosneet_scraper/', './langmap/merged.tsv')
    dictgen.run()
    dictgen.export_dictionary()
