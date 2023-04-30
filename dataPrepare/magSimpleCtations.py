import jsonlines
from tqdm import tqdm
from collections import Counter

mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
n = 5
with open(mag_dir+'PaperReferences.txt.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        n -= 1
        if n == 0:
            break
        lines = lines.strip().split('\t')
        print(lines)
