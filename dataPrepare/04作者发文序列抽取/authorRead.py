# nohup python -u authorRead.py > authorRead.log 2>&1 &
import jsonlines
from tqdm import tqdm

import pickle as pk
# 将存在set中的pub，变为由list存储，这样可以存到jsonlines形式
authorSeq = pk.load(open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/authorSeq.pk', 'rb'))
with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/authorSeq.jsonl', mode='w') as writer:
    for k,v in tqdm(authorSeq.items()):
        for year,publist in v.items():
            for Pubtype, Pubset in publist.items():
                v[year][Pubtype] = list(Pubset)
        writer.write({k:v})