class Products:
    def __init__(self, vendor_code, product_name, price, quantity):
        self.vendor_code = vendor_code
        self.product_name = product_name
        self.price = price
        self.quantity = quantity


class Sales:
    def __init__(self, date, vendor_code, price, quantity, seller_id):
        self.date = date
        self.vendor_code = vendor_code
        self.price = price
        self.quantity = quantity
        self.seller_id = seller_id


class Employees:
    def __init__(self, employee_id, surname, name):
        self.employee_id = employee_id
        self.surname = surname
        self.name = name


