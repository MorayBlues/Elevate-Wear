# Urban Threads Kenya - E-Commerce & Inventory System

**Urban Threads Kenya** is a full-stack Flask web application designed for a contemporary Kenyan fashion and apparel brand. The platform features an interactive customer storefront with seamless WhatsApp ordering, as well as a feature-rich admin control panel for inventory tracking, variant control, image hosting, and order management.

## Key Features

##  Customer Storefront

* **Featured Showcase:** High-impact hero section showcasing the newest additions to the store collection.

* **Product Catalog & Filters:** Detailed view of products organized by category and subcategory.

* **Interactive Image Galleries:** Live thumbnail switching on product detail pages allowing users to inspect images interactively.

* **Direct WhatsApp Integration:** Built-in WhatsApp ordering flow on product pages, plus a custom message builder on the Contact page that pre-fills user details directly into WhatsApp (`wa.me`).

* **Responsive Styling:** Dark/Light adaptive design built with custom CSS variables using modern fonts (*Space Grotesk* & *Inter*).

###  Admin Management Portal

* **Secure Authentication:** Protected admin sub-routes utilizing session-based security and password hash verification (`werkzeug.security`).

* **Store Metrics Dashboard:** Real-time visibility into total product counts and pending customer orders.

* **Product & Variant Builder:**

  * Add products with dynamically appendable sizing and color variants.

  * Upload multiple product photos in one batch directly to Cloudinary.

  * Automated primary image assignment (`is_cover`).

* **Social Media Copywriter Tool:** One-click clipboard button on product listings to instantly format and copy captions for Instagram/TikTok marketing.

* **Order Tracking & Manual Creation:** Track order statuses (`pending`, `fulfilled`) and manually input customer orders via a dynamic JS dropdown that queries variant prices via API endpoints.

##  Tech Stack

* **Backend:** Python 3, Flask (Blueprints, Sessions, Context Objects)

* **Database:** PostgreSQL (`psycopg2`)

* **Image Hosting:** Cloudinary API

* **Frontend:** HTML5, CSS3 (Custom Variables & Responsive Flex/Grid), Vanilla JavaScript (Fetch API, DOM manipulation, Clipboard API)

* **Configuration:** `python-dotenv`

* **Version Control:** Git

## File & Project Structure

```
Urban-Threads-Kenya/
├── app.py                   # Flask application factory and blueprint registrations
├── auth.py                  # Admin authentication & password hashing utilities
├── database connection setup & teardown
├── db.py                    # Cloudinary integration for cloud file uploads
├── main.py                  # Main entry point for local execution
├── migrate.py               # Database migration script runner
├── script.py                # Admin helper script (password hash generation)
├── requirements.txt         # Project dependency manifest
├── migrations/
│   └── 001_init.sql         # Initial SQL database schema definition
├── routes/
│   ├── admin.py             # Admin controller endpoints & API routes
│   └── customer.py          # Customer controller routes (catalog, details, static pages)
├── static/
│   ├── css/
│   │   ├── base.css         # Global variables, typography & reset styles
│   │   ├── admin.css        # Admin portal styling (dark theme, tables, cards)
│   │   └── customer.css     # Storefront styling (layout, thumbnails, WhatsApp buttons)
│   ├── images/              # Static media assets & brand logos
│   └── js/
│       ├── admin.js         # Admin dynamic UI, form rows, clipboard, & API fetches
│       └── user.js          # Customer UI, image thumbnail gallery switcher, WhatsApp API builder
└── templates/
    ├── base_admin.html      # Admin layout shell
    ├── base_customer.html   # Customer layout shell
    ├── index.html           # Storefront landing page
    ├── products.html        # Main product catalog listing
    ├── product_detail.html  # Single product gallery and details page
    ├── about.html           # Brand story, mission, and vision
    ├── contact.html         # Contact page with integrated WhatsApp messaging
    ├── login.html           # Admin portal login view
    ├── admin-dashboard.html # Admin analytics overview
    ├── Admin-products.html  # Inventory management table view
    ├── add-product.html     # Add new product & upload images view
    ├── edit_product.html    # Edit existing product details & variants view
    ├── orders.html         # Order management view
    └── add-order.html       # Manual order creation view

```

## Getting Started

### 1. Prerequisites

* **Python 3.8+** installed on your system.

* **PostgreSQL** database instance running locally or hosted remotely.

* **Cloudinary** account credentials for handling image uploads.

### 2. Environment Setup

Clone the repository and navigate into the project directory:

```
git clone https://github.com/your-username/Urban-Threads-Kenya.git
cd Urban-Threads-Kenya

```

Create and activate a virtual environment:

```
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate

```

Install the required dependencies:

```
pip install -r requirements.txt

```

### 3. Environment Variables Configuration

Create a `.env` file in the root directory and specify your environment variables:

```
SECRET_KEY=your_flask_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/urban_threads_db
CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

```

### 4. Database Setup & Migration

Run the built-in migration script to set up your PostgreSQL database tables:

```
python migrate.py

```

To create your initial admin user, generate a hashed password using `script.py` (or Python's `werkzeug.security`), then insert it into your PostgreSQL database:

```
INSERT INTO admin_users (user_name, password_hash) 
VALUES ('admin', 'your_generated_hash_here');

```

### 5. Running the Application

Execute the application launcher:

```
python main.py

```

Access the storefront in your web browser at:
`http://127.0.0.1:5000/`

Access the admin login page at:
`http://127.0.0.1:5000/admin/login`

## 🔗 Route Reference

### Customer Routes

| Route | Method | Description | 
| ----- | ----- | ----- | 
| `/` | `GET` | Landing page showcasing recent products | 
| `/products` | `GET` | Full catalog of available items | 
| `/products/<id>` | `GET` | Individual product view with gallery & WhatsApp checkout | 
| `/about` | `GET` | Brand history, mission, and vision statement | 
| `/contact` | `GET` | Contact details with auto-filling WhatsApp messenger | 

### Admin Routes

| Route | Method | Access | Description | 
| ----- | ----- | ----- | ----- | 
| `/admin/login` | `GET / POST` | Public | Admin authentication portal | 
| `/admin/logout` | `GET` | Admin | Clears admin session | 
| `/admin/dashboard` | `GET` | Admin | Store summary metrics (pending orders & total products) | 
| `/admin/products` | `GET` | Admin | Management listing of all items | 
| `/admin/products/add` | `GET / POST` | Admin | Create product, attach variants, and upload photos | 
| `/admin/products/<id>/edit` | `GET / POST` | Admin | Modify product info, pricing, and variants | 
| `/admin/products/<id>` | `POST` | Admin | Delete a product from inventory | 
| `/admin/orders` | `GET` | Admin | View customer order history | 
| `/admin/orders/<id>` | `POST` | Admin | Update status of an order | 
| `/admin/orders/add` | `GET / POST` | Admin | Manually record customer order | 
| `/admin/api/variants/<id>` | `GET` | Admin | Internal API returning variant JSON for order forms | 
