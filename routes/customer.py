from flask import Blueprint
from db import get_db
customer = Blueprint('customer', __name__)
from flask import render_template

@customer.route('/products')
def products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT products.id, products.name, products.price, categories.category, categories.subcategory, images.image_url FROM products JOIN categories ON products.categories_id = categories.id JOIN images ON images.products_id = products.id WHERE images.is_cover = true;")
    results = cur.fetchall()
    return render_template('products.html', products=results)

@customer.route('/products/<int:product_id>')
def product_detail(product_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products JOIN categories ON products.categories_id = categories.id WHERE products.id = %s;",(product_id,))
    product = cur.fetchone()
    cur.execute("SELECT * FROM images WHERE products_id = %s;", (product_id,))
    images = cur.fetchall()
    cur.execute("SELECT * FROM variants WHERE products_id = %s;",(product_id,))
    variants = cur.fetchall()
    return render_template('product_detail.html', product=product, images=images, variants=variants)

@customer.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT products.id, products.name, products.price, categories.category, categories.subcategory, images.image_url FROM products JOIN categories ON products.categories_id = categories.id JOIN images ON images.products_id = products.id WHERE images.is_cover = true ORDER BY products.id DESC LIMIT 4;")
    results = cur.fetchall()
    return render_template('index.html', featured_products=results)

@customer.route('/about')
def about():
    return render_template('about.html')

@customer.route('/contact')
def contact():
    return render_template('contact.html')