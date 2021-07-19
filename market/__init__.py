from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# SQLite kullanarak market.db isminde veri tabani olusturduk
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# veri tabaninin guvenlik anahtari
app.config['SECRET_KEY'] = 'c0532df955dc7e39aa1abf99'
db = SQLAlchemy(app)
# Musteri sifresi Orn: 123 ise Veri tabaninda 123 olarak tutulmamasi icin, girilen sifreleri sifrelemek amaciyla
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market import routes
