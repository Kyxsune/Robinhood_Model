from Stock_Parser import *
from datetime import datetime
from Task_Manager.celery import app
from pymongo import MongoClient

e
@app.task
def post_daily_collection(result, i):
    '''
    This function posts the minute updated stock price info
    Parameters
    ----------
    result Result returned from a YQL query
    i Index of the stock interested in
    Returns
    -------
    returns a formatted post
    '''
    post = {
        "Symbol": get_stock_symbol(result,i),
        "MarketPrice": get_market_price(result, i),
        "Volume": get_volume(result, i),
        "ShortRatio": get_short_ratio(result, i),
        "BidPrice": get_bid_price(result,i),
        "AskPrice": get_ask_price(result,i),
        "Time": datetime.utcnow()
    }
    return post


@app.task
def update_stock_table(db):
    '''
    This function takes info from the daily collection database and posts it to the stock profile
    Parameters
    ----------
    collection: Name of the collection

    Returns
    -------
    Updates the stock table based on query of daily collection
    '''
    pipeline = { #Query
        {"$sort": {"$Time":1}},
        {"$group": {"_id": "$Symbol",
                    "AvgVolume": {"$avg": "$Volume"},
                    "AvgShort": {"$avg": "$ShortRatio"},
                    "TodaysHigh": {"$max": "$MarketPrice"},
                    "TodaysLow": {"$min":"$MarketPrice"},
                    "Open": {"$first":"$MarketPrice"},
                    "Close":{"$last":"$MarketPrice"}
                    }
         }
    }
    for i in db.daily_stock.aggregate(pipeline):
        post = { # Uses BSON unicode strings as keys
            "Today_Open": i[u'Open'],
            "Today_Close": i[u'Close'],
            "Today_Low": i[u'TodaysLow'],
            "Today_High": i[u'TodaysHigh'],
            "Average_Short": i[u'AvgShort'],
            "Average_Volume": i[u'AvgVolume'],
            "Time": datetime.utcnow()
        }
        db.stock_table.replace_one( # May need to be rewritten
            {"_id":[u'id']},
            post,
            upsert=True
        )

