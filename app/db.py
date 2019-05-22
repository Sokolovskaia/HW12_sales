import sqlite3

from app.domain import Products


def open_db(url):
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


# Создание схемы
def init_db(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            vendor_code INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0)
        );
        """)
        connection.commit()


def get_all(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT vendor_code, product_name, price, quantity  
          FROM products""")
        items = []
        for row in cursor:  # [Row, Row] -> [Good, Good]
            items.append(
                Products(
                    row['vendor_code'],
                    row['product_name'],
                    row['price'],
                    row['quantity']
                )
            )
        return items


def search_by_vendor_code(connection, vendor_code):
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT vendor_code, product_name, price, quantity 
                 FROM products 
                WHERE vendor_code = :vendor_code""",
            {'vendor_code': vendor_code}
        )
        for row in cursor:
            return Products(
                row['vendor_code'],
                row['product_name'],
                row['price'],
                row['quantity']
            )


def add(connection, product):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO products(vendor_code, product_name, price, quantity) 
             VALUES (:vendor_code, :product_name, :price, :quantity)
        """, {'vendor_code': product.vendor_code, 'product_name': product.product_name, 'price': product.price,
              'quantity': product.quantity})
        connection.commit()


def remove_by_vendor_code(connection, vendor_code):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        DELETE FROM products
              WHERE vendor_code = :vendor_code
        """, {'vendor_code': vendor_code})
        connection.commit()
