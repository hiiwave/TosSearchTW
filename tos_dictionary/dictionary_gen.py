import pandas as pd
from pathlib import Path


class NeetReader():
    def __init__(self, path_neet):
        self.path_neet = Path(path_neet)

    def read(self):
        neettables = {}
        neetnames = ['items', 'npcs', 'zones', 'skills', 'attributes']
        for name in neetnames:
            path = self.path_neet / (name + '.json')
            df = pd.read_json(path, orient='records')
            df = df.rename({'Name or Alias': 'Name'}, axis='columns')
            df['category'] = name
            neettables[name] = df
        return neettables


class DictionaryGenerator():
    def __init__(self, path_neet, path_langmap):
        self.neettables = NeetReader(path_neet).read()
        self.path_langmap = Path(path_langmap)
        self.langmap = pd.DataFrame()
        self.result_table = pd.DataFrame()

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

    def export(self, output='output/'):
        tables = [table for _, table in self.neettables.items()]
        tables = [df[['tw', 'en', 'ClassID', 'category']] for df in tables]
        for df in tables:
            print(df.head())
        result_table = pd.concat(tables)
        result_table = result_table.drop_duplicates(subset=['tw'])
        result_table = result_table.drop_duplicates(subset=['en'])
        self.result_table = result_table
        self.export_table(result_table, output)

    def export_table(self, result, output):
        self.to_json(result, Path(output) / 'result_list.json',
                     orient='records')
        tables_en = result.set_index('en')
        self.to_json(tables_en, Path(output) / 'tables_en.json',
                     orient='index')
        tables_tw = result.set_index('tw')
        self.to_json(tables_tw, Path(output) / 'tables_tw.json',
                     orient='index')


if __name__ == '__main__':
    dictgen = DictionaryGenerator(
        '../tosneet_scraper/output/', './langmap/merged.tsv')
    dictgen.run()
    dictgen.export()
