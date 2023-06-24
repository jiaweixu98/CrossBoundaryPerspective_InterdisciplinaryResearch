# nohup python -u getPaper2doi.py > getPaper2doi.log 2>&1 &
import jsonlines
from tqdm import tqdm
import pickle as pk
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
paper2doi = {}
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/casPapersRefLargerThan4.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        # 这是一个字典
        for k,v in lines.items():
            paper2doi[k] = v['doi']
print('len(paper2doi): ',len(paper2doi))
# 56190774
pk.dump(paper2doi, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2doiCas.pk', 'wb'))