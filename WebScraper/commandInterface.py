import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
import psycopg2.extras as extras 
from legoScraper import *
from bestBuyScraper import *
from sys import exit


conn = psycopg2.connect("dbname=LegoScraper user=postgres password=123qwe")
cur = conn.cursor()

def insertProductPriceEntry(scrapeObject, target_url):

    pid = 0
    try:
        cur.execute("INSERT INTO products(product_id, product_name, product_url) VALUEs (%i, '%s', '%s')" % (scrapeObject["set_number"], scrapeObject["name"], target_url))
        #cur.execute("SELECT id FROM products WHERE product_url = '%s';" % target_url)
        #pid = result = [item for item, in cur]
        conn.commit()
        cur.execute("INSERT INTO price(product_url, price, date, site_id, time) VALUES ('%s', %d, '%s', %i, '%s')" % (target_url, scrapeObject["price"], scrapeObject["dateTime"], scrapeObject["site"], scrapeObject["dateTime"]))
        conn.commit()
    except:
        print("Product %i exists in DB" % scrapeObject["set_number"])

    #cur.execute("INSERT INTO price(product_url, price, date, site_id, time) VALUES ('%s', %d, '%s', %i, '%s')" % (target_url, scrapeObject["price"], scrapeObject["dateTime"], scrapeObject["site"], scrapeObject["dateTime"]))

    conn.commit()
    
def userInput():
    while True:
        command = input("Enter command: ")
        commandList = command.split()
        match commandList[0]:
            case "help":
                print("You can enter commands such as 'track'")
            case "track":
                target_url = commandList[1]
                if "lego.com" in target_url:
                    i = scrapeLego(target_url)
                elif "bestbuy.com" in target_url:
                    i = scrapeBestBuy(target_url)
                insertProductPriceEntry(i, target_url)
                print(i)
            case "lowestprice":
                transaction="""SELECT date, MIN(price) price
                        FROM price 
                        INNER JOIN products USING (product_url)
                        INNER JOIN sites USING (site_id)
                        WHERE product_id = %i
                        GROUP BY date
                        ORDER BY date;""" % int(commandList[1])
                cur.execute(transaction)
                result = cur.fetchall()
                print(result)
            case "currentprice":
                transaction="""SELECT site_name site, MAX(date), price price
                        FROM price 
                        INNER JOIN products USING (product_url)
                        INNER JOIN sites USING (site_id)
                        WHERE product_id = %i
                        GROUP BY site, price
                        ORDER BY site;""" % int(commandList[1])
                cur.execute(transaction)
                result = cur.fetchall()
                print(result)
            case "pricegraph":
                if commandList[2] == "Best":
                    commandList[2] = "Best Buy"
                    del commandList[3]
                if commandList.len == 2:
                    transaction="""SELECT date
                                    FROM price 
                                    INNER JOIN products USING (product_url)
                                    INNER JOIN sites USING (site_id)
                                    WHERE product_id = %i AND site_name = '%s'
                                    ORDER BY date ASC;""" % (int(commandList[1]), "Best Buy")
                    cur.execute(transaction)
                    x = [item for item, in cur]
                    x = pd.to_datetime(x)
                    transaction="""SELECT price 
                                    FROM price 
                                    INNER JOIN products USING (product_url)
                                    INNER JOIN sites USING (site_id)
                                    WHERE product_id = %i AND site_name = '%s'
                                    ORDER BY date ASC;""" % (int(commandList[1]), "Best Buy")
                    cur.execute(transaction)
                    y = np.array(cur.fetchall())
                    plt.plot(x, y, label="Best Buy")
                    transaction="""SELECT date
                                    FROM price 
                                    INNER JOIN products USING (product_url)
                                    INNER JOIN sites USING (site_id)
                                    WHERE product_id = %i AND site_name = '%s'
                                    ORDER BY date ASC;""" % (int(commandList[1]), "Lego")
                    cur.execute(transaction)
                    x = [item for item, in cur]
                    x = pd.to_datetime(x)
                    transaction="""SELECT price 
                                    FROM price 
                                    INNER JOIN products USING (product_url)
                                    INNER JOIN sites USING (site_id)
                                    WHERE product_id = %i AND site_name = '%s'
                                    ORDER BY date ASC;""" % (int(commandList[1]), "Lego")
                    cur.execute(transaction)
                    y = np.array(cur.fetchall())
                    plt.plot(x, y, '-.', label = "Lego")
                    plt.xlabel("Date")  # add X-axis label 
                    plt.ylabel("Price")  # add Y-axis label 
                    plt.title("Price over time for %s for all sites" % (commandList[1]))  # add title 
                    plt.gcf().autofmt_xdate()
                    plt.show()
                elif commandList.len > 2:
                    transaction="""SELECT date
                                    FROM price 
                                    INNER JOIN products USING (product_url)
                                    INNER JOIN sites USING (site_id)
                                    WHERE product_id = %i AND site_name = '%s'
                                    ORDER BY date ASC;""" % (int(commandList[1]), commandList[2])
                    cur.execute(transaction)
                    x = [item for item, in cur]
                    x = pd.to_datetime(x)
                    transaction="""SELECT price 
                                    FROM price 
                                    INNER JOIN products USING (product_url)
                                    INNER JOIN sites USING (site_id)
                                    WHERE product_id = %i AND site_name = '%s'
                                    ORDER BY date ASC;""" % (int(commandList[1]), commandList[2])
                    cur.execute(transaction)
                    y = np.array(cur.fetchall())
                    plt.plot(x, y)
                    plt.xlabel("Date")  # add X-axis label 
                    plt.ylabel("Price")  # add Y-axis label 
                    plt.title("Price over time for %s at %s" % (commandList[1], commandList[2]))  # add title 
                    plt.gcf().autofmt_xdate()
                    plt.show()
            case "exit":
                exit()