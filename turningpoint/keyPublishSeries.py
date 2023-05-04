# nohup python -u keyPublishSeries.py -u > keyPublishSeries.log 2>&1 &
import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
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

# ##############################################################################################################

# # 累计主要参与者期刊数
# def cumKeyJounalNum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     publishedJournalSet = set()
#     for _, yearpublist in publist.items():
#         # 是第一作者或末位作者
#         if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
#             for rank1paper in yearpublist['rank1']:
#                 publishedJournalSet.add(paper2journalid[rank1paper])
#             for rankLastpaper in yearpublist['rankLast']:
#                 publishedJournalSet.add(paper2journalid[rankLastpaper])
#             series[yearid] = len(publishedJournalSet)
#             yearid += 1
#     return series


# # 累计第一作者参与期刊
# def cumFirstJounalNum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     publishedJournalSet = set()
#     for _, yearpublist in publist.items():
#         # 是第一作者或末位作者
#         if len(yearpublist['rank1']) > 0:
#             for rank1paper in yearpublist['rank1']:
#                 publishedJournalSet.add(paper2journalid[rank1paper])
#             series[yearid] = len(publishedJournalSet)
#             yearid += 1
#     return series


# # 累计末位作者参与者期刊数
# def cumKeyLastNum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     publishedJournalSet = set()
#     for _, yearpublist in publist.items():
#         # 是末位作者
#         if len(yearpublist['rankLast']) > 0:
#             for rankLastpaper in yearpublist['rankLast']:
#                 publishedJournalSet.add(paper2journalid[rankLastpaper])
#             series[yearid] = len(publishedJournalSet)
#             yearid += 1
#     return series



# ##############################################################################################################

# 主要负责文献：开始年份
def keyStartYearpublist(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    for year, yearpublist in publist.items():
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            return int(year)
# 主要负责文献：休止年份
def keyEndYearpublist(publist):
    for year, yearpublist in sorted(publist.items(), reverse=True):
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            return int(year)
# 主要负责文献：年份跨度
def keySpanYearpublist(publist):
    return keyEndYearpublist(publist) - keyStartYearpublist(publist)



# 累计主要参与者JCR学科(控制年份, 控制职业生涯长度)
def cumKeyJFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            for rank1paper in yearpublist['rank1']:
                for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            for rankLastpaper in yearpublist['rankLast']:
                for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series

# 累计一作JCR学科
def cumFirstJFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者
        if len(yearpublist['rank1']) > 0:
            for rank1paper in yearpublist['rank1']:
                for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series

# 累计末位作者JCR学科
def cumLastJFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是末位作者
        if len(yearpublist['rankLast']) > 0:
            for rankLastpaper in yearpublist['rankLast']:
                for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series


########################################################################
# 主要参与者JCR学科BreakThrough的时间点
def KeyBreakthrough(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            for rank1paper in yearpublist['rank1']:
                for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            for rankLastpaper in yearpublist['rankLast']:
                for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series









##############################################################################################################

# # 累计主要参与者CI学科
# def cumKeyJCINum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     publishedJournalFieldSet = set()
#     for _, yearpublist in publist.items():
#         # 是第一作者或末位作者
#         if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
#             for rank1paper in yearpublist['rank1']:
#                 for field in mag2journal[paper2journalid[rank1paper]]['CitationIndexList']:
#                     publishedJournalFieldSet.add(field)
#             for rankLastpaper in yearpublist['rankLast']:
#                 for field in mag2journal[paper2journalid[rankLastpaper]]['CitationIndexList']:
#                     publishedJournalFieldSet.add(field)
#             series[yearid] = len(publishedJournalFieldSet)
#             yearid += 1
#     return series

# # 累计一作JCR学科
# def cumFirstJCINum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     publishedJournalFieldSet = set()
#     for _, yearpublist in publist.items():
#         # 是第一作者
#         if len(yearpublist['rank1']) > 0:
#             for rank1paper in yearpublist['rank1']:
#                 for field in mag2journal[paper2journalid[rank1paper]]['CitationIndexList']:
#                     publishedJournalFieldSet.add(field)
#             series[yearid] = len(publishedJournalFieldSet)
#             yearid += 1
#     return series

# # 累计末位作者JCR学科
# def cumLastJCINum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
#     series = {}
#     yearid = 1
#     publishedJournalFieldSet = set()
#     for _, yearpublist in publist.items():
#         # 是末位作者
#         if len(yearpublist['rankLast']) > 0:
#             for rankLastpaper in yearpublist['rankLast']:
#                 for field in mag2journal[paper2journalid[rankLastpaper]]['CitationIndexList']:
#                     publishedJournalFieldSet.add(field)
#             series[yearid] = len(publishedJournalFieldSet)
#             yearid += 1
#     return series








# KeySeriesCombineDict = {}
# LastSeriesCombineDict = {}
# FirstSeriesCombineDict = {}

# KeyJournalSeriesCombineDict = {}
# FirstJournalSeriesCombineDict = {}

# LastJournalSeriesCombineDict = {}


KeyFieldSeriesCombineDict = {}
FirstFieldSeriesCombineDict = {}
LastFieldSeriesCombineDict = {}

# FinalActiveAuthorSeq里面的作者发文，是按顺序来的
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='r') as reader:
    # 每一行是一个字典
    for lines in tqdm(reader):
        # 看这个字典（其实此循环只有1个元素）
        for authorid, publist in lines.items():
            # 控制主要年份
            if (1997 < keyStartYearpublist(publist) < 2003) and ( 7< keySpanYearpublist(publist)< 11  ):
                for yearid, keyPubNum in cumKeyJFieldNum(publist).items():
                    if yearid not in KeyFieldSeriesCombineDict:
                        KeyFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        KeyFieldSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in cumFirstJFieldNum(publist).items():
                    if yearid not in FirstFieldSeriesCombineDict:
                        FirstFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        FirstFieldSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in cumLastJFieldNum(publist).items():
                    if yearid not in LastFieldSeriesCombineDict:
                        LastFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        LastFieldSeriesCombineDict[yearid].append(keyPubNum)

KeyJFieldSeriesAVGdict = {}
FirstJFieldSeriesAVGdict = {}
LastJFieldSeriesAVGdict = {}

for k,v in KeyFieldSeriesCombineDict.items():
    KeyJFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in FirstFieldSeriesCombineDict.items():
    FirstJFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in LastFieldSeriesCombineDict.items():
    LastJFieldSeriesAVGdict[k] = sum(v)/len(v)


pk.dump(KeyJFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyJField98_02_8_10SeriesAVGdict.pk', 'wb'))
pk.dump(FirstJFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstJField98_02_8_10SeriesAVGdict.pk', 'wb'))
pk.dump(LastJFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastJField98_02_8_10SeriesAVGdict.pk', 'wb'))


# KeyNumAuthor = {}
# FirstNumAuthor = {}
# LastNumAuthor = {}

# for k,v in KeyFieldSeriesCombineDict.items():
#     KeyNumAuthor[k] = len(v)
# for k,v in FirstFieldSeriesCombineDict.items():
#     FirstNumAuthor[k] = len(v)
# for k,v in LastFieldSeriesCombineDict.items():
#     LastNumAuthor[k] = len(v)


# pk.dump(KeyNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyNumAuthor.pk', 'wb'))
# pk.dump(FirstNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstNumAuthor.pk', 'wb'))
# pk.dump(LastNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastNumAuthor.pk', 'wb'))

# with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='w') as writer:
#     with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeq.jsonl', mode='r') as reader:
#         for lines in tqdm(reader):
#             for authorid, publist in lines.items():
#                 # 只保留职业生涯短于80年的
#                 if commonspanYearpublist(publist) < 81:
#                     writer.write({authorid: publist})