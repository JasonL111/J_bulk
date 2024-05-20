from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  
    invite_code = db.Column(db.String(14), nullable=False)

def check_and_remove_invite_code(invite_code):
    with open('invite_codes.txt', 'r') as file:
        lines = file.readlines()
    
    if invite_code + '\n' in lines:
        with open('invite_codes.txt', 'w') as file:
            for line in lines:
                if line.strip() != invite_code:
                    file.write(line)
        return True
    return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def ShowMain():
    return render_template('index.html')

@app.route("/view")
def View():
    return render_template('view.html')

@app.route("/create")
def Create():
    return render_template('create.html')

@app.route("/sign", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ShowMain'))
    if request.method == 'POST':
        email = request.form.get('email')
        invite_code = request.form.get('invite_code')
        password = request.form.get('password')
        

        if not check_and_remove_invite_code(invite_code):
            flash('Invalid or already used invite code.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(email=email, invite_code=invite_code, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Your account has been created! You are now logged in.', 'success')
        return redirect(url_for('ShowMain'))

    return render_template('sign.html') 
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ShowMain'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('ShowMain'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html') 

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/FAQs")
def FAQs():
    return render_template('FAQs.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created")
    app.run(debug=True)