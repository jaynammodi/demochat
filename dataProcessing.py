
import json, csv, pandas
from pprint import pprint




# DATA PROCESSING
def cleanDB(db):
    clean_data = []
    for x in db:
        thisrow = {k: v for k, v in x.items() if v != "" and pandas.notnull(v)}
        clean_data.append(thisrow)
    return clean_data

def parseCSV(filepath):
    csv_file = pandas.read_csv(filepath)
    data = []

    for x in range(len(csv_file)):
        thisrow = {}
        for key in csv_file.columns:
            thisrow[key] = csv_file[key][x]
        data.append(thisrow)
    return data
        
def buildProductDB(filepath):
    global product_db
    product_db = cleanDB(parseCSV(filepath))

def buildCustomerDB(filepath):
    global customer_db
    customer_db = cleanDB(parseCSV(filepath))

def buildOrdersDB(filepath):
    global order_db
    order_db = cleanDB(parseCSV(filepath))

def buildOffersDB(filepath):
    global offers_db
    offers_db = cleanDB(parseCSV(filepath))

def buildStoreDetails():
    global store_details
    store_details = {
        "name": "Flipkart",
        "address": "Bengaluru, Karnataka",
        "phone": "080 4666 4666",
        "email": "jaynam@kwiqreply.io",
        "website": "https://www.flipkart.com/"
    }

def buildStoreDBS(dir):
    buildProductDB(dir + "products.csv")
    buildCustomerDB(dir + "customers.csv")
    buildOrdersDB(dir + "orders.csv")
    buildOffersDB(dir + "offers.csv")
    buildStoreDetails()

def getStoreDetails():
    global store_details, offers_db, order_db, customer_db, product_db
    return {"store": store_details, "offers": offers_db, "orders": order_db, "customers": customer_db, "products": product_db}

def getProductTD():
    global product_db
    all_prods = []
    for x in product_db:
        cur_str = ["{} - {}".format(k, x[k]) for k in x.keys()]
        all_prods.append(" | ".join(cur_str))
    return all_prods

buildStoreDBS("sample_data/")
pprint(getStoreDetails())
for x in getProductTD():
    print(x)
# pprint(getProductTD())