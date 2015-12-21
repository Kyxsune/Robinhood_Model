__author__ = 'kyxsune'

from simplejson import load
from urllib import urlopen , quote_plus
from operator import concat

# Pull From Yahoo
def stock_get(Symbols):
    '''
    This function is for getting stock info from the yahoo finance api
    :param Symbols: A list of symbols format ["APPL","GOOG","etc"]
    :return: Returns a dictionary of the parse JSON
    '''
    if not type(Symbols) is list: #Make sure Symbols is a list (if not raise an error)
        raise TypeError("Must be a list of the Stock Symbols")
    # Create URL from Components (used in line for loop and reduce to simplify
    base_url = 'https://query.yahooapis.com/v1/public/yql?q=select * '
    query = 'from yahoo.finance.quotes where symbol in '
    sub = [('{' + str(x) + '},') for x in range(len(Symbols))]
    query_full = (query + '(' + '"' + reduce(concat,sub)[:-1] + '"' + ')').format(*Symbols)
    url_full = base_url + quote_plus(query_full) + '&format=json&env=http://datatables.org/alltables.env' # This last part is a workaround due to Yahoo error stuff
    # Open and load json into dictionary used simplejson and urllib
    result = load(urlopen(url_full))
    return result

# Frequently Called functions
def get_market_price(result,i):
    '''
    This function is for getting the price info (quote) out of the Dict returned by the yahoo finance api
    Parameters
    ----------
    result: the dict returned by the stock_get function
    i the index of the desired symbol

    Returns
    -------
    The market price of the stock currently
    '''
    return float(result['query']['results']['quote'][i]['LastTradePriceOnly'])

def get_ask_price(result,i):
    '''
    This function is for getting the price info (ask) out of the Dict returned by the yahoo finance api
    Ask price is the price the seller is willing to offer for the security
    Parameters
    ----------
    result: the dict returned by the stock_get function
    i the index of the desired symbol

    Returns
    -------
    The ask price of the stock currently
    '''
    return float(result['query']['results']['quote'][i]['Ask'])

def get_bid_price(result,i):
    '''
    This function is for getting the price info (bid) out of the Dict returned by the yahoo finance api
    Bid price is the price the buyer is willing to pay for the security
    Parameters
    ----------
    result: the dict returned by the stock_get function
    i the index of the desired symbol

    Returns
    -------
    The bid price of the stock currently
    '''
    return float(result['query']['results']['quote'][i]['Bid'])

def get_volume(result,i):
    '''
    This function is for getting the volume out of the Dict returned by the yahoo finance api
    Volume is the amount of securities presently on the exchange
    Parameters
    ----------
    result: the dict returned by the stock_get function
    i the index of the desired symbol

    Returns
    -------
    The bid price of the stock currently
    '''
    return float(result['query']['results']['quote'][i]['Volume'])

def get_short_ratio(result,i):
    '''
    This function is for getting the Short Ratio out of the Dict returned by the yahoo finance api
    Short ratio is the ratio of shorted stock to normal stock in the company (Average Volume/Shorts Volume)
    Parameters
    ----------
    result: the dict returned by the stock_get function
    i the index of the desired symbol

    Returns
    -------
    The bid price of the stock currently
    '''
    return float(result['query']['results']['quote'][i]['ShortRatio'])

def get_stock_symbol(result,i):
    '''
    This function is for getting the stock symbol out of the Dict returned by the yahoo finance api
    Parameters
    ----------
    result: the dict returned by the stock_get function
    i the index of the desired symbol

    Returns
    -------
    The stock symbol
    '''
    return result['query']['results']['quote'][i]['symbol']

# Custom For niche cases (if frequently used add above)
def get_blank(result,i,x=0):
    '''
    This is a generic function for pulling values out of the stock_get function
    Parameters
    ----------
    result the dict returned by the stock_get function
    i the index of the stock
    x dictionary key desired

    Returns
    -------

    '''
    if x:
       return float(result['query']['results']['quote'][i][x])
    else:
        return None


