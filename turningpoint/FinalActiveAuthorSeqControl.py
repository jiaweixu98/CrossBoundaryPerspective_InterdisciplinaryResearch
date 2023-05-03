import jsonlines
from tqdm import tqdm
with jsonlines.open('../../DataCrossBoundaryPerspective_InterdisciplinaryResearch/FinalActiveAuthorSeq.jsonl', mode='r') as reader:
    for lines in tqdm(reader):
        # 看这个字典（其实此循环只有1个元素）
        for authorid, publist in lines.items():
            for year, pub in publist.items():
                print(year)
                print(type(year))
                break
            break
        break
