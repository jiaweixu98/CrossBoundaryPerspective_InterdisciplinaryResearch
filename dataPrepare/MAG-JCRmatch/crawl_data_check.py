# 手动调整了一些明显的错误(个位数的错误记录，没啥影响)
from tqdm import tqdm
from collections import Counter
dist_ScieJcrMatchSub = {}
name_list = []
with open('jcr/ahci.txt') as FileObj:
    for lines in tqdm(FileObj):
        temp = lines.strip().split('\t')
        if 'Journal-name' == temp[0]:
            continue
        name_list.append(temp[0])
        # dist_ScieJcrMatchSub[temp[0]] = {'Issn':temp[1], 'eIssn': temp[2],'category':temp[3],'2021-JIF':temp[4],'2021-Q':temp[5],'2021-JCI':temp[6]}
c = Counter(name_list)
for k,v in c.items():
    if v >1:
        print(k,v)
