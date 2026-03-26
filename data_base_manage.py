import sqlite3


class Database():
    def __init__(self, database):
        self.con = sqlite3.connect(f'{database}.db')
        self.cur = self.con.cursor()
        self.main_table = 'pars_subreddits'
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.main_table} (
                         id INTEGER PRIMARY KEY,
                         name_subreddit VARCHAR(50) 
                         CHECK(LENGTH(name_subreddit) <= 50) UNIQUE
                         )
            ''')


    def add_record(self, record):
        self.cur.execute(f'''
                INSERT INTO {self.main_table} (name_subreddit) VALUES (?)
            ''',(record,)
            )
        self.con.commit()


    def close(self):
        self.con.close()


    def remove_record(self, id):
        self.cur.execute(f'''
                DELETE FROM {self.main_table} WHERE id = (?)
            ''', (id,))
        self.con.commit()


    def print_database(self):
        self.cur.execute(
            f'SELECT name_subreddit FROM {self.main_table}'
        )
        return self.processing(self.cur.fetchall())


    def processing(self, lst):
        new_lst = []
        for cursor in lst:
            new_lst.append(cursor[0])

        return new_lst


    def random_print(self):
        self.cur.execute(
            f'''SELECT name_subreddit FROM {self.main_table} 
            ORDER BY RANDOM() LIMIT 1'''
        )
        return self.processing(self.cur.fetchall())
