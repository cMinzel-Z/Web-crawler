# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 18:17:27 2020

@author: Minzel
"""

import re
import os
import pandas as pd
import shutil
from tld import get_tld


original = r'activity.py'
target = r'targ_activity'


def getURL(file):
    df = pd.read_json(file,encoding="utf-8")
    url_l = df[df.url.str.contains("facebook") == False].url.dropna().tolist()
    return url_l

url_l = getURL("data/improved_data.json")
url_l = url_l
print(url_l)

def autoCopy(original, target, url_l):
    i = 0
    for i in range(len(url_l)):
        shutil.copyfile(original, target + str(i) + ".py")
        i+=1

def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
        
def changeLines(target, url_l):
    i = 0
    for i in range(len(url_l)):
        domain = get_tld(url_l[i], as_object=True).fld
        alter(target + str(i) + ".py", "ActivitySpider", "ActivitySpider" + str(i))
        alter(target + str(i) + ".py", "name = \"\"", "name = \"" + "act" + str(i) + "\"")
        alter(target + str(i) + ".py", "allowed_domains = []", "allowed_domains = [\"" + domain + "\"]")
        alter(target + str(i) + ".py", "start_urls = []", "start_urls = [\"" + url_l[i] + "\"]")
        alter(target + str(i) + ".py", "data/items.json", "data/items_" + str(i) + ".json")
        i+=1

def cmdScrapy(url_l):
    i = 0
    for i in range(len(url_l)):
        os.system("python "+ "targ_activity" + str(i) + ".py")
        print("OK")
        i+=1
        
def actDedup(file, i=0):
    try:
        df = pd.read_json(file,encoding="utf-8")
        df.drop_duplicates(subset ="activities", 
                             keep = False, inplace = True) 
        act_val = df.activities.values
        act_val_l = act_val.tolist()
        act_val_l = ', '.join(act_val_l)
        act_val_l = act_val_l.split(", ")
        
        acts = ', '.join(list(set(act_val_l)))
    except:
        acts = ""
    try:
        s_url = df.start_url.values[0]
    except:
        s_url = ""
    newDF = pd.DataFrame(columns=['start_url','activities'])
    newDF = newDF.append({'start_url' : s_url, 'activities' : acts} , ignore_index=True)
    newDF.to_json("data/row_data" + str(i) + ".json")
    
def mergeJson(re_rule="row_data\d*"):
    dir_list = os.listdir('data/')
    json_data_list = []
    
    for file in dir_list:  
        # If the matched data is not None, add this data to the new list
        if  re.match(re_rule, file) != None:  
            json_data_list.append(file)
    
    newDF = pd.DataFrame()
    for json_file in json_data_list:
        df = pd.read_json("data/" + json_file,encoding="utf-8")
        newDF = newDF.append(df, ignore_index = True)
    newDF.to_json("data/merged_data.json")
    
def autoRows(url_l):
    i = 0
    for i in range(len(url_l)):
        actDedup("data/items_"+str(i)+".json", i=i)
        print("OK")
        i+=1

def finalMerge(file1, file2):
    df1 = pd.read_json(file1,encoding="utf-8")
    df2 = pd.read_json(file2,encoding="utf-8")
    df2 = df2.rename(columns={'start_url':'url'})
    final_df = pd.merge(df1, df2, how='left', on='url')
    final_df.to_json("data/final_data.json")

if __name__ == "__main__":
#    autoCopy(original, target, url_l)       
#    changeLines(target, url_l)
#    cmdScrapy(url_l)
#    autoRows(url_l)
    mergeJson(re_rule="row_data\d*")
    finalMerge("data/improved_data.json", "data/merged_data.json")
    