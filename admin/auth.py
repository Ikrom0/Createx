from flask import jsonify, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from models import Admin
from validators.forms import validate_admin

from . import admin


@admin.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        admin_data = {
            "username": request.form.get("username", "").strip(),
            "password": request.form.get("password", "")
        }

        errors = validate_admin(admin_data)

        if errors:
            return jsonify({
                "success": False,
                "errors": errors
            }), 400

        admin = Admin.query.filter_by(username=admin_data["username"]).first()

        login_user(admin)

        return jsonify({
            "success": True, 
            "redirect_url": url_for("admin.dashboard")
        }), 201

    return render_template("admin/login.html")


@admin.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("admin.login"))

