# nohup python -u disparity.py > getAllMatrix.log 2>&1 &

import numpy as np
# pickle 存储
import pickle as pk
# 进度条
from tqdm import tqdm

#文献发表年份对应，获得一篇文献的发表年份
paperYear = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperYear.pk', 'rb'))
# 文献期刊对应，一篇文献属于某本期刊。如果使用mag level 0 分类，此部分需要调整
paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
# 一本期刊对应的学科类别。如果使用mag level 0 分类，此部分需要调整
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

#建一个空的引文矩阵，每一年计算一次。三个维度分别为：citationMatrx3D[施引年份][施引文献学科][被引文献学科]
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
        # 构建引文矩阵
        try:
            citationMatrix3D[paperYear[lines[0]]][index_map[magid2bigcategory[paper2journalid[lines[0]]]]][index_map[magid2bigcategory[paper2journalid[lines[1]]]]] += 1
            citationCount += 1
        except:
            continue

print('全部引文矩阵建好了！看18亿条引用关系，开始保存。')
print('citationCount: ',citationCount)
pk.dump(citationMatrix3D, open('citationMatrix3D.pk', 'wb'))
print('保存完毕')
