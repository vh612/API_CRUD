#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# appMySQL.py
#######################

import os
import pymysql

from flaskext.mysql import MySQL

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug import check_password_hash

DB_name = os.environ['HOME'].split("/")[-1]
DB_user = DB_name

app = Flask(__name__)

mysql = MySQL()
 
# MySQL configurations

app.config['MYSQL_DATABASE_USER'] = DB_user
app.config['MYSQL_DATABASE_PASSWORD'] = 'fitlab'
app.config['MYSQL_DATABASE_DB'] = DB_name
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/add', methods=['POST'])

def add_user():

	try:
		_json = request.json
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']

		# validate the received values
		if _name and _email and _password and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "INSERT INTO " + DB_name + "(user_name, user_email, user_password) VALUES(%s, %s, %s)"
			data = (_name, _email, _hashed_password,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM " + DB_name)
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM " + DB_name + "WHERE user_id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['POST'])

def update_user():

	try:
		_json = request.json
		_id = _json['id']
		_name = _json['name']
		_email = _json['email']
		_password = _json['pwd']

		# validate the received values
		if _name and _email and _password and _id and request.method == 'POST':
			#do not save password as a plain text
			_hashed_password = generate_password_hash(_password)
			# save edits
			sql = "UPDATE " + DB_name + " SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
			data = (_name, _email, _hashed_password, _id,)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM " + DB_name + " WHERE user_id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == '__main__':

    homeDir = os.environ['HOME']
    userID = homeDir.split("/")[-1]

    if userID[2] == "6":
        port = "2" + userID[3:7]
    if userID[2] == "7":
        port = "3" + userID[3:7]

    print("Personal API Port: %s" %(port))

    app.run(port=int(port),host='0.0.0.0',use_reloader=False)
