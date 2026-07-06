from functools import wraps
from flask import session, redirect, url_for
from werkzeug.security import check_password_hash
from db import get_db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

def verify_admin(user,password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM admin_users WHERE admin_users.user_name = %s;",(user,))
    admin = cur.fetchone()
    if admin is None:
        return False
    if admin:
        stored_hash = admin[0]
        return check_password_hash(stored_hash, password)
