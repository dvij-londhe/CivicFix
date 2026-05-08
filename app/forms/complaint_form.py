from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ComplaintForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(message='Title can\'t be empty!')])
    description = TextAreaField("Description", validators=[DataRequired()])
    category = SelectField("Category",
                           choices=[
                               ("", "-- Select Category --"),
                               ("pothole", "Pothole"),
                               ("garbage", "Garbage"),
                               ("street light", "Street Light"),
                               ("water leakage", "Water Leakage"),
                               ("drainage", "Drainage Issue"),
                               ("traffic signal", "Traffic Signal Problem"),
                               ("electricity", "Electricity"),
                               ("other", "Other")
                           ])

    location = StringField("Location", validators=[DataRequired(message="Location is required!")])
    coordinates = StringField("Co-ordinates", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='Images Only!')])
    submit = SubmitField("Submit Complaint")