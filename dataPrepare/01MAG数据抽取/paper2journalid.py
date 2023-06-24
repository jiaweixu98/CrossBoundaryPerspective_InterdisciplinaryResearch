# paper2journalid的对应
import jsonlines
from tqdm import tqdm
import pickle as pk
paper2journalid = {}

with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        for k,v in lines.items():
            paper2journalid[k] = v['journalID']
print(len(paper2journalid))
# 56190774
pk.dump(paper2journalid, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'wb'))
