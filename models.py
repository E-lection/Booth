import sqlite3 as sql

def insertUser(username, password, station_id, vote_url, public_key):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password,station_id,vote_url,public_key) VALUES (?,?,?,?,?)", (username,password,station_id,vote_url,public_key))
    con.commit()
    con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT id, username, password, station_id, vote_url, public_key FROM users")
	users = cur.fetchall()
	con.close()
	return users

def deleteUser(username):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE username=\'" + username + "\'")
    con.close()
    return
