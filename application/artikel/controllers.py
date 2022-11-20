from flask import Flask, request, jsonify, make_response, Blueprint
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
import pymysql
import datetime
import hashlib
from application.database import select, insert


artikel = Blueprint('artikel', __name__, static_folder = '../../upload/artikel', static_url_path="/media")

# # Flask JWT Extended Configuration
# artikel.config['SECRET_KEY'] 							= "INI_SECRET_KEY"
# artikel.config['JWT_HEADER_TYPE']						= "JWT"
# artikel.config['JWT_ACCESS_TOKEN_EXPIRES'] 				= datetime.timedelta(days=1) #1 hari token JWT expired
# jwt = JWTManager(artikel)




@artikel.route('/get', methods=['GET'])
# @jwt_required()
def get_data_artikel():
	query = "SELECT * FROM artikel WHERE 1=1"
	values = ()

	id_artikel = request.args.get("id_artikel")
	judul = request.args.get("judul")
	konten = request.args.get("konten")
	tb = request.args.get("thumbnail") 

	if id_artikel:
		query += " AND id_artikel=%s "
		values += (id_artikel,)
	if judul:
		query += " AND judul LIKE %s " 
		values += ("%"+judul+"%", )
	

	json_data = select(query,values)
	return make_response(jsonify(json_data),200)


@artikel.route('/create', methods=['POST'])
@jwt_required()
def insert_data_artikel():
    # validasi admin 
	username = str(get_jwt()["username"])
	role = str(get_jwt()["role"])
	if role != "1":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)
		
	hasil = {"status": "gagal membuat artikel"}

	try:
		data = request.json

		query = """INSERT INTO artikel(
											judul,
											konten,
											penulis,
											thumbnail
																					) 
						VALUES(%s,%s,%s,%s)"""

		

		values = (	data["judul"],  data["konten"] ,username, data["thumbnail"])
		insert(query,values)
		hasil = {"status": "berhasil membuat artikel"}

	except Exception as e:
		err = str(e)
		print((err))

	return jsonify(hasil)


@artikel.route('/update_data_artikel', methods=['PUT'])
@jwt_required()
def update_data_artikel():
    
	
	hasil = {"status": "gagal update data artikel"}
	
	try:
		data = request.json
		id_artikel_awal = data["id_artikel_awal"]

		query = "UPDATE tb_artikel SET id_artikel = %s "
		values = (id_artikel_awal, )

		if "id_artikel_ubah" in data:
			query += ", id_artikel = %s"
			values += (data["id_artikel_ubah"], )
		if "nama" in data:
			query += ", nama = %s"
			values += (data["nama"], )
		if "umur" in data:
			query += ", umur = %s"
			values += (data["umur"], )
		if "alamat" in data:
			query += ", alamat = %s"
			values += (data["alamat"], )

		query += " WHERE id_artikel = %s"
		values += (id_artikel_awal, )

		insert(query,values)
		hasil = {"status": "berhasil update data artikel"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@artikel.route('/delete_data_artikel/<id_artikel>', methods=['DELETE'])
@jwt_required()
def delete_data_artikel(id_artikel):
	id_user = str(get_jwt()["id_user"])
	role = str(get_jwt()["role"])

	if role == "2":
		return make_response(jsonify({'error': 'Akun yang digunakan tidak memiliki akses ke API ini','status_code':403}), 403)

	hasil = {"status": "gagal hapus data artikel"}
	
	try:
		query = "DELETE FROM tb_artikel WHERE id_artikel=%s"
		values = (id_artikel,)
		insert(query,values)
		hasil = {"status": "berhasil hapus data artikel"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)
