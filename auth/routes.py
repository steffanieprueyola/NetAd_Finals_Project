from flask import render_template, request, redirect, url_for, session, flash
from auth import auth_bp
from auth.models import users

# LOGIN PAGE
@auth_bp.route("/")
def login_page():
    return render_template("login.html")

# LOGIN PROCESS
@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # check credentials
    if username in users and users[username] == password:
        session["user"] = username   # 🔐 create session
        return redirect(url_for("dashboard.home"))

    flash("Invalid username or password")
    return redirect(url_for("auth.login_page"))

# LOGOUT
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
