import pandas as pd
import json

data0=pd.read_csv("iso_codes_spain.csv")
print(data0)
kkeys={}
for item in data0.iterrows():
    print(item[1])
    if item[1]["Subdivision name "].split(" [")[0][len(item[1]["Subdivision name "].split(" [")[0])-1:]==" ":
        kkeys[item[1]["Subdivision name "].split(" [")[0][:-1]]=item[1]["3166-2 code "]
    else:
        kkeys[item[1]["Subdivision name "].split(" [")[0]]=item[1]["3166-2 code "]
print(kkeys.keys())
data10=pd.read_csv("https://raw.githubusercontent.com/montera34/escovid19data/master/data/output/covid19-provincias-spain_consolidated.csv")
print(data10["province"].unique())
#print(data10.columns)

kkeys2={}
for item in list(kkeys.keys()):
    for item1 in data10["province"].unique():
        test=item1.split("/")
        if len(test)==2:
            if item==test[0] or item==test[1]:
                print(item,item1,kkeys[item].replace("ES-","").replace(" ",""))
                kkeys2[item1]=kkeys[item].replace("ES-","").replace(" ","")
        else:
            if item==item1:
                print(item,item1,kkeys[item].replace("ES-","").replace(" ",""))
                kkeys2[item1]=kkeys[item].replace("ES-","").replace(" ","")

print(kkeys2)                
print(data10["province"].unique())
