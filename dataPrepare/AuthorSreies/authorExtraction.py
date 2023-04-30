# nohup python -u authorExtraction.py > authorExtraction.log 2>&1 &
from tqdm import tqdm
import pickle as pk
import jsonlines
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
# paper保证是JCR期刊上的
paperSet = pk.load(open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperJournalset.pk', 'rb'))

# mag2journal = pk.load(open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk','rb'))
# journal_set = set(list(mag2journal.keys()))

# PaperId	AuthorId	AffiliationId	AuthorSequenceNumber	OriginalAuthor	OriginalAffiliation
# 4200388619	4202301102	196733613	4	Dongkyu Kim	Korea Gas Corporation (KOGAS) Research Institute, 960, Incheonsinhang-daero, Yeonsu-gu,

# paperID 0
# AuthorId 1
# AffiliationId 2
# AuthorSequenceNumber 3
# paperAuthorNum = {}
# with open(mag_dir+'PaperAuthorAffiliations.txt', encoding="ISO-8859-1") as FileObj:
#     for lines in tqdm(FileObj):
#         temp = lines.split('\t')
#         try:
#             if temp[0] in paperSet:
#                 paperAuthorNum[temp[0]] = max(paperAuthorNum.get(temp[0], 0), int(temp[3]))
#         except:
#             continue
# pk.dump(paperAuthorNum, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperAuthorNum.pk', 'wb'))
authorSeq = {}
paperAuthorNum = pk.load(open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperAuthorNum.pk', 'rb'))
paperYear = pk.load(open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/paperYear.pk', 'rb'))

with open(mag_dir+'PaperAuthorAffiliations.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        temp = lines.split('\t')
        try:
            if temp[0] in paperSet:
                # author第一次出现的话，需要初始化
                if temp[1] not in authorSeq:
                    authorSeq[temp[1]] = {}
                # 某author的某年的第一篇文献出现的话，需要初始化
                if paperYear[temp[0]] not in authorSeq[temp[1]]:
                    authorSeq[temp[1]][paperYear[temp[0]]] = {'rank1':set(), 'rankLast':set(), 'others':set() }
                # 如果是第一作者
                if int(temp[3]) == 1:
                    # 这里增加一个文献
                    authorSeq[temp[1]][paperYear[temp[0]]]['rank1'].add(temp[0])
                elif int(temp[3]) == paperAuthorNum[temp[0]]:
                    authorSeq[temp[1]][paperYear[temp[0]]]['rankLast'].add(temp[0])
                    # 其他作者
                else:
                    authorSeq[temp[1]][paperYear[temp[0]]]['others'].add(temp[0])
        except:
            continue
print('authorSeq',len(authorSeq))
# print(authorSeq)
pk.dump(authorSeq, open('../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/authorSeq.pk', 'wb'))