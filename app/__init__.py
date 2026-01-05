from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
from config import Config
import os

# Inisialisasi Ekstensi (kosong dulu)
mysql = MySQL()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Pastikan folder upload ada
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Hubungkan Ekstensi ke App
    mysql.init_app(app)
    socketio.init_app(app)

    # Daftarkan Blueprints (Rute yang dipisah-pisah)
    from app.auth.routes import auth
    from app.main.routes import main
    
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app