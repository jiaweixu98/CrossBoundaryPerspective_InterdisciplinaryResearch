# 保留cas大类中包含的期刊，且期刊参考文献数量>4
# nohup python -u casJournalRefLargerThan4.py > casJournalRefLargerThan4.log 2>&1 &
import jsonlines
from tqdm import tqdm
import pickle as pk
magid2bigcategory = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/magid2bigcategory.pk','rb'))
journal_set = set(list(magid2bigcategory.keys()))
referenceCounter = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/referenceCounter.pk','rb'))
C = 0
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/casPapersRefLargerThan4.jsonl', mode='w') as writer:
    with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='r') as reader:
        for lines in tqdm(reader):
            # 一个字典
            for k,v in lines.items():
                try:
                    if v['journalID'] in journal_set and referenceCounter[k] >4:
                        writer.write({k:{'year':v['year'], 'doi':v['doi'], 'journalID':v['journalID'],'FamilyId':v['FamilyId']}})
                        C += 1
                except:
                    continue
# 56190774
print(C)
# pk.dump(paper2journalid, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'wb'))


