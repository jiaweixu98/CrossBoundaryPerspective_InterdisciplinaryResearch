# nohup python -u activeAuthorExtraction.py > activeAuthorExtraction.log 2>&1 &

import jsonlines
from tqdm import tqdm
import pickle as pk
# 抽取比较活跃的作者

# 考虑作者位次
def AuthorCount(YearPublist, authorRank):
# yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    count = 0
    if authorRank != 'both':
        for year, publist in YearPublist.items():
            if len(publist[authorRank]) > 0:
                count += 1
    else:
        for year, publist in YearPublist.items():
            if len(publist['rank1']) > 0 or len(publist['rankLast']) > 0:
                count += 1
    return count

def AuthorPublistTimeRank(YearPublist):
    YearPublistRanked = {}
    for k,v in sorted(YearPublist.items()):
        if int(k) < 1801 or int(k) > 2021:
            return ''
        YearPublistRanked[k] = v
    return YearPublistRanked

# 这里抽出来所有曾经至少3年，以第一作者或末位作者身份发表过论文的作者，全部的发文序列。
with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeq.jsonl', mode='w') as writer:
    with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/authorSeq.jsonl', mode='r') as reader:
        for lines in tqdm(reader):
            for authorID, YearPublist in lines.items():
                # 至少有2年以第一作者身份，发论文
                if AuthorCount(YearPublist,'both') > 1:
                    temp = AuthorPublistTimeRank(YearPublist)
                    if temp == '':
                        continue
                    writer.write({authorID: temp})
# print(authornumPubYearsFreq)
# print(Rank1authornumPubYearsFreq)
# print(RankLasTauthornumPubYearsFreq)
# print(RankIMportantAuthornumPubYearsFreq)

# pk.dump(authornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/authornumPubYearsFreq.pk', 'wb'))
# pk.dump(Rank1authornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/Rank1authornumPubYearsFreq.pk', 'wb'))
# pk.dump(RankLasTauthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/RankLasTauthornumPubYearsFreq.pk', 'wb'))
# pk.dump(RankIMportantAuthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/RankIMportantAuthornumPubYearsFreq.pk', 'wb'))
