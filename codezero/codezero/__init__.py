from flask import Flask, render_template, request, url_for, redirect, flash, abort
from peewee import *
import applicant_methods
import mentor_methods
import interview_methods
import forms
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

try:
    from forms import *
except Exception:
    from .forms import *
try:
    from models import *
except Exception:
    from .models import *
try:
    from interview_methods import *
except Exception:
    from .interview_methods import *

try:
    from applicant_methods import *
except Exception:
    from .applicant_methods import *

try:
    from mentor_methods import *
except Exception:
    from .mentor_methods import *


def user_list():
    array = []
    array.append(('Username', 'Password', 'Applicant name'))
    for item in User.select():
        if len(item.applicant) != 0:
            array.append((item.login, item.password, item.applicant[0].first_name))
        else:
            array.append((item.login, item.password))

    return array


def create_user(form):
    user = User.create(login=form.login.data, password=form.password.data, role='applicant')
    applicant = Applicant.create(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                                 city=str(form.city.data).lower(), user=user.id)

    Applicant_methods.assign_id_to_applicant(applicant)
    Applicant_methods.assign_school_to_applicant(applicant)
    interview_methods.assign_interview(applicant)



app = Flask(__name__)
app.secret_key = 'aosjndajndjansdojnasd.asdadas.d.d.1'

class_list = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None


@app.route('/', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = forms.LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class

        try:
            user = User.get(form.username.data == User.login)
        except DoesNotExist:
            flash('Invalid username or password.')
            return render_template('login.html', form=form)
        if user.password == form.password.data:
            login_user(user)
        else:
            flash('Invalid password.')
            return render_template('login.html', form=form)

        # next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
        #    return Flask.abort(400)
        if current_user.role == 'admin':
            return redirect(url_for('homepage'))
        elif current_user.role == 'applicant':
            return redirect(url_for('user_page'))
        elif current_user.role == 'mentor':
            return redirect(url_for('mentor_page'))
        else:
            return redirect(url_for('user_page'))
    return render_template('login.html', form=form)


@app.route('/admin', methods=["GET", "POST"])
@login_required
def homepage():
    if current_user.role != 'admin':
        abort(404)
    LISTA = Applicant_methods.get_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("index.html", LISTA=LISTA, list_length=list_length, class_list=class_list)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("login"))


@app.route('/user', methods=["GET", "POST"])
@login_required
def user_page():
    return render_template("user.html", user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user.role != 'admin':
            return redirect(url_for("user_page"))
        else:
            return redirect(url_for("homepage"))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You have successfully registered", "success")
        create_user(form)
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route('/mentor', methods=["GET", "POST"])
@login_required
def mentor_page():
    if current_user.is_authenticated:
        if current_user.role != 'mentor':
            abort(404)
    else:
        abort(404)
    mentor = Mentor.get(user_id=current_user.id)
    interviewlots = InterviewSlot.select().where(InterviewSlot.assigned_mentor == mentor.id)
    interviews = Interview.select().join(InterviewSlot).where(InterviewSlot.assigned_mentor == mentor.id)
    form = forms.AddInterviewSlot()
    if form.validate_on_submit():
        InterviewSlot.create(start=form.start.data, end=form.end.data, reserved=False, assigned_mentor=mentor.id)
        return redirect(url_for("mentor_page"))
    return render_template("mentor_site.html", interviewlots=interviewlots, interviews=interviews, form=form)


@app.route('/mentors', methods=["GET", "POST"])
@login_required
def mentors():
    LISTA = mentor_methods.get_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("mentors.html", LISTA=LISTA, list_length=list_length, class_list=class_list)


@app.route('/users', methods=["GET", "POST"])
def users():
    LISTA = user_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("users.html", LISTA=LISTA, list_length=list_length, class_list=class_list)


if __name__ == "__main__":
    app.run(debug=True)