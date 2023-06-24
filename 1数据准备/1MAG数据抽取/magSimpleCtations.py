# 计算MAG中文章的参考文献数量和被引量（不做任何处理）
# nohup python -u magSimpleCtations.py > magSimpleCtations.log 2>&1 &
import jsonlines
from tqdm import tqdm
from collections import Counter
import pickle as pk
referenceCounter = Counter()
citationCounter = Counter()
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
with open(mag_dir+'PaperReferences.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        lines = lines.strip().split('\t')
        if len(lines) != 2:
            continue
        #数据结构为：施引文献：被引文献。 前者引用后者
        referenceCounter[lines[0]] += 1
        citationCounter[lines[1]] += 1
        
print('len(citationCounter)',len(citationCounter))
print('len(referenceCounter)',len(referenceCounter))

pk.dump(referenceCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/referenceCounter.pk','wb'))
pk.dump(citationCounter, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/citationCounter.pk','wb'))