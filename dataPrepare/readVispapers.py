import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

# 发表文献数量，得到x[年份]，y[当年发表文献的数量]
#reference
numAvgreferencesCounter = {}
#citation
numAvgcitationCountCounter = {}
# journal count
# numJournalCountCounter = {}
# journal category count
# numCategoryCounter = {}

# 读citationCounts和referenceCounts到内存
referenceCounter = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/referenceCounter.pk','rb'))
citationCounter = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/citationCounter.pk','rb'))


# mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'


with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        for k, v in lines.items():
            try:
                if int(v['year']) not in numAvgreferencesCounter:
                    try:
                        numAvgreferencesCounter[int(v['year'])] = [referenceCounter[k]]
                    except:
                        numAvgreferencesCounter[int(v['year'])] = [0]
                    try:
                        numAvgcitationCountCounter[int(v['year'])] = [citationCounter[k]]
                    except:
                        numAvgcitationCountCounter[int(v['year'])] = [0]
                    # numJournalCountCounter[int(v['year'])] = set()
                    # numJournalCountCounter[int(v['year'])].add(v['journalID'])
                #     numCategoryCounter[int(v['year'])] = set()
                #     for i in set(mag2journal[v['journalID']]['FieldList']):
                #         numCategoryCounter[int(v['year'])].add(i)
                else:
                    try:
                        numAvgreferencesCounter[int(v['year'])].append(referenceCounter[k])
                    except:
                        numAvgreferencesCounter[int(v['year'])].append(0)
                    try:
                        numAvgcitationCountCounter[int(v['year'])].append(citationCounter[k])
                    except:
                        numAvgcitationCountCounter[int(v['year'])].append(0)
                    # numJournalCountCounter[int(v['year'])].add(v['journalID'])
                    # for i in set(mag2journal[v['journalID']]['FieldList']):
                    #     numCategoryCounter[int(v['year'])].add(i)
            except:
                continue


for k,v in numAvgreferencesCounter.items():
    numAvgreferencesCounter[k] = sum(v)/len(v)

for k,v in numAvgcitationCountCounter.items():
    numAvgcitationCountCounter[k] = sum(v)/len(v)

# for k,v in numJournalCountCounter.items():
#     numJournalCountCounter[k] = len(v)

# for k,v in numCategoryCounter.items():
#     numCategoryCounter[k] = len(v)

pk.dump(numAvgreferencesCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numAvgreferencesCounter.pk', 'wb'))

pk.dump(numAvgcitationCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numAvgcitationCountCounter.pk', 'wb'))

# pk.dump(numJournalCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numJournalCountCounter.pk','wb'))

# pk.dump(numCategoryCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numCategoryCounter.pk','wb'))