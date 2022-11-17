import json
import os
import pymysql


conn = pymysql.connect(
	host="localhost",
	user="root",
	passwd="",
	database="klinik"
)

def select(query, values, conn=conn):
	mycursor = conn.cursor()
	mycursor.execute(query, values)
	row_headers = [x[0] for x in mycursor.description]
	myresult = mycursor.fetchall()
	json_data = []
	for result in myresult:
		json_data.append(dict(zip(row_headers, result)))
	return json_data

def insert(query, val, conn=conn):
	mycursor = conn.cursor()
	mycursor.execute(query,val)
	conn.commit()