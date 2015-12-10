from Stock_Parser import *
import datetime


def post_daily_collection(result, i):
    post = {
        "Market Price": get_market_price(result, i),
        "Volume": get_volume(result, i),
        "Short Ratio": get_short_ratio(result, i)
    }
    return post
