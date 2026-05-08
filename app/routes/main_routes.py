from flask import Blueprint, redirect, url_for, render_template

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/learnmore")
def learn_more():
    return render_template("learnmore.html")