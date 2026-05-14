from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def home():

    # protect dashboard
    if "user" not in session:
        return redirect(url_for("auth.login_page"))

    return render_template("index.html")
