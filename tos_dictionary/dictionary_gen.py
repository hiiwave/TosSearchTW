import pandas as pd
import numpy as np
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
            self.addimg(df, name)
            df['category'] = name
            neettables[name] = df
        return neettables

    def addimg(self, df, name):
        if 'img' in df:
            return
        assert name in ['zones', 'npcs']
        if name == 'zones':
            df['img'] = "thumbnails/zones.png"
        elif name == 'npcs':
            conditions = [
                df['Rank'] == 'Boss',
                df['Rank'] == 'NPC'
            ]
            choices = ['thumbnails/boss.png', 'thumbnails/person.png']
            df['img'] = np.select(conditions, choices,
                                  default='thumbnails/mon.png')


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
        print("Start processing..")
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

    def export(self, output='output/'):
        tables = [table for _, table in self.neettables.items()]
        tables = [df[['tw', 'en', 'ClassID', 'category', 'img']] for df in tables]
        result_table = pd.concat(tables)
        result_table = result_table.drop_duplicates(subset=['tw'])
        result_table = result_table.drop_duplicates(subset=['en'])
        self.result_table = result_table
        self.export_table(result_table, output)

    def export_table(self, result, output):
        self.to_json(result,
                     Path(output) / 'result_list.json',
                     orient='records')
        tables_en = result.set_index('en')
        tables_en = tables_en[['ClassID', 'category']]
        self.to_json(tables_en, Path(output) / 'tables_en.json',
                     orient='index')
        tables_tw = result.set_index('tw')
        tables_tw = tables_en[['ClassID', 'category']]
        self.to_json(tables_tw, Path(output) / 'tables_tw.json',
                     orient='index')


if __name__ == '__main__':
    dictgen = DictionaryGenerator(
        '../tosneet_scraper/output/', './langmap/merged.tsv')
    dictgen.run()
    dictgen.export()
