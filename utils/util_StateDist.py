import json

with open("data/StateAndDistrict.json","r",encoding="utf-8") as file:
    data = json.load(file)

def geo_data():
        temp = dict()
        for i in data:
            temp[i['name']] = tuple(j['name'] for j in i['districts'])
        return temp
