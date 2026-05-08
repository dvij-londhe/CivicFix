from flask import Blueprint, redirect, url_for, render_template, session, flash

notification = Blueprint('notification', __name__)

@notification.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for("auth.login"))
    
    return render_template("notifications.html")