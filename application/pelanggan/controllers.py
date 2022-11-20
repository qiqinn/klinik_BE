from flask import Flask, request, jsonify, make_response, Blueprint
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
import pymysql
import datetime
import hashlib
from application.database import select, insert


pelanggan = Blueprint('pelanggan', __name__, static_folder = '../../upload/pelanggan', static_url_path="/media")


@pelanggan.route('/get', methods=['GET'])
@jwt_required()
def get_data_pelanggan():
    # validasi admin 
	username = str(get_jwt()["username"])
	role = str(get_jwt()["role"])
	if role != "1":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)
	
    
	query = "SELECT * FROM pelanggan WHERE 1=1"
	values = ()

	id_pelanggan = request.args.get("id_pelanggan")
	nama = request.args.get("nama_pelanggan")
	umur = request.args.get("usia")

	if id_pelanggan:
		query += " AND id_pelanggan =%s "
		values += (id_pelanggan,)
	if nama:
		query += " AND nama_pelanggan LIKE %s " 
		values += ("%"+nama+"%", )
	if umur:
		query += " AND usia=%s "
		values += (umur,)

	json_data = select(query,values)
	return make_response(jsonify(json_data),200)

@pelanggan.route('/register', methods=['POST'])
def register_pelanggan():

	hasil = {"status": "gagal register"}
	try:
		data = request.json
		print(data)

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
											berat_badan,
											role
										) 
						VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

		password = data["password_pelanggan"]
		password_enc = hashlib.md5(password.encode('utf-8')).hexdigest()


		values = (	data["username_pelanggan"],  password_enc ,data["nama_pelanggan"],
					data["email"], data["no_hp"],data["alamat"], data["jenis_kelamin"], data["usia"], 
					data["gol_darah"], data["tinggi_badan"], data["berat_badan"], 0)
		insert(query,values)
		hasil = {"status": "berhasil insert data pelanggan"}

	except Exception as e:
		err = str(e)
		if '1062' in err:
			hasil = {"status" : "username sudah ada"}
			return jsonify(hasil)
		print((err))

	return jsonify(hasil)


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
