import sqlite3


class DatabaseTemplate():
    def __init__(self, database, main_table):
        self.con = sqlite3.connect(f'{database}.db')
        self.cur = self.con.cursor()
        self.main_table = main_table


    def add_record(self, record):
        self.cur.execute(f'''
                INSERT INTO {self.main_table} (name_subreddit) VALUES (?)
            ''',(record,)
            )
        self.con.commit()


    def close(self):
        self.con.close()


class DatabaseSubreddits(DatabaseTemplate):
    def __init__(self, database):
        super().__init__(database, 'pars_subreddits')
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.main_table} (
                        id INTEGER PRIMARY KEY,
                        name_subreddit VARCHAR(50) 
                        CHECK(LENGTH(name_subreddit) <= 50) UNIQUE
                        )
            ''')
        self.con.commit()


    def text_database(self):
        subreddits = self.print_database()
        text = ''
        for item in subreddits:
            text += str(item) + ', '
        if text != '':
            text = text[:-2]
        return text


    def random_print(self):
        self.cur.execute(
            f'''SELECT name_subreddit FROM {self.main_table} 
            ORDER BY RANDOM() LIMIT 1'''
        )
        return self.processing_list(self.cur.fetchall())


    def print_database(self):
        self.cur.execute(
            f'SELECT name_subreddit FROM {self.main_table}'
        )
        return self.processing_list(self.cur.fetchall())


    def remove_record(self, record):
        self.cur.execute(f'''
            DELETE FROM {self.main_table} WHERE name_subreddit = (?)
            ''', (record, ))
        self.con.commit()


    def processing_list(self, lst):
        new_lst = []
        for item in lst:
            new_lst.append(item[0])
        return new_lst


class SuperUserDatabase(DatabaseTemplate):
    def __init__(self, database):
        super().__init__(database, 'superusers')
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.main_table}(
                        id INTEGER PRIMARY KEY,
                        nickname VARCHAR(50)
                        CHECK(LENGTH(nickname) <= 50) UNIQUE,
                        user_id VARCHAR(200)
                        CHECK(LENGTH(user_id) <= 200) UNIQUE
            )
            ''')
        self.con.commit()


    def add_record(self, nickname, user_id):
        self.cur.execute(f'''
                INSERT INTO {self.main_table} (nickname, user_id) VALUES ((?), (?))
            ''',(nickname, user_id)
            )
        self.con.commit()


    def is_admin(self, nickname, user_id):
        self.cur.execute(f'''
            SELECT id FROM {self.main_table}
            WHERE (((?) = nickname) AND ((?) = user_id))
            ''', (nickname, user_id))
        found = self.cur.fetchall()

        if found == []:
            return False
        return True
