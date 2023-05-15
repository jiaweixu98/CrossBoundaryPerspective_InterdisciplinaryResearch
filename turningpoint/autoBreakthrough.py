# nohup python -u autoBreakthrough.py -u > CASautoBreakthrough1999-2003INITIAL_SPAN1JCR.log 2>&1 &
# nohup python -u autoBreakthrough.py > CASautoBreakthrough1999-2003INITIAL_SPAN1CAS.log 2>&1 &

import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

#参数设置
START_YAER = 1999
END_YAER = 2003
CUT_YEAR_COUNT = 17
INITIAL_SPAN = 1
CATE_TYPE = 'CAS'

print('参数设置: START_YAER: %d, END_YAER: %d, CUT_YEAR_COUNT: %d, CATE_TYPE %s, INITIAL_SPAN%d'%(START_YAER, END_YAER, CUT_YEAR_COUNT,CATE_TYPE,INITIAL_SPAN))


paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
magid2bigcategory = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/magid2bigcategory.pk', 'rb'))
nonBreakthroughJournal = {'MULTIDISCIPLINARY SCIENCES','SOCIAL SCIENCES, INTERDISCIPLINARY'}
# ##############################################################################################################

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
    return truthSpan


##################################################################################################################
# 主要参与者JCR学科BreakThrough的时间点, 参数cutYear是纳入观察的年数
def Breakthrough(publist, cutYear=100, initialSpan=1, TypeStr='both'):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    # cutYear是控制的年数，必须比initialSpan大1或以上
    if cutYear <= initialSpan:
        raise('初始学科年份与生涯长度不匹配')
    initialSet = set()
    yearid = 0
    if TypeStr == 'both':
        for _, yearpublist in publist.items():
            
            # 是第一作者或末位作者
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0 or yearid <= initialSpan:
                    for rank1paper in yearpublist['rank1']:
                        for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                            if field not in nonBreakthroughJournal:
                                initialSet.add(field)
                    for rankLastpaper in yearpublist['rankLast']:
                        for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                            if field not in nonBreakthroughJournal:
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
    # 仅观察第一作者的breakthrough情况
    elif TypeStr == 'rank1':
        for _, yearpublist in publist.items():
            # 是第一作者
            if len(yearpublist['rank1']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0 or yearid <= initialSpan:
                    for rank1paper in yearpublist['rank1']:
                        for field in mag2journal[paper2journalid[rank1paper]]['FieldList']:
                            if field not in nonBreakthroughJournal:
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
    # 仅观察末位作者的breakthrough情况
    elif TypeStr == 'rankLast':
        for _, yearpublist in publist.items():
            # 是末位作者
            if len(yearpublist['rankLast']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0 or yearid <= initialSpan:
                    for rankLastpaper in yearpublist['rankLast']:
                        for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                            if field not in nonBreakthroughJournal:
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
    return 0


# 主要参与者CAS学科BreakThrough的时间点, 参数cutYear是纳入观察的年数
def BreakthroughForCAS(publist, cutYear=100, initialSpan=1, TypeStr='both'):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    # cutYear是控制的年数，必须比initialSpan大1或以上
    if cutYear <= initialSpan:
        raise('初始学科年份与生涯长度不匹配')
    initialSet = set()
    yearid = 0
    if TypeStr == 'both':
        for _, yearpublist in publist.items():
            
            # 是第一作者或末位作者
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0 or yearid <= initialSpan:
                    for rank1paper in yearpublist['rank1']:
                        field = magid2bigcategory[paper2journalid[rank1paper]]
                        if field != '综合性期刊':
                            initialSet.add(field)
                    for rankLastpaper in yearpublist['rankLast']:
                        field = magid2bigcategory[paper2journalid[rankLastpaper]]
                        if field != '综合性期刊':
                            initialSet.add(field)
                # 非处女作之年，看是否符合"转向标准"
                else:
                    for rank1paper in yearpublist['rank1']:
                        # 对这个 rank1paper 默认是转向文献，直到有一个熟悉的学科出现，才不是。
                        flag = 1
                        field = magid2bigcategory[paper2journalid[rank1paper]]
                        # 突破的条件：这本期刊所有的学科都是新的（nonBreakthroughJournal里的不算）；
                        # 如果领域是出现过的，或者是跨学科领域，那么认为不是突破性学科。
                        if (field in initialSet) or (field == '综合性期刊') :
                            flag = 0
                        # 如果全部过了一遍，没有老东西出现就承认是转向了，这一年就是转向年；否则继续去看下一年的文章是否是转向的
                        if flag == 1:
                            return yearid
                    for rankLastpaper in yearpublist['rankLast']:
                        flag = 1
                        field = magid2bigcategory[paper2journalid[rankLastpaper]]
                        if (field in initialSet) or (field == '综合性期刊') :
                            flag = 0
                        if flag == 1:
                            return yearid
    # 仅观察第一作者的breakthrough情况
    elif TypeStr == 'rank1':
        for _, yearpublist in publist.items():
            # 是第一作者
            if len(yearpublist['rank1']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0 or yearid <= initialSpan:
                    for rank1paper in yearpublist['rank1']:
                        field = magid2bigcategory[paper2journalid[rank1paper]]
                        if field != '综合性期刊':
                            initialSet.add(field)
                # 非处女作之年，看是否符合"转向标准"
                else:
                    for rank1paper in yearpublist['rank1']:
                        # 对这个 rank1paper 默认是转向文献，直到有一个熟悉的学科出现，才不是。
                        flag = 1
                        field = magid2bigcategory[paper2journalid[rank1paper]]
                            # 突破的条件：这本期刊所有的学科都是新的（nonBreakthroughJournal里的不算）；
                            # 如果领域是出现过的，或者是跨学科领域，那么认为不是突破性学科。
                        if (field in initialSet) or (field == '综合性期刊') :
                            flag = 0
                        # 如果全部过了一遍，没有老东西出现就承认是转向了，这一年就是转向年；否则继续去看下一年的文章是否是转向的
                        if flag == 1:
                            return yearid
    # 仅观察末位作者的breakthrough情况
    elif TypeStr == 'rankLast':
        for _, yearpublist in publist.items():
            # 是末位作者
            if len(yearpublist['rankLast']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0 or yearid <= initialSpan:
                    for rankLastpaper in yearpublist['rankLast']:
                        field = magid2bigcategory[paper2journalid[rankLastpaper]]
                        if field != '综合性期刊':
                            initialSet.add(field)
                # 非处女作之年，看是否符合"转向标准"
                else:
                    for rankLastpaper in yearpublist['rankLast']:
                        flag = 1
                        field = magid2bigcategory[paper2journalid[rankLastpaper]]
                        if (field in initialSet) or (field == '综合性期刊') :
                            flag = 0
                        if flag == 1:
                            return yearid
    # 如果所有的文章都看完了，还没有转向，说明这个人一辈子都没有突破自己第一年的情况；输出-1，即没有转向过。
    return 0


#从3开始的原因，3才可以看出转向变化对生涯的影响。设置了initialSpan = 2，所以开始年份必须至少为3
for cutyearCount in range(INITIAL_SPAN+1,CUT_YEAR_COUNT,1):
    KeyBreakthroughCounter = Counter()
    FirstBreakthroughCounter = Counter()
    LastBreakthroughCounter = Counter()
    # FinalActiveAuthorSeq里面的作者发文，是按顺序来的
    with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeqForCAS.jsonl', mode='r') as reader:
        # 每一行是一个字典
        for lines in tqdm(reader):
            # 看这个字典（其实此循环只有1个元素）
            for authorid, publist in lines.items():
                # 主要贡献者，START_YAER-END_YAER，cutyearCount及以上
                if ((START_YAER-1) < StartYearpublist(publist, 'both') < (END_YAER+1)) and ( (cutyearCount-1) < TrueSpanYearpublist(publist, 'both') ):
                    # 共3年，此处cutYear设置为3
                    KeyBreakthroughCounter[BreakthroughForCAS(publist,cutYear=cutyearCount,initialSpan=INITIAL_SPAN,TypeStr='both')] += 1
                # 第一作者，98-02，3及以上
                if ((START_YAER-1) < StartYearpublist(publist, 'rank1') < (END_YAER+1)) and ( (cutyearCount-1) < TrueSpanYearpublist(publist, 'rank1')):
                    FirstBreakthroughCounter[BreakthroughForCAS(publist,cutYear=cutyearCount,initialSpan=INITIAL_SPAN,TypeStr='rank1')] += 1
                # 末位作者，98-02，3及以上
                if ((START_YAER-1) < StartYearpublist(publist, 'rankLast') < (END_YAER+1)) and ( (cutyearCount-1) < TrueSpanYearpublist(publist, 'rankLast')):
                    LastBreakthroughCounter[BreakthroughForCAS(publist,cutYear=cutyearCount,initialSpan=INITIAL_SPAN,TypeStr='rankLast')] += 1

    pk.dump(KeyBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyBreakthroughCounter%d_%d_True%dCutInitialSpan%d%s.pk'%(START_YAER,END_YAER,cutyearCount,INITIAL_SPAN,CATE_TYPE), 'wb'))
    pk.dump(FirstBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstBreakthroughCounter%d_%d_True%dCutInitialSpan%d%s.pk'%(START_YAER,END_YAER,cutyearCount,INITIAL_SPAN,CATE_TYPE), 'wb'))
    pk.dump(LastBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastBreakthroughCounter%d_%d_True%dCutInitialSpan%d%s.pk'%(START_YAER,END_YAER,cutyearCount,INITIAL_SPAN,CATE_TYPE), 'wb'))