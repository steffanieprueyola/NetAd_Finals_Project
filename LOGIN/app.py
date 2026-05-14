from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# CONFIG

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# DATABASE

db = SQLAlchemy(app)

# LOGIN MANAGER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# USER MODEL

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

# LOAD USER

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

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

        else:

            flash('INVALID USERNAME OR PASSWORD')

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

# CREATE DATABASE + TEST ACCOUNT

with app.app_context():

    db.create_all()

    existing_user = User.query.filter_by(username='admin').first()

    if not existing_user:

        hashed_password = generate_password_hash('securepassword')

        user = User(
            username='admin',
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

# RUN APP

if __name__ == '__main__':

    app.run(debug=True)
