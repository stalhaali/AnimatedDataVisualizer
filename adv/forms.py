from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from adv.models import User

class RegistrationForm(FlaskForm):
    """
    A class to represent a Flask form for registrating a user.

    ...

    Attributes
    ----------
    username : StringField
        username of the user
    email : StringField
        email of the user
    password : PasswordField
        password of the user
    confirm_password: PasswordField
        password used to confirm password for the user
    submit: SubmitField
        submit button used to submit user information
    """
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
    """
    A class to represent a Flask form for loging in a user.

    ...

    Attributes
    ----------
    email : StringField
        email of the user
    password : PasswordField
        password of the user
    remember: BooleanField
        used to keep user logged in when closing tab
    submit: SubmitField
        submit button used to submit user login information
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateGraphBarForm(FlaskForm):
    """
    A class to represent a Flask form for creating a BAR graph

    ...

    Attributes
    ----------
    spreadsheet : FileField
        data used for creating the graph
    dropdown_list : list
        contains choices to sort graph by (high or low)
    dropdown_list2 : list
        contains choices for orientation of graph, horizontal or vertical
    dropdown_list3 : list
        contains choices for number of bars in graph, 1-10
    title: StringField
        title of graph
    sort: SelectField
        drop down for sorting choice
    orientation: SelectField
        drop down for orientation choice
    bars_visible: SelectField
        drop down for number of bars choice
    submit: SubmitField
        submit button used to submit user bar graph information
    """
    spreadsheet = FileField("Upload Data (Excel Document)", validators=[FileAllowed(['csv']), DataRequired()])
    dropdown_list = ['Ascending', 'Descending'] # You can get this from your model
    dropdown_list2= ['Horizontal', 'Vertical']
    dropdown_list3= [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    title = StringField('Title', validators=[DataRequired()])
    sort = SelectField('Sort by', choices=dropdown_list, default=1)
    orientation = SelectField('Orientation', choices=dropdown_list2, default=1)
    bars_visible = SelectField('Bars Visible', choices=dropdown_list3, default=5)
    submit = SubmitField('Create!')

class CreateGraphNonBarForm(FlaskForm):
    """
    A class to represent a Flask form for creating a graph other than a Bar Graph

    ...

    Attributes
    ----------
    spreadsheet : FileField
        data used for creating the graph
    title: StringField
        title of graph
    submit: SubmitField
        submit button used to submit user graph information
    """
    spreadsheet = FileField("Upload Data (Excel Document)", validators=[FileAllowed(['csv']), DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create!')

class DeleteGraphForm(FlaskForm):
    """
    A class to represent a Flask form for deleting a graph

    ...

    Attributes
    ----------
    submit: SubmitField
        submit button used to confirm graph deletion
    """
    submit = SubmitField('Delete!')

class VideoForm(FlaskForm):
    """
    A class to represent a Flask form for saving a graph

    ...

    Attributes
    ----------
    submit: SubmitField
        submit button used to save graph in user's database
    """
    submit = SubmitField('Save Video')

class ContactForm(FlaskForm):
    """
    A class to represent a Flask form for Contacting creators.

    ...

    Attributes
    ----------
    name : StringField
        name of the user
    email : StringField
        email of the user
    content: TextAreaField
        content of email
    submit: SubmitField
        submit button used to send email
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')

