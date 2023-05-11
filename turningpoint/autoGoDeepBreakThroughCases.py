# nohup python -u autoGoDeepBreakThroughCases.py -u > autoGoDeepBreakThroughCases.log 2>&1 &
import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk

#参数设置
START_YAER = 1998
END_YAER = 2002
CUT_YEAR_COUNT = 3
print('参数设置: START_YAER: %d, END_YAER: %d, CUT_YEAR_COUNT: %d'%(START_YAER, END_YAER, CUT_YEAR_COUNT))

paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 'rb'))
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
def Breakthrough(publist, cutYear=100, TypeStr='both'):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
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
                if len(initialSet) == 0:
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
                if len(initialSet) == 0:
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
            if  len(yearpublist['rankLast']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0:
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

    

def BreakthroughMostFreqCombinations(publist, cutYear=100, TypeStr='both'):
    # yearPublist  {2023:{'rank1':set(), 'rankLast':set(), 'others':set() }, ...}
    initialSet = set()
    yearid = 0
    if TypeStr == 'both':
        for _, yearpublist in publist.items():
            if len(yearpublist['rank1']) > 0 or len(yearpublist['rankLast']) > 0:
            # 是第一作者或末位作者，才算一个时点
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0:
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
                            return yearid, initialSet, set(mag2journal[paper2journalid[rank1paper]]['FieldList'])
                    for rankLastpaper in yearpublist['rankLast']:
                        flag = 1
                        for field in mag2journal[paper2journalid[rankLastpaper]]['FieldList']:
                            if (field in initialSet) or (field in nonBreakthroughJournal) :
                                flag = 0
                        if flag == 1:
                            return yearid, initialSet, set(mag2journal[paper2journalid[rankLastpaper]]['FieldList'])
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
                if len(initialSet) == 0:
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
                            return yearid, initialSet, set(mag2journal[paper2journalid[rank1paper]]['FieldList'])
    # 仅观察末位作者的breakthrough情况
    elif TypeStr == 'rankLast':
        for _, yearpublist in publist.items():
            # 是末位作者
            if  len(yearpublist['rankLast']) > 0:
                yearid += 1
                # 如果已经到了cutYear了，直接结束循环（到此，强行结束该研究者的职业生涯）。
                if yearid > cutYear:
                    break
                # 处女作之年，要初始化
                if len(initialSet) == 0:
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
                            return yearid, initialSet, set(mag2journal[paper2journalid[rankLastpaper]]['FieldList'])
    # 如果所有的文章都看完了，还没有转向，说明这个人一辈子都没有突破自己第一年的情况；输出-1，即没有转向过。
    return 0,initialSet

if __name__ == '__main__':
    #从2开始的原因，2才可以看出变化
    for cutyearCount in range(2,CUT_YEAR_COUNT,1):
        # 转向的组合
        KeyBreakthroughCombineCounter = Counter()
        # 初始学科的计数，也可以用作归一化
        KeyInitialSetCounter = Counter()
        # 从未转向的人的组合
        KeyNoBreakthroughCounter = Counter()
        # 转向的组合
        FirstBreakthroughCombineCounter = Counter()
        # 初始学科的计数，也可以用作归一化
        FirstInitialSetCounter = Counter()
        # 从未转向的人的组合
        FirstNoBreakthroughCounter = Counter()
        # 转向的组合
        LastBreakthroughCombineCounter = Counter()
        # 初始学科的计数，也可以用作归一化
        LastInitialSetCounter = Counter()
        # 从未转向的人的组合
        LastNoBreakthroughCounter = Counter()

        # FinalActiveAuthorSeq里面的作者发文，是按顺序来的
        with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='r') as reader:
            # 每一行是一个字典
            for lines in reader:
                # 看这个字典（其实此循环只有1个元素）
                for authorid, publist in lines.items():
                    # 主要贡献者，START_YAER-END_YAER，cutyearCount及以上
                    if ((START_YAER-1) < StartYearpublist(publist, 'both') < (END_YAER+1)) and ( (cutyearCount-1) < TrueSpanYearpublist(publist, 'both') ):
                        temp = BreakthroughMostFreqCombinations(publist,cutYear=cutyearCount,TypeStr='both')
                        # if temp[0] == 0: # 一直没有转向
                        #     KeyInitialSetCounter[' $$ '.join(sorted(temp[1]))] += 1
                        #     KeyNoBreakthroughCounter[' $$ '.join(sorted(temp[1]))] += 1
                        # else: # 发生过转向
                        #     KeyInitialSetCounter[' $$ '.join(sorted(temp[1]))] += 1
                        #     KeyBreakthroughCombineCounter[' $$ '.join(sorted(temp[1]))+'------'+' $$ '.join(sorted(temp[2]))] += 1
                        if temp[0] == 0: # 一直没有转向
                            for fieldItem in temp[1]:
                                KeyInitialSetCounter[fieldItem] += 1
                                KeyNoBreakthroughCounter[fieldItem] += 1
                        else: # 发生过转向
                            for fieldItem in temp[1]:
                                KeyInitialSetCounter[fieldItem] += 1
                                for BreakthroughFieldItem in temp[2]:
                                    # 从a跳到b, a和b不能一样
                                    if fieldItem != BreakthroughFieldItem:
                                        KeyBreakthroughCombineCounter[fieldItem+' -->>>>-- '+BreakthroughFieldItem] += 1

                    # 第一作者，98-02，3及以上
                    if ((START_YAER-1) < StartYearpublist(publist, 'rank1') < (END_YAER+1)) and ( (cutyearCount-1) < TrueSpanYearpublist(publist, 'rank1')):
                        temp = BreakthroughMostFreqCombinations(publist,cutYear=cutyearCount,TypeStr='rank1')
                        # if temp[0] == 0: # 一直没有转向
                        #     FirstInitialSetCounter[' $$ '.join(sorted(temp[1]))] += 1
                        #     FirstNoBreakthroughCounter[' $$ '.join(sorted(temp[1]))] += 1
                        # else: # 发生过转向
                        #     FirstInitialSetCounter[' $$ '.join(sorted(temp[1]))] += 1
                        #     FirstBreakthroughCombineCounter[' $$ '.join(sorted(temp[1]))+'------'+' $$ '.join(sorted(temp[2]))]+= 1
                        if temp[0] == 0: # 一直没有转向
                            for fieldItem in temp[1]:
                                FirstInitialSetCounter[fieldItem] += 1
                                FirstNoBreakthroughCounter[fieldItem] += 1
                        else: # 发生过转向
                            for fieldItem in temp[1]:
                                FirstInitialSetCounter[fieldItem] += 1
                                for BreakthroughFieldItem in temp[2]:
                                    # 从a跳到b, a和b不能一样
                                    if fieldItem != BreakthroughFieldItem:
                                        KeyBreakthroughCombineCounter[fieldItem+' -->>>>-- '+BreakthroughFieldItem] += 1
                    # 末位作者，98-02，3及以上
                    if ((START_YAER-1) < StartYearpublist(publist, 'rankLast') < (END_YAER+1)) and ( (cutyearCount-1) < TrueSpanYearpublist(publist, 'rankLast')):
                        temp = BreakthroughMostFreqCombinations(publist,cutYear=cutyearCount,TypeStr='rankLast')
                        # if temp[0] == 0: # 一直没有转向
                        #     LastInitialSetCounter[' $$ '.join(sorted(temp[1]))] += 1
                        #     LastNoBreakthroughCounter[' $$ '.join(sorted(temp[1]))] += 1
                        # else: # 发生过转向
                        #     LastInitialSetCounter[' $$ '.join(sorted(temp[1]))] += 1
                        #     LastBreakthroughCombineCounter[' $$ '.join(sorted(temp[1]))+'------'+' $$ '.join(sorted(temp[2]))]+= 1
                        if temp[0] == 0: # 一直没有转向
                            for fieldItem in temp[1]:
                                LastInitialSetCounter[fieldItem] += 1
                                LastNoBreakthroughCounter[fieldItem] += 1
                        else: # 发生过转向
                            for fieldItem in temp[1]:
                                LastInitialSetCounter[fieldItem] += 1
                                for BreakthroughFieldItem in temp[2]:
                                    # 从a跳到b, a和b不能一样
                                    if fieldItem != BreakthroughFieldItem:
                                        LastBreakthroughCombineCounter[fieldItem+' -->>>>-- '+BreakthroughFieldItem] += 1



        print('cutyearCount:',cutyearCount)
        try:
            print('KeyBreakthroughCombineCounter:',len(KeyBreakthroughCombineCounter))
            for i in range(100):
                print(sorted(KeyBreakthroughCombineCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n')
        try:
            print('KeyInitialSetCounter:',len(KeyInitialSetCounter))
            for i in range(100):
                print(sorted(KeyInitialSetCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n')
        try:
            print('KeyNoBreakthroughCounter:',len(KeyNoBreakthroughCounter))
            for i in range(100):
                print(sorted(KeyNoBreakthroughCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n\n\n\n')
        try:
            print('FirstBreakthroughCombineCounter:',len(FirstBreakthroughCombineCounter))
            for i in range(100):
                print(sorted(FirstBreakthroughCombineCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n')
        try:
            print('FirstInitialSetCounter:',len(FirstInitialSetCounter))
            for i in range(100):
                print(sorted(FirstInitialSetCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n')
        try:
            print('FirstNoBreakthroughCounter:',len(FirstNoBreakthroughCounter))
            for i in range(100):
                print(sorted(FirstNoBreakthroughCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n\n\n\n')
        try:
            print('LastBreakthroughCombineCounter:',len(LastBreakthroughCombineCounter))
            for i in range(100):
                print(sorted(LastBreakthroughCombineCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n')
        try:
            print('LastInitialSetCounter:',len(LastInitialSetCounter))
            for i in range(100):
                print(sorted(LastInitialSetCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n')
        try:
            print('LastNoBreakthroughCounter:',len(LastNoBreakthroughCounter))
            for i in range(100):
                print(sorted(LastNoBreakthroughCounter.items(),key=lambda x:-x[1])[i])
        except:
            pass
            print('======\n\n\n\n')
        

        pk.dump(KeyInitialSetCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyInitialSetCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(KeyNoBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyNoBreakthroughCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(KeyBreakthroughCombineCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyBreakthroughCombineCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(FirstInitialSetCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstInitialSetCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(FirstNoBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstNoBreakthroughCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(FirstBreakthroughCombineCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FirstBreakthroughCombineCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(LastInitialSetCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastInitialSetCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(LastNoBreakthroughCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastNoBreakthroughCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))
        pk.dump(LastBreakthroughCombineCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/LastBreakthroughCombineCounter%d_%d_True%dCut.pk'%(START_YAER,END_YAER,cutyearCount), 'wb'))