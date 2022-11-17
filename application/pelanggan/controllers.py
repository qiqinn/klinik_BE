from flask import Flask, request, jsonify, make_response, Blueprint
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
import pymysql
import datetime
import hashlib
from application.database import select, insert


pelanggan = Blueprint('pelanggan', __name__, static_folder = '../../upload/pelanggan', static_url_path="/media")

# # Flask JWT Extended Configuration
# pelanggan.config['SECRET_KEY'] 							= "INI_SECRET_KEY"
# pelanggan.config['JWT_HEADER_TYPE']						= "JWT"
# pelanggan.config['JWT_ACCESS_TOKEN_EXPIRES'] 				= datetime.timedelta(days=1) #1 hari token JWT expired
# jwt = JWTManager(pelanggan)




# @pelanggan.route('/get_data_pelanggan', methods=['GET'])
# # @jwt_required()
# def get_data_pelanggan():
# 	query = "SELECT * FROM pelanggan WHERE 1=1"
# 	values = ()

# 	id_pelanggan = request.args.get("id_pelanggan")
# 	nama = request.args.get("nama")
# 	umur = request.args.get("umur")

# 	if id_pelanggan:
# 		query += " AND id_pelanggan=%s "
# 		values += (id_pelanggan,)
# 	if nama:
# 		query += " AND nama LIKE %s " 
# 		values += ("%"+nama+"%", )
# 	if umur:
# 		query += " AND umur=%s "
# 		values += (umur,)

# 	json_data = select(query,values)
# 	return make_response(jsonify(json_data),200)

@pelanggan.route('/register', methods=['POST'])
def insert_data_pelanggan():

	hasil = {"status": "gagal insert data siswa"}
	try:
		data = request.json
		print(data)


		# query_temp = "SELECT id_pelanggan FROM pelanggan WHERE id_pelanggan=%s"
		# values_temp = (data["id_pelanggan"], )
		# data_temp = select(query_temp, values_temp)

		# if len(data_temp) != 0:
		# 	hasil = {
		# 		"status": "gagal insert data pelanggan",
		# 		"deskripsi" : "Sudah ada id didalam DB"
		# 	}
		# 	return make_response(jsonify(hasil), 400)

		query = """INSERT INTO pelanggan(
											username_pelanggan,
											password_pelanggan,
											nama_pelanggan,
											email,
											no_hp,
											alamat,
											jenis_kelamin,
											usia,
											gol_darah,
											tinggi_badan,
											berat_badan
										) 
						VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

		password = data["password_pelanggan"]
		password_enc = hashlib.md5(password.encode('utf-8')).hexdigest()

		values = (	data["username_pelanggan"],  password_enc ,data["nama_pelanggan"],
					data["email"], data["no_hp"],data["alamat"], data["jenis_kelamin"], data["usia"], 
					data["gol_darah"], data["tinggi_badan"], data["berat_badan"])
		insert(query,values)
		hasil = {"status": "berhasil insert data pelanggan"}

	except Exception as e:
		err = str(e)
		if '1062' in err:
			hasil = "username sudah ada"
			return jsonify(hasil)
		print((err))

	return jsonify(hasil)
# @pelanggan.route("/login", methods=["POST"])
# def login():
# 	data = request.json

# 	username = data["username_pelanggan"]
# 	password = data["password_pelanggan"]

# 	username = username.lower()
# 	password_enc = hashlib.md5(password.encode('utf-8')).hexdigest() # Convert password to md5

# 	# Cek kredensial didalam database
# 	query = " SELECT id_pelaggan, password, role FROM pelanggan WHERE username_pelanggan = %s "
# 	values = (username, )

# 	data_user = select(query, values)
# 	print(data_user)

# 	# if len(data_user) == 0:
# 	# 	return make_response(jsonify(deskripsi="Username tidak ditemukan"), 401)

# 	# data_user	= data_user[0]

# 	# db_id_user 	= data_user[0]
# 	# db_password = data_user[1]
# 	# db_role		= data_user[2]

# 	# if password_enc != db_password:
# 	# 	return make_response(jsonify(deskripsi="Password salah"), 401)

# 	jwt_payload = {
# 		"id_user" : "Halo",
# 		"role" : "db_role"
# 	}

# 	access_token = create_access_token(username, additional_claims=jwt_payload)

# 	return jsonify(access_token=access_token)

@pelanggan.route('/update_data_pelanggan', methods=['PUT'])
@jwt_required()
def update_data_pelanggan():
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal update data pelanggan"}
	
	try:
		data = request.json
		id_pelanggan_awal = data["id_pelanggan_awal"]

		query = "UPDATE tb_pelanggan SET id_pelanggan = %s "
		values = (id_pelanggan_awal, )

		if "id_pelanggan_ubah" in data:
			query += ", id_pelanggan = %s"
			values += (data["id_pelanggan_ubah"], )
		if "nama" in data:
			query += ", nama = %s"
			values += (data["nama"], )
		if "umur" in data:
			query += ", umur = %s"
			values += (data["umur"], )
		if "alamat" in data:
			query += ", alamat = %s"
			values += (data["alamat"], )

		query += " WHERE id_pelanggan = %s"
		values += (id_pelanggan_awal, )

		insert(query,values)
		hasil = {"status": "berhasil update data pelanggan"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@pelanggan.route('/delete_data_pelanggan/<id_pelanggan>', methods=['DELETE'])
@jwt_required()
def delete_data_pelanggan(id_pelanggan):
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal hapus data pelanggan"}
	
	try:
		query = "DELETE FROM tb_pelanggan WHERE id_pelanggan=%s"
		values = (id_pelanggan,)
		insert(query,values)
		hasil = {"status": "berhasil hapus data pelanggan"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)
