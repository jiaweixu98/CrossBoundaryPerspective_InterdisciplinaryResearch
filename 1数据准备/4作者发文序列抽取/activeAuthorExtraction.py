# nohup python -u activeAuthorExtraction.py > activeAuthorExtractionFoRCAS.log 2>&1 &

import jsonlines
from tqdm import tqdm
import pickle as pk
# 抽取比较活跃的作者

# 考虑作者位次的作者发文数量，必须大于1
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
# 按时间排序
def AuthorPublistTimeRank(YearPublist):
    YearPublistRanked = {}
    for k,v in sorted(YearPublist.items()):
        # 如果一个人的发文序列中，有不存在的年份，直接给这个人drop掉（数量应该极少）
        if int(k) < 1801 or int(k) > 2021:
            return ''
        YearPublistRanked[k] = v
    return YearPublistRanked



# 开始年份
def commonstartYearpublist(publist):
    return int(list(publist.keys())[0])
# 休止年份
def commonendYearpublist(publist):
    return int(list(publist.keys())[-1])
# 年份跨度
def commonspanYearpublist(publist):
    return commonendYearpublist(publist) - commonstartYearpublist(publist)




# 这里抽出来所有曾经至少2年，以第一作者或末位作者身份发表过论文的作者，全部的发文序列。
with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeqForCAS.jsonl', mode='w') as writer:
    with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASauthorSeq.jsonl', mode='r') as reader:
        for lines in tqdm(reader):
            for authorID, YearPublist in lines.items():
                # 至少有2年以第一作者身份或末位作者身份，发论文
                if AuthorCount(YearPublist,'both') > 1:
                    #按时间顺序排序，同时丢掉离谱的时间
                    temp = AuthorPublistTimeRank(YearPublist)
                    if temp == '':
                        continue
                    # 大于80显然不是正常的学术生涯轨迹，去掉
                    if commonspanYearpublist(temp) < 81:
                        writer.write({authorID: temp})
# print(authornumPubYearsFreq)
# print(Rank1authornumPubYearsFreq)
# print(RankLasTauthornumPubYearsFreq)
# print(RankIMportantAuthornumPubYearsFreq)

# pk.dump(authornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/authornumPubYearsFreq.pk', 'wb'))
# pk.dump(Rank1authornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/Rank1authornumPubYearsFreq.pk', 'wb'))
# pk.dump(RankLasTauthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/RankLasTauthornumPubYearsFreq.pk', 'wb'))
# pk.dump(RankIMportantAuthornumPubYearsFreq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/RankIMportantAuthornumPubYearsFreq.pk', 'wb'))
