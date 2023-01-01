import sqlite3

db = sqlite3.connect('server.db')
sql = db.cursor()

sql.execute('''CREATE TABLE IF NOT EXISTS users (
	ltuid INT,
	ltoken TEXT,
	uid INT
	)''')

db.commit()

user_ltuid = input('Tuid: ')
user_ltoken = input('Token: ')
user_uid = input('UID: ')

sql.execute('SELECT ltuid FROM users')
if sql.fetchone() is None:
	sql.execute(f"INSERT INTO users VALUES (?, ?, ?)", (user_ltuid, user_ltoken, user_uid))
	db.commit()

	print('Данные сохранены!')
else:
	print('Такая запись уже имеется!')
	
	for value in sql.execute("SELECT * FROM users"):
		print(value)