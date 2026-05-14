from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

app = Flask(__name__)

# CONFIG
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT DB
db.init_app(app)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# LOAD USER
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# LOGIN ROUTE
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('INVALID USERNAME OR PASSWORD', 'error')

    return render_template('login.html')


# DASHBOARD
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# CREATE DATABASE + ADMIN USER
def create_admin():
    existing_user = User.query.filter_by(username='admin').first()

    if not existing_user:
        admin = User(
            username='admin',
            password=generate_password_hash('securepassword')
        )
        db.session.add(admin)
        db.session.commit()


# RUN APP
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()

    app.run(debug=True)
