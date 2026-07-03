import db
from flask import Flask
app = Flask(__name__)
db.init_app(app)
from routes.admin import admin
from routes.customer import customer
app.register_blueprint(admin)
app.register_blueprint(customer)