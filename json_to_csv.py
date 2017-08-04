import json
import os
import re
import sys
import csv
import io

 
def convertToCSV(jsonData, keys):
    returnData = {}
    global counter
    row = []

    groups = ["cited_patents","inventors","application_citations",
                "applications", "assignees","citedby_patents","coinventors",
                "cpc_subgroups", "cpc_subsections", "cpcs", "IPCs", 
                "locations", "nber_subcategories","nbers","patents",
                "uspc_mainclasses", "uspc_subclasses","uspcs","years", 
                "rawinventors","wipos","gov_interests"]

    common = list(set(groups).intersection(set(keys)))

    if(len(common)>0):
        # Generate the length of maximum results
        length_dict = len(jsonData[common[0]])  
        for group in common:
            if len(jsonData[group]) > length_dict:
                length_dict = len(jsonData[group])
    else:  
        length_dict = 1
    for i in range(0, length_dict):
        row = []
        returnData[i] = {}
        for key in keys:
            if key in common:
                try:
                    index = keys.index(key)
                    tempData = jsonData[key][i]
                    tempKeys = sorted(tempData.keys())
                    for k in tempKeys:
                        returnData[i][k] = tempData[k]
                except:
                    pass
            else:
                returnData[i][key] = jsonData[key]
    return returnData
 
def writeCSV(a, filename):
    write = csv.writer(io.open(filename, 'w', newline='', encoding='Latin-1'))
    groups = ["cited_patents","inventors","application_citations",
                "applications", "assignees","citedby_patents","coinventors",
                "cpc_subgroups", "cpc_subsections", "cpcs", "IPCs", 
                "locations", "nber_subcategories","nbers","patents",
                "uspc_mainclasses", "uspc_subclasses","uspcs","years", 
                "rawinventors","wipos","gov_interests"]
    key = list(a.keys())
    key = list(set(groups).intersection(set(key)))
    j = a[key[0]]
    i = 0
    prevRow = []
    if (j is not None):
        for jsonData in j:
            k = 0
            keys = jsonData.keys()
            csvData = convertToCSV(jsonData, sorted(keys))
            if (i==0):
                write.writerow(list(sorted(csvData[0].keys())))
            for key in csvData.keys():
                row = []
                row2 = []
                data = csvData[key]
                for k in sorted(csvData[0].keys()):
                    try:
                        row = row + [data[k]]
                    except:
                        row = row + [csvData[0][k]]
                flag = False
                for item in row:
                    if item != "":
                        flag = True
                if (flag):
                    try:
                        row = [str(s).encode("Latin-1", "replace").decode('cp1252') for s in row]
                    except:
                        pass
                    write.writerow(row)
            i += 1
 
def merge_csv(fd,q,requests):
    diri = [d for d in os.listdir(fd) if re.search(q+'_\d+.csv',d)]
    csv_out = open(os.path.join(fd, q+'.csv'), 'w')
    for line in open(os.path.join(fd,q+'_0.csv')):
        csv_out.write(line)
    for i in range(requests):
        f = open(os.path.join(fd, q+'_'+str(i)+'.csv'), 'r+', encoding='Latin-1')
        if sys.version_info >= (3,):
            next(f)
        else:
            f.next()
        for line in f:
            csv_out.write(line)
        f.close()
    csv_out.close()
 
def main(fd, q, requests):
    diri = [d for d in os.listdir(fd) if re.search(q+'_\d+.json',d)]
    for d in diri:
        filename = fd + '/' + d
        data = open(filename, "r").read()
        try:
            b = json.loads(data)
        except:
            print("ERROR")
            sys.exit(1)
        filename = filename.replace('.json', '.csv')
        writeCSV(b, filename)
    merge_csv(fd, q, requests)

    # Remove individual component files
    for d in diri:
        os.remove(os.path.join(fd,d))
        os.remove(os.path.join(fd,d.replace('.json','.csv')))