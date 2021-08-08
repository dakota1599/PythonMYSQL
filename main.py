from util.sql_service import SQLService
from util.composer import Composer


#The main function that kicks off the program.  Everything begins and ends here.
def main():
    sql_serv = SQLService()
    if(sql_serv.connect()):
        print("\nWelcome.  Here are your tables: \n")
        for table in sql_serv.show_tables():
            print(table)
        operate(sql_serv)
        print('Goodbye!')
        return sql_serv.close()
    else:
        print('Goodbye...')

#Operate orchestrates all interactions with the user.  This function will call all
#necessary classes and objects.
def operate(sql_serv:SQLService):
    close = False
    #The composer object for gathering data
    comp = Composer()
    while(close == False):
        print('What operation would you like to complete?\n')
        opt = input("1)Add a customer\n2)Add an Order\n3)Remove an Order\n"+
            "4)Ship an Order\n5)Print Pending Orders\n6)Restock a Product\n"+
            "0)Exit\n"
        )
        #Python does not have case functionality, so we are left with the old
        #if conditional statements.
        #Escape option
        if(opt == '0'):
            return

        #Adding a customer option
        elif(opt == '1'):
            ret = comp.add_customer() 
            if ret == False:
                print('Information Discarded.')
                continue
            sql_serv.insert_customer(ret)
        
        #Adding an order option
        elif(opt == '2'):
            ret = comp.add_order()
            if ret == False:
                print('Informatin Discarded.')
                continue
            sql_serv.insert_order(ret)
        
        #Removing an order option
        elif(opt == '3'):
            ret = comp.remove_order()
            if ret == False:
                continue
            sql_serv.remove_order(ret)

        #Shipping an order option
        elif(opt == '4'):
            ret = comp.ship_order()
            if ret == False:
                continue
            sql_serv.ship_order(ret)

        #Listing pending orders option
        elif(opt == '5'):
            print('Order ID - Order Date (Oldest - Newest)')
            res = ''
            for row in sql_serv.select(
                'Select * from orders where ShippedDate is null order by OrderDate;'
            ):
                res += (f"{row[0]} - {row[3]}\n")
            print(res)
        
        #List products due for restocking option
        elif(opt == '6'):
            print('Products Due for Resocking\n-----------------')
            res = ''
            rows = sql_serv.select(
                'Select ProductID,UnitsInStock,UnitsOnOrder,ReorderLevel from products Where Discontinued = \'n\''
            )
            for row in rows:
                units = row[1] + row[2]
                if(units < row[3]):
                    res += f"ID: {row[0]} - {units} units | Reorder level: {row[3]}\n"
            print(res)

            ret = comp.restock_product(rows)
            if ret == False:
                continue
            sql_serv.restock_product(ret)



#Kicks off the main function
if __name__ == "__main__":
    main()