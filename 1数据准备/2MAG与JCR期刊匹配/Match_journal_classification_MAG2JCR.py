# nohup python -u Match_journal_classification_MAG2JCR.py -u > Match_journal_classification_MAG2JCR.log 2>&1 &
from tqdm import tqdm
import pandas as pd
import pickle as pk
mag_dir = '/home/dell/kd_paper_data/data/MAG-20220502/data_dump_v1/2022-05-02/mag/'
data_dir = '../../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/'
if __name__ == '__main__':


    # 从MAG中抽期刊
    not_matched_by_issn = {}
    dist_JournalIdIssns_NmName = {}
    with open(mag_dir+'Journals.txt') as FileObj:
        for lines in FileObj:
            temp = lines.split('\t')
            if 'JournalId' == temp[0]:
                continue
            if '42102314 of physical therapy and health promotion' == temp[0]:
                # 不确定是否有文章属于：42102314
                continue
            # if  len(temp[4]) > 9:
            #     print([lines])
            #     continue
            # if eval(temp[5])[0] == '' and temp[4] == '':
            #     print([lines])
            #     continue
            try:
                dist_JournalIdIssns_NmName[temp[0]] = {'name':temp[2], 'Issn': temp[4],'Issns':eval(temp[5]),'Publisher':temp[8]}
            except:
                try:
                    dist_JournalIdIssns_NmName[temp[0]] = {'name':temp[2],'Issn': temp[4],'Issns':[''],'Publisher':temp[8]}
                except:
                    continue
    dist_JournalIdIssns_NmName['42102314'] = {'name':'journal of physical therapy and health promotion', 'Issn': '2376-1601','Issns':["2376-1636","2376-1601"],'Publisher':'Bowen Publishing Company'}
    dist_JournalIdIssns_NmName['206542314'] = {'name':'configurations', 'Issn': '1063-1801','Issns':["1080-6520","1063-1801"],'Publisher':'Johns Hopkins University Press'}
    dist_JournalIdIssns_NmName['4210211510'] = {'name':'bioscientia medicina', 'Issn': '2598-0580','Issns':["2598-0580","2598-0580"],'Publisher':''}

    # 看一下长啥样：发现有一些东西没有issn和issns
    # check issn
    # n = 10
    # for k,v in dist_JournalIdIssns_NmName.items():
    #     if len(v['Issn']) > 9:
    #         print(k,v)
    #         n-=1
    #     if n ==0:
    #         break

    # 将issn字段全部合并，后面用issn匹配mag和jcr
    for i,j in dist_JournalIdIssns_NmName.items():
        try:
            dist_JournalIdIssns_NmName[i]['allIssn'] = [j['Issn']] + j['Issns']
        except:
            # print(i,j)
            # 有一些解析错误的
            dist_JournalIdIssns_NmName[i]['allIssn'] = []

    # debug: 一些Issn不在Issns中的情况，多半是解析错误
    # for i,j in dist_JournalIdIssns_NmName.items():
    #     try:
    #         if j['Issn'] not in j['Issns'] and j['Issn'] != '':
    #             print([i],j)
    #     except:
    #         print([i],j)
    # pd.DataFrame(dist_JournalIdIssns_NmName).T.to_csv('dist_JournalIdIssns_NmName.csv')

    # 读jcr数据，希望为每个jcr数据都匹配到一个mag对应的期刊
    dist_ScieJcrMatchSub = {}
    with open(data_dir+'jcr/scie.txt') as FileObj:
        for lines in FileObj:
            temp = lines.strip().split('\t')
            if 'Journal-name' == temp[0]:
                continue
            dist_ScieJcrMatchSub[temp[0]] = {'Issn':temp[1], 'eIssn': temp[2],'category':temp[3],'2021-JIF':temp[4],'2021-Q':temp[5],'2021-JCI':temp[6]}

    dist_AhciJcrMatchSub = {}
    with open(data_dir+'jcr/ahci.txt') as FileObj:
        for lines in FileObj:
            temp = lines.strip().split('\t')
            if 'Journal-name' == temp[0]:
                continue
            dist_AhciJcrMatchSub[temp[0]] = {'Issn':temp[1], 'eIssn': temp[2],'category':temp[3],'2021-JIF':temp[4],'2021-Q':temp[5],'2021-JCI':temp[6]}

    dist_SsciJcrMatchSub = {}
    with open(data_dir+'jcr/ssci.txt') as FileObj:
        for lines in FileObj:
            temp = lines.strip().split('\t')
            if 'Journal-name' == temp[0]:
                continue
            dist_SsciJcrMatchSub[temp[0]] = {'Issn':temp[1], 'eIssn': temp[2],'category':temp[3],'2021-JIF':temp[4],'2021-Q':temp[5],'2021-JCI':temp[6]}

#依次匹配
# scie
    import difflib
    def similar(seq1, seq2):
        return difflib.SequenceMatcher(a=seq1.lower(), b=seq2.lower()).ratio()
    journal_cate = {}
    for i,j in dist_ScieJcrMatchSub.items():
        flag = 0
        if j['Issn'] != 'N/A' or j['eIssn'] != 'N/A':
            for magi, magj in dist_JournalIdIssns_NmName.items():
                if j['Issn'] in magj['allIssn'] or j['eIssn'] in magj['allIssn']:
                    if magi not in journal_cate:
                        journal_cate[magi]= {'jcrCate':j['category'], 'jcrName':i, 'magName':magj['name'],'magIssn':magj['allIssn'],'jcrIssn':j['Issn'],
                                            'jcrEIssn':j['eIssn'],'2021-JIF':j['2021-JIF'],'2021-Qscie':j['2021-Q'],'2021-Qssci':'N/A','2021-Qahci':'N/A','2021-JCI':j['2021-JCI']}
                        flag = 1
                        break
                    else:
                        journal_cate[magi]['jcrCate'] += '$'+j['category']
                        journal_cate[magi]['2021-Qscie'] = j['2021-Q']
                        flag = 1
                        break

        if flag == 0:
            print('not found=====',i,j)
            not_matched_by_issn[i]=j


    print('hereafter: dist_AhciJcrMatchSub')

# ahci
    for i,j in dist_AhciJcrMatchSub.items():
        flag = 0
        if j['Issn'] != 'N/A' or j['eIssn'] != 'N/A':
            for magi, magj in dist_JournalIdIssns_NmName.items():
                if j['Issn'] in magj['allIssn'] or j['eIssn'] in magj['allIssn']:
                    # 如果已经出现过了
                    if magi in journal_cate:
                        journal_cate[magi]['jcrCate'] += '$'+j['category']
                        journal_cate[magi]['2021-Qahci'] = j['2021-Q']
                        # achi 其实不会有Q的说法
                        flag = 1
                        break
                    else:
                        journal_cate[magi]= {'jcrCate':j['category'], 'jcrName':i, 'magName':magj['name'],'magIssn':magj['allIssn'],'jcrIssn':j['Issn'],
                                            'jcrEIssn':j['eIssn'],'2021-JIF':j['2021-JIF'],'2021-Qahci':j['2021-Q'],'2021-Qssci':'N/A','2021-Qscie':'N/A','2021-JCI':j['2021-JCI']}
                        flag = 1
                        break
        if flag == 0:
            print('not found=====',i,j)
            not_matched_by_issn[i]=j

    print('hereafter: dist_SsciJcrMatchSub')

# ssci
    for i,j in dist_SsciJcrMatchSub.items():
        flag = 0
        if j['Issn'] != 'N/A' or j['eIssn'] != 'N/A':
            for magi, magj in dist_JournalIdIssns_NmName.items():
                if j['Issn'] in magj['allIssn'] or j['eIssn'] in magj['allIssn']:
                    if magi not in journal_cate:
                        journal_cate[magi]= {'jcrCate':j['category'], 'jcrName':i, 'magName':magj['name'],'magIssn':magj['allIssn'],'jcrIssn':j['Issn'],
                                            'jcrEIssn':j['eIssn'],'2021-JIF':j['2021-JIF'],'2021-Qssci':j['2021-Q'], '2021-Qahci': 'N/A',  '2021-Qscie': 'N/A','2021-JCI':j['2021-JCI']}
                        flag = 1
                        break
                    else:
                        journal_cate[magi]['jcrCate'] += '$'+j['category']
                        journal_cate[magi]['2021-Qssci'] = j['2021-Q']
                        flag = 1
                        break
        if flag == 0:
            print('not found=====',i,j)
            not_matched_by_issn[i]=j
    print(len(journal_cate))

    for i,j in not_matched_by_issn.items():
        flag = 0
        for magi, magj in dist_JournalIdIssns_NmName.items():
            if i.lower() == magj['name'].lower() or similar(i,magj['name']) > 0.9:
                journal_cate[magi]= {'jcrCate':j['category'], 'jcrName':i, 'magName':magj['name'],'magIssn':magj['allIssn'],'jcrIssn':j['Issn'],'jcrEIssn':j['eIssn'],'2021-JIF':j['2021-JIF'],'2021-Q':j['2021-Q'],'2021-JCI':j['2021-JCI']}
                flag = 1
                break
        if flag == 0:
            print('not found=====',i,j)
    print(len(journal_cate))

    pk.dump(journal_cate,open(data_dir+'journal_cate.pkl','wb'))
    pk.dump(not_matched_by_issn,open(data_dir+'not_matched_by_issn.pkl','wb'))