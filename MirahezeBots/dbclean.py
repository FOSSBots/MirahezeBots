import sqlite3


def main():
    file = input("Full path to the deletion list: ")
    with open(file, 'r') as f: # ensure the file is open and closed properly
        users = f.readlines()
    database = input("Full path to database: ")
    with sqlite3.connect(database) as conn:
        curs = conn.cursor()
        for user in users:
            curs.execute('DELETE FROM nick_values WHERE nick_id = ?', (user,))
            curs.execute('DELETE FROM nicknames WHERE nick_id = ?', (user,))
            curs.execute('DELETE FROM nick_ids WHERE nick_id = ?', (user,))
        conn.commit()
main()
