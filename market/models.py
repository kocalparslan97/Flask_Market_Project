from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # Musteri tablosundan musteri id numarasini aliyoruz
    return User.query.get(int(user_id))


# Veri tabaninda Musteri tablosundan veri cekiliyor
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=5000)  # default money value
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        # Musteri butcesinin , her 4 basamakta bir virgul ekleyerek okunakligini arttiriyoruz
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        # girilen sifreyi hash ile sifrele
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attemted_password):
        # dogrulamak icin girilen 2. sifre ile dogru sifre hash i karsilastir
        return bcrypt.check_password_hash(self.password_hash, attemted_password)

    def can_purchase(self, item_obj):
        # alinacak olan item ucreti ile musteri butcesini karsilastir
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        # mevcut olan urunu satmak icin
        return item_obj in self.items


# Market urunlerinin veri tabani tablosundan veri cekiliyor
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # 30 karakter ile sinirli, bos olamaz, benzersiz olacak
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    # Model in primary key arar
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user):
        # Satin alma fonksiyonu
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        # Mevcut urunu satma fonksiyonu
        self.owner = None
        user.budget += self.price
        db.session.commit()
