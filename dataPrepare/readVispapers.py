import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk
import numpy as np
# 计算bootstrap，对于大规模数据，这里的内存占用非常可怕。减少sample的数量和batch应该会有用.https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.bootstrap.html#:~:text=of%20the%20statistic.-,batchint%2C%20optional,-The%20number%20of
# The number of resamples to process in each vectorized call to statistic. Memory usage is O(batch`*``n`), where n is the sample size. Default is None, in which case batch = n_resamples (or batch = max(n_resamples, n) for method='BCa').
from scipy.stats import bootstrap

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

# numBOOTSAvgreferencesCounter = {}
# numBOOTSAvgcitationCountCounter = {}
# 中位数
numBOOTSmedreferencesCounter = {}
# 中位数
numBOOTSmedcitationCountCounter = {}

# print('numAvgreferencesCounter')
# for k,v in tqdm(numAvgreferencesCounter.items()):
#     # 计算平均数的bootstrap
#     res = bootstrap((v,), np.mean, confidence_level=0.95, batch=1, n_resamples=5)
#     numBOOTSAvgreferencesCounter[k] = [np.mean(v),res.confidence_interval]
#     # 计算中位数的bootstrap
#     res = bootstrap((v,), np.median, confidence_level=0.95, batch=1, n_resamples=5)
#     numBOOTSmedreferencesCounter[k] = [np.median(v),res.confidence_interval]

# print('numAvgcitationCountCounter')
# for k,v in tqdm(numAvgcitationCountCounter.items()):
#     # 计算平均数的bootstrap
#     res = bootstrap((v,), np.mean, confidence_level=0.95, batch=1, n_resamples=5)
#     numBOOTSAvgcitationCountCounter[k] = [np.mean(v),res.confidence_interval]
#     # 计算中位数的bootstrap
#     res = bootstrap((v,), np.median, confidence_level=0.95, batch=1, n_resamples=5)
#     numBOOTSmedcitationCountCounter[k] = [np.median(v),res.confidence_interval]





print('numAvgreferencesCounter')
for k,v in tqdm(numAvgreferencesCounter.items()):
    # 计算中位数的bootstrap
    numBOOTSmedreferencesCounter[k] = np.median(v)

print('numAvgcitationCountCounter')
for k,v in tqdm(numAvgcitationCountCounter.items()):
    # 计算中位数的bootstrap
    numBOOTSmedcitationCountCounter[k] = np.median(v)



# for k,v in numJournalCountCounter.items():
#     numJournalCountCounter[k] = len(v)

# for k,v in numCategoryCounter.items():
#     numCategoryCounter[k] = len(v)

# pk.dump(numAvgreferencesCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numAvgreferencesCounter.pk', 'wb'))

# pk.dump(numAvgcitationCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numAvgcitationCountCounter.pk', 'wb'))

# pk.dump(numJournalCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numJournalCountCounter.pk','wb'))

# pk.dump(numCategoryCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numCategoryCounter.pk','wb'))

# pk.dump(numBOOTSAvgreferencesCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numBOOTSAvgreferencesCounter.pk', 'wb'))
pk.dump(numBOOTSmedreferencesCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numBOOTSmedreferencesCounter.pk', 'wb'))
# pk.dump(numBOOTSAvgcitationCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numBOOTSAvgcitationCountCounter.pk', 'wb'))
pk.dump(numBOOTSmedcitationCountCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/numBOOTSmedcitationCountCounter.pk', 'wb'))