import pymysql.cursors

from app_setting import DB_CONNECTION_DICT
from .hasher import salt_txt, encrypt, decrypt


class DB(object):
    def __init__(self, private_key, public_key):

        self.conn = pymysql.connect(**DB_CONNECTION_DICT)

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
        else:
            count = 0
        return salted, count

    # this is not thread safe
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

    def get_top_100(self):
        result = []
        self.cursor.execute('''
        select * from data order by count desc
        ''')
        for item in self.cursor.fetchall():
            result.append((decrypt(item[1], self.private_key, self.public_key), item[2]))
        return result
