from tqdm import tqdm
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'

# # 一个decode的小技巧：有些东西不能用utf-8 decode
# with open(mag_dir+'Papers.txt','rb') as FileObj:
#     for lines in tqdm(FileObj):
#         try:
#             if lines.decode('utf-8').split('\t')[0] == '4200388619':
#                 print(lines.decode('utf-8').split('\t')[0])
#         except:
#             if lines.decode('latin-1').split('\t')[0] == '4200388619':
#                 print(lines.decode('latin-1').split('\t')[0])



# ['PaperId', 'Rank', 'Doi', 'DocType', 'Genre', 'IsParatext', 'PaperTitle', 'OriginalTitle', 'BookTitle', 'Year', 'Date', 'OnlineDate', 'Publisher', 'JournalId', 'ConferenceSeriesId', 'ConferenceInstanceId', 'Volume', 'Issue', 'FirstPage', 'LastPage', 'ReferenceCount', 'CitationCount', 'EstimatedCitation', 'OriginalVenue', 'FamilyId', 'FamilyRank', 'DocSubTypes', 'OaStatus', 'BestUrl', 'BestFreeUrl', 'BestFreeVersion', 'DoiLower', 'CreatedDate', 'UpdatedDate\n']
# ['2064559496', '20828', '10.1016/J.SOLMAT.2010.05.026', 'Journal', 'journal-article', 'f', 'single walled carbon nanotube network electrodes for dye solar cells', 'Single walled carbon nanotube network electrodes for dye solar cells', '', '2010', '2010-10-01', '2010-06-02', 'North-Holland', '166040772', '', '', '94', '10', '1665', '1672', '40', '33', '33', 'Solar Energy Materials and Solar Cells', '', '', '', 'closed', 'https://doi.org/10.1016/j.solmat.2010.05.026', '', '', '10.1016/j.solmat.2010.05.026', '2016-06-24', '2021-11-03 23:47:31.356428\n']

# paperID 0
# doi 2
# doctype 3
# Genre 4
# referenceCount
# citationCount
# year 9
# Date 10
# journalID 13
C = 0
with open(mag_dir+'Papers.txt', encoding="ISO-8859-1") as FileObj:
    for lines in tqdm(FileObj):
        C += 1
print(C)
