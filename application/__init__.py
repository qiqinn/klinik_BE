from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from application.database import select, insert
import pymysql
import datetime
import hashlib

# Import Blueprint
from .siswa.controllers import siswa
from .pelanggan.controllers import pelanggan

# Membuat server Flask
app = Flask(__name__)

# Config JWT
app.config['SECRET_KEY'] 							= "ini_secret_key"
app.config['JWT_HEADER_TYPE']						= "JWT"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] 				= datetime.timedelta(days=1) #1 hari token JWT expired
jwt = JWTManager(app)


@app.route('/')
@app.route('/index')
def index():
	return "Hello, World!"


@app.route("/login", methods=["POST"])
def login():
	ROUTE_NAME = request.path

	data = request.json

	username = data["username_pelanggan"]
	password = data["password_pelanggan"]

	username = username.lower()
	password_enc = hashlib.md5(password.encode('utf-8')).hexdigest() # Convert password to md5

	# Cek kredensial didalam database
	query = " SELECT * FROM pelanggan WHERE username_pelanggan = %s AND password_pelanggan =  %s"
	values = (username, password_enc)

	data_user = select(query, values)
	print(data_user)
	print(type(data_user))

	if len(data_user) == 0:
		return make_response(jsonify(deskripsi="Username  dan passaword salah"), 401)

	data_user	= data_user[0]
	print(data_user)

	db_id_user 	= data_user["id_pelanggan"]
	db_username = data_user["username_pelanggan"]
	# db_role		= data_user["role"]

	# if password_enc != db_password:
	# 	return make_response(jsonify(deskripsi="Password salah"), 401)

	jwt_payload = {
		"id_user" : db_id_user,
		"role" : db_username
	}

	access_token = create_access_token(username, additional_claims=jwt_payload)

	return jsonify(access_token=access_token)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Awwww, Halaman Tidak Ditemukan','status_code':404}), 404)

@app.errorhandler(500)
def not_found(error):
	return make_response(jsonify({'error': 'Yaah, Servernya Error','status_code':500}), 500)

#register blueprint
app.register_blueprint(siswa, url_prefix='/siswa')
app.register_blueprint(pelanggan, url_prefix='/pelanggan')
