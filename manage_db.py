from data_base_manage import Database


DATABASE = Database('subreddits')

while True:
    new_value = input()
    if new_value == 'q':
        break
    DATABASE.add_record(new_value)

DATABASE.close()