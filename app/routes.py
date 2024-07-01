import os
from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for, \
     request, session, flash, get_flashed_messages, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, Admin, Product

main = Blueprint('main', __name__)


@main.route('/user_register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        user_email = request.form['email']
        existing_user = User.query.filter_by(user_username=user_username, user_email=user_email).first()
        if existing_user:
            return redirect(url_for('main.user_login'))
        user = User(user_username=user_username, user_password=user_password, user_email=user_email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.user_login'))
    return render_template("user_register.html")


@main.route('/', methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        user = User.query.filter_by(user_username=user_username).first()
        if user and user.user_password == user_password:
            login_user(user)
            return redirect(url_for('main.user_index'))
        return redirect(url_for('main.user_register'))
    return render_template("user_login.html")


@main.route('/user_index')
@login_required
def user_index():
    items_list = Product.query.all()
    for item in items_list:
        product_image = item.product_image
        if isinstance(product_image, str):
            item.product_image = os.path.basename(product_image)
        else:
            print(f"Warning: 'product_image' is not a string: {product_image}")
    return render_template('user_index.html', items_list=items_list)


@main.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.user_login'))


# Cart Section

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    items = Product.query.all()
    item = next((item for item in items if item.id == product_id), None)
    if not item:
        return redirect(url_for('main.user_index'))

    cart = session.get('user_cart', [])
    for cart_item in cart:
        if cart_item['product_id'] == product_id:
            cart_item['quantity'] += 1
            break
    else:
        cart.append({'product_id': item.id, 'product_name': item.product_name, 'product_price': float(item.product_price), 'product_image': item.product_image, 'quantity': 1})

    session['user_cart'] = cart
    return redirect(url_for('main.user_shop'))


@main.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    quantity = int(request.form['quantity'])

    cart = session.get('user_cart', [])
    for cart_item in cart:
        if cart_item['product_id'] == product_id:
            cart_item['quantity'] = quantity
            break

    session['user_cart'] = cart
    return redirect(url_for('main.user_cart'))


@main.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('user_cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]

    session['user_cart'] = cart
    return redirect(url_for('main.user_cart'))


@main.route('/user_checkout', methods=['GET', 'POST'])
def user_checkout():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        postcode = request.form.get('postcode')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        create_account = request.form.get('create_account')
        ship_different_address = request.form.get('ship_different_address')
        order_notes = request.form.get('order_notes')
        shipping = request.form.get('shipping')
        terms_and_conditions = request.form.get('terms_and_conditions')

        cart_items = request.form.getlist('cart_items[]')
        quantities = request.form.getlist('quantities[]')
        prices = request.form.getlist('prices[]')
        total = float(request.form.get('total', 0))
        shipping_cost = float(request.form.get('shipping_cost', 0))

        if not terms_and_conditions:
            flash('You must agree to the terms and conditions.', 'error')
            return redirect(url_for('main.user_checkout'))

        session.pop('user_cart', None)
        return render_template('user_checkout.html', message="Payment successful", total=total, shipping_cost=shipping_cost)

    cart = session.get('user_cart', [])
    subtotal = sum(float(item['product_price']) * item['quantity'] for item in cart)
    shipping = 3.00
    total = subtotal + shipping
    return render_template('user_checkout.html', cart=cart, subtotal=subtotal, shipping_cost=shipping, total=total)

@main.route('/user_cart')
def user_cart():
    cart = session.get('user_cart', [])
    subtotal = sum(float(item['product_price']) * item['quantity'] for item in cart)
    shipping = 3.00
    total = subtotal + shipping
    return render_template('user_cart.html', cart=cart, subtotal=subtotal, shipping=shipping, total=total)


# Other Links Section

@main.route('/user_contact')
def user_contact():
    return render_template("user_contact.html")


@main.route('/user_shop')
def user_shop():
    items_list = Product.query.all()
    for item in items_list:
        product_image = item.product_image
        if isinstance(product_image, str):
            item.product_image = os.path.basename(product_image)
        else:
            print(f"Warning: 'product_image' is not a string: {product_image}")
    return render_template('user_shop.html', items_list=items_list)


@main.route('/user_testimonial')
def user_testimonial():
    return render_template("user_testimonial.html")


# Admin Section

@main.route('/admin_register', methods=['POST', 'GET'])
def admin_register():
    if request.method == 'POST':
        admin_username = request.form['username']
        admin_password = request.form['password']
        admin_email = request.form['email']
        existing_admin = Admin.query.filter_by(admin_username=admin_username, admin_email=admin_email).first()
        if existing_admin:
            return redirect(url_for('main.admin_login'))
        admin = Admin(admin_username=admin_username, admin_password=admin_password, admin_email=admin_email)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('main.admin_login'))
    return render_template("admin_register.html")


@main.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form['username']
        admin_password = request.form['password']
        admin = Admin.query.filter_by(admin_username=admin_username).first()
        if admin and admin.admin_password == admin_password:
            login_user(admin)
            return redirect(url_for('main.admin_index'))
        return redirect(url_for('main.admin_register'))
    return render_template("admin_login.html")


@main.route('/admin_index')
@login_required
def admin_index():
    items_list = Product.query.all()
    for item in items_list:
        product_image = item.product_image
        if isinstance(product_image, str):
            item.product_image = os.path.basename(product_image)
        else:
            print(f"Warning: 'product_image' is not a string: {product_image}")
    return render_template('admin_index.html', items_list=items_list)


@main.route('/admin_logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('main.admin_login'))


@main.route('/admin_add_product', methods=['POST', 'GET'])
@login_required
def admin_add_product():
    if request.method == 'POST':
        product_name = request.form['name']
        product_image = request.files['image']
        product_description = request.form['description']
        product_price = request.form['price']
        product_category = request.form['category']

        image_directory = 'app/static/img'
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)

        image_path = os.path.join(image_directory, product_image.filename)
        product_image.save(image_path)

        new_product = Product(
            product_name=product_name,
            product_image=image_path,
            product_description=product_description,
            product_price=product_price,
            product_category=product_category
        )

        db.session.add(new_product)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")
        finally:
            db.session.close()
    return redirect(url_for('main.admin_index'))


@main.route('/admin_delete_product/<int:product_id>', methods=['POST'])
@login_required
def admin_delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('main.admin_index'))
