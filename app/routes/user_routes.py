from flask import Blueprint, redirect, url_for, render_template, session, flash
from app.models.complaint_model import get_reports_info, get_recent_reports
user_bp = Blueprint("user", __name__)

@user_bp.route("/dashboard")
def dashboard():
    if ('user_id' not in session) or session.get('isAdmin'):
        return redirect(url_for("auth.login"))


    info = get_reports_info(session['user_id'])
    recent_reports = get_recent_reports(session['user_id'])

    return render_template('dashboard.html', info=info, recent_reports=recent_reports)
