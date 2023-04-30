# paperJournalset, 我们所需要的paper的set
import jsonlines
from tqdm import tqdm
import pickle as pk
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
paperJournalset = set()
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        paperJournalset.add(list(lines.keys())[0])
print(len(paperJournalset))
# 56190774
pk.dump(paperJournalset, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperJournalset.pk', 'wb'))
