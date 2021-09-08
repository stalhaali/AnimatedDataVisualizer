from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from adv.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateGraphBarForm(FlaskForm):
    spreadsheet = FileField("Upload Data (Excel Document)", validators=[FileAllowed(['csv']), DataRequired()])
    dropdown_list = ['Highest', 'Lowest'] # You can get this from your model
    dropdown_list2= ['Horizontal', 'Vertical']
    dropdown_list3= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    title = StringField('Title', validators=[DataRequired()])
    sort = SelectField('Sort by', choices=dropdown_list, default=1)
    orientation = SelectField('Orientation', choices=dropdown_list2, default=1)
    bars_visible = SelectField('Bars Visible', choices=dropdown_list3, default=5)
    submit = SubmitField('Create!')

class CreateGraphNonBarForm(FlaskForm):
    spreadsheet = FileField("Upload Data (Excel Document)", validators=[FileAllowed(['csv']), DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create!')

class DeleteGraphForm(FlaskForm):
    submit = SubmitField('Delete!')

class VideoForm(FlaskForm):
    submit = SubmitField('Save Video')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')

