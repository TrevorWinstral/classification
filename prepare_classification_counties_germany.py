
import urllib.request as urllib2
import bz2
import pandas as pd
import json
from os import listdir
from os.path import isfile, join
import json
onlyfiles = [f for f in listdir('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/') if isfile(join('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/', f))]
'''
with bz2.open('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+onlyfiles[-3], "r") as bzinput:
    print(bzinput)
    lines = []
    for i, line in enumerate(bzinput):
        if i == 10: break
        tweets = json.loads(line)
        lines.append(tweets)
'''
'''
filename0 = "/Users/olgabuchel/Downloads/2020-rki-archive-master/data/2_parsed/data_2020-06-08-02-30.json"
with open(filename0, 'r') as file:
    print(json.load(file)[0])
'''
print(onlyfiles)




filename = "/Users/olgabuchel/Downloads/2020-03-27-12-00_dump.csv.bz2"
import bz2
import csv
from functools import partial

class BZ2_CSV_LineReader(object):
    def __init__(self, filename, buffer_size=4*1024):
        self.filename = filename
        self.buffer_size = buffer_size

    def readlines(self):
        with open(self.filename, 'rb') as file:
            for row in csv.reader(self._line_reader(file)):
                yield row

    def _line_reader(self, file):
        buffer = ''
        decompressor = bz2.BZ2Decompressor()
        reader = partial(file.read, self.buffer_size)

        for bindata in iter(reader, b''):
            block = decompressor.decompress(bindata).decode('utf-8')
            buffer += block
            if '\n' in buffer:
                lines = buffer.splitlines(True)
                if lines:
                    buffer = '' if lines[-1].endswith('\n') else lines.pop()
                    for line in lines:
                        yield line

main_df=pd.DataFrame()
main_df2=pd.DataFrame()
if __name__ == '__main__':
    for el in onlyfiles:
        if ".csv" in el:
            #print(el)
            bz2_csv_filename = '/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+el
            all_rows=[]
            kkeys=[]
            ind=0
            for row in BZ2_CSV_LineReader(bz2_csv_filename).readlines():
                if ind>0:
                    row[10]=row[10].split(" ")[0].replace(",","")
                    all_rows.append(row)
                else:
                    kkeys=row
                ind+=1
            #print(kkeys)    
            df = pd.DataFrame(all_rows, columns=kkeys)
            df['AnzahlFall']=pd.to_numeric(df["AnzahlFall"])
            df0=df.groupby(['Landkreis','Bundesland','Datenstand',kkeys[9]])['AnzahlFall'].sum().reset_index()
            main_df=pd.concat([main_df,df0])
            #print(main_df.groupby(['Landkreis','Bundesland','Datenstand',kkeys[9]])['AnzahlFall'].sum().reset_index())
        elif ".json" in el:
            bz2_csv_filename = '/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+el
            all_rows=[]
            kkeys=[]
            ind=0
            #print(BZ2_CSV_LineReader(bz2_csv_filename).readlines()[0])
            with open(bz2_csv_filename) as file1:
                data=json.load(file1)#bz2.decompress(file1)
                #print(data[0])
                for row in data[0]["features"]:
                    #print(row)
                    list(row["attributes"].values())[10]=list(row["attributes"].values())[10].split(" ")[0].replace(",","")
                    all_rows.append(list(row["attributes"].values()))
                    #print(row["attributes"].values())
                kkeys=list(data[0]["features"][0]["attributes"].keys())
                print(kkeys)
            df = pd.DataFrame(all_rows, columns=kkeys)
            #print(df)
            df['AnzahlFall']=pd.to_numeric(df["AnzahlFall"])
            df0=df.groupby(['Landkreis','Bundesland','Datenstand',kkeys[9]])['AnzahlFall'].sum().reset_index()
            main_df2=pd.concat([main_df2,df0])
            #main_df=main_df2
            #print(main_df2.groupby(['Landkreis','Bundesland','Datenstand',kkeys[9]])['AnzahlFall'].sum().reset_index())
main_df3=pd.concat([main_df,main_df2])
df4=main_df3.groupby(['Landkreis','Bundesland','Datenstand',kkeys[9]])['AnzahlFall'].sum().reset_index()
print(df4.transpose())
