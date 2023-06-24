# nohup python -u disparity.py > getAllMatrix.log 2>&1 &
# 获得属于CAS大类的学科的引用情况
import numpy as np
import pickle as pk
from tqdm import tqdm
# 这里是我们考虑的文献名录，约3000万篇。我们只考虑这3000多万篇文献中的引用关系。
# paperSet = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperJournalsetCas.pk', 'rb'))
#文献发表年份对应
paperYear = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperYear.pk', 'rb'))
# 文献作者数量对应 
# paperAuthorNum = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperAuthorNum.pk', 'rb'))
# 文献期刊对应
paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
# 期刊学科对应
# mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 
# 'rb'))
# 大学科
magid2bigcategory = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/magid2bigcategory.pk', 'rb'))

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

# 年份、施引学科、被引学科。最重要的矩阵！有了这个就可以算disparity了
citationMatrix3D = np.zeros((2022, 18, 18))
citationCount = 0
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
with open(mag_dir+'PaperReferences.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        lines = lines.strip().split('\t')
        if len(lines) != 2:
            continue
        #数据结构为：施引文献：被引文献。 前者引用后者
        # citationMatrx3D[施引年份][施引文献学科][被引文献学科]
        try:
            citationMatrix3D[paperYear[lines[0]]][index_map[magid2bigcategory[paper2journalid[lines[0]]]]][index_map[magid2bigcategory[paper2journalid[lines[1]]]]] += 1
            citationCount += 1
        except:
            continue

print('全部引文矩阵建好了！看18亿条引用关系，开始保存。')
print('citationCount: ',citationCount)
pk.dump(citationMatrix3D, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/citationMatrix3D.pk', 'wb'))
print('保存完毕')
