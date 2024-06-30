"""
Fruits Shop using Flask Framework

This module defines routes and views for the Fruits Shop web application. 
It includes user registration, login, logout, and the index page where users can view available products.

The application uses the Flask framework for building web applications and Flask-Login for user session management.

Imports:
- os: For file path operations.
- Blueprint: For creating routes and views in the Flask application.
- render_template: For rendering HTML templates.
- redirect, url_for: For redirecting to different routes.
- request: For accessing request data.
- session: For storing user session data.
- flash, get_flashed_messages: For sending and displaying flash messages.
- jsonify: For creating JSON responses.
- login_user, login_required, logout_user, current_user: For user authentication and session management.
- User, Admin, Product: SQLAlchemy models for user, admin, and product data.
"""

import os
from flask import current_app as app
from flask import Blueprint, render_template, redirect, url_for, \
     request, session, flash, get_flashed_messages, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, Admin, Product

main = Blueprint('main', __name__)

""" ################################################# USER ################################################## """

@main.route('/user_register', methods=['POST', 'GET'])
def user_register():
    """
    Handle user registration.

    Handles both GET and POST requests. For GET requests, it renders the registration page.
    For POST requests, it processes the registration form, creates a new user, and redirects to the login page.

    POST Request Args:
        - username (str): The desired username for the new user.
        - password (str): The password for the new user.
        - email (str): The email address of the new user.

    Returns:
        - Redirect: Redirects to the login page after successful registration.
        - RenderTemplate: Renders the registration page for GET requests.
    """
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
    """
    Handle user login.

    Handles both GET and POST requests. For GET requests, it renders the login page.
    For POST requests, it processes the login form and authenticates the user.

    POST Request Args:
        - username (str): The username of the user attempting to log in.
        - password (str): The password of the user attempting to log in.

    Returns:
        - Redirect: Redirects to the user index page upon successful login or to the registration page on failure.
        - RenderTemplate: Renders the login page for GET requests.
    """
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
    """
    Display the index page for logged-in users.

    Fetches all products from the database, processes the product images to extract filenames, and renders the 
    index page where users can view available products.

    Returns:
        - RenderTemplate: Renders the index page with a list of products.
    """
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
    """
    Handle user logout.

    Logs out the current user and redirects to the login page.

    Returns:
        - Redirect: Redirects to the login page after successful logout.
    """
    logout_user()
    return redirect(url_for('main.user_login'))

""" ############################################### User End ################################################## """

""" ############################################# User Cart Start #############################################

This section of the code handles user cart functionalities including adding items to the cart, 
updating item quantities, removing items, and processing the checkout. 

Routes:
- `/add_to_cart/<int:product_id>`: Add a product to the user's cart.
- `/update_quantity/<int:product_id>`: Update the quantity of a product in the cart.
- `/remove_from_cart/<int:product_id>`: Remove a product from the cart.
- `/user_checkout`: Process the checkout and clear the cart.
- `/user_cart`: Display the cart contents, subtotal, shipping cost, and total.

Each route handles specific actions related to the user's shopping cart.
"""

@main.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    """
    Add a product to the user's cart.

    Fetches the product by ID and adds it to the cart stored in the session. If the product is already in the cart,
    increments the quantity by 1. Otherwise, adds the product with a quantity of 1.

    Args:
        product_id (int): The ID of the product to be added to the cart.

    Returns:
        Redirect: Redirects to the user index page again after adding the product to the cart.
    """
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
    return redirect(url_for('main.user_cart'))

@main.route('/update_quantity/<int:product_id>', methods=['POST'])
def update_quantity(product_id):
    """
    Update the quantity of a product in the cart.

    Updates the quantity of a specific product in the cart based on the form data.

    Args:
        product_id (int): The ID of the product whose quantity is to be updated.

    POST Request Args:
        - quantity (int): The new quantity for the product.

    Returns:
        Redirect: Redirects to the user cart page after updating the quantity.
    """
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
    """
    Remove a product from the user's cart.

    Removes a specific product from the cart based on its ID.

    Args:
        product_id (int): The ID of the product to be removed from the cart.

    Returns:
        Redirect: Redirects to the user cart page after removing the product.
    """
    cart = session.get('user_cart', [])
    cart = [item for item in cart if item['product_id'] != product_id]

    session['user_cart'] = cart  # Correct the session key to 'user_cart'
    return redirect(url_for('main.user_cart'))

@main.route('/user_checkout', methods=['GET', 'POST'])
def user_checkout():
    """
    Handle the checkout process.

    Clears the user's cart and processes the checkout. This is a placeholder for the checkout logic.

    POST Request:
        - A form submission triggers this route to process the checkout.

    Returns:
        - RenderTemplate: Renders the checkout page with a success message.
    """
    if request.method == 'POST':
        # Retrieve form data
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

        # Extract the cart items from the form submission
        cart_items = request.form.getlist('cart_items[]')
        quantities = request.form.getlist('quantities[]')
        prices = request.form.getlist('prices[]')
        total = float(request.form.get('total', 0))
        shipping_cost = float(request.form.get('shipping_cost', 0))

        if not terms_and_conditions:
            flash('You must agree to the terms and conditions.', 'error')
            return redirect(url_for('main.user_checkout'))

        # Handle the checkout logic here (e.g., save order, charge customer, etc.)
        # Example:
        # process_order(first_name, last_name, company_name, address, city, country, postcode, mobile, email, create_account, ship_different_address, order_notes, shipping, total)

        session.pop('user_cart', None)  # Clear the cart after successful payment
        return render_template('user_checkout.html', message="Payment successful", total=total, shipping_cost=shipping_cost)

    # If GET request, show the checkout page with current cart details
    cart = session.get('user_cart', [])
    subtotal = sum(float(item['product_price']) * item['quantity'] for item in cart)
    shipping = 3.00  # Example shipping cost
    total = subtotal + shipping
    return render_template('user_checkout.html', cart=cart, subtotal=subtotal, shipping_cost=shipping, total=total)


@main.route('/user_cart')
def user_cart():
    """
    Display the user's cart.

    Fetches the cart from the session, calculates the subtotal, shipping cost, and total,
    and renders the cart page.

    Returns:
        - RenderTemplate: Renders the user cart page with cart details.
    """
    cart = session.get('user_cart', [])
    subtotal = sum(float(item['product_price']) * item['quantity'] for item in cart)
    shipping = 3.00
    total = subtotal + shipping
    return render_template('user_cart.html', cart=cart, subtotal=subtotal, shipping=shipping, total=total)

""" ############################################# User Cart End ############################################### """

""" ############################################ Other Links WIP ############################################## """


@main.route('/user_404')
def user_fournotfour():
    return render_template("user_404.html")


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

""" ############################################ Other Links END ############################################## """

""" ################################################## ADMIN ################################################## """

@main.route('/admin_register', methods=['POST', 'GET'])
def admin_register():
    """
    Register a new admin user.

    Handles both GET and POST requests to show the registration form and create a new admin user.

    GET Request:
        - Displays the admin registration form.

    POST Request:
        - Submits the registration form with the following data:
            - `username` (str): The admin's username.
            - `password` (str): The admin's password.
            - `email` (str): The admin's email address.

    Returns:
        - Redirect: Redirects to the admin login page after successful registration or displays the registration form.
    """
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
    """
    Log in an existing admin user.

    Handles both GET and POST requests to show the login form and authenticate an admin user.

    GET Request:
        - Displays the admin login form.

    POST Request:
        - Submits the login form with the following data:
            - `username` (str): The admin's username.
            - `password` (str): The admin's password.

    Returns:
        - Redirect: Redirects to the admin index page after successful login or to the admin registration page on failure.
    """
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
    """
    View all products.

    Retrieves and displays all products in the catalog. This route is accessible only to logged-in admin users.

    Returns:
        - RenderTemplate: Renders the admin index page with a list of all products.
    """
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
    """
    Log out the current admin user.

    Logs out the current admin user and redirects to the admin login page.

    Returns:
        - Redirect: Redirects to the admin login page after logging out.
    """
    logout_user()
    return redirect(url_for('main.admin_login'))

@main.route('/admin_add_product', methods=['POST', 'GET'])
@login_required
def admin_add_product():
    """
    Add a new product to the catalog.

    Handles both GET and POST requests to show the add product form and create a new product.

    GET Request:
        - Displays the add product form.

    POST Request:
        - Submits the form with the following data:
            - `name` (str): The product's name.
            - `image` (File): The product's image file.
            - `description` (str): The product's description.
            - `price` (float): The product's price.
            - `category` (str): The product's category.

    Returns:
        - Redirect: Redirects to the admin index page after successfully adding the product.
    """
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
    """
    Delete a product from the catalog.

    Deletes a specific product from the catalog based on its ID.

    Args:
        product_id (int): The ID of the product to be deleted.

    POST Request:
        - A form submission triggers this route to delete the product.

    Returns:
        - Redirect: Redirects to the admin index page after deleting the product.
    """
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('main.admin_index'))

""" ############################################ ADMIN END ############################################## """