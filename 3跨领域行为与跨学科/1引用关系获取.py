# nohup python -u getCiting2cited.py > getCiting2citedCited2Citing.log 2>&1 &
# 获得属于CAS大类的学科的引用情况
# import numpy as np
import pickle as pk
from tqdm import tqdm
# 这里是我们考虑的文献名录，约3000万篇。我们只考虑这3000多万篇文献中的引用关系。
paperSet = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperJournalsetCas.pk', 'rb'))
#文献发表年份对应
# paperYear = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperYear.pk', 'rb'))
# 文献作者数量对应 
# paperAuthorNum = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperAuthorNum.pk', 'rb'))
# 文献期刊对应
# paper2journalid = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paper2journalid.pk', 'rb'))
# 期刊学科对应
# mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk', 
# 'rb'))
# 大学科
# magid2bigcategory = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/magid2bigcategory.pk', 'rb'))
citing2cited = {}
cited2citing = {}

mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
with open(mag_dir+'PaperReferences.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        lines = lines.strip().split('\t')
        if len(lines) != 2:
            continue
        #数据结构为：施引文献：被引文献。 前者引用后者
        # 施引文献是我们关注的重要文献
        if lines[0] in paperSet:
            # 施引文献的参考文献列表出现过
            if lines[0] in citing2cited:
                citing2cited[lines[0]].append(lines[1])
            else:
                citing2cited[lines[0]] = [lines[1]]
        # 引用文献是我们关注的重要文献
        if lines[1] in paperSet:
            # 这篇被引文献已经出现过了
            if lines[1] in cited2citing:
                cited2citing[lines[1]].append(lines[0])
            else:
                cited2citing[lines[1]] = [lines[0]]

print('citing2cited和cited2citing构建完毕')
print('len(citing2cited): ',len(citing2cited))
print('len(cited2citing): ',len(cited2citing))
print('citing2cited保存中···')

pk.dump(citing2cited, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/citing2cited.pk', 'wb'))
print('citing2cited保存完毕')
print('cited2citing保存中···')
pk.dump(cited2citing, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/cited2citing.pk', 'wb'))
print('cited2citing保存完毕')