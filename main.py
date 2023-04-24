import pickle as pk
from collections import Counter

# strip function
def strip(x):
    return x.strip()

journal_cate = pk.load(open('data\journal_cate.pkl','rb'))
for k,v in journal_cate.items():
    print(k,v)
    break
# SubjectCounter = Counter()

# for k,v in journal_cate.items():
#     stripedV = list(map(strip, v['jcrCate'].split(',')))
#     SubjectCounter.update(stripedV)
# print(SubjectCounter)