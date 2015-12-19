from Stock_Parser import *
from datetime import datetime
from Task_Manager.celery import app

@app.task()
def updated_stock_list(db):
    '''
    This function updates the list of stocks to be tracked. Can be modified from the command line and web interface
    Parameters
    ----------
    db The database to be updated.

    Returns
    -------

    '''
    Stock_list = []
    pipeline = { #Query
        {"$sort": {"$Time":1}},
        {"$group": {"_id": "$Symbol",
                    }
         }
    }
    for i in db.stock_list.aggregate(pipeline):
        Stock_list.append(i[u'_id'])
    return Stock_list

@app.task
def post_daily_collection(result, db): # Ran by the half minute
    '''
    This function posts the half minute updated stock price info
    Parameters
    ----------
    result Result returned from a YQL query
    db database to be modified
    Returns
    -------
    adds to the daily collection
    '''
    for i in range(len(result)):
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

@app.task
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
        x = str(i[u'_id']) + '_history'

        db[x].insert_one(post)


@app.task
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

