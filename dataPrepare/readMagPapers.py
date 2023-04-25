mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'

# 一个decode的小技巧：有些东西不能用utf-8 decode
with open(mag_dir+'Papers.txt','rb') as FileObj:
    for lines in FileObj:
        try:
            if lines.decode('utf-8').split('\t')[0] == '4200388619':
                print(lines.decode('utf-8').split('\t')[0])
        except:
            if lines.decode('latin-1').split('\t')[0] == '4200388619':
                print(lines.decode('latin-1').split('\t')[0])