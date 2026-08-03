from flask import Blueprint
from flask import request
from auth import verify_admin
from auth import login_required
from flask import session, redirect, url_for
from flask import render_template
from cloudinary_upload import upload_image
from flask import jsonify
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
            return redirect(url_for('admin.dashboard'))
        else:
             return render_template('login.html', error="Invalid Username or Password")
    else:
        return render_template('login.html')

@admin.route('/admin/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('customer.index'))

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    products = cur.fetchone()
    product_count = products[0]
    cur.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending';")
    orders = cur.fetchone()
    pending_order_count = orders[0]
    return render_template('admin-dashboard.html', product_count = product_count, pending_order_count = pending_order_count)

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
        image_files = request.files.getlist('image_file[]')
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

            cover_image_set = False
            for file in image_files:
                 if file.filename == '':
                      continue
                 image_url = upload_image(file)
                 is_cover = not cover_image_set
                 cur.execute("INSERT INTO images(products_id, image_url, is_cover) VALUES(%s, %s, %s);",(product_id, image_url, is_cover))
                 cover_image_set = True

            for size, color in zip(sizes, colors):
                cur.execute("INSERT INTO variants(products_id, size, color, availability_flag) VALUES(%s, %s, %s, %s);", (product_id, size, color, True))

            conn.commit()
            return render_template('add-product.html', success="Product added successfully!")
        except psycopg2.Error as e:
            conn.rollback()
            return render_template('add-product.html', error="Failed to add product. Try again!")
    else:
        return render_template('add-product.html')
    
@admin.route('/admin/orders')
@login_required
def orders():
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders;")
            results = cur.fetchall()
            return render_template('orders.html', orders = results)

@admin.route('/admin/orders/<int:order_id>', methods=['POST'])
@login_required
def update_order(order_id):
     conn = get_db()
     cur = conn.cursor()
     status = request.form['status']
     cur.execute("UPDATE orders SET status = %s WHERE id = %s;",(status, order_id))
     conn.commit()
     return redirect(url_for('admin.orders')) 

@admin.route('/admin/products')
@login_required
def products_listing_view():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT products.id, products.name, products.price, products.description, categories.category, categories.subcategory, images.image_url FROM products JOIN categories ON products.categories_id = categories.id JOIN images ON images.products_id = products.id WHERE images.is_cover = true;")
    results = cur.fetchall()
    return render_template('Admin-products.html', products=results)

@admin.route('/admin/products/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
     conn = get_db()
     cur = conn.cursor()
     cur.execute("DELETE FROM products WHERE  id = %s;",(product_id,))
     conn.commit()
     return redirect(url_for('admin.products_listing_view'))

@admin.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
     conn = get_db()
     cur = conn.cursor()
     if request.method == 'GET':
          cur.execute("SELECT * FROM products JOIN categories ON products.categories_id = categories.id WHERE products.id = %s;",(product_id,))
          product = cur.fetchone()
          cur.execute("SELECT * FROM categories;")
          categories = cur.fetchall()
          cur.execute("SELECT * FROM variants WHERE products_id = %s;",(product_id,))
          variants = cur.fetchall()
          return render_template('edit_product.html', product=product, categories=categories, variants=variants)
          
     else:
          name = request.form['name']
          price = request.form['price']
          description = request.form['description']
          categories_id = request.form['categories_id']
          existing_ids = request.form.getlist('existing_variant_id[]')
          existing_sizes = request.form.getlist('existing_size[]')
          existing_colors = request.form.getlist('existing_color[]')
          new_sizes = request.form.getlist('size[]')
          new_colors = request.form.getlist('color[]')
          try:
               cur.execute("UPDATE products SET name = %s, price = %s, description = %s, categories_id = %s WHERE id = %s;",(name, price, description, categories_id, product_id))
               for variant_id, size, color in zip(existing_ids, existing_sizes, existing_colors):
                    if f'remove_{variant_id}' in request.form:
                         cur.execute("DELETE FROM variants WHERE id = %s;", (variant_id,))
                    else:
                         cur.execute("UPDATE variants SET size = %s, color = %s WHERE id = %s;", (size, color, variant_id))   
               for size, color in zip(new_sizes, new_colors):
                    cur.execute("INSERT INTO variants(products_id, size, color, availability_flag) VALUES(%s, %s, %s, %s);", (product_id, size, color, True))           
               conn.commit()
               return redirect(url_for('admin.products_listing_view'))
          except psycopg2.Error as e:
            conn.rollback()
            return render_template('edit_product.html', error="Failed to Edit product.Try Again!")

@admin.route('/admin/orders/add', methods=['GET', 'POST'])
@login_required
def add_order():
     conn = get_db()
     cur = conn.cursor()
     cur.execute("SELECT id, name FROM products;")
     products = cur.fetchall()
     if request.method == 'POST':
          customer_name = request.form['customer_name']
          customer_phone = request.form['customer_phone']
          number_of_items = request.form['number_of_items']
          status = request.form['status']
          product_name = request.form['product_name']
          product_size = request.form['product_size']
          product_color = request.form['product_color']
          price_at_purchase = request.form['price_at_purchase']
          try:
               cur.execute("INSERT INTO orders (customer_name, customer_phone, number_of_items, status, product_name, product_size, product_color, price_at_purchase) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (customer_name, customer_phone, number_of_items, status, product_name, product_size, product_color, price_at_purchase))
               conn.commit()
               return render_template('add-order.html', products=products, success = "order added successfully!")
          except psycopg2.Error as e:
               conn.rollback()
               return render_template('add-order.html', products=products, error="Failed to add order. Try Again!")
     else:
          return render_template('add-order.html', products=products)

@admin.route('/admin/api/variants/<int:product_id>')
@login_required
def get_variants(product_id):
     conn = get_db()
     cur = conn.cursor()
     cur.execute("SELECT variants.id, variants.size, variants.color, products.price FROM variants JOIN products ON variants.products_id = products.id WHERE variants.products_id = %s;", (product_id,))
     results = cur.fetchall()
     variants_list = []
     for row in results:
          variants_list.append({
               'id': row[0],
               'size': row[1],
               'color': row[2],
               'price': row[3]
          })
     return jsonify(variants_list)          