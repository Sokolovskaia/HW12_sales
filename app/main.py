import waitress
from flask import Flask, render_template, request, redirect, url_for

from app import db

import os

from app.domain import Products, Sales, Employees


def start():
    app = Flask(__name__)
    db_url = 'db.sqlite'

    @app.route("/", methods=['GET'])
    def index():
        search = request.args.get('search')  ## ----
        if search:
            search_result = db.search_product(db.open_db(db_url), search)  ## ----
            return render_template('index.html', items=search_result, search=search)
        get_all_result = db.get_all(db.open_db(db_url))
        return render_template('index.html', items=get_all_result)

    @app.route("/product_details/<vendor_code>", methods=['GET'])
    def details_of_product(vendor_code):
        search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
        return render_template('product_details.html', item=search_by_vendor_code_result)

    @app.route("/add", methods=['GET'])
    def add_form():
        return render_template('add.html')

    @app.route("/add", methods=['POST'])
    def add_product():
        vendor_code = int(request.form['vendor_code'])
        product_name = request.form['product_name']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
        product = Products(vendor_code, product_name, price, quantity)
        db.add(db.open_db(db_url), product)
        return redirect(url_for('index'))

    @app.route("/remove/<vendor_code>", methods=['GET'])
    def remove_form(vendor_code):
        search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
        return render_template('remove.html', item=search_by_vendor_code_result)

    @app.route("/remove/<vendor_code>", methods=['POST'])
    def remove(vendor_code):
        db.remove_by_vendor_code(db.open_db(db_url), vendor_code)
        return redirect(url_for('index'))

    @app.route("/edit_product/<vendor_code>", methods=['GET'])
    def edit_form(vendor_code):
        search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
        return render_template('edit_product.html', item=search_by_vendor_code_result)

    @app.route("/edit_product/<vendor_code>", methods=['POST'])
    def edit(vendor_code):
        product_name = request.form['product_name']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
        product = Products(vendor_code, product_name, price, quantity)
        db.edit_by_vendor_code(db.open_db(db_url), product)
        return redirect(url_for('index', vendor_code=vendor_code))

    # ---------------------------------------------------------------------------------

    @app.route("/sell/<vendor_code>", methods=['GET'])
    def sell_form(vendor_code):
        search_by_vendor_code_result = db.search_by_vendor_code(db.open_db(db_url), vendor_code)
        return render_template('sell.html', item=search_by_vendor_code_result)

    @app.route("/sell/<vendor_code>", methods=['POST'])
    def sell(vendor_code):
        date = request.form['date']
        price = int(request.form['price'])
        quantity = int(request.form['quantity'])
        seller_id = int(request.form['seller_id'])
        sale = Sales(date, vendor_code, price, quantity, seller_id)
        db.sale_by_vendor_code(db.open_db(db_url), sale)
        return redirect(url_for('index', vendor_code=vendor_code))

    @app.route("/statistics", methods=['GET'])
    def statistics():
        get_statistics_result = db.get_statistics(db.open_db(db_url))
        return render_template('statistics.html', items=get_statistics_result)









    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9873, debug=True)


if __name__ == '__main__':
    start()
