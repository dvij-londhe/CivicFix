from flask import Blueprint, redirect, url_for, render_template, session, flash
import bcrypt
from app.forms.auth_form import LoginForm, RegistrationForm
from app.models.user_model import create_user, get_user_by_email
from app.models.admin_model import get_admin_by_email

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():

    if 'user_id' in session:
        return redirect(url_for('user.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        admin = get_admin_by_email(email)
        if admin and bcrypt.checkpw(password.encode('utf-8'), admin['password'].encode('utf-8')):
            session['user_id'] = admin['id']
            session['username'] = admin['name']
            session['isAdmin'] = True
            session.pop("_flashes", None)
            flash("Login Successful", "success")
            return redirect(url_for("admin.dashboard"))


        user = get_user_by_email(email)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                session['user_id'] = user['id']
                session['username'] = user['name']
                session['isAdmin'] = False
                session.pop("_flashes", None)
                flash("Login Successful", "success")
                return redirect(url_for("user.dashboard"))
        else:
            flash("Invalid email or password", "error")
            # return redirect(url_for("auth.login"))
    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        create_user(name, email, hashed_pw)
        session.pop("_flashes", None)
        flash("Registration Successful, Please login", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))