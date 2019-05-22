import waitress
from flask import Flask, render_template, request, redirect, url_for

from app import db, domain

import os


def start():
    app = Flask(__name__)
    db_url = 'data/db.sqlite'

    @app.route("/", methods=['GET'])
    def index():
        get_all_result = db.get_all(db.open_db(db_url))
        return render_template('index.html', items=get_all_result)




    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9877, debug=True)


if __name__ == '__main__':
    start()
