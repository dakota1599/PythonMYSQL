import mysql.connector

#This service handles all communication with the server.  If a query is being sent or received, it goes through
#this service.  It is the engine of this application.
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

            #For testing - If you local environment has the same server login, you can login by setting host
            #to test and everything else to empty.
            if self.conn_info['host'] == 'test':
                self.conn_info['host'] = 'localhost'
                self.conn_info['user'] ='cs4430'
                self.conn_info['pass'] = 'cs4430'
                self.conn_info['database'] = 'northwind'

            #Attempts a connection to the database server
            try:
                self.connection = self.connection.connect(
                    host = self.conn_info['host'],
                    user = self.conn_info['user'],
                    password = self.conn_info['pass'],
                    database = self.conn_info['database']
                    )
                release = True
            #Failure to do so will prompt a retry or escape
            except Exception as ex:
                print(str(ex))
                print('Error, unable to connect to SQL Server.  Please check the accuracy of your Server credentials.')
                if input('Try again? (y/n)') == 'y':
                    continue
                else:
                    return False

        return True
    
    #This shows all the tables in the selected database.
    def show_tables(self):
        cursor = self.connection.cursor()
        cursor.execute("show tables;")
        
        result = cursor.fetchall()

        cursor.close()
        return result

    #Method for sending select queries
    def select(self, query:str):
        cursor = self.connection.cursor()
        #Attempts the query
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        #Spits out error if failure occurs
        except Exception as ex:
            print(str(ex))
            return False
    
    #For inserting customers
    def insert_customer(self, cust:dict):
        ret = self.select(
            f"SELECT * FROM customers where CustomerID = '{cust['customer_id']}';"
        )
        #If the request for an option returns something, then we know the ID is in use
        #and cannot be used.
        if len(ret) > 0:
            print("This ID is already in use.  Cannot complete request")
            return False

        cursor = self.connection.cursor()

        #Attempts inserting of customer account
        try:
            cursor.execute(f"INSERT INTO customers (CustomerID,CompanyName,ContactName,ContactTitle,Address,City,Region,PostalCode,Country,Phone,Fax) VALUES ('{cust['customer_id']}','{cust['company_name ']}','{cust['contact_name']}','{cust['contact_title']}','{cust['address']}','{cust['city']}','{cust['region']}','{cust['postal_code']}','{cust['country']}','{cust['phone']}','{cust['fax']}');")
            self.connection.commit()

            print('Successfully inserted 1 record, ID:', cursor.lastrowid)
            return True
        #Error if failure
        except Exception as ex:
            print(str(ex))
            return False
    
    def insert_order(self, order:dict):
        prods = str(order['product_id']).split(',')
        res = prods
        #We cycle through a list of products to see if a) the products exists and b) if they are not discontinued.
        for prod in prods:
            try:
                ret = self.select(
                    f"SELECT Discontinued FROM products where ProductID = '{abs(int(prod))}';"
                )
            except Exception as ex:
                print(str(ex))
                return False
            
            #If any of these conditions are met, the product id is removed from the final list.
            if(ret == False):
                print(f"Product #{prod} does not exist.")
                res.remove(prod)
                continue
            for row in ret:
                if(row[0] == 'y'):
                    print(f"Product #{prod} is discontinued.  Cannot be added to order.")
                    res.remove(prod)
                    break
            
        #If all product ids are eliminated, then no transaction can be made.
        if len(res) == 0:
            print("All selected products are not available.  Order has been cancelled.")
            return False

        cursor = self.connection.cursor()
        #Attempts the transaction
        try:
            cursor.execute(f"INSERT INTO orders (CustomerID, EmployeeID, OrderDate, RequiredDate, ShippedDate, ShipVia,Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry)"+
                f" VALUES('{order['customer_id']}','{order['employee_id']}','{order['order_date']}','{order['required_date']}',null,null,0.0,'{order['ship_name']}','{order['ship_address']}','{order['ship_city']}','{order['ship_region']}','{order['ship_postal_code']}','{order['ship_country']}');")
        
            self.connection.commit()
            ordID = cursor.lastrowid
            #Looping sql queries for each id in the list
            for prod in res:
                cursor.execute(f"INSERT INTO order_details (OrderID, ProductID, UnitPrice, Quantity, Discount)"+
                    f" VALUES({ordID},'{prod}','{order['unit_price']}','{order['quantity']}','{order['discount']}');")
                self.connection.commit()
            print("Successfully inserted order.")
            return True
        except Exception as ex:
            print(str(ex))
            return False

    #Simply removes the order by id.  If the id doesn't exist, or an error occurs, then error
    #handling takes over.
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

    #For closing the database server connection when finished.
    def close(self):
        self.connection.close()

    def ship_order(self, info:dict):
        cursor = self.connection.cursor()

        #Edits ship data for the desired record.
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

        #Pushes a query with the data generated within the composer.
        try:
            cursor.execute(f"UPDATE products SET UnitsInStock = {prod['qty']} WHERE ProductID = {prod['id']}")
            self.connection.commit()

            print(f"Product #{prod['id']} has been restocked to {prod['qty']} units.")
            return True
        except Exception as ex:
            print(str(ex))
            return False