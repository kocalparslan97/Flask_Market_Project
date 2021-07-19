from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    # localhost baslayinca ilk gelen web sayfasi
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])  # Market sayfasi veri alma ve veri gonderme fonk. sahip
@login_required  # Uye olmayan market sayfasina giremez
def market_page():
    # Urun satin alma islemleri icin degisken
    purchase_form = PurchaseItemForm()
    # Urun satma islemleri icin degisken
    selling_form = SellItemForm()
    if request.method == "POST":
        # Urun satin alma islemleri
        # Satin alinacak urunu degiskene ata
        purchase_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        if p_item_object:
            # Musteri , urune butcesi yeter mi ?
            if current_user.can_purchase(p_item_object):
                # Urunu satin aliyor
                p_item_object.buy(current_user)
                # Tebrik ve bilgilendirme mesaji gosteriliyor
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$",
                      category='success')
            else:
                # Eger Musteri butcesi yetersiz ise bu mesaj gosteriliyor
                flash(f"Unfortunately, You don't have enough money to purchase {p_item_object.name}", category='danger')
        # Urun satma İslemleri
        # Satilacak olan urunu degiskene ata
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            # Musteri urunu satabilir mi ?
            if current_user.can_sell(s_item_object):
                # Musteri urunu satma islemi gerceklesiyor
                s_item_object.sell(current_user)
                # Satis sonrasi tebrik ve bilgilendirme mesaji
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
        # Bu satin alma ve satma islemlerinden sonra market sayfasina geri don
        return redirect(url_for('market_page'))
    # Satilan urunu tekrardan market raflarinda sergileme
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # Uye kaydi olusturmak icin
    form = RegisterForm()
    if form.validate_on_submit():
        # Kayit formunda yazilan bilgileri veri tabanina ekliyoruz
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        # Tebrik ve bilgilendirme mesaji gosteriliyor
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        # Kaydolduktan sonra market sayfasina yonlendirme yapiliyor
        return redirect(url_for('market_page'))
    # Kayit esnasinda gerekli kosullari saglamazsa girilen veriler hata mesaji gostermek icin
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Muvcut Musteri giris ekrani
    form = LoginForm()
    # Giris ekrani kosullari
    if form.validate_on_submit():
        # login sayfasinda yazilan kullanici adini degiskende tut
        attemted_user = User.query.filter_by(username=form.username.data).first()
        # Mevcut Musteri kullanici adi ile login ekraninda yazilan kullanici adi esit mi?
        if attemted_user and attemted_user.check_password_correction(
                attemted_password=form.password.data
        ):
            login_user(attemted_user)
            flash(f'Success! You are logged in as: {attemted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    # Musteri hesabindan cikis yaparsa
    logout_user()
    flash("You have been logged Out!", category='info')
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)
