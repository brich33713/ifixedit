from models import db, connect_db, Category, Subcategory, Trade, Issue, Issue_Parts, Part
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class Admin_Login_Form(FlaskForm):
    """Form for logging in admin"""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])