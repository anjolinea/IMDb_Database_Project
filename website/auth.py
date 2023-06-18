from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import DB
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # TODO: do basic checks like is username unique?
        if password1 != password2:
            flash("Passwords do not match!", category="error")
        else:
            db = DB()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (username, firstname, lastname, password) VALUES (?, ?, ?, ?)",
                (username, firstName, lastName, generate_password_hash(password1, method='scrypt')),
            )
            db.commit()
            db.close()
            flash("Account created!", category="success")
            return redirect(url_for('views.home'))
        
    return render_template("sign_up.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usr = request.form.get("username")
        pwd = request.form.get("password")

        # TODO: do basic check like does username exist?
        if True:
            db = DB()
            cursor = db.cursor()
            hash_password = cursor.execute('SELECT password FROM users WHERE username = ?', (usr,)).fetchone()[0]
            db.close()
            if check_password_hash(hash_password, pwd):
                return redirect(url_for('views.home'))
                flash("Successfully logged in!", category="success")
            else:
                flash("Password incorrect!", category="error")
        else:
            flash("User does not exist!", category="error")
    
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return "<p>Logout</p>"
