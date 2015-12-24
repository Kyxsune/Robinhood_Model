from flask import *
from pymongo import MongoClient

#Define Application and Database
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Bokeh Goes Here'

@app.route('/stock_add', methods=['GET','POST'])
def stock_interest():
    if request.method == 'GET':
        pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')