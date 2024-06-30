import os
from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, get_flashed_messages
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, Admin, Product


main = Blueprint('main', __name__)

############################################ USER ###############################################

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
            # Directly set the attribute on the object or create a new attribute
            item.product_image = os.path.basename(product_image)
        else:
            print(f"Warning: 'product_image' is not a string: {product_image}")

    return render_template('user_index.html', items_list=items_list)


@main.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.user_login'))


@main.route('/user_404')
def user_fournotfour():
    return render_template("user_404.html")


@main.route('/user_cart')
def user_cart():
    return render_template("user_cart.html")


@main.route('/user_checkout')
def user_checkout():
    return render_template("user_checkout.html")


@main.route('/user_contact')
def user_contact():
    return render_template("user_contact.html")


@main.route('/user_shopdetail')
def user_shopdetail():
    return render_template("user_shop-detail.html")


@main.route('/user_shop')
def user_shop():
    return render_template("user_shop.html")


@main.route('/user_testimonial')
def user_testimonial():
    return render_template("user_testimonial.html")

############################################ ADMIN ##############################################

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
            # Directly set the attribute on the object or create a new attribute
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

        # Ensure the directory exists
        image_directory = 'app/static/img'
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)

        # Save the image file and get the file path
        image_path = os.path.join(image_directory, product_image.filename)
        product_image.save(image_path)

        # Create a new product instance
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