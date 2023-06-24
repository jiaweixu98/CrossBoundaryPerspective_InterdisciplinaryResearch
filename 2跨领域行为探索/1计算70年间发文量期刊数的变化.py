# nohup python -u keyPublishSeries.py -u > keyPublishSeriesForCAScontrol.log 2>&1 &
import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
magid2bigcategory = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/magid2bigcategory.pk', 'rb'))

# 主要负责文献：开始年份
def StartYearpublist(publist, Typestr='both'):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    if Typestr == 'both':
        for year, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
                return int(year)
    elif Typestr == 'rank1':
        for year, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0:
                return int(year)
    elif Typestr == 'rankLast':
        for year, yearpublist in publist.items():
            if len(yearpublist['rankLast']) > 0:
                return int(year)
    if Typestr == 'all':
        for year, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0 or len(yearpublist['others']) > 0:
                return int(year)
    return -1
# 主要负责文献：休止年份
def EndYearpublist(publist, Typestr='both'):
    if Typestr == 'both':
        for year, yearpublist in sorted(publist.items(), reverse=True):
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
                return int(year)
    elif Typestr == 'rank1':
        for year, yearpublist in sorted(publist.items(), reverse=True):
            if len(yearpublist['rank1']) > 0:
                return int(year)
    elif Typestr == 'rankLast':
        for year, yearpublist in sorted(publist.items(), reverse=True):
            if len(yearpublist['rankLast']) > 0:
                return int(year)
    if Typestr == 'all':
        for year, yearpublist in sorted(publist.items(), reverse=True):
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) or len(yearpublist['others']) > 0:
                return int(year)
    return -1
# 主要负责文献：年份跨度
def SpanYearpublist(publist, Typestr='both'):
    return EndYearpublist(publist,Typestr) - StartYearpublist(publist,Typestr)

# 主要负责文献：真实年份跨度
def TrueSpanYearpublist(publist, Typestr='both'):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    truthSpan = 0
    if Typestr == 'both':
        for _, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
                truthSpan += 1
    elif Typestr == 'rank1':
        for _, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0:
                truthSpan += 1
    elif Typestr == 'rankLast':
        for _, yearpublist in publist.items():
            if len(yearpublist['rankLast']) > 0:
                truthSpan += 1
    elif Typestr == 'all':
        for _, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0 or len(yearpublist['others']) > 0:
                truthSpan += 1
    return truthSpan

# 主要负责文献：核心发文数量时间序列
def ListKeyPub(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    for _, yearpublist in publist.items():
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            series[yearid] = len(yearpublist['rank1'])+len(yearpublist['rankLast'])
            yearid += 1
    return series

# 第一作者文献：核心发文数量时间序列
def ListFirstPub(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    for _, yearpublist in publist.items():
        if len(yearpublist['rank1']) > 0 :
            series[yearid] = len(yearpublist['rank1'])
            yearid += 1
    return series

# # 末位作者文献：核心发文数量时间序列
def ListLastPub(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    for _, yearpublist in publist.items():
        if len(yearpublist['rankLast']) > 0 :
            series[yearid] = len(yearpublist['rankLast'])
            yearid += 1
    return series

# # 所有文献：核心发文数量时间序列
def ListAllPub(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    for _, yearpublist in publist.items():
        if len(yearpublist['others']) > 0 or len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            series[yearid] = len(yearpublist['others']) + len(yearpublist['rank1'])+ len(yearpublist['rankLast'])
            yearid += 1
    return series

# ##############################################################################################################

# # 累计主要参与者期刊数
def cumKeyJournalNum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
#         # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalSet.add(paper2journalid[rank1paper])
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalSet.add(paper2journalid[rankLastpaper])
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series


# # 累计任意作者期刊数
def cumAllJournalNum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
#         # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) or len(yearpublist['others']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalSet.add(paper2journalid[rank1paper])
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalSet.add(paper2journalid[rankLastpaper])
            for otherspaper in yearpublist['others']:
                publishedJournalSet.add(paper2journalid[otherspaper])
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series

# # 累计第一作者参与期刊
def cumFirstJournalNum(publist):
#     # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
#         # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalSet.add(paper2journalid[rank1paper])
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series


# # 累计末位作者参与者期刊数
def cumLastJournalNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalSet = set()
    for _, yearpublist in publist.items():
#         # 是末位作者
        if len(yearpublist['rankLast']) > 0:
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalSet.add(paper2journalid[rankLastpaper])
            series[yearid] = len(publishedJournalSet)
            yearid += 1
    return series







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

def cumAllJFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0 or len(yearpublist['others']) > 0:
            for rank1paper in yearpublist['rank1']:
                for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            for rankLastpaper in yearpublist['rankLast']:
                for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                    publishedJournalFieldSet.add(field)
            for otherp in yearpublist['others']:
                for field in mag2journal[paper2journalid[otherp]]['FieldList']:
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

# # 累计一作CI学科
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

# # 累计末位作者CI学科
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


# 累计主要参与者CAS学科
def cumKeyJCASFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[rank1paper]])
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[rankLastpaper]])
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series

# 累计一作CAS学科
def cumFirstJCASFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是第一作者
        if len(yearpublist['rank1']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[rank1paper]])
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series

# 累计末位作者CAS学科
def cumLastJCASFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        # 是末位作者
        if len(yearpublist['rankLast']) > 0:
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[rankLastpaper]])
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series

# 累计全部作者CAS学科
def cumAllJCASFieldNum(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    series = {}
    yearid = 1
    publishedJournalFieldSet = set()
    for _, yearpublist in publist.items():
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0 or len(yearpublist['others']) > 0:
            for rank1paper in yearpublist['rank1']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[rank1paper]])
            for rankLastpaper in yearpublist['rankLast']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[rankLastpaper]])
            for Otherpaper in yearpublist['others']:
                publishedJournalFieldSet.add(magid2bigcategory[paper2journalid[Otherpaper]])
            series[yearid] = len(publishedJournalFieldSet)
            yearid += 1
    return series


# 存发文量
KeySeriesCombineDict = {}
LastSeriesCombineDict = {}
FirstSeriesCombineDict = {}
AllSeriesCombineDict = {}

# 存期刊数量
KeyJournalSeriesCombineDict = {}
FirstJournalSeriesCombineDict = {}
LastJournalSeriesCombineDict = {}
AllJournalSeriesCombineDict = {}


#存JCR学科
KeyFieldSeriesCombineDict = {}
FirstFieldSeriesCombineDict = {}
LastFieldSeriesCombineDict = {}
AllFieldSeriesCombineDict = {}


#存CAS学科
KeyCASFieldSeriesCombineDict = {}
FirstCASFieldSeriesCombineDict = {}
LastCASFieldSeriesCombineDict = {}
AllCASFieldSeriesCombineDict = {}

# 下面存储的是限定年代、作者发文时间的
#########################
# 存发文量
ControlKeySeriesCombineDict = {}
ControlLastSeriesCombineDict = {}
ControlFirstSeriesCombineDict = {}
ControlAllSeriesCombineDict = {}

# 存期刊数量
ControlKeyJournalSeriesCombineDict = {}
ControlFirstJournalSeriesCombineDict = {}
ControlLastJournalSeriesCombineDict = {}
ControlAllJournalSeriesCombineDict = {}


#存JCR学科
ControlKeyFieldSeriesCombineDict = {}
ControlFirstFieldSeriesCombineDict = {}
ControlLastFieldSeriesCombineDict = {}
ControlAllFieldSeriesCombineDict = {}


#存CAS学科
ControlKeyCASFieldSeriesCombineDict = {}
ControlFirstCASFieldSeriesCombineDict = {}
ControlLastCASFieldSeriesCombineDict = {}
ControlAllCASFieldSeriesCombineDict = {}


CountBoth = 0
CountFirst = 0
CountLast = 0
CountAll = 0
# FinalActiveAuthorSeq里面的作者发文，是按顺序来的
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeqForCAS.jsonl', mode='r') as reader:
    # 每一行是一个字典
    for lines in tqdm(reader):
        # 看这个字典（其实此循环只有1个元素）
        for authorid, publist in lines.items():
            # 1999年至2003年，真实年份为7年
            if (1998< StartYearpublist(publist, 'all') < 2004) and ( 6 < TrueSpanYearpublist(publist, 'all') < 8):
                CountAll += 1
                for yearid, keyPubNum in cumAllJCASFieldNum(publist).items():
                    if yearid not in ControlAllCASFieldSeriesCombineDict:
                        ControlAllCASFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlAllCASFieldSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in ListAllPub(publist).items():
                    if yearid not in ControlAllSeriesCombineDict:
                        ControlAllSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlAllSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in cumAllJFieldNum(publist).items():
                    if yearid not in ControlAllFieldSeriesCombineDict:
                        ControlAllFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlAllFieldSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in cumAllJournalNum(publist).items():
                    if yearid not in ControlAllJournalSeriesCombineDict:
                        ControlAllJournalSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlAllJournalSeriesCombineDict[yearid].append(keyPubNum)
            if (1998< StartYearpublist(publist, 'both') < 2004) and ( 6 < TrueSpanYearpublist(publist, 'both') < 8):
                CountBoth += 1
                for yearid, keyPubNum in cumKeyJCASFieldNum(publist).items():
                    if yearid not in ControlKeyCASFieldSeriesCombineDict:
                        ControlKeyCASFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlKeyCASFieldSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in ListKeyPub(publist).items():
                    if yearid not in ControlKeySeriesCombineDict:
                        ControlKeySeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlKeySeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in cumKeyJFieldNum(publist).items():
                    if yearid not in ControlKeyFieldSeriesCombineDict:
                        ControlKeyFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlKeyFieldSeriesCombineDict[yearid].append(keyPubNum)
                for yearid, keyPubNum in cumKeyJournalNum(publist).items():
                    if yearid not in ControlKeyJournalSeriesCombineDict:
                        ControlKeyJournalSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlKeyJournalSeriesCombineDict[yearid].append(keyPubNum)
                
            if (1998< StartYearpublist(publist, 'rank1') < 2004) and ( 6 < TrueSpanYearpublist(publist, 'rank1') < 8):
                CountFirst += 1
                 # CAS学科
                
                for yearid, keyPubNum in cumFirstJCASFieldNum(publist).items():
                    if yearid not in ControlFirstCASFieldSeriesCombineDict:
                        ControlFirstCASFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlFirstCASFieldSeriesCombineDict[yearid].append(keyPubNum)
                # 计算平均发文量
                
                for yearid, keyPubNum in ListFirstPub(publist).items():
                    if yearid not in ControlFirstSeriesCombineDict:
                        ControlFirstSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlFirstSeriesCombineDict[yearid].append(keyPubNum)
                # JCR学科 KeyCASFieldSeriesCombineDict
                for yearid, keyPubNum in cumFirstJFieldNum(publist).items():
                    if yearid not in ControlFirstFieldSeriesCombineDict:
                        ControlFirstFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlFirstFieldSeriesCombineDict[yearid].append(keyPubNum)
                # 期刊数 KeyCASFieldSeriesCombineDict
                
                for yearid, keyPubNum in cumFirstJournalNum(publist).items():
                    if yearid not in ControlFirstJournalSeriesCombineDict:
                        ControlFirstJournalSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlFirstJournalSeriesCombineDict[yearid].append(keyPubNum)
            if (1998< StartYearpublist(publist, 'rankLast') < 2004) and ( 6 < TrueSpanYearpublist(publist, 'rankLast') < 8):
                CountLast += 1

                for yearid, keyPubNum in cumLastJCASFieldNum(publist).items():
                    if yearid not in ControlLastCASFieldSeriesCombineDict:
                        ControlLastCASFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlLastCASFieldSeriesCombineDict[yearid].append(keyPubNum)
    
                for yearid, keyPubNum in ListLastPub(publist).items():
                    if yearid not in ControlLastSeriesCombineDict:
                        ControlLastSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlLastSeriesCombineDict[yearid].append(keyPubNum)
        
                
                for yearid, keyPubNum in cumLastJFieldNum(publist).items():
                    if yearid not in ControlLastFieldSeriesCombineDict:
                        ControlLastFieldSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlLastFieldSeriesCombineDict[yearid].append(keyPubNum)
                
                
                for yearid, keyPubNum in cumLastJournalNum(publist).items():
                    if yearid not in ControlLastJournalSeriesCombineDict:
                        ControlLastJournalSeriesCombineDict[yearid] = [keyPubNum]
                    else:
                        ControlLastJournalSeriesCombineDict[yearid].append(keyPubNum)
                
            # CAS学科
            # for yearid, keyPubNum in cumKeyJCASFieldNum(publist).items():
            #     if yearid not in KeyCASFieldSeriesCombineDict:
            #         KeyCASFieldSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         KeyCASFieldSeriesCombineDict[yearid].append(keyPubNum)
            # for yearid, keyPubNum in cumFirstJCASFieldNum(publist).items():
            #     if yearid not in FirstCASFieldSeriesCombineDict:
            #         FirstCASFieldSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         FirstCASFieldSeriesCombineDict[yearid].append(keyPubNum)
            # for yearid, keyPubNum in cumLastJCASFieldNum(publist).items():
            #     if yearid not in LastCASFieldSeriesCombineDict:
            #         LastCASFieldSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         LastCASFieldSeriesCombineDict[yearid].append(keyPubNum)
            # for yearid, keyPubNum in cumAllJCASFieldNum(publist).items():
            #     if yearid not in AllCASFieldSeriesCombineDict:
            #         AllCASFieldSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         AllCASFieldSeriesCombineDict[yearid].append(keyPubNum)
            # 计算平均发文量
            # for yearid, keyPubNum in ListKeyPub(publist).items():
            #     if yearid not in KeySeriesCombineDict:
            #         KeySeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         KeySeriesCombineDict[yearid].append(keyPubNum)
            # for yearid, keyPubNum in ListFirstPub(publist).items():
            #     if yearid not in FirstSeriesCombineDict:
            #         FirstSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         FirstSeriesCombineDict[yearid].append(keyPubNum)
            # for yearid, keyPubNum in ListLastPub(publist).items():
            #     if yearid not in LastSeriesCombineDict:
            #         LastSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         LastSeriesCombineDict[yearid].append(keyPubNum)
            # for yearid, keyPubNum in ListAllPub(publist).items():
            #     if yearid not in AllSeriesCombineDict:
            #         AllSeriesCombineDict[yearid] = [keyPubNum]
            #     else:
            #         AllSeriesCombineDict[yearid].append(keyPubNum)
            # JCR学科 KeyCASFieldSeriesCombineDict
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
            for yearid, keyPubNum in cumAllJFieldNum(publist).items():
                if yearid not in AllFieldSeriesCombineDict:
                    AllFieldSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    AllFieldSeriesCombineDict[yearid].append(keyPubNum)
            # 期刊数 KeyCASFieldSeriesCombineDict
            for yearid, keyPubNum in cumKeyJournalNum(publist).items():
                if yearid not in KeyJournalSeriesCombineDict:
                    KeyJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    KeyJournalSeriesCombineDict[yearid].append(keyPubNum)
            for yearid, keyPubNum in cumFirstJournalNum(publist).items():
                if yearid not in FirstJournalSeriesCombineDict:
                    FirstJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    FirstJournalSeriesCombineDict[yearid].append(keyPubNum)
            for yearid, keyPubNum in cumLastJournalNum(publist).items():
                if yearid not in LastJournalSeriesCombineDict:
                    LastJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    LastJournalSeriesCombineDict[yearid].append(keyPubNum)
            for yearid, keyPubNum in cumAllJournalNum(publist).items():
                if yearid not in AllJournalSeriesCombineDict:
                    AllJournalSeriesCombineDict[yearid] = [keyPubNum]
                else:
                    AllJournalSeriesCombineDict[yearid].append(keyPubNum)



# 存发文平均数
# KeySeriesAVGdict = {}
# FirstSeriesAVGdict = {}
# LastSeriesAVGdict = {}
# AllSeriesAVGdict = {}

# KeyNumAuthor = {}
# FirstNumAuthor = {}
# LastNumAuthor = {}
# AllNumAuthor = {}
# for k,v in KeySeriesCombineDict.items():
#     KeySeriesAVGdict[k] = sum(v)/len(v)
#     KeyNumAuthor[k] = len(v)
# for k,v in FirstSeriesCombineDict.items():
#     FirstSeriesAVGdict[k] = sum(v)/len(v)
#     FirstNumAuthor[k] = len(v)
# for k,v in LastSeriesCombineDict.items():
#     LastSeriesAVGdict[k] = sum(v)/len(v)
#     LastNumAuthor[k] = len(v)
# for k,v in AllSeriesCombineDict.items():
#     AllSeriesAVGdict[k] = sum(v)/len(v)
#     AllNumAuthor[k] = len(v)

# pk.dump(KeySeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASKeySeriesAVGdict.pk', 'wb'))
# pk.dump(FirstSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASFirstSeriesAVGdict.pk', 'wb'))
# pk.dump(LastSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASLastSeriesAVGdict.pk', 'wb'))
# pk.dump(AllSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASAllSeriesAVGdict.pk', 'wb'))

# pk.dump(KeyNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASKeyNumAuthor.pk', 'wb'))
# pk.dump(FirstNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASFirstNumAuthor.pk', 'wb'))
# pk.dump(LastNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASLastNumAuthor.pk', 'wb'))
# pk.dump(AllNumAuthor, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CASAllNumAuthor.pk', 'wb'))








# 存发文平均数(控制后)
KeySeriesAVGdict = {}
FirstSeriesAVGdict = {}
LastSeriesAVGdict = {}
AllSeriesAVGdict = {}


for k,v in ControlKeySeriesCombineDict.items():
    KeySeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlFirstSeriesCombineDict.items():
    FirstSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlLastSeriesCombineDict.items():
    LastSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlAllSeriesCombineDict.items():
    AllSeriesAVGdict[k] = sum(v)/len(v)

pk.dump(KeySeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlCASKeySeriesAVGdict.pk', 'wb'))
pk.dump(FirstSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlCASFirstSeriesAVGdict.pk', 'wb'))
pk.dump(LastSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlCASLastSeriesAVGdict.pk', 'wb'))
pk.dump(AllSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlCASAllSeriesAVGdict.pk', 'wb'))






# 存CAS学科平均数
# KeyJCASFieldSeriesAVGdict = {}
# FirstJCASFieldSeriesAVGdict = {}
# LastJCASFieldSeriesAVGdict = {}
# AllJCASFieldSeriesAVGdict = {}
# for k,v in KeyCASFieldSeriesCombineDict.items():
#     KeyJCASFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in FirstCASFieldSeriesCombineDict.items():
#     FirstJCASFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in LastCASFieldSeriesCombineDict.items():
#     LastJCASFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in AllCASFieldSeriesCombineDict.items():
#     AllJCASFieldSeriesAVGdict[k] = sum(v)/len(v)

# pk.dump(KeyJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyJCASFieldSeriesAVGdict.pk', 'wb'))
# pk.dump(FirstJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstJCASFieldSeriesAVGdict.pk', 'wb'))
# pk.dump(LastJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastJCASFieldSeriesAVGdict.pk', 'wb'))
# pk.dump(AllJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/AllJCASFieldSeriesAVGdict.pk', 'wb'))

# 存CAS学科平均数（控制后）
KeyJCASFieldSeriesAVGdict = {}
FirstJCASFieldSeriesAVGdict = {}
LastJCASFieldSeriesAVGdict = {}
AllJCASFieldSeriesAVGdict = {}
for k,v in ControlKeyCASFieldSeriesCombineDict.items():
    KeyJCASFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlFirstCASFieldSeriesCombineDict.items():
    FirstJCASFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlLastCASFieldSeriesCombineDict.items():
    LastJCASFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlAllCASFieldSeriesCombineDict.items():
    AllJCASFieldSeriesAVGdict[k] = sum(v)/len(v)

pk.dump(KeyJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlKeyJCASFieldSeriesAVGdict.pk', 'wb'))
pk.dump(FirstJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlFirstJCASFieldSeriesAVGdict.pk', 'wb'))
pk.dump(LastJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlLastJCASFieldSeriesAVGdict.pk', 'wb'))
pk.dump(AllJCASFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlAllJCASFieldSeriesAVGdict.pk', 'wb'))

# 存JCR学科平均数, KeyJCRFieldSeriesAVGdict
# KeyJCRFieldSeriesAVGdict = {}
# FirstJCRFieldSeriesAVGdict = {}
# LastJCRFieldSeriesAVGdict = {}
# AllJCRFieldSeriesAVGdict = {}
# for k,v in KeyFieldSeriesCombineDict.items():
#     KeyJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in FirstFieldSeriesCombineDict.items():
#     FirstJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in LastFieldSeriesCombineDict.items():
#     LastJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in AllFieldSeriesCombineDict.items():
#     AllJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
# pk.dump(KeyJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyJCRFieldSeriesAVGdict.pk', 'wb'))
# pk.dump(FirstJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstJCRFieldSeriesAVGdict.pk', 'wb'))
# pk.dump(LastJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastJCRFieldSeriesAVGdict.pk', 'wb'))
# pk.dump(AllJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/AllJCRFieldSeriesAVGdict.pk', 'wb'))


# 存JCR学科平均数， 控制后
KeyJCRFieldSeriesAVGdict = {}
FirstJCRFieldSeriesAVGdict = {}
LastJCRFieldSeriesAVGdict = {}
AllJCRFieldSeriesAVGdict = {}
for k,v in ControlKeyFieldSeriesCombineDict.items():
    KeyJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlFirstFieldSeriesCombineDict.items():
    FirstJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlLastFieldSeriesCombineDict.items():
    LastJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlAllFieldSeriesCombineDict.items():
    AllJCRFieldSeriesAVGdict[k] = sum(v)/len(v)
pk.dump(KeyJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlKeyJCRFieldSeriesAVGdict.pk', 'wb'))
pk.dump(FirstJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlFirstJCRFieldSeriesAVGdict.pk', 'wb'))
pk.dump(LastJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlLastJCRFieldSeriesAVGdict.pk', 'wb'))
pk.dump(AllJCRFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlAllJCRFieldSeriesAVGdict.pk', 'wb'))


# 存期刊数平均数 KeyJournalSeriesAVGdict
# KeyJournalSeriesAVGdict = {}
# FirstJournalSeriesAVGdict = {}
# LastJournalSeriesAVGdict = {}
# AllJournalSeriesAVGdict = {}
# for k,v in KeyJournalSeriesCombineDict.items():
#     KeyJournalSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in FirstJournalSeriesCombineDict.items():
#     FirstJournalSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in LastJournalSeriesCombineDict.items():
#     LastJournalSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in AllJournalSeriesCombineDict.items():
#     AllJournalSeriesAVGdict[k] = sum(v)/len(v)
# pk.dump(KeyJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyJournalSeriesAVGdict.pk', 'wb'))
# pk.dump(FirstJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstJournalSeriesAVGdict.pk', 'wb'))
# pk.dump(LastJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastJournalSeriesAVGdict.pk', 'wb'))
# pk.dump(AllJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/AllJournalSeriesAVGdict.pk', 'wb'))

# 存期刊数平均数 （控制后）
KeyJournalSeriesAVGdict = {}
FirstJournalSeriesAVGdict = {}
LastJournalSeriesAVGdict = {}
AllJournalSeriesAVGdict = {}
for k,v in ControlKeyJournalSeriesCombineDict.items():
    KeyJournalSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlFirstJournalSeriesCombineDict.items():
    FirstJournalSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlLastJournalSeriesCombineDict.items():
    LastJournalSeriesAVGdict[k] = sum(v)/len(v)
for k,v in ControlAllJournalSeriesCombineDict.items():
    AllJournalSeriesAVGdict[k] = sum(v)/len(v)
pk.dump(KeyJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlKeyJournalSeriesAVGdict.pk', 'wb'))
pk.dump(FirstJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlFirstJournalSeriesAVGdict.pk', 'wb'))
pk.dump(LastJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlLastJournalSeriesAVGdict.pk', 'wb'))
pk.dump(AllJournalSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/ControlAllJournalSeriesAVGdict.pk', 'wb'))

# with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='w') as writer:
#     with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeq.jsonl', mode='r') as reader:
#         for lines in tqdm(reader):
#             for authorid, publist in lines.items():
#                 # 只保留职业生涯短于80年的
#                 if commonspanYearpublist(publist) < 81:
#                     writer.write({authorid: publist})
print('CountBoth',CountBoth)
print('CountFirst',CountFirst)
print('CountLast',CountLast)
print('CountAll',CountAll)