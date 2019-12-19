import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
import json

class Access_db:
    def __init__(self, adm_name='b6c63018cf3194'):
        self._adm_name = adm_name
        self.connect_to_db()
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass
    
    def __get_credent(self):
        with open('db_login_info.json') as json_file:
            data = json.load(json_file)
            try:
                return [data[self._adm_name]['password'], data[self._adm_name]['host'], data[self._adm_name]['schema']]
            except KeyError:
                print(f'No {self._adm_name} user')
                return None
    
    def connect_to_db(self):
        password, host, schema = self.__get_credent()
        self.db = pymysql.connect(host=host, user=self._adm_name, password=password, db=schema)

        if self.db is None:
            print("Can't connect to db")
            return None

        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT VERSION()")

        data = self.cursor.fetchone() # Fetch a single row using fetchone() method.
        print ("Database version : %s " % data)




class User(Access_db):
    def __init__(self):
        Access_db.__init__(self)
        self.cursor = self.db.cursor()
    
    def __del__(self):
        try:
            self.db.close()
        except:
            pass
    
    def add_usr(self, email, name, org_name, password):
        password_hash = generate_password_hash(password)
        sql = """
            CALL `rms_site`.`add_user`('%s', '%s', '%s', '%s');
            """%(email, name, org_name, password_hash)
        self.cursor.execute(sql)
        self.db.commit()
    
    def get_usr_id(self, email):
        sql = "SELECT `id` FROM `users` WHERE `e-mail`='%s';"%(email)
        self.cursor.execute(sql)
        return self.cursor.fetchone()[0]
    

    def validate_password(self, email, password):
        sql = "SELECT `id`, `name`, `password-hash` FROM `users` WHERE `e-mail`='%s';"%(email)
        self.cursor.execute(sql)
        self.__usr_data = self.cursor.fetchone()
        try:
            return check_password_hash(self.__usr_data[2], password), self.__usr_data[0], self.__usr_data[1]
        except:
            return False, None, None



if __name__ == "__main__":
    u = User()
    # u.add_usr('test_email@gmail.com', 'John L', 'RKDC', 'qwerty123')
    # print(u.validate_password('dfgd', 'qdfr'))
    # print(u.get_usr_id('test_email@gmail.com'))