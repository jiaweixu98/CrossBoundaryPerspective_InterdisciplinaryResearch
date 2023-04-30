import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk


# 发表文献数量，得到x[年份]，y[当年发表文献的数量]
#reference, dirty
# numAvgreferencesCounter = {}
#citation, dirty
# numAvgcitationCountCounter = {}
# journal count
numJournalCountCounter = {}
# journal category count
numCategoryCounter = {}

mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'


with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        for k, v in lines.items():
            try:
                if int(v['year']) not in numCategoryCounter:
                    # numAvgreferencesCounter[int(v['year'])] = [int(v['referenceCount'])]
                    # numAvgcitationCountCounter[int(v['year'])] = [int(v['citationCount'])]
                    # numJournalCountCounter[int(v['year'])] = set()
                    # numJournalCountCounter[int(v['year'])].add(v['journalID'])
                    numCategoryCounter[int(v['year'])] = set()
                    for i in set(mag2journal[v['journalID']]['FieldList']):
                        numCategoryCounter[int(v['year'])].add(i)
                else:
                    # numAvgreferencesCounter[int(v['year'])].append(int(v['referenceCount']))
                    # numAvgcitationCountCounter[int(v['year'])].append(int(v['citationCount']))
                    # numJournalCountCounter[int(v['year'])].add(v['journalID'])
                    for i in set(mag2journal[v['journalID']]['FieldList']):
                        numCategoryCounter[int(v['year'])].add(i)
            except:
                continue


# for k,v in numAvgreferencesCounter.items():
#     numAvgreferencesCounter[k] = sum(v)/len(v)

# for k,v in numAvgcitationCountCounter.items():
#     numAvgcitationCountCounter[k] = sum(v)/len(v)

# for k,v in numJournalCountCounter.items():
#     numJournalCountCounter[k] = len(v)

for k,v in numCategoryCounter.items():
    numCategoryCounter[k] = len(v)

# pk.dump(numAvgreferencesCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numAvgreferencesCounter.pk', 'wb'))

# pk.dump(numAvgcitationCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numAvgcitationCountCounter.pk', 'wb'))

# pk.dump(numJournalCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numJournalCountCounter.pk','wb'))

pk.dump(numCategoryCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numCategoryCounter.pk','wb'))