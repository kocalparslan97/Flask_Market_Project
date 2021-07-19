from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


# Kayit formundaki kosullar yer aliyor
class RegisterForm(FlaskForm):
    # Kayit olurken yazdigimiz kullanici adi ile veri tabanindaki kullanici adlarini karsilastiriyor
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exits! Please try a different username')

    # Kayit olurken yazdigimiz email ile veri tabanindaki email adreslerini karsilastiriyor
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    # Eger ustteki kosullari sagliyorsa , bu verileri degiskene atiyor
    # DataRequired()- > bos gecilemez olmasi icin
    username = StringField(label='Username :', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address :', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password :', validators=[Length(min=6), DataRequired()])
    # password1 ile password2 ayni olmasi gerekiyor sifre olusturulurken
    password2 = PasswordField(label='Confirm Password :', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


# Musteri Giriş formu
class LoginForm(FlaskForm):
    username = StringField(label='Username :', validators=[DataRequired()])
    password = PasswordField(label='Password :', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')
