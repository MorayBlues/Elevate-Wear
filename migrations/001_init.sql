CREATE TABLE categories(id SERIAL PRIMARY KEY, category TEXT NOT NULL, subcategory TEXT NOT NULL, UNIQUE(category, subcategory)); 
CREATE TABLE products(id SERIAL PRIMARY KEY, categories_id INTEGER NOT NULL REFERENCES categories(id), name TEXT NOT NULL, price DECIMAL(10,2) NOT NULL, description TEXT NOT NULL); 
CREATE TABLE images(id SERIAL PRIMARY KEY, products_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE, image_url VARCHAR(255) NOT NULL, is_cover BOOLEAN NOT NULL);
CREATE UNIQUE INDEX ON images(products_id) WHERE is_cover = true; 
CREATE TABLE variants(id SERIAL PRIMARY KEY, products_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE, size VARCHAR(55) NOT NULL, color VARCHAR(55) NOT NULL, availability_flag BOOLEAN NOT NULL, UNIQUE(size, color, products_id));
CREATE TABLE orders(id SERIAL PRIMARY KEY, variants_id INTEGER REFERENCES variants(id) ON DELETE SET NULL,customer_name TEXT NOT NULL, customer_phone VARCHAR(20) NOT NULL, number_of_items INTEGER NOT NULL, status TEXT CHECK (status in('pending', 'contacted', 'cancelled', 'fulfilled')) NOT NULL, price_at_purchase DECIMAL(10,2) NOT NULL, product_name TEXT NOT NULL, product_size VARCHAR(55) NOT NULL, product_color VARCHAR(55) NOT NULL,  ordered_at TIMESTAMPTZ DEFAULT now() NOT NULL);
CREATE TABLE admin_users(id SERIAL PRIMARY KEY, user_name VARCHAR(25) NOT NULL, password_hash VARCHAR(255) NOT NULL);

-- SELECT products.id, products.name, products.price, categories.category, categories.subcategory, images.image_url 
-- FROM products JOIN categories ON products.categories_id = categories.id 
-- JOIN images ON images.products_id = products.id 
-- WHERE images.is_cover = true;


-- SELECT * FROM products JOIN categories ON products.categories_id = categories.id;
-- WHERE products.id = %s;
-- SELECT * FROM images WHERE products_id = %s;
-- SELECT * FROM variants WHERE products_id = %s;

-- SELECT products.id, products.name, products.price, categories.category, categories.subcategory, images.image_url FROM products JOIN categories ON products.categories_id = categories.id JOIN images ON images.products_id = products.id WHERE images.is_cover = true ORDER BY products.id DESC LIMIT 4;

SELECT user_name FROM admin_users;