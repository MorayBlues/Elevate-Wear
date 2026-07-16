from flask import Blueprint
from flask import request
from auth import verify_admin
from auth import login_required
from flask import session
import psycopg2
from db import get_db
admin = Blueprint('admin',__name__)

@admin.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        user = request.form['username']
        
        if verify_admin(user,password):
            session['admin_logged_in'] = True
            return "Login successful"
        else:
            return "Invalid username or password"
    else:
        return '''
        <form method="post">
        <input name ="username" placeholder="username">
        <input name ="password" type="password" placeholder="password">
        <button type="submit">Login</button>
        </form>
        '''

@admin.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return "Logged out"

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    return "Welcome to the dashboard"

@admin.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        category = request.form['category']
        subcategory = request.form['subcategory']
        image_urls = request.form.getlist('image_url[]')
        sizes = request.form.getlist('size[]')
        colors =request.form.getlist('color[]')
        try:
            cur.execute("INSERT INTO categories(category, subcategory) VALUES(%s, %s) ON CONFLICT (category, subcategory) DO NOTHING RETURNING id;", (category, subcategory))
            result = cur.fetchone()
            if result is None:
                cur.execute("SELECT id FROM categories WHERE category = %s AND subcategory = %s;", (category, subcategory))
                result = cur.fetchone()
            category_id = result[0]  

            cur.execute("INSERT INTO products(categories_id, name, price, description) VALUES(%s, %s, %s, %s) RETURNING id;", (category_id, name, price, description)) 
            result = cur.fetchone()
            product_id = result[0]

            for index, url in enumerate(image_urls):
                is_cover = (index == 0)
                cur.execute("INSERT INTO images(products_id, image_url, is_cover) VALUES(%s, %s, %s);", (product_id, url, is_cover))

            for size, color in zip(sizes, colors):
                cur.execute("INSERT INTO variants(products_id, size, color, availability_flag) VALUES(%s, %s, %s, %s);", (product_id, size, color, True))

            conn.commit()
            return "Product added successfully"
        except psycopg2.Error as e:
            conn.rollback()
            return f"Failed to add product: {e}"
    else:
        return '''
        <form method="POST">
            Name: <input name ="name"><br>
            Price: <input name="price"><br>
            Description: <input name="description"><br>
            Category: <input name="category"><br>
            Subcategory: <input name="subcategory"><br>
            Image URL 1: <input name="image_url[]"><br>
            Image URL 2: <input name="image_url[]"><br>
            Size 1: <input name="size[]"> Color 1: <input name="color[]"><br>
            Size 2: <input name="size[]"> Color 2: <input name="color[]"><br>
            <button type="submit">Add Product</button>
        </form>    
        '''