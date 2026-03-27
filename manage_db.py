from models import DatabaseSubreddits, SuperUserDatabase

DATABASE_U = SuperUserDatabase('database')
DATABASE_S = DatabaseSubreddits('database')

DATABASE_U.add_record('hokadva', '687994915')

DATABASE_U.close()