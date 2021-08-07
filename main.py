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
    comp = Composer(sql_serv.conn_info['database'])
    while(close == False):
        print('What operation would you like to complete?\n')
        opt = input("1)Add a customer\n2)Add an Order\n3)Remove an Order\n"+
            "4)Ship an Order\n5)Print Pending Orders\n6)Restock a Product\n"+
            "0)Exit\n"
        )
        if(opt == '0'):
            return

        elif(opt == '1'):
            ret = comp.add_customer() 
            if ret == False:
                print('Information Discarded.')
                continue
            sql_serv.insert_customer(ret)
        
        elif(opt == '2'):
            ret = comp.add_order()
            if ret == False:
                print('Informatin Discarded.')
                continue
            sql_serv.insert_order(ret)
        
        elif(opt == '3'):
            ret = comp.remove_order()
            if ret == False:
                continue
            sql_serv.remove_order(ret)

        elif(opt == '4'):
            ret = comp.ship_order()
            if ret == False:
                continue
            sql_serv.ship_order(ret)

        elif(opt == '5'):
            print('Order ID - Order Date (Oldest - Newest)')
            res = ''
            for row in sql_serv.select(
                'Select * from orders where ShippedDate is null order by OrderDate;'
            ):
                res += (f"{row[0]} - {row[3]}\n")
            print(res)


if __name__ == "__main__":
    main()