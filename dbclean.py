file = input("Full path to the deletion list: ")
users = []
userfile = open(file, 'r')
for line in userfile:
  users.append(line)
databse = input("Full path to database: ")
with sqlite3.connect(database) as conn: 
  with conn.cursor() as curs:
    for user in users:
      curs.execute('DELETE FROM nick_values WHERE nick_id = ?', user)
      curs.execute('DELETE FROM nicknames WHERE nick_id = ?', user)
      curs.execute('DELETE FROM nick_ids WHERE nick_id = ?', user)
  conn.commit()
