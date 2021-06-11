import os
import flask
from flask import redirect, url_for, request, render_template
import arrow  # Replacement for datetime, based on moment.js
# import datetime

from pymongo import MongoClient

import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

client = MongoClient('mongodb://localhost:27017/')
db = client.tododb

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html', items = list(db.tododb.find()))

@app.route('/insert/', methods=['POST'])
def insert():
    item_doc = {
        'title': request.form['title'],
        'body': request.form['body']
    }
    db.tododb.insert_one(item_doc)

    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times", methods=['POST'])
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    content = request.get_json()
    print(content)

    km_list = content['km_list'];
    distance = float(content['distance']);
    begin_date = content['begin_date'];
    # dt_begin_date = arrow.get(begin_date, 'YYYY-MM-DDTHH:mm');

    print(begin_date);

    result = [];


    for info in km_list:
        print(info)
        n_km = float(info['km'])
        # open_time = acp_times.open_time(n_km, distance, begin_date).format('YYYY-MM-DDTHH:mm')

        # close_time = acp_times.close_time(n_km, distance, begin_date).format('YYYY-MM-DDTHH:mm')
        open_time="2021-05-01T00:00"
        close_time="2021-07-01T00:00"
        result.append(
            {
                "index": int(info['index']),
                "open_time": open_time,
                "close_time": close_time
            }
        )


    print(result)
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")



    # import os
    # from flask import Flask, redirect, url_for, request, render_template
    # from pymongo import MongoClient
    #
    # app = Flask(__name__)
    #
    # client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
    # db = client.tododb
    #
    # @app.route('/')
    # def index():
    #     return render_template('index.html',
    # 			  items=list(db.tododb.find()))
    #
    # @app.route('/insert/', methods=['POST'])
    # def insert():
    #     item_doc = {
    #         'title': request.form['title'],
    #         'body': request.form['body']
    #     }
    #     db.tododb.insert_one(item_doc)
    #
    #     return redirect(url_for('index'))
    #
    # if __name__ == "__main__":
    #     app.run(host='0.0.0.0', debug=True)



    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    # open_time = acp_times.open_time(km, distance, begin_date.isoformat).format('YYYY-MM-DDTHH:mm')

    # close_time = acp_times.close_time(km, distance, begin_date.isoformat).format('YYYY-MM-DDTHH:mm')
    # open_time="2021-05-01T00:00"
    # close_time="2021-07-01T00:00"
    # result = {"open_time": open_time, "close_time": close_time}



#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
