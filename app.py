import db
import os
from flask import Flask
from routes.admin import admin
from routes.customer import customer
app = Flask(__name__)
db.init_app(app)
app.register_blueprint(admin)
app.register_blueprint(customer)
app.secret_key = os.environ.get("SECRET_KEY")