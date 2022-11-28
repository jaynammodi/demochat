
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

def buildCatalog():
    global catalog, product_db
    catalog = {}

    for x in product_db:
        if x["Category"] not in catalog.keys():
            catalog[x["Category"]] = {
            "title": x["Category"],
            "rows": [
                {
                "id": x["Handle"],
                "title": x["Title"],
                "description": "{} | {}".format(x["Desc"], x["Price"])
                },
            ]
        }
        else:
            catalog[x["Category"]]["rows"].append({
                "id": x["Handle"],
                "title": x["Title"],
                "description": "{} | {}".format(x["Desc"], x["Price"])
            })           
    return catalog

def buildOffers():
    global offers_db, product_db
    offers = {}

    for x in offers_db:
        if x["Product"] not in offers.keys():
            offers[x["Product"]] = {
                "title": x["Product"],
                "rows": [
                    {
                    "id": x["Offer"],
                    "title": x["Offer"],
                    "description": x["Desc"]
                    },
                ]
            }
        else:
            offers[x["Product"]]["rows"].append({
                "id": x["Offer"],
                "title": x["Offer"],
                "description": x["Desc"]
            })


    payload = json.dumps({
            "to": "<WHOEVER>",
            "recipient_type": "individual",
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                "type": "text",
                "text": "Shopping Menu - Sample"
                },
                "body": {
                "text": "Hi {}, welcome to our store, please choose a product you want to know more about:".format(user_details['name'])
                },
                "footer": {
                "text": "Click on view products to see!"
                },
                "action": {
                "button": "View Products",
                "sections": [
                    {
                    "title": "Clothes",
                    "rows": [
                        {
                        "id": "white_t",
                        "title": "White T-Shirt",
                        "description": "Solid white Polycot T-Shirt"
                        },
                        {
                        "id": "black_t",
                        "title": "Black T-Shirt",
                        "description": "Solid black Polycot T-Shirt"
                        },
                    ]
                    },
                    {
                    "title": "Shoes",
                    "rows": [
                        {
                        "id": "white_sneakers",
                        "title": "White Sneakers",
                        "description": "Contemporary Classic White Sneakers"
                        },
                        {
                        "id": "black_sneakers",
                        "title": "Black Sneakers",
                        "description": "Contemporary Classic Black Sneakers"
                        },
                    ]
                    }
                ]
                }
            }
        })
        # print(" > Generated Payload: ", payload)
    
buildStoreDBS("sample_data/")
pprint(getStoreDetails())
for x in getProductTD():
    print(x)

pprint(buildCatalog())
# pprint(getProductTD())
    