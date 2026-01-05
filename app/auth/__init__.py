from flask import Blueprint

# Ini mendefinisikan variabel 'bp' yang dicari oleh error tadi
bp = Blueprint('auth', __name__)

# Import routes harus di bawah definisi bp untuk menghindari circular import
from app.auth import routes