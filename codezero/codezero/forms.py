from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
								Length, EqualTo)

try:
    from models import User, Applicant
except Exception:
    from .models import User, Applicant


# from models import User


def username_exists(form, field):
    if User.select().where(User.login == field.data).exists():
		raise ValidationError("User already exists")

def email_exists(form, field):
    if Applicant.select().where(Applicant.email == field.data).exists():
		raise ValidationError("Email already exists")

class RegisterForm(Form):
    login = StringField(
		"Username",
		validators=[
			DataRequired(),
			Regexp(r'^[a-zA-Z0-9_]+$',
				message=("Username should be one word, letters, "
						"numbers, and underscores only.")
			),
            username_exists
		])

    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   )
        ])
    last_name = StringField(
        "Last name",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   )
        ])
	email = StringField(
		"Email",
		validators=[
			DataRequired(),
			Email(),
			email_exists
			])

    city = StringField(
        "City",
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9_]+$',
                   message=("Username should be one word, letters, "
                            "numbers, and underscores only.")
                   )
        ])


	password = PasswordField(
		"Password",
		validators=[
			DataRequired(),
			Length(min=2),
			EqualTo("password2", message="Passwords must match")])
	password2 = PasswordField(
		"Confirm Password",
		validators=[DataRequired()])

class LoginForm(Form):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])