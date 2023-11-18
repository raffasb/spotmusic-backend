from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
#from db import get_songs
import os 

import pymysql

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "send_wildcard": "False"}}) # Compliant
csrf = CSRFProtect(app) 



db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_local_host = os.environ.get('DB_LOCAL_HOST')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    try:
        if db_connection_name:
            unix_socket = '/cloudsql/{}'.format(db_connection_name)
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
            print ('tchau')
        else:
            print ('oi')
            conn = pymysql.connect(user=db_user, password=db_password,
                                host=db_local_host, db=db_name,cursorclass=pymysql.cursors.DictCursor)

    except pymysql.MySQLError as e:
        print(e)

    return conn

def get_songs():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM songs;')
        songs = cursor.fetchall()
        if result > 0:
           got_songs = jsonify(songs)

        else:
            got_songs = 'Nenhuma Musica Cadastrada na Playlist'

    conn.close()

    return got_songs


@app.route('/')
def songs():
    return get_songs()

# @app.route("/")
# def pagina_inicial():
#     return "Hello World, this is Rafael Barros from 11ASOO - Hackathon"    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))