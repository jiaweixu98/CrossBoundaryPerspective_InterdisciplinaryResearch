# nohup python -u diversityForEachPaper.py > diversityForEachPaper.log 2>&1 &
# 获得属于CAS大类的学科的引用情况
import numpy as np
import pickle as pk
from tqdm import tqdm

# 学科对应
index_map = {'医学': 0,
 '工程技术': 1,
 '生物学': 2,
 '化学': 3,
 '物理与天体物理': 4,
 '农林科学': 5,
 '材料科学': 6,
 '计算机科学': 7,
 '环境科学与生态学': 8,
 '地球科学': 9,
 '心理学': 10,
 '数学': 11,
 '法学': 12,
 '经济学': 13,
 '管理学': 14,
 '人文科学': 15,
 '教育学': 16,
 '综合性期刊':17}




# 输出，paper对应的跨学科性
paper2idDegree = {}
# 从这里得到各年度的学科间差异度
DijtMatrix = pk.load(open('DijtMatrix.pk', 'rb'))
# 大学科
magid2bigcategory = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/magid2bigcategory.pk', 'rb'))
# 这里是我们考虑的文献名录，约3000万篇。我们只考虑这3000多万篇文献中的引用关系。
paperSet = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperJournalsetCas.pk', 'rb'))

# 文献期刊对应
paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))

#文献发表年份对应
paperYear = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperYear.pk', 'rb'))




# 从这里得到参考文献列表
citing2cited = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/citing2cited.pk', 'rb'))

# 计算重要文献的跨学科程度
def refInterdisciplinarity(paper):
    try:
        paperReflist = citing2cited[paper]
    except:
        # 没有参考文献，跨学科性设为0（一般不可能）
        return 0
    # 存参考文献学科分布
    reflist = np.zeros(18)
    for ref in paperReflist:
        try:
            reflist[index_map[magid2bigcategory[paper2journalid[ref]]]] += 1
        except:
            continue
    # pi 和 pj 都有了
    try:
        Pijlist = reflist/reflist.sum()
        # 这里非常坑，不会报错
    except:
        # 如果报错，一定是分母为0，跨学科性设为0即可
        return 0
    # 跨学科性初始化为0
    idDegree = 0
    # 年份，影响差异性的取值; 很奇怪有些paper没有年份(来自1800或者2022，不用管了)
    try:
        year = paperYear[paper]
    except:
        print('no year! key error: ',paper)
        return 0
    for i in range(18):
        if Pijlist[i] == 0:
            continue
        else:
            for j in range(18):
                idDegree += Pijlist[i]*Pijlist[j]*DijtMatrix[year][i][j]
    return idDegree

# 开始计算跨学科性
for paper in tqdm(paperSet):
    paper2idDegree[paper] = refInterdisciplinarity(paper)

print('（极端年份如1800年可能缺少）所有文献的跨学科性计算完毕，开始保存。')
print('len(paper2idDegree)',len(paper2idDegree))
pk.dump(paper2idDegree, open('paper2idDegree.pk', 'wb'))
print('保存完毕')