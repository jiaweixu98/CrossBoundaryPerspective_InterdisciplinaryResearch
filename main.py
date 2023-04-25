from collections import Counter
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'

# strip function
# def strip(x):
#     return x.strip()
# journal_cate key: mag journal id. values: a dictionary containing the metadata of the journals. e.g. jcrCate, jcrName, JCI, JiF 


count = 10
for k,v in journal_cate.items():
    print(v['jcrCate'].split('$'))
    count -= 1
    if count == 0:
        break
# SubjectCounter = Counter()

# for k,v in journal_cate.items():
#     stripedV = list(map(strip, v['jcrCate'].split(',')))
#     SubjectCounter.update(stripedV)
# print(SubjectCounter)