# nohup python -u keyPublishSeries.py -u > keyPublishSeries.log 2>&1 &
import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))

# # 主要负责文献：核心发文数量时间序列
# def ListKeyPub(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     for _, yearpublist in publist.items():
#         if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
#             series[yearid] = len(yearpublist['rank1'])+len(yearpublist['rankLast'])
#             yearid += 1
#     return series

# # 第一作者文献：核心发文数量时间序列
# def ListFirstPub(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     for _, yearpublist in publist.items():
#         if len(yearpublist['rank1']) > 0 :
#             series[yearid] = len(yearpublist['rank1'])
#             yearid += 1
#     return series

# # 末位作者文献：核心发文数量时间序列
# def ListLastPub(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     for _, yearpublist in publist.items():
#         if len(yearpublist['rankLast']) > 0 :
#             series[yearid] = len(yearpublist['rankLast'])
#             yearid += 1
#     return series

##############################################################################################################

# 累计主要参与者期刊数
def cumKeyJounalNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalSet.add(rank1paper)
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalSet.add(rankLastpaper)
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series


# 累计第一作者参与期刊
def cumFirstJounalNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalSet.add(rank1paper)
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series


# 累计末位作者参与者期刊数
def cumKeyLastNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
        # 是末位作者
        if len(yearpublist['rankLast']) > 0:
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalSet.add(rankLastpaper)
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series


# KeySeriesCombineDict = {}
# LastSeriesCombineDict = {}
# FirstSeriesCombineDict = {}

KeyJournalSeriesCombineDict = {}
FirstJournalSeriesCombineDict = {}

LastJournalSeriesCombineDict = {}

# FinalActiveAuthorSeq里面的作者发文，是按顺序来的
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='r') as reader:
    # 每一行是一个字典
    for lines in tqdm(reader):
        # 看这个字典（其实此循环只有1个元素）
        for authorid, publist in lines.items():
            for yearid, keyPubNum in cumKeyJounalNum(publist).items():
                if yearid not in KeyJournalSeriesCombineDict:
                    KeyJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    KeyJournalSeriesCombineDict[yearid].append(keyPubNum)
            for yearid, keyPubNum in cumFirstJounalNum(publist).items():
                if yearid not in FirstJournalSeriesCombineDict:
                    FirstJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    FirstJournalSeriesCombineDict[yearid].append(keyPubNum)
            for yearid, keyPubNum in cumKeyLastNum(publist).items():
                if yearid not in LastJournalSeriesCombineDict:
                    LastJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    LastJournalSeriesCombineDict[yearid].append(keyPubNum)

KeyJournalSeriesAVGdict = {}
FirstJournalSeriesAVGdict = {}
LastJournalSeriesAVGdict = {}

for k,v in KeyJournalSeriesCombineDict.items():
    KeyJournalSeriesAVGdict[k] = sum(v)/len(v)
for k,v in FirstJournalSeriesCombineDict.items():
    FirstJournalSeriesAVGdict[k] = sum(v)/len(v)
for k,v in LastJournalSeriesCombineDict.items():
    LastJournalSeriesAVGdict[k] = sum(v)/len(v)


pk.dump(KeyJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyJournalSeriesAVGdict.pk', 'wb'))
pk.dump(FirstJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstJournalSeriesAVGdict.pk', 'wb'))
pk.dump(LastJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastJournalSeriesAVGdict.pk', 'wb'))

# with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='w') as writer:
#     with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeq.jsonl', mode='r') as reader:
#         for lines in tqdm(reader):
#             for authorid, publist in lines.items():
#                 # 只保留职业生涯短于80年的
#                 if commonspanYearpublist(publist) < 81:
#                     writer.write({authorid: publist})