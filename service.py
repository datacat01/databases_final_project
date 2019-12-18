import pymysql
from models import Access_db
from checks import is_number

class Dishes(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_table(self):
        sql = "SELECT `id`, `name`, `cost` FROM `dish` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def get_dish_info(self, dish_name):
        sql = "SELECT `id`, `name`, `cost` FROM `dish` WHERE (`usr_id`='%s') and (`dish`.`name` = '%s');"%(self._usr_id, dish_name)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchone()
        return self.usr_table
    
    def add_dish(self, dish_name, cost):
        sql = """CALL `rms_site`.`add_dish`
                 ('%s', '%s', '%s');"""%(self._usr_id, dish_name, cost)
        self.cursor.execute(sql)
        self.db.commit()
    
    def rm_dish(self, dish_id):
        sql = "DELETE FROM `dish` WHERE (`usr_id`='%s') and (`id`='%s');"%(self._usr_id, dish_id)
        self.cursor.execute(sql)
        self.db.commit()




class Clients(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_table(self):
        sql = "SELECT `id`, `name`, `phone` FROM `client` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def get_client_info(self, client_data):
        if type(client_data) is str:
            sql = """SELECT `id`, `name`, `phone` 
            FROM `client` WHERE (`usr_id`='%s') and (`client`.`phone` = '%s');"""%(self._usr_id, client_data)
        else:
            sql = """SELECT `id`, `name`, `phone` 
            FROM `client` WHERE (`usr_id`='%s') and (`client`.`id` = '%s');"""%(self._usr_id, client_data)
        self.cursor.execute(sql)
        info = self.cursor.fetchone()
        return info
    
    def add_client(self, client_name, phone):
        sql = """CALL `rms_site`.`add_client_in`
                 ('%s', '%s', '%s');"""%(self._usr_id, client_name, phone)
        self.cursor.execute(sql)
        self.db.commit()

    
    def rm_client(self, client_id):
        sql = "DELETE FROM `client` WHERE (`usr_id`='%s') and (`id`='%s');"%(self._usr_id, client_id)
        self.cursor.execute(sql)
        self.db.commit()



class Reservations(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_table(self):
        sql = "SELECT `id`, `table_id`, `client_id`, `time_from`, `time_to`, `cli_arrived` FROM `reservation` WHERE `usr_id`='%s' ORDER BY `time_from` DESC;"%(self._usr_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def get_table_size(self):
        sql = "SELECT Count(*) FROM `reservation` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.size = self.cursor.fetchall()
        return self.size[0][0]
    
    def add_reservation(self, client_name, client_phone, pers_count, time_from, time_to):
        try:
            sql = """CALL `rms_site`.`create_reservation`
                    ('%s', '%s', '%s', '%s', '%s', '%s');"""%(self._usr_id, client_name, client_phone, pers_count, time_from, time_to)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            return 'Smth went wrong'

    def rm_reservation(self, r_id):
        # sql = """CALL `rms_site`.`rm_reservation`
        #          ('%s', '%s', '%s', '%s', '%s', '%s');"""%(self._usr_id, client_name, client_phone, pers_count, time_from, time_to)
        sql= "CALL `rms_site`.`delete_reservation`('%s', '%s')"%(self._usr_id, r_id)
        self.cursor.execute(sql)
        self.db.commit()



class Tables(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_table(self):
        sql = "SELECT `id`, `pers_count` FROM `table` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def get_table_size(self):
        sql = "SELECT Count(*) FROM `table` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.size = self.cursor.fetchall()
        return self.size[0][0]
    
    def get_table_info(self, client_phone):
        sql = """SELECT `id`, `pers_count` 
        FROM `table` WHERE (`usr_id`='%s');"""%(self._usr_id, client_phone)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchone()
        return self.usr_table
    
    def add_table(self, pers_count):
        if is_number(pers_count) is not False:
            sql = """INSERT INTO `table`(usr_id, pers_count)
                        VALUES ('%s', '%s');"""%(self._usr_id, pers_count)
            self.cursor.execute(sql)
            self.db.commit()
            return 'Success'
        else:
            return 'Not a valid input'
    
    def rm_table(self, tbl_id):
        if is_number(tbl_id) is not False:
            sql = """CALL `rms_site`.`rm_tbl`
                 ('%s', '%s');"""%(self._usr_id, tbl_id)
            self.cursor.execute(sql)
            self.db.commit()
            return 'Success'
        else:
            return 'Not a valid input'


class Orders(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_table(self):
        sql = "SELECT `id`, `reservation_id`, `price`, `order_time`, `payment_time` FROM `order` WHERE `usr_id`='%s' ORDER BY `order_time` DESC LIMIT 20;"%(self._usr_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def get_table_size(self):
        sql = "SELECT Count(*) FROM `order` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.size = self.cursor.fetchall()
        return self.size[0][0]
    
    def add_order(self, reservation_id, price, order_time, payment_time):
        try:
            if reservation_id is not None:
                sql = """CALL `rms_site`.`add_order`
                        ('%s', '%s', '%s', '%s', '%s');"""%(self._usr_id, reservation_id, price, order_time, payment_time)
            else:
                sql = """CALL `rms_site`.`add_order_not_reserved`
                        ('%s', '%s', '%s', '%s');"""%(self._usr_id, price, order_time, payment_time)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            return 'Smth went wrong'


class Order_Item(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_items_for_order(self, order_id):
        sql = "SELECT `dish_id`, `amount` FROM `order_item` WHERE (`usr_id`='%s' AND `order_id`='%s');"%(self._usr_id, order_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def add_order_item(self, order_id, dish_id, amount):
        try:
            sql = """CALL `rms_site`.`add_order_item`
                    ('%s', '%s', '%s', '%s');"""%(self._usr_id, order_id, dish_id, amount)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            return 'Smth went wrong'
    
    def rm_order_item(self, order_id, dish_id):
        try:
            sql = """CALL `rms_site`.`remove_order_item`
                    ('%s', '%s', '%s');"""%(self._usr_id, order_id, dish_id)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            return 'Smth went wrong'


class Sales(Access_db):
    def __init__(self, usr_id):
        self._usr_id = usr_id
        Access_db.__init__(self)
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def get_table(self):
        sql = "SELECT `id`, `order_id`, `payment_time`, `price` FROM `sales_log` WHERE `usr_id`='%s' ORDER BY `payment_time` DESC;"%(self._usr_id)
        self.cursor.execute(sql)
        self.usr_table = self.cursor.fetchall()
        return self.usr_table
    
    def get_table_size(self):
        sql = "SELECT Count(*) FROM `sales_log` WHERE `usr_id`='%s';"%(self._usr_id)
        self.cursor.execute(sql)
        self.size = self.cursor.fetchall()
        return self.size[0][0]
    
    def get_income(self):
        sql="select rms_site.income_total('%s');"%(self._usr_id)
        self.cursor.execute(sql)
        income = self.cursor.fetchall()
        return income[0][0]



if __name__ == "__main__":
    # test = Orders(1)
    # print(test.get_table())
    # test.add_order(11, 56, '2019-12-13 09:04', '2019-12-13 10:16')
    # print(test.get_table_size())

    # test1= Order_Item(1)
    # test1.add_order_item(1, 2, 1)
    # print(test1.get_items_for_order(1))
    # print(test.get_table_size())

    test2 = Sales(1)
    print(test2.get_income())
