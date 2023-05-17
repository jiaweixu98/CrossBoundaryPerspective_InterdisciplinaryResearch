# paperYear: paperYear的keyValue对
from tqdm import tqdm
import pickle as pk
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'

paperYear = {}

with open(mag_dir+'Papers.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        temp = lines.split('\t')
        try:
            if len(temp[9])!=4 or int(temp[9])< 1801 or int(temp[9])>2021:
                continue
            paperYear[temp[0]] = int(temp[9])
        except:
            continue

print(len(paperYear))
pk.dump(paperYear, open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperYear.pk', 'wb'))
