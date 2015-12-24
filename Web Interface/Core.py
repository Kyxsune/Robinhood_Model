from flask import *
from pymongo import MongoClient
from flask_bootstrap import Bootstrap

#Define Application and Database
def create_app():
    app = Flask(__name__)
    app.debug = True
    Bootstrap(app)
    return app

app = create_app()

# Define Routes
@app.route('/')
def hello_world():
    return render_template('add.html')

@app.route('/stock_add', methods=['GET','POST'])
def stock_interest():
    if request.method == 'GET':
        pass

# Run Application
if __name__ == '__main__':
    app.run(host='0.0.0.0')