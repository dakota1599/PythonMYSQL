import mysql.connector

class SQLService:

    def __init__(self):
        self.connection = mysql.connector
    
    def connect(self):
        release = False
        self.conn_info = {}
        while(release == False):
            print('Please enter your SQL Server below:\n')
            self.conn_info['host'] = input('Enter Server Host: ')
            self.conn_info['user'] = input('Enter Server Username: ')
            self.conn_info['pass'] = input('Enter Server Password: ')
            self.conn_info['database'] = input('Enter Server Database: ')

            #For testing
            if self.conn_info['host'] == 'test':
                self.conn_info['host'] = 'localhost'
                self.conn_info['user'] ='cs4430'
                self.conn_info['pass'] = 'cs4430'
                self.conn_info['database'] = 'northwind'

            try:
                self.connection = self.connection.connect(
                    host = self.conn_info['host'],
                    user = self.conn_info['user'],
                    password = self.conn_info['pass'],
                    database = self.conn_info['database']
                    )
                release = True
            except:
                print('Error, unable to connect to SQL Server.  Please check the accuracy of your Server credentials.')
                if input('Try again? (y/n)') == 'y':
                    continue
                else:
                    return False

        return True
    
    def show_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("show tables;")
        
        result = cursor.fetchall()

        cursor.close()
        return result

    def select(self, query:str):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as ex:
            print(str(ex))
            return False
    
    def insert_customer(self, cust:dict):

        ret = self.select(
            f"SELECT * FROM customers where CustomerID = '{cust['customer_id']}';"
        )

        if len(ret) > 0:
            print("This ID is already in use.  Cannot complete request")
            return False

        cursor = self.connection.cursor()

        try:
            cursor.execute(f"INSERT INTO customers (CustomerID,CompanyName,ContactName,ContactTitle,Address,City,Region,PostalCode,Country,Phone,Fax) VALUES ('{cust['customer_id']}','{cust['company_name ']}','{cust['contact_name']}','{cust['contact_title']}','{cust['address']}','{cust['city']}','{cust['region']}','{cust['postal_code']}','{cust['country']}','{cust['phone']}','{cust['fax']}');")
            self.connection.commit()

            print('Successfully inserted 1 record, ID:', cursor.lastrowid)
            return True
        except Exception as ex:
            print(str(ex))
            return False
    
    def insert_order(self, order:dict):

        ret = self.select(
            f"SELECT * FROM products where ProductID = {order['product_id']}"
        )
        if(ret == False):
            print("Product does not exist.")
            return False
        else:
            for row in ret:
                if(row[9] == 'y'):
                    print("Product is discontinued.  Cannot complete order.")
                    return False

        cursor = self.connection.cursor()
        try:
            cursor.execute(f"INSERT INTO orders (CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia,Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)"+
                f" VALUES('{order['customer_id']}','{order['employee_id']}','{order['order_date']}','{order['required_date']}',null,null,0.0,'{order['ship_name']}','{order['ship_address']}','{order['ship_city']}','{order['ship_region']}','{order['ship_postal_code']}','{order['ship_country']}');")
        
            self.connection.commit()

            cursor.execute(f"INSERT INTO order_details (OrderID, ProductID, UnitPrice, Quantity, Discount)"+
                f" VALUES({cursor.lastrowid},'{order['product_id']}','{order['unit_price']}','{order['quantity']}','{order['discount']}');")

            self.connection.commit()
            print("Successfully inserted order.")
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def remove_order(self, ord):
        cursor = self.connection.cursor()

        try:
            cursor.execute(f"DELETE FROM order_details WHERE OrderID = {ord};")
            self.connection.commit()
            cursor.execute(f"DELETE FROM orders WHERE OrderID = {ord};")
            self.connection.commit()

            print(f"Order #{ord} successfully deleted.\n")
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def close(self):
        self.connection.close()

    def ship_order(self, info:dict):
        cursor = self.connection.cursor()

        try:
            cursor.execute((f"UPDATE orders set ShippedDate = '{info['shipped_date']}',"+
                    f"ShipVia = '{info['ship_via']}', Freight = '{info['freight']}' "+
                    f"WHERE OrderID = {info['order_id']};"
            ))
            self.connection.commit()

            print("Order has been shipped.")
            return True
        except Exception as ex:
            print(str(ex))
            return False
    
    def restock_product(self, prod:dict):
        cursor = self.connection.cursor()

        try:
            cursor.execute(f"UPDATE products SET UnitsInStock = {prod['qty']} WHERE ProductID = {prod['id']}")
            self.connection.commit()

            print(f"Product #{prod['id']} has been restocked to {prod['qty']} units.")
            return True
        except Exception as ex:
            print(str(ex))
            return False