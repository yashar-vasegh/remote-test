import pymysql.cursors
import os

from .hasher import salt_txt, encrypt, decrypt
from app_setting import db_host, db_name, db_pass, db_user

class DB(object):
    def __init__(self, private_key, public_key):
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
            CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
            CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
            cloudsql_unix_socket = os.path.join('/cloudsql', CLOUDSQL_CONNECTION_NAME)

            self.conn = pymysql.connect(
                unix_socket=cloudsql_unix_socket,
                user=CLOUDSQL_USER,
                passwd=CLOUDSQL_PASSWORD)
        else:
            self.conn=pymysql.connect(host=db_host,
                              user=db_user,
                              passwd=db_pass,
                              db=db_name)

        self.private_key = private_key
        self.public_key = public_key
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def get_word(self, word):
        salted = salt_txt(word)
        self.cursor.execute('''
            select count from data where id = %s
        ''', (salted,))

        count = self.cursor.fetchone()
        if count:
            count = count[0]
        else: count = 0
        return salted, count

    def update_db_word(self, word, count_added):
        salted, count = self.get_word(word)
        if count:
            count += count_added
            self.cursor.execute(''' update data set count = %s where id= %s ''', (count, salted))
        else:
            self.cursor.execute(''' insert into data (id, word, count) 
                                    values (%s, %s , %s)''', (salted,
                                                              encrypt(word, self.private_key, self.public_key, cypher='AES'),
                                                              count_added))
            count = count_added


        self.cursor.close()
        return count

    def get_hash_word(self, hash):
        word = decrypt(hash, self.private_key, self.public_key, cypher='AES')
        self.cursor.execute('''
            select count from data where id = %s
        ''', (hash,))

        count = self.cursor.fetchone()
        if count:
            count = count[0]
        else: count = 0
        return word, count

    def get_top_100(self):
        result = []
        self.cursor.execute('''
        select * from data order by count desc
        ''')
        for item in self.cursor.fetchall():
            result.append((decrypt(item[1], self.private_key, self.public_key), item[2]))
        return result


