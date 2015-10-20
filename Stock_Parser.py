__author__ = 'kyxsune'

from simplejson import load
from urllib import urlopen , quote_plus
from operator import concat


def stock_get(Symbols):
    '''
    This function is for getting stock info from the yahoo finance api
    :param Symbols: A list of symbols format ["APPL","GOOG","etc"]
    :return: Returns a dictionary of the parse JSON
    '''
    if not type(Symbols) is list: #Make sure Symbols is a list (if not raise an error)
        raise TypeError("Must be a list of the Stock Symbols")
    # Create URL from Components (used in line for loop and reduce to simplify
    Base_url = 'https://query.yahooapis.com/v1/public/yql?q=select * '
    query = 'from yahoo.finance.quote where symbol in '
    sub = [('{' + str(x) + '},') for x in range(len(Symbols))]
    query_full = (query + '(' + reduce(concat,sub)[:-1] + ')').format(*Symbols)
    url_full = Base_url + quote_plus(query_full) + '&format=json&env=http://datatables.org/alltables.env' # This last part is a workaround due to Yahoo error stuff
    # Open and load json into dictionary used simplejson and urllib
    result = load(urlopen(url_full))
    return result

j = ['"GOOG"','"APPL"','"SNE"']

print stock_get(j)['query']['results']['quote']

