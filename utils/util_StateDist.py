import json

def geo_data(language):
    with open(f"data/StateAndDistrict{language}.json","r",encoding="utf-8") as file:
        data = json.load(file)
        temp = dict()
        for i in data:
            temp[i['name']] = tuple(j['name'] for j in i['districts'])
        return temp
