class Products:
    def __init__(self, vendor_code, product_name, price, quantity):
        self.vendor_code = vendor_code
        self.product_name = product_name
        self.price = price
        self.quantity = quantity


class Sales:
    def __init__(self, data, vendor_code, product_name, price, quantity, seller_id):
        self.data = data
        self.vendor_code = vendor_code
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.seller_id = seller_id


class Employees:
    def __init__(self, seller_id, surname, name):
        self.seller_id = seller_id
        self.surname = surname
        self.name = name
