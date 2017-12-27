import pymysql

#Writes the query to the database
def write_to_db(query):
	#Establish a connection to the database
	db = pymysql.connect(host='localhost', port=8889,user='root',password='root',db='tennisapp',cursorclass=pymysql.cursors.DictCursor)
	db.autocommit(True) #Will automatically update the database when written to
	#Write to the database
	cur = db.cursor()
	cur.execute(query)
	#Cleanup
	cur.close()
	db.close()

#Reads the query from the database
def read_from_db(query):
	db = pymysql.connect(host='localhost', port=8889,user='root',password='root',db='tennisapp',cursorclass=pymysql.cursors.DictCursor)
	db.autocommit(True)
	cur = db.cursor()
	cur.execute(query)
	results = cur.fetchall()
	cur.close()
	db.close()
	return results