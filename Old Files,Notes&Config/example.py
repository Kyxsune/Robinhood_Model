__author__ = 'kyxsune'

import simplejson, urllib2

result = simplejson.load(urllib2.urlopen('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quote%20where%20symbol%20in%20(%22goog%22%2C%22SNE%22%2C%22INTC%22)&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback='))

print result['query']['results']['quote'][1]