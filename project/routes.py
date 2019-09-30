from flask import *
from project import db
from project.model import Student
from project.forms import LoginForm, RegisterForm
from flask_login import login_user, current_user, logout_user, login_required

admin = Blueprint('admin',__name__)

@admin.route('/')
def index():
    return render_template('index.html')

@admin.route('/login', methods=['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        stu = Student.query.filter_by(rollno = form.rollno.data).first()

        if stu is not None and stu.check_password(form.password.data) :

            flash('Logged in successfully.')
            login_user(stu)
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('admin.index')

            return redirect(next)

        else:
            flash('User is not registered.')
            return render_template('login.html', form = form)

    return render_template('login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Student(
                    name=form.name.data,
                    rollno=form.rollno.data,
                    branch=form.branch.data,
                    official_email=form.official_email.data,
                    password=form.password.data,
                    )
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('admin.loginPage'))
    return render_template('register.html', form=form)