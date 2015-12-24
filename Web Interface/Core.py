from flask import Flask, request , render_template , redirect , url_for
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
    return "Bokeh Server goes here"


@app.route('/result', methods=['POST'])
def it_worked():
    return "It worked"


@app.route('/stock_add', methods=['GET','POST'])
def stock_interest():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        sl = MongoClient()
        post = { "_id" : str(request.form['Symbol']) }
        sl.stock_list.insert_one(post)
        MongoClient().close()
        return redirect(url_for('it_worked'))

# Run Application
if __name__ == '__main__':
    app.run(host='0.0.0.0')