from flask import render_template, request, redirect, url_for, session, flash
from auth import auth_bp
from auth.models import ADMIN

@auth_bp.route("/")
def login_page():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in ADMIN and ADMIN[username] == password:
        session["user"] = username
        return redirect(url_for("dashboard.home"))

    flash("Invalid username or password")
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))
