import pandas as pd
from pathlib import Path


class DictionaryGenerator():
    def __init__(self, path_neet, path_langmap):
        self.path_neet = Path(path_neet)
        self.path_langmap = Path(path_langmap)

    def read_langmap(self):
        df = pd.read_csv(self.path_langmap, sep='\t',
                         names=['tw', 'en', 'korean'],
                         usecols=[0, 1, 2],
                         error_bad_lines=False)
        return df

    def readjson(self, filename):
        path = self.path_neet / filename
        df = pd.read_json(path, orient='records')

        return df
