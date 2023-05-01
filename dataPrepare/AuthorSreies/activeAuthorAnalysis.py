import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk


# 开始年份
def commonstartYearpublist(publist):
    return int(list(publist.keys())[0])
# 休止年份
def commonendYearpublist(publist):
    return int(list(publist.keys())[-1])
# 年份跨度
def commonspanYearpublist(publist):
    return commonendYearpublist(publist) - commonstartYearpublist(publist)


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


CommonStartYearCounter = Counter()
CommonEndYearCounter = Counter()
CommonSpanYearCounter = Counter()
KeyStartYearCounter = Counter()
KeyEndYearCounter = Counter()
KeySpanYearCounter = Counter()

with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        for authorid, publist in lines.items():
            CommonStartYearCounter[commonstartYearpublist(publist)] += 1
            CommonEndYearCounter[commonendYearpublist(publist)] += 1
            CommonSpanYearCounter[commonspanYearpublist(publist)] += 1
            KeyStartYearCounter[keyStartYearpublist(publist)] += 1
            KeyEndYearCounter[keyEndYearpublist(publist)] += 1
            KeySpanYearCounter[keySpanYearpublist(publist)] += 1


pk.dump(CommonStartYearCounter, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CommonStartYearCounter.pk', 'wb'))
pk.dump(CommonEndYearCounter, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CommonEndYearCounter.pk', 'wb'))
pk.dump(CommonSpanYearCounter, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/CommonSpanYearCounter.pk', 'wb'))
pk.dump(KeyStartYearCounter, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyStartYearCounter.pk', 'wb'))
pk.dump(KeyEndYearCounter, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeyEndYearCounter.pk', 'wb'))
pk.dump(KeySpanYearCounter, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/KeySpanYearCounter.pk', 'wb'))

# with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='w') as writer:
#     with jsonlines.open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/activeAuthorSeq.jsonl', mode='r') as reader:
#         for lines in tqdm(reader):
#             for authorid, publist in lines.items():
#                 # 只保留职业生涯短于80年的
#                 if commonspanYearpublist(publist) < 81:
#                     writer.write({authorid: publist})