#!/usr/bin/env python3
import requests
import json
import time
import sqlite3
import datetime
def job ():
    try:
        url = 'http://api.ipstack.com/check?access_key=576131dcca46aea1f083706eba8b0f88&output=json&fields=main&hostname=1'
        result = requests.get(url).content
    except (requests.exceptions.RequestException) as err:
        print (err)
    content = json.loads(result)
    dataframe = list ()
    for key in content:
            value = content[key]
            dataframe.append(value)
    try:
        con = sqlite3.connect('mojabaza.db')
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS iplokacija (
            id integer primary key autoincrement,
            timestamp REAL DEFAULT (datetime('now', 'localtime')),
            ip text,
            hostname text,
            type text,
            continent_code text,
            continent_name text,
            country_code text,
            country_name text,
            region_code text,
            region_name text,
            city text,
            zip integer,
            latitude float,
            longitude float
            )""" )
        cur.execute("INSERT INTO iplokacija (ip,hostname,type,continent_code,continent_name,country_code,country_name,region_code,region_name,city,zip,latitude,longitude) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",dataframe) 
    except Exception as e:
        print ('Greska: ', e)
    con.commit()
    cur.execute("SELECT * from iplokacija order by id DESC LIMIT 1 ")
    print (cur.fetchone(),sep='\n')
    con.close()
if __name__ == '__main__':
    while True:
        starttime=time.time()
        job()
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    
