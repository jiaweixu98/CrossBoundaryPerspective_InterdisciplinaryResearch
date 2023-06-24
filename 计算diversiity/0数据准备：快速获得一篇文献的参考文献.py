# nohup python -u getCiting2cited.py > getCiting2citedCited2Citing.log 2>&1 &
# 快速获得一篇文献的参考文献
import pickle as pk
from tqdm import tqdm
# citing文献与cited文献的对应，存到内存中
citing2cited = {}

# 这里需要自己设定：需要计算哪些文章的跨学科性？
paperSet = set()


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

print('citing2cited构建完毕')
print('len(citing2cited): ',len(citing2cited))
print('citing2cited保存中···')

pk.dump(citing2cited, open('citing2cited.pk', 'wb'))
print('citing2cited保存完毕')