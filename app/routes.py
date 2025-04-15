from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import User

# Create a blueprint for authentication routes
auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def index():
    if 'user_id' in session:
        # Get the user from the database
        user = User.get_by_id(session['user_id'])
        if user:
            return render_template('dashboard.html', username=user.username, name=user.name)
    # If not logged in, redirect to login page
    return redirect(url_for('auth.login'))

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            user = User.authenticate(username, password)
            if user:
                session['user_id'] = user.id
                return redirect(url_for('auth.index'))
            else:
                flash('Invalid username or password')
        else:
            flash('Please enter both username and password')
    
    return render_template('login.html')

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if username and password and name:
            user = User.create_user(username, password, name)
            if user:
                session['user_id'] = user.id
                return redirect(url_for('auth.index'))
            else:
                flash('Username already exists')
        else:
            flash('Please fill all fields')
    
    return render_template('register.html')

@auth_routes.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login')) 