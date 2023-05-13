# nohup python -u authorDesciption.py > authorDesciptionForCAS.log 2>&1 &

import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk
# 得到 能发文的年数的分布图，考虑作者的不同身份
#1. 有发文的总年数，分布图
#2. 以第一作者身份发文的年数，分布图
#3. 以末位作者身份发文的年数，分布图
#4. 以末位作者或第一作者身份发文的年数，分布图

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



# 整体情况
authornumPubYearsFreq = Counter()
# 第一作者的情况
Rank1authornumPubYearsFreq = Counter()
# 末位作者的情况
RankLasTauthornumPubYearsFreq = Counter()
# 第一作者或末位作者的情况
RankIMportantAuthornumPubYearsFreq = Counter()
# 非第一作者或末位作者的情况
RankNotIMportantAuthornumPubYearsFreq = Counter()


# n = 100
with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASauthorSeq.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        # n -= 1
        # if n == 0:
        #     break
        for authorID, YearPublist in lines.items():
            authornumPubYearsFreq[len(YearPublist)] += 1
            Rank1authornumPubYearsFreq[AuthorCount(YearPublist,'rank1')] += 1
            RankLasTauthornumPubYearsFreq[AuthorCount(YearPublist,'rankLast')] += 1
            RankIMportantAuthornumPubYearsFreq[AuthorCount(YearPublist,'both')] += 1
            RankNotIMportantAuthornumPubYearsFreq[AuthorCount(YearPublist,'others')] += 1

# print(authornumPubYearsFreq)
# print(Rank1authornumPubYearsFreq)
# print(RankLasTauthornumPubYearsFreq)
# print(RankIMportantAuthornumPubYearsFreq)

pk.dump(authornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASauthornumPubYearsFreq.pk', 'wb'))
pk.dump(Rank1authornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASRank1authornumPubYearsFreq.pk', 'wb'))
pk.dump(RankLasTauthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASRankLasTauthornumPubYearsFreq.pk', 'wb'))
pk.dump(RankIMportantAuthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASRankIMportantAuthornumPubYearsFreq.pk', 'wb'))
pk.dump(RankNotIMportantAuthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASRankNotIMportantAuthornumPubYearsFreq.pk', 'wb'))

