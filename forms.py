from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'User'), ('contractor', 'Contractor')], validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ComplaintForm(FlaskForm):
    district = StringField('District', validators=[DataRequired(), Length(max=100)])
    corporation_type = SelectField('Corporation Type', 
                                   choices=[('District Corporation', 'District Corporation'),
                                           ('Municipality', 'Municipality'),
                                           ('Panchayath', 'Panchayath')],
                                   validators=[DataRequired()])
    road_name = StringField('Road Name', validators=[DataRequired(), Length(max=200)])
    national_highway = StringField('National Highway (if applicable)', validators=[Optional(), Length(max=100)])
    landmark = StringField('Landmark (School, Hospital, etc.)', validators=[DataRequired(), Length(max=200)])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    description = TextAreaField('Description of the Issue', validators=[DataRequired()])

class AcknowledgementForm(FlaskForm):
    acknowledgement = TextAreaField('Acknowledgement', validators=[DataRequired()])
