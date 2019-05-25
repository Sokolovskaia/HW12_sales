import sqlite3

from app.domain import Products, Sales, Statistics


def open_db(url):
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


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


def create_table_employees(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
          employee_id INTEGER PRIMARY KEY AUTOINCREMENT
        , surname TEXT NOT NULL
        , name TEXT NOT NULL
        );
        """)
        connection.commit()


def create_table_sales(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
          date NUMERIC NOT NULL
        , vendor_code INTEGER NOT NULL
        , price INTEGER NOT NULL
        , quantity INTEGER NOT NULL CHECK (quantity >= 0)
        , seller_id TEXT NOT NULL
         
        , FOREIGN KEY (vendor_code) REFERENCES products (vendor_code)
        , FOREIGN KEY (seller_id) REFERENCES employees (employee_id) 
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
        for row in cursor:
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


def edit_by_vendor_code(connection, product):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE products 
           SET vendor_code = :vendor_code
             , product_name = :product_name
             , price = :price
             , quantity = :quantity
         WHERE vendor_code = :vendor_code
        """, {'vendor_code': product.vendor_code, 'product_name': product.product_name, 'price': product.price,
              'quantity': product.quantity})
        connection.commit()


def search_product(connection, search):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT vendor_code
             , product_name
             , price
             , quantity
          FROM products
         WHERE :search=vendor_code OR :search=product_name""", {'search': search})
        items = []
        for row in cursor:
            items.append(
                Products(
                    row['vendor_code'],
                    row['product_name'],
                    row['price'],
                    row['quantity']
                )
            )
        return items


def sale_by_vendor_code(connection, sale):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO sales(date, vendor_code, price, quantity, seller_id) 
             VALUES (:date, :vendor_code, :price, :quantity, :seller_id)
        """, {'date': sale.date, 'vendor_code': sale.vendor_code, 'price': sale.price,
              'quantity': sale.quantity, 'seller_id': sale.seller_id})
        connection.commit()


def get_statistics(connection):
    with connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT s.date, s.vendor_code, p.product_name, s.price, s.quantity, s.seller_id, e.surname, e.name  
          FROM sales s LEFT JOIN products p 
            ON s.vendor_code = p.vendor_code
     LEFT JOIN employees e 
            ON s.seller_id = e.employee_id""")
        items = []
        for row in cursor:
            items.append(
                Statistics(
                    row['date'],
                    row['vendor_code'],
                    row['product_name'],
                    row['price'],
                    row['quantity'],
                    row['seller_id'],
                    row['surname'],
                    row['name']
                )
            )
        return items
