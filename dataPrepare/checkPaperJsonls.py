import jsonlines
from tqdm import tqdm
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
n = 10
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        if n == 0:
            break
        n -= 1
    print(lines)