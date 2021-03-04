# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 15:27:21 2020

@author: Minzel
"""

import re
import os
import requests
import json
import pandas as pd
from pymongo import MongoClient
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> Hello World!</h1>'

@app.route('/Searcher')
def searcher():
    return render_template('my-form-searcher.html')

@app.route('/Searcher', methods=['POST'])
def searcher_post():
    iter_list = request.form['kws']
    headers = { 'apikey': '20f43de0-bafc-11ea-8a86-61355e28dbdc' }
    iter_list = list(iter_list.split(","))
    
    def fireUpIter(iter_item, nums=100, filename="data"):
        params = (("q",iter_item),("tbm","lcl"),("device","desktop"),
                  ("gl","GB"),("hl","en"),("location","Wales,United Kingdom"),
                  ("num",nums),
                    )
        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
        j = response.text
        data = json.loads(j)
        try:
            df = pd.DataFrame(data["maps_results"])
            df.to_json("data/" + filename + ".json")
        except:
            print("No matching result")
    
    def mergeJson(re_rule="data_\d*"):
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
        return newDF
    
    def autoTrigger(func, iter_list):
        i = 0
        for iter_item in iter_list:
            filename = "data_" + str(i)
            func(iter_item, filename=filename)
            i += 1
            
    autoTrigger(fireUpIter, iter_list)
    newDF = mergeJson(re_rule="data_\d*")
    newDF.to_json("data/searcher_result.json")
    return "<h1> Search succeeded!</h1>"

@app.route('/Crawler')
def crawler():
    def firstProcess(file="data/searcher_result.json"):
        df = pd.read_json(file,encoding="utf-8")
        df.drop_duplicates(subset ="title", 
                         keep = False, inplace = True) 
        df.drop_duplicates(subset ="place_id", 
                         keep = False, inplace = True) 
        try:
            df = df.drop("extensions", axis=1)
        except:
            pass
        url_list = df["url"].values.tolist()
        return df, url_list
    
    def get_text_bs(html):
        tree = BeautifulSoup(html, 'lxml')
    
        body = tree.body
        if body is None:
            return None
    
        for tag in body.select('script'):
            tag.decompose()
        for tag in body.select('style'):
            tag.decompose()
    
        text = body.get_text(separator='\n')
        text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
        return text
    
    def parseIter(url_list):
        price_range = []
        for url in url_list:
            min_price = 0
            max_peice = 0
            try:
                response = requests.get(url)
                text = get_text_bs(response.text)
                
                price_list = re.findall(r"£\d*",text)
                price_list=[s.strip('£') for s in price_list]      
                price_list=[int(i) for i in price_list]
                if len(price_list) >= 2:
                    min_price = min(price_list)
                    max_peice = max(price_list)
                    price_range.append(str(min_price) + ' - ' + str(max_peice)) 
                elif len(price_list) == 1:
                    min_price = min(price_list)
                    price_range.append('0 - ' + str(min_price)) 
                else:
                    price_range.append(None)
                    
                #If the response was successful, no Exception will be raised
                response.raise_for_status()
    
            except HTTPError as http_err:
                print(f'HTTP error occurred: {http_err}')
            except Exception as err:
                price_range.append(None)
                print(f'Other error occurred: {err}') 
            else:
                print('Success!')
                
        return price_range

    def dataClean(df, price_range_list):
        df["price_range"] = price_range_list
        df = df.drop(columns=['coordinates', 'place_id', 'paid'])
        df = df.reset_index(drop=True)
        new_cols = df["directions"].apply(pd.Series)
        new_cols.rename(columns={'url':'google_map_url'}, inplace = True)
        result = pd.concat([df, new_cols ], axis=1)
        result = result.drop(columns=['directions'])
        result["google_map_url"].fillna(value=0)
        result["google_map_url"] = 'https://www.google.com' + result["google_map_url"].astype(str)
        result.loc[result['google_map_url'] == 'https://www.google.comnan','google_map_url'] = None
        return result

    df, url_list = firstProcess(file="data/searcher_result.json")
    price_range_list = parseIter(url_list)
    result = dataClean(df, price_range_list)
    result.to_json("data/improved_data.json")   
    return "<h1> Successfully crawled!</h1>"

@app.route('/ToXLSX')
def to_xlsx():
    return render_template('my-form.html')

@app.route('/ToXLSX', methods=['POST'])
def to_xlsx_post():
    file_path = request.form['aimfile']
    to_path = request.form['tofile']
    test_df = pd.read_json("data/" + file_path + ".json",encoding="utf-8")
    test_df.to_excel("data/" + to_path + ".xlsx", encoding='utf-8')
    return "<h1> Conversion succeeded!</h1>"

@app.route('/SaveInDB')
def save_in_db():
    client = MongoClient('localhost', 27017)
    db = client['GG_search_flask_db']
    collection_currency = db['PAP_addr']
    
    with open('data/improved_data.json') as f:
        file_data = json.load(f)
    
    # if pymongo < 3.0, use insert()
    #collection_currency.insert(file_data)
    # if pymongo >= 3.0 use insert_one() for inserting one document
    collection_currency.insert_one(file_data)
    # if pymongo >= 3.0 use insert_many() for inserting many documents
    #collection_currency.insert_many(file_data)
    
    client.close()
    return "<h1> Successfully saved to the database!</h1>"


app.run()