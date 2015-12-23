from flask import *
from pymongo import MongoClient

#Define Application and Database
app = Flask(__name__)
db = MongoClient()['stox']


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')