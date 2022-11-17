from flask import Flask, request, jsonify, make_response, Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from application.database import select, insert

siswa = Blueprint('siswa', __name__, static_folder = '../../upload/siswa', static_url_path="/media")

@siswa.route('/get_data_siswa', methods=['GET'])
# @jwt_required()
def get_data_siswa():
	query = "SELECT * FROM tb_siswa WHERE 1=1"
	values = ()

	nis = request.args.get("nis")
	nama = request.args.get("nama")
	umur = request.args.get("umur")

	if nis:
		query += " AND nis=%s "
		values += (nis,)
	if nama:
		query += " AND nama LIKE %s " 
		values += ("%"+nama+"%", )
	if umur:
		query += " AND umur=%s "
		values += (umur,)

	json_data = select(query,values)
	return make_response(jsonify(json_data),200)

@siswa.route('/insert_data_siswa', methods=['POST'])
@jwt_required()
def insert_data_siswa():
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])


	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)
	hasil = {"status": "gagal insert data siswa"}
	
	try:
		data = request.json

		query_temp = "SELECT nis FROM tb_siswa WHERE nis=%s"
		values_temp = (data["nis"], )
		data_temp = select(query_temp, values_temp)

		if len(data_temp) != 0:
			hasil = {
				"status": "gagal insert data siswa",
				"deskripsi" : "Sudah ada NIS didalam DB"
			}
			return make_response(jsonify(hasil), 400)

		query = "INSERT INTO tb_siswa(nis, nama, umur, alamat) VALUES(%s,%s,%s,%s)"
		values = (data["nis"], data["nama"], data["umur"], data["alamat"],)
		insert(query,values)
		hasil = {"status": "berhasil insert data siswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@siswa.route('/update_data_siswa', methods=['PUT'])
@jwt_required()
def update_data_siswa():
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal update data siswa"}
	
	try:
		data = request.json
		nis_awal = data["nis_awal"]

		query = "UPDATE tb_siswa SET nis = %s "
		values = (nis_awal, )

		if "nis_ubah" in data:
			query += ", nis = %s"
			values += (data["nis_ubah"], )
		if "nama" in data:
			query += ", nama = %s"
			values += (data["nama"], )
		if "umur" in data:
			query += ", umur = %s"
			values += (data["umur"], )
		if "alamat" in data:
			query += ", alamat = %s"
			values += (data["alamat"], )

		query += " WHERE nis = %s"
		values += (nis_awal, )

		insert(query,values)
		hasil = {"status": "berhasil update data siswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@siswa.route('/delete_data_siswa/<nis>', methods=['DELETE'])
@jwt_required()
def delete_data_siswa(nis):
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal hapus data siswa"}
	
	try:
		query = "DELETE FROM tb_siswa WHERE nis=%s"
		values = (nis,)
		insert(query,values)
		hasil = {"status": "berhasil hapus data siswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)
