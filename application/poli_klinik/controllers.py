from flask import Flask, request, jsonify, make_response, Blueprint
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
import pymysql
import datetime
import hashlib
from application.database import select, insert


poli_klinik = Blueprint('poli_klinik', __name__, static_folder = '../../upload/poli_klinik', static_url_path="/media")



@poli_klinik.route('/get', methods=['GET'])
# @jwt_required()
def get_data_poli_klinik():
	query = "SELECT * FROM poli_klinik WHERE 1=1"
	values = ()

	id_poli_klinik = request.args.get("id_poli")
	nama_poli = request.args.get("nama_poli")

	if id_poli_klinik:
		query += " AND id_poli=%s "
		values += (id_poli_klinik,)
	if nama_poli:
		query += " AND nama_poli LIKE %s " 
		values += ("%"+nama_poli+"%", )
	

	json_data = select(query,values)
	return make_response(jsonify(json_data),200)


@poli_klinik.route('/sign_up', methods=['POST'])
@jwt_required()
def insert_sign_up_klinik():
    # validasi admin 
	username = str(get_jwt()["username"])
	role = str(get_jwt()["role"])
	if role != "0":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)
		
	hasil = {"status": "gagal daftar poli_klinik"}

	try:
		query_temp = "SELECT * FROM pelanggan WHERE username_pelanggan=%s"
		values_temp = (username )
		data_temp = select(query_temp, values_temp)
		print(data_temp[0])
		data =  data_temp[0]

		query = """INSERT INTO poli_klinik(
											id_pelanggan,
											nama_pelanggan,
											usia,
											alamat,
											status
																					) 
						VALUES(%s,%s,%s,%s,%s)"""

		

		values = (	data["id_pelanggan"],  data["nama_pelanggan"] ,data["usia"], data["alamat"],"masuk antrian")
		insert(query,values)
		hasil = {"status": "berhasil mendaftar poli_klinik"}

	except Exception as e:
		err = str(e)
		print((err))

	return jsonify(hasil)


@poli_klinik.route('/update_data_poli_klinik', methods=['PUT'])
@jwt_required()
def update_data_poli_klinik():
    
	
	hasil = {"status": "gagal update data poli_klinik"}
	
	try:
		data = request.json
		id_poli_klinik_awal = data["id_poli_klinik_awal"]

		query = "UPDATE tb_poli_klinik SET id_poli_klinik = %s "
		values = (id_poli_klinik_awal, )

		if "id_poli_klinik_ubah" in data:
			query += ", id_poli_klinik = %s"
			values += (data["id_poli_klinik_ubah"], )
		if "nama" in data:
			query += ", nama = %s"
			values += (data["nama"], )
		if "umur" in data:
			query += ", umur = %s"
			values += (data["umur"], )
		if "alamat" in data:
			query += ", alamat = %s"
			values += (data["alamat"], )

		query += " WHERE id_poli_klinik = %s"
		values += (id_poli_klinik_awal, )

		insert(query,values)
		hasil = {"status": "berhasil update data poli_klinik"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@poli_klinik.route('/delete_data_poli_klinik/<id_poli_klinik>', methods=['DELETE'])
@jwt_required()
def delete_data_poli_klinik(id_poli_klinik):
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal hapus data poli_klinik"}
	
	try:
		query = "DELETE FROM tb_poli_klinik WHERE id_poli_klinik=%s"
		values = (id_poli_klinik,)
		insert(query,values)
		hasil = {"status": "berhasil hapus data poli_klinik"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)
