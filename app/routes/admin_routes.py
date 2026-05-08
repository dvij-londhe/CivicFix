from flask import Blueprint, redirect, render_template, flash, session, url_for, jsonify, request
from app.models.complaint_model import get_all_reports, get_admin_stats, updateStatus, search_reports, get_category_stats, get_monthly_stats

admin = Blueprint("admin", __name__, url_prefix="/admin")

@admin.route("/dashboard")
def dashboard():
    if not session.get('isAdmin'):
        return redirect(url_for("auth.login"))

    status = request.args.get('status')
    query = request.args.get("q")
    reports = search_reports(query, status)
    stats = get_admin_stats()
    return render_template("admin/admin.html", stats=stats, reports=reports)

@admin.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):
    if not session.get('isAdmin'):
        return redirect(url_for("auth.login"))

    new_status = request.form.get("status")
    updateStatus(id, new_status)
    session.pop("_flashes", None)
    flash("Status updated successfully", "success")
    return redirect(request.referrer)


@admin.route("/reports")
def reports():
    if not session.get("isAdmin"):
        return redirect(url_for("auth.login"))

    status = request.args.get('status')
    query = request.args.get("q")
    reports = search_reports(query, status)
    count = len(reports)

    return render_template("admin/admin-reports.html", reports=reports, count=count)

@admin.route("/admin-analytics")
def admin_analytics():
    if not session.get("isAdmin"):
        return redirect(url_for("auth.login"))

    stats = get_admin_stats()
    return render_template("admin/admin-analytics.html", stats=stats)


@admin.route("/analytics_data")
def analytics_data():
    stats = get_admin_stats()
    categories = get_category_stats()
    monthly = get_monthly_stats()

    return jsonify({
        "total_reports": stats['total'],
        "pending": stats['pending'],
        "progress": stats['in_progress'],
        "resolved": stats['resolved'],
        "categories": categories,
        "monthly": monthly
    })

