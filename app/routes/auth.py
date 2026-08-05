from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("task.view_tasks"))
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("That username or password did not match.", "error")
            return render_template("login.html", username=username)
        session.clear()
        session["user_id"] = user.id
        session["username"] = user.username
        flash("Welcome back. Your focus board is ready.", "success")
        return redirect(url_for("task.view_tasks"))
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("task.view_tasks"))
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")
        if len(username) < 3 or len(username) > 40 or not username.replace("_", "").isalnum():
            flash("Use 3–40 letters, numbers, or underscores for your username.", "error")
        elif len(password) < 6:
            flash("Your password needs at least 6 characters.", "error")
        elif password != confirmation:
            flash("The passwords do not match.", "error")
        elif User.query.filter_by(username=username).first():
            flash("That username is already taken.", "error")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Sign in to start planning.", "success")
            return redirect(url_for("auth.login"))
        return render_template("register.html", username=username)
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("auth.login"))
