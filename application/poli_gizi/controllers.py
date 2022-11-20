from flask import Flask, request, jsonify, make_response, Blueprint
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
import pymysql
import datetime
import hashlib
from application.database import select, insert


poli_gizi = Blueprint('poli_gizi', __name__, static_folder = '../../upload/poli_gizi', static_url_path="/media")



@poli_gizi.route('/get_antrian', methods=['GET'])
# @jwt_required()
def get_data_poli_gizi():
	query = "SELECT * FROM poli_gizi WHERE 1=1"
	values = ()

	id_antrian = request.args.get("id_antrian")
	nama = request.args.get("nama_pelanggan")
	waktu = request.args.get("timestamp")
	status = request.args.get("status") 

	if id_antrian:
		query += " AND id_antrian=%s "
		values += (id_antrian,)
	if nama:
		query += " AND nama LIKE %s " 
		values += ("%"+nama+"%", )
	if waktu:
		query += " AND timestamp LIKE %s " 
		values += ("%"+waktu+"%", )
	if status:
		query += " AND status LIKE %s " 
		values += ("%"+status+"%", )
	

	json_data = select(query,values)
	return make_response(jsonify(json_data),200)


@poli_gizi.route('/sign_up', methods=['POST'])
@jwt_required()
def insert_sign_up_gizi():
    # validasi admin 
	username = str(get_jwt()["username"])
	role = str(get_jwt()["role"])
	if role != "0":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)
		
	hasil = {"status": "gagal daftar poli_gizi"}

	try:
		query_temp = "SELECT * FROM pelanggan WHERE username_pelanggan=%s"
		values_temp = (username )
		data_temp = select(query_temp, values_temp)
		print(data_temp[0])
		data =  data_temp[0]

		query = """INSERT INTO poli_gizi(
											id_pelanggan,
											nama_pelanggan,
											usia,
											alamat,
											status
																					) 
						VALUES(%s,%s,%s,%s,%s)"""

		

		values = (	data["id_pelanggan"],  data["nama_pelanggan"] ,data["usia"], data["alamat"],"masuk antrian")
		insert(query,values)
		hasil = {"status": "berhasil mendaftar poli_gizi"}

	except Exception as e:
		err = str(e)
		print((err))

	return jsonify(hasil)


@poli_gizi.route('/update_data_poli_gizi', methods=['PUT'])
@jwt_required()
def update_data_poli_gizi():
    
	
	hasil = {"status": "gagal update data poli_gizi"}
	
	try:
		data = request.json
		id_poli_gizi_awal = data["id_poli_gizi_awal"]

		query = "UPDATE tb_poli_gizi SET id_poli_gizi = %s "
		values = (id_poli_gizi_awal, )

		if "id_poli_gizi_ubah" in data:
			query += ", id_poli_gizi = %s"
			values += (data["id_poli_gizi_ubah"], )
		if "nama" in data:
			query += ", nama = %s"
			values += (data["nama"], )
		if "umur" in data:
			query += ", umur = %s"
			values += (data["umur"], )
		if "alamat" in data:
			query += ", alamat = %s"
			values += (data["alamat"], )

		query += " WHERE id_poli_gizi = %s"
		values += (id_poli_gizi_awal, )

		insert(query,values)
		hasil = {"status": "berhasil update data poli_gizi"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@poli_gizi.route('/delete_data_poli_gizi/<id_poli_gizi>', methods=['DELETE'])
@jwt_required()
def delete_data_poli_gizi(id_poli_gizi):
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal hapus data poli_gizi"}
	
	try:
		query = "DELETE FROM tb_poli_gizi WHERE id_poli_gizi=%s"
		values = (id_poli_gizi,)
		insert(query,values)
		hasil = {"status": "berhasil hapus data poli_gizi"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)
