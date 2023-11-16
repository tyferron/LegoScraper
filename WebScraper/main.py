# -*- coding: utf-8 -*-
import numpy
import pandas
import matplotlib
import psycopg2
import psycopg2.extras as extras 
from legoScraper import *
from timer import *
import sched, time
import threading

conn = psycopg2.connect("dbname=LegoScraper user=postgres password=123qwe")
cur = conn.cursor()

def addProductPriceEntry(scrapeObject, target_url):
    try:
        cur.execute("INSERT INTO products(product_id, product_name, product_url) VALUEs (%i, '%s', '%s')" % (scrapeObject["set_number"], scrapeObject["name"], target_url))
    except:
        print("Product %i exists in DB" % scrapeObject["set_number"])
    cur.execute("INSERT INTO price(product_id, price, date, site_id, time) VALUES (%i, %d, '%s', %i, '%s')" % (scrapeObject["set_number"], scrapeObject["price"], scrapeObject["dateTime"], scrapeObject["site"], scrapeObject["dateTime"]))
        

target_url = input("Enter Target URL: ")
i = scrapeLego(target_url)

thread = threading.Thread(target=trackerRunner())
thread.start()






addProductPriceEntry(i, target_url)

conn.commit()

print(i)

cur.close()
conn.close()