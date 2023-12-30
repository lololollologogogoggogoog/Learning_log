import sqlite3
from django.http import Http404


class Protection:
    __slots__ = 'request', 'user_ip'

    def __init__(self, request=0, user_ip='127.0.0.1'):
        self.request = request
        self.user_ip = user_ip

    def table_set(self):
        conn = sqlite3.connect('users.sqlite3')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT exists users ('
                    'ip text PRIMARY KEY,'
                    'warms int,'
                    'ban int DEFAULT 0)')

    def insert(self):
        try:
            conn = sqlite3.connect('users.sqlite3')
            cur = conn.cursor()
            cur.execute('INSERT INTO users VALUES(?, 0, 0)', (self.user_ip,))
            conn.commit()
        except sqlite3.Error:
            pass

    def select_warms(self):
        conn = sqlite3.connect('users.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT warms FROM users WHERE ip=?', (self.user_ip,))
        data = cur.fetchone()
        conn.close()

        if data:
            return data[0]
        else:
            return 0

    def update_warms(self):
        conn = sqlite3.connect('users.sqlite3')
        cur = conn.cursor()
        amount_warms = self.select_warms()
        new_warm = amount_warms + 1
        cur.execute('UPDATE users SET warms=? WHERE ip=?', (
            new_warm,
            self.user_ip))
        conn.commit()
        conn.close()
        if new_warm > 2:
            self.ban_user()

    def ban_user(self):
        conn = sqlite3.connect('users.sqlite3')
        cur = conn.cursor()
        cur.execute('UPDATE users SET ban=1 WHERE ip=?',
                    (self.user_ip,))
        conn.commit()
        conn.close()

    def select_ban_ip(self):
        conn = sqlite3.connect('users.sqlite3')
        cur = conn.cursor()
        cur.execute('SELECT ip FROM users WHERE ban=1')
        data = cur.fetchone()
        conn.commit()
        conn.close()

        if data:
            print(data)
            return data
        else:
            return '0'

    def setup(self):
        self.table_set()
        self.insert()
        self.update_warms()
        self.select_ban_ip()


protection = Protection()
protection.setup()
