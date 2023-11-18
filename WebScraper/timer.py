from apscheduler.schedulers.blocking import BlockingScheduler
import psycopg2
import psycopg2.extras as extras 
from legoScraper import *
from bestBuyScraper import *




def addProductPriceEntry(scrapeObject, target_url):
    conn = psycopg2.connect("dbname=LegoScraper user=postgres password=123qwe")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO price(product_url, price, date, site_id, time) VALUES ('%s', %d, '%s', %i, '%s')" % (target_url, scrapeObject["price"], scrapeObject["dateTime"], scrapeObject["site"], scrapeObject["dateTime"]))
    except:
        print("OH NO! " + cur)
    conn.commit()
    cur.close()
    conn.close()

def trackerRunner():
    conn = psycopg2.connect("dbname=LegoScraper user=postgres password=123qwe")
    cur = conn.cursor()
    cur.execute("SELECT product_url FROM products;")
    result = [item for item, in cur]
    conn.commit()
    cur.close()
    conn.close()
    for item in result:
        if "lego.com" in item:
            i = scrapeLego(item)
        elif "bestbuy.com" in item:
            i = scrapeBestBuy(item)
        addProductPriceEntry(i, item)
        print("added "+item)
        print(i)

#def startScheduledTimer():
scheduler = BlockingScheduler()
scheduler.add_job(trackerRunner, 'interval', hours=6)
scheduler.start()