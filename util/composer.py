import sys

#Composer will gather the data needed to be passed into queries.
class Composer:
    def __init__(self, data):
        self.release = False
        self.database = data
        return

    #Gathers customer data
    def add_customer(self):
        cust = {'customer_id':'','company_name ':'','contact_name':'','contact_title':'',
            'address':'','city':'','region':'','postal_code':'','country':'',
            'phone':'','fax':''
        }
        print("Please enter in necessary details")
        for key in cust.keys():
            cust[key] = input(f"{key.upper()}: ")
            sys.stdout.flush()

        if(self.verify(cust) == True):
            return cust
        else:
            return False
    
    #Gathers order data for the orders and order_details tables.
    def add_order(self):
        order = {'customer_id':'','employee_id':'',
            'order_date':'','required_date':'','ship_name':'','ship_address':'',
            'ship_city':'','ship_region':'','ship_postal_code':'',
            'ship_country':'','product_id':'','unit_price':'','quantity':'',
            'discount':''
        }

        for key in order.keys():
            order[key] = input(f"{key.upper()}: ")
        
        if(self.verify(order) == True):
            return order
        else:
            return False
    
    #Gathers the id of the order to be deleted.
    def remove_order(self):
        ord = input("Enter the Order ID of the order you wish to remove: ")
        try:
            int(ord)
        except:
            print("You must enter a numerical ID.")
            return False
        if(input("Are you sure you wish to delete this order? (y/n) ") == 'y'):
            return ord
        return False

    #Gathers data needed to update the order's ship status.
    def ship_order(self):
        info = {'order_id':'','shipped_date': '', 'ship_via':'','freight':''}

        for key in info.keys():
            info[key] = input(f"{key.upper()}: ")

        if(self.verify(info) == True):
            return info
        else:
            return False
    
    #Gathers information needed to identify and restock a product.
    def restock_product(self, rows):
        prod = {}
        prod['id'] = input('ID (or \'n\' to exit): ')
        cQty = -1
        try:
            if prod['id'] == 'n':
                return False
            for row in rows:
                if row[0] == int(prod['id']):
                    cQty = row[1]
        
            if cQty == -1:
                print("You entered an incorrect ProductID.")
                return False

        
            prod['qty'] = int(input('Enter amount you want to add: ')) + cQty
            return prod
        
        except Exception as ex:
            print(str(ex))
            return False


    #Verifies that the user wants to complete their transaction.
    def verify(self, arr:dict):
        ret = "Is this correct? (y/n)\n"
        for item_name, item_value in arr.items():
            ret +=(f'{item_name.upper()}: {item_value}\n')
        print(ret)

        while(True):
            val = input("Confirm (y/n) >")
            if(val == 'y'):
                return True
            elif(val == 'n'):
                return False
