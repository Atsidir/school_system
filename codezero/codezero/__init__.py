from flask import Flask, render_template, request, url_for, redirect, flash
from peewee import *
import applicant_methods
import mentor_methods
import forms
from flask_login import LoginManager, UserMixin, login_required, login_user,logout_user,current_user

try:
    from models import *
except Exception:
    from .models import *

try:
    from applicant_methods import *
except Exception:
    from .applicant_methods import *

try:
    from mentor_methods import *
except Exception:
    from .mentor_methods import *

app = Flask(__name__)
app.secret_key = 'aosjndajndjansdojnasd.asdadas.d.d.1'

class_list = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get(User.id==user_id)
    except DoesNotExist:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = forms.LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class


        user = User.get(form.username.data == User.login)
        login_user(user)

        flash('Logged in successfully.')

        #next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
        #    return Flask.abort(400)
        return redirect(url_for('user_page'))
    return render_template('login.html', form=form)



@app.route('/', methods=["GET", "POST"])
def homepage():
    LISTA = applicant_methods.get_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("index.html", LISTA=LISTA, list_length=list_length, class_list=class_list)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You've been logged out.", "success")
	return redirect(url_for("homepage"))

@app.route('/user',methods=["GET", "POST"])
@login_required
def user_page():

    return str("{} magic happens {}").format(current_user.login,current_user.password)


@app.route('/mentors', methods=["GET", "POST"])
def mentors():
    LISTA = mentor_methods.get_list()
    list_length = int(len(LISTA))
    if request.method == "GET":
        return render_template("mentors.html", LISTA=LISTA, list_length=list_length, class_list=class_list)


if __name__ == "__main__":
    app.run(debug=True)
