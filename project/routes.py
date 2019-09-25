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

        if stu.check_password(form.password.data) and stu is not None:

            login_user(stu)
            flash('Logged in successfully.')
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('admin.index')

            return redirect(next)
    return render_template('login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Student(
                    name=form.name.data,
                    roll_no=form.roll_no.data,
                    branch=form.branch.data,
                    official_email=form.official_email.data,
                    password=form.password.data,
                    )
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('student.login'))
    return render_template('register.html', form=form)