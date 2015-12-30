from datetime import datetime , timedelta

from Stock_Parser import *
from Task_Manager.celery.celery import celery
from pymongo import MongoClient


@celery.task
def post_daily_collection(db): # Ran by the minute
    '''
    This function posts the minute updated stock price info
    Parameters
    ----------
    db database to be modified
    Returns
    -------
    adds to the daily collection
    '''
    db = MongoClient()[db]
    Stock_list = []
    pipeline = [ #Query
        {"$group": {"_id": "$_id",
                    }
         },
    ]
    for i in db.stock_list.aggregate(pipeline): # This can be written more efficiently
        x = str(i[u'_id'])
        Stock_list.append(x)
    result = stock_get(Stock_list)
    for i in range(len(result['query']['results']['quote'])):
        post = {
            "Symbol": get_stock_symbol(result,i),
            "MarketPrice": get_market_price(result, i),
            "Volume": get_volume(result, i),
            "ShortRatio": get_short_ratio(result, i),
            "BidPrice": get_bid_price(result,i),
            "AskPrice": get_ask_price(result,i),
            "Time": datetime.utcnow()
        }
        db.daily_stock.insert_one(post)
    MongoClient().close()

#post_daily_collection('stox')

@celery.task
def update_Historical_table(db): # Ran by the 15 minute
    '''
    This function takes info from the daily collection database and posts it to the collection for the historical
    data table
    Parameters: database
    ----------
    collection: Name of the collection

    Returns
    -------
    Updates the stock table based on query of daily collection
    '''
    db = MongoClient()[db]
    d = datetime.utcnow()
    d_5 = d - timedelta(seconds=300)
    pipeline = [ #Query
        {"$match": {
            "Time": {
                "$gte": d_5},
                    }},
        {"$group": {"_id": "$Symbol",
                    "PeriodAvgVolume": {"$avg": "$Volume"},
                    "PeriodAvgShort": {"$avg": "$ShortRatio"},
                    "PeriodAvgAskPrice": {"$avg": "$AskPrice"},
                    "PeriodAvgBidPrice": {"$avg": "$BidPrice"},
                    "PeriodHigh": {"$max": "$MarketPrice"},
                    "PeriodLow": {"$min":"$MarketPrice"},
                    "PeriodOpen": {"$first":"$MarketPrice"},
                    "PeriodClose": {"$last":"$MarketPrice"},
                    "HighVolume": {"$min":"$Volume"},
                    "LowVolume": {"$max":"$Volume"},
                    "OpenVolume": {"$first":"$Volume"},
                    "CloseVolume": {"$last":"$Volume"}
                    },
         }
    ]
    #print list(db.daily_stock.aggregate(pipeline))
    for i in db.daily_stock.aggregate(pipeline):
        post = { # Uses BSON unicode strings as keys
            # Price and Short Information
            "Open": i[u'PeriodOpen'],
            "Close": i[u'PeriodClose'],
            "Low": i[u'PeriodLow'],
            "High": i[u'PeriodHigh'],
            "Average_Short": i[u'PeriodAvgShort'],
            "Average_Ask": i[u'PeriodAvgAskPrice'],
            "Average_Bid": i[u'PeriodAvgBidPrice'],
            # Volume Data
            "Open_Volume": i[u'OpenVolume'],
            "Close_Volume": i[u'CloseVolume'],
            "High_Volume": i[u'HighVolume'],
            "Low_Volume": i[u'LowVolume'],
            "Average_Volume": i[u'PeriodAvgVolume'],
            "Time": datetime.utcnow()
        }
        x = str(i[u'_id']) + '_history'
        db[x].insert_one(post)
    MongoClient().close()

#update_Historical_table('stox')

@celery.task
def update_stock_table(db): # Ran by the minute
    '''
    This function takes info from the daily collection database and posts it to the stock profile
    Parameters: database
    ----------
    collection: Name of the collection

    Returns
    -------
    Updates the stock table based on query of daily collection
    '''
    db = MongoClient()[db]
    pipeline = [ #Query
        {"$sort": {"Time":1}},
        {"$group": {"_id": "$Symbol",
                    "AvgVolume": {"$avg": "$Volume"},
                    "AvgShort": {"$avg": "ShortRatio"},
                    "TodaysHigh": {"$max": "$MarketPrice"},
                    "TodaysLow": {"$min":"$MarketPrice"},
                    "Open": {"$first":"$MarketPrice"},
                    "Close": {"$last":"$MarketPrice"}
                    },
         }
    ]
    for i in db.daily_stock.aggregate(pipeline):
        post = { # Uses BSON unicode strings as keys
            "_id": i[u'_id'],
            "Today_Open": i[u'Open'],
            "Today_Close": i[u'Close'],
            "Today_Low": i[u'TodaysLow'],
            "Today_High": i[u'TodaysHigh'],
            "Average_Short": i[u'AvgShort'],
            "Average_Volume": i[u'AvgVolume'],
            "Time": datetime.utcnow()
        }
        db.stock_table.replace_one( # May need to be rewritten
            {"_id": i[u'_id']},
            post,
            upsert=True
        )
    MongoClient().close()
#update_stock_table('stox')

@celery.task
def clear_daily_collection(db):
    '''
    Clears out the daily database
    Parameters
    ----------
    db

    Returns
    -------
    '''
    db = MongoClient()[db]
    db.daily_stock.drop()
    MongoClient().close()

@celery.task
def post33():
    print("itworked")
