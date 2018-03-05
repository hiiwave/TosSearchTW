from pathlib import Path


def langmap_merge():
    TSVS = ['ETC.tsv', 'INTL.tsv', 'ITEM.tsv',
            'QUEST.tsv', 'QUEST_JOBSTEP.tsv',
            'QUEST_LV_0100.tsv', 'QUEST_LV_0200.tsv',
            'QUEST_LV_0300.tsv', 'QUEST_LV_0400.tsv',
            'QUEST_UNUSED.tsv', 'SKILL.tsv', 'UI.tsv']
    path_langmap = Path('./langmap')
    path_output = path_langmap / 'merged.tsv'

    with path_output.open('w', encoding='utf-8') as outfile:
        for tsv in TSVS:
            path_tsv = path_langmap / tsv
            with path_tsv.open(encoding='utf-8') as infile:
                outfile.write(infile.read())


if __name__ == '__main__':
    langmap_merge()
