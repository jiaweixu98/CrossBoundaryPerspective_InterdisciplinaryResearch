# nohup python -u breakthrough.py -u > breakthrough.log 2>&1 &
import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
nonBreakthroughJournal = {'MULTIDISCIPLINARY SCIENCES','SOCIAL SCIENCES, INTERDISCIPLINARY'}
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

##################################################################################################################
# 主要参与者JCR学科BreakThrough的时间点
def KeyBreakthrough(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    initialSet = set()
    yearid = 0
    for _, yearpublist in publist.items():
        yearid += 1
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            # 处女作之年，要初始化
            if len(initialSet) == 0:
                for rank1paper in yearpublist['rank1']:
                    for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                        initialSet.add(field)
                for rankLastpaper in yearpublist['rankLast']:
                    for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                        initialSet.add(field)
            # 非处女作之年，看是否符合"转向标准"
            else:
                for rank1paper in yearpublist['rank1']:
                    # 对这个 rank1paper 默认是转向文献，直到有一个熟悉的学科出现，才不是。
                    flag = 1
                    for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                        # 突破的条件：这本期刊所有的学科都是新的（nonBreakthroughJournal里的不算）；
                        # 如果领域是出现过的，或者是跨学科领域，那么认为不是突破性学科。
                        if (field in initialSet) or (field in nonBreakthroughJournal) :
                            flag = 0
                    # 如果全部过了一遍，没有老东西出现就承认是转向了，这一年就是转向年；否则继续去看下一年的文章是否是转向的
                    if flag == 1:
                        return yearid
                for rankLastpaper in yearpublist['rankLast']:
                    flag = 1
                    for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                        if (field in initialSet) or (field in nonBreakthroughJournal) :
                            flag = 0
                    if flag == 1:
                        return yearid
    # 如果所有的文章都看完了，还没有转向，说明这个人一辈子都没有突破自己第一年的情况；输出-1，即没有转向过。
    return -1


# 第一作者JCR学科BreakThrough的时间点
def FirstBreakthrough(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    initialSet = set()
    yearid = 0
    for _, yearpublist in publist.items():
        yearid += 1
        # 是第一作者或末位作者
        if len(yearpublist['rank1']) > 0:
            # 处女作之年，要初始化
            if len(initialSet) == 0:
                for rank1paper in yearpublist['rank1']:
                    for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                        initialSet.add(field)
            # 非处女作之年，看是否符合"转向标准"
            else:
                for rank1paper in yearpublist['rank1']:
                    # 对这个 rank1paper 默认是转向文献，直到有一个熟悉的学科出现，才不是。
                    flag = 1
                    for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                        # 突破的条件：这本期刊所有的学科都是新的（nonBreakthroughJournal里的不算）；
                        # 如果领域是出现过的，或者是跨学科领域，那么认为不是突破性学科。
                        if (field in initialSet) or (field in nonBreakthroughJournal) :
                            flag = 0
                    # 如果全部过了一遍，没有老东西出现就承认是转向了，这一年就是转向年；否则继续去看下一年的文章是否是转向的
                    if flag == 1:
                        return yearid
    # 如果所有的文章都看完了，还没有转向，说明这个人一辈子都没有突破自己第一年的情况；输出-1，即没有转向过。
    return -1


# 末位作者JCR学科BreakThrough的时间点
def LastBreakthrough(publist):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    initialSet = set()
    yearid = 0
    for _, yearpublist in publist.items():
        yearid += 1
        # 是末位作者
        if len(yearpublist['rankLast']) > 0:
            # 处女作之年，要初始化
            if len(initialSet) == 0:
                for rankLastpaper in yearpublist['rankLast']:
                    for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                        initialSet.add(field)
            # 非处女作之年，看是否符合"转向标准"
            else:
                for rankLastpaper in yearpublist['rankLast']:
                    flag = 1
                    for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                        if (field in initialSet) or (field in nonBreakthroughJournal) :
                            flag = 0
                    if flag == 1:
                        return yearid
    # 如果所有的文章都看完了，还没有转向，说明这个人一辈子都没有突破自己第一年的情况；输出-1，即没有转向过。
    return -1

KeyFieldSeriesCombineDict = {}
FirstFieldSeriesCombineDict = {}
LastFieldSeriesCombineDict = {}

KeyBreakthroughCounter = Counter()
FirstBreakthroughCounter = Counter()
LastBreakthroughCounter = Counter()
# FinalActiveAuthorSeq里面的作者发文，是按顺序来的
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='r') as reader:
    # 每一行是一个字典
    for lines in tqdm(reader):
        # 看这个字典（其实此循环只有1个元素）
        for authorid, publist in lines.items():
            # 控制主要年份，和生涯寿命
            if (1997 < keyStartYearpublist(publist) < 2003) and ( 8 < keySpanYearpublist(publist)< 10  ):
                # 统计不同年份转向的人
                KeyBreakthroughCounter[KeyBreakthrough(publist)] += 1
                FirstBreakthroughCounter[FirstBreakthrough(publist)] += 1
                LastBreakthroughCounter[LastBreakthrough(publist)] += 1
            # if (1997 < keyStartYearpublist(publist) < 2003) and ( 8 < keySpanYearpublist(publist)< 10  ):
            #     for yearid, keyPubNum in cumKeyJFieldNum(publist).items():
            #         if yearid not in KeyFieldSeriesCombineDict:
            #             KeyFieldSeriesCombineDict[yearid] = [keyPubNum]
            #         else:
            #             KeyFieldSeriesCombineDict[yearid].append(keyPubNum)
            #     for yearid, keyPubNum in cumFirstJFieldNum(publist).items():
            #         if yearid not in FirstFieldSeriesCombineDict:
            #             FirstFieldSeriesCombineDict[yearid] = [keyPubNum]
            #         else:
            #             FirstFieldSeriesCombineDict[yearid].append(keyPubNum)
            #     for yearid, keyPubNum in cumLastJFieldNum(publist).items():
            #         if yearid not in LastFieldSeriesCombineDict:
            #             LastFieldSeriesCombineDict[yearid] = [keyPubNum]
            #         else:
            #             LastFieldSeriesCombineDict[yearid].append(keyPubNum)


pk.dump(KeyBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyBreakthroughCounter98_02_9.pk', 'wb'))
pk.dump(FirstBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstBreakthroughCounter98_02_9.pk', 'wb'))
pk.dump(LastBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastBreakthroughCounter98_02_9.pk', 'wb'))

# KeyJFieldSeriesAVGdict = {}
# FirstJFieldSeriesAVGdict = {}
# LastJFieldSeriesAVGdict = {}

# for k,v in KeyFieldSeriesCombineDict.items():
#     KeyJFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in FirstFieldSeriesCombineDict.items():
#     FirstJFieldSeriesAVGdict[k] = sum(v)/len(v)
# for k,v in LastFieldSeriesCombineDict.items():
#     LastJFieldSeriesAVGdict[k] = sum(v)/len(v)


# pk.dump(KeyJFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyJField98_02_8_10SeriesAVGdict.pk', 'wb'))
# pk.dump(FirstJFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstJField98_02_8_10SeriesAVGdict.pk', 'wb'))
# pk.dump(LastJFieldSeriesAVGdict, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastJField98_02_8_10SeriesAVGdict.pk', 'wb'))


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