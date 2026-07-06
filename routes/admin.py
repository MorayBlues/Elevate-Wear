from flask import Blueprint
from flask import request
from auth import verify_admin
from auth import login_required
from flask import session
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