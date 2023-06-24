# nohup python -u readMagPapers.py -u > readMagPapers.log 2>&1 &
from tqdm import tqdm
import pickle as pk
import jsonlines

mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
mag2journal = pk.load(open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/mag2journal.pk','rb'))
journal_set = set(list(mag2journal.keys()))

# ['PaperId', 'Rank', 'Doi', 'DocType', 'Genre', 'IsParatext', 'PaperTitle', 'OriginalTitle', 'BookTitle', 'Year', 'Date', 'OnlineDate', 'Publisher', 'JournalId', 'ConferenceSeriesId', 'ConferenceInstanceId', 'Volume', 'Issue', 'FirstPage', 'LastPage', 'ReferenceCount', 'CitationCount', 'EstimatedCitation', 'OriginalVenue', 'FamilyId', 'FamilyRank', 'DocSubTypes', 'OaStatus', 'BestUrl', 'BestFreeUrl', 'BestFreeVersion', 'DoiLower', 'CreatedDate', 'UpdatedDate\n']
# ['2064559496', '20828', '10.1016/J.SOLMAT.2010.05.026', 'Journal', 'journal-article', 'f', 'single walled carbon nanotube network electrodes for dye solar cells', 'Single walled carbon nanotube network electrodes for dye solar cells', '', '2010', '2010-10-01', '2010-06-02', 'North-Holland', '166040772', '', '', '94', '10', '1665', '1672', '40', '33', '33', 'Solar Energy Materials and Solar Cells', '', '', '', 'closed', 'https://doi.org/10.1016/j.solmat.2010.05.026', '', '', '10.1016/j.solmat.2010.05.026', '2016-06-24', '2021-11-03 23:47:31.356428\n']

# paperID 0
# doi 2
# year 9
# journalID 13
# referenceCount 20
# citationCount 21
# FamilyId 24 （约2%）
C = 0
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/papers.jsonl', mode='w') as writer:
    with open(mag_dir+'Papers.txt', encoding="ISO-8859-1") as FileObj:
        for lines in tqdm(FileObj):
            temp = lines.split('\t')
            try:
                if temp[13] in journal_set:
                    if '1800'< temp[9] <'2022':
                        writer.write({temp[0]:{'year':temp[9], 'doi':temp[2], 'journalID':temp[13],'FamilyId':temp[24]}})
                        C += 1
            except:
                continue
print('C: ',C)