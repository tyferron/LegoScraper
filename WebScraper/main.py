# -*- coding: utf-8 -*-
import numpy
import pandas
import matplotlib
import psycopg2
import psycopg2.extras as extras 
from legoScraper import *
from bestBuyScraper import *
#from timer import *
import sched, time
import threading
import multiprocessing 



def addProductPriceEntry(scrapeObject, target_url):
    conn = psycopg2.connect("dbname=LegoScraper user=postgres password=123qwe")
    cur = conn.cursor()
    pid = 0
    try:
        cur.execute("INSERT INTO products(product_id, product_name, product_url) VALUEs (%i, '%s', '%s')" % (scrapeObject["set_number"], scrapeObject["name"], target_url))
        #cur.execute("SELECT id FROM products WHERE product_url = '%s';" % target_url)
        #pid = result = [item for item, in cur]
    except:
        print("Product %i exists in DB" % scrapeObject["set_number"])

    #cur.execute("INSERT INTO price(product_url, price, date, site_id, time) VALUES ('%s', %d, '%s', %i, '%s')" % (target_url, scrapeObject["price"], scrapeObject["dateTime"], scrapeObject["site"], scrapeObject["dateTime"]))

    conn.commit()
    cur.close()
    conn.close()
    
def userInput():
    while True:
        target_url = input("Enter Target URL: ")
        if "lego.com" in target_url:
            i = scrapeLego(target_url)
        elif "bestbuy.com" in target_url:
            i = scrapeBestBuy(target_url)
        addProductPriceEntry(i, target_url)
        print(i)
        
userInput()
       
#p1 = multiprocessing.Process(target=userInput)
#p2 = multiprocessing.Process(target=startScheduledTimer)
#print("Starting process 1")
#p1.start()
#print("Starting process 2")
#p2.start()

#cur.close()
#conn.close()