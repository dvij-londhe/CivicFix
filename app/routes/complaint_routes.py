from flask import Blueprint, render_template, url_for, session, redirect, current_app, flash, request
from werkzeug.utils import secure_filename
from app.forms.complaint_form import ComplaintForm
from app.models.complaint_model import create_complaint, get_all_reports_by_id
from app.models.notification_model import create_notification
import os


complaint = Blueprint("complaint", __name__)

#View Complaints
@complaint.route("/myreports")
def my_reports():
    if 'user_id' not in session:
        return redirect(url_for("auth.login"))

    if session.get('isAdmin'):
        return redirect(url_for("auth.login"))


    status = request.args.get('status')
    all_reports = get_all_reports_by_id(session['user_id'], status)
    return render_template("myreports.html", all_reports = all_reports)



#Create Complaint
@complaint.route("/report", methods=["POST", "GET"])
def report():
    if 'user_id' not in session:
        return redirect(url_for("auth.login"))

    form = ComplaintForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        location = form.location.data
        co_ordinates = form.coordinates.data
        image_file = form.image.data
        filename = None

        if image_file:
            filename = secure_filename(image_file.filename)

            upload_path = os.path.join(
                current_app.root_path,
                'static\\uploads',
                filename
            )

            image_file.save(upload_path)

        create_complaint(session['user_id'],
                         title,
                         description,
                         category,
                         location,
                         co_ordinates,
                         filename)
        session.pop("_flashes", None)
        flash("Complaint submitted successfully", "success")
        return redirect(url_for("user.dashboard"))

    return render_template("report.html", form=form)