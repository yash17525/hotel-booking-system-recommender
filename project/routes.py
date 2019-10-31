from flask import *
from project import db
from project.model import Student, SupplementaryExam, Teachers, Enrollments, Result
from project.forms import LoginForm, RegisterForm, SupplementaryExamForm, UpdateUserForm, TeachersLoginForm, ResultForm, EnrollNewForm
from flask_login import login_user, current_user, logout_user, login_required
from project.picture_handler import add_profile_pic

admin = Blueprint('admin',__name__)

@admin.route('/')
def index():
    # db.drop_all()
    # db.create_all()
    return render_template('index.html')

# @admin.route('/login', methods=['GET', 'POST'])
# def loginPage():
#     form = LoginForm()
#     if form.validate_on_submit():
#         student = Student.query.filter_by(rollno = form.rollno.data).first()
#         if student is not None and student.check_password(form.password.data) :
#             flash('Logged in successfully.')
#             login_user(student)
#             return redirect(url_for('admin.dashboard', rollno=student.rollno))
#         else:
#             flash('User is not registered.')
#             return render_template('login.html', form = form)
#     return render_template('login.html', form=form)


# @admin.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user = Student(
#                 name=form.name.data,
#                 rollno=form.rollno.data,
#                 branch=form.branch.data,
#                 official_email=form.official_email.data,
#                 password=form.password.data,
#                 )
#         db.session.add(user)
#         db.session.commit()
#         flash('Thanks for registering! Now you can login!')
#         return redirect(url_for('admin.loginPage'))
#     return render_template('register.html', form=form)

@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('admin.index'))

# @admin.route('/user/<rollno>/dashboard', methods=['POST', 'GET'])
# @login_required
# def dashboard(rollno):

#     form = UpdateUserForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             name = current_user.name
#             pic = add_profile_pic(form.picture.data, name)
#             current_user.profile_image = pic
#         db.session.commit()
#         return redirect(url_for('admin.dashboard', rollno=rollno))

#     profile_image = url_for('static', filename = 'profile_pics/' + current_user.profile_image)
#     student = Student.query.filter_by(rollno=rollno).first_or_404()
#     return render_template('dashboard.html', profile_image=profile_image, student=student, form=form)



# @admin.route('/user/<rollno>/register_exam', methods=['GET', 'POST'])
# @login_required
# def registerExam(rollno):
#     student = Student.query.filter_by(rollno=rollno).first_or_404()
#     form = SupplementaryExamForm()
#     if form.validate_on_submit():
#         supplementary_exam = SupplementaryExam(
#                                 rollno=form.rollno.data,
#                                 name=form.name.data,
#                                 subject_code=form.subject_code.data,            
#                                 branch=form.branch.data,
#                                 )
#         db.session.add(supplementary_exam)
#         db.session.commit()
#         flash('Thanks for registering for exam. Once your payment status is uploaded & detected you will be eligible to give the exam.')
#         return redirect(url_for('admin.dashboard', rollno=rollno))
#     elif request.method == 'GET':
#         form.rollno.data = current_user.rollno
#         form.name.data = current_user.name
#         form.branch.data = current_user.branch
#     return render_template('register_exam.html', form=form)

# @admin.route('/user/<rollno>/enrollments', methods=['GET', 'POST'])
# @login_required
# def enrollments(rollno):
#     enrollments = SupplementaryExam.query.filter_by(rollno=rollno)
#     return render_template('enrollments.html', enrollments=enrollments)


#############################################################################################################################################################

# Teacher's Area

@admin.route('/teacherslogin', methods=['GET', 'POST'])
def TeachersLogin():
    form = TeachersLoginForm()
    if form.validate_on_submit():
        teacher = Teachers.query.filter_by(email = form.email.data).first()
        if teacher is not None and teacher.check_password(form.password.data) :
            flash('Logged in successfully.')
            login_user(teacher)
            return redirect(url_for('admin.TeachersDashboard', email = teacher.email))
        else:
            flash('User is not registered.')
            return render_template('teacherslogin.html', form = form)
    return render_template('teacherslogin.html', form=form)

@admin.route('/<email>/teachersdashboard', methods=['GET', 'POST'])
def TeachersDashboard(email):
    teacher = Teachers.query.filter_by(email=email).first()
    enrollments = Enrollments.query.all()
    return render_template('teachersdashboard.html', teacher=teacher, enrollments=enrollments)

@admin.route('/current_enrollments_all')
def CurrentEnrollmentsAll():
    enrollments = Enrollments.query.all()
    return render_template('current_enrollments_all.html', enrollments = enrollments)


# Student's Area

@admin.route('/resultlogin', methods=['GET', 'POST'])
def ResultLogin():
    form = ResultForm()
    rollno = form.rollno.data
    if form.validate_on_submit():
        return redirect(url_for('admin.ResultDisplay', rollno = rollno))
    return render_template('resultlogin.html', form=form)

@admin.route('/<rollno>/result', methods=['GET', 'POST'])
def ResultDisplay(rollno):
    result = Result.query.filter_by(rollno=rollno).first()

    resultData = []

    resultData.append(['Roll No.', result.rollno, 0])
    resultData.append(['Name', result.name, 0])
    resultData.append(['Branch', result.branch, 0])

    subjectName1 = result.subject1.split(', ')[0]
    subjectMarks1 = result.subject1.split(', ')[1]
    if int(subjectMarks1) < 30:
        if not Enrollments.query.filter_by(rollno=result.rollno, subject=subjectName1).all():
            resultData.append([subjectName1, subjectMarks1, 1])
        else:
            resultData.append([subjectName1, subjectMarks1, 2])
    else:
        resultData.append([subjectName1, subjectMarks1, 0])
    subjectName2 = result.subject2.split(', ')[0]
    subjectMarks2 = result.subject2.split(', ')[1]
    if int(subjectMarks2) < 30:
        if not Enrollments.query.filter_by(rollno=result.rollno, subject=subjectName1).all():
            resultData.append([subjectName1, subjectMarks1, 1])
        else:
            resultData.append([subjectName1, subjectMarks1, 2])
    else:
        resultData.append([subjectName2, subjectMarks2, 0])

    return render_template('result.html', resultData = resultData)
    
@admin.route('/<rollno>/<subject>/enrollnew', methods=['GET', 'POST'])
def EnrollNew(rollno, subject):
    form = EnrollNewForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(rollno=rollno).first()
        print(student)
        if student is not None and student.check_password(form.password.data):
            newEnrollment = Enrollments(rollno=rollno, subject=subject)
            db.session.add(newEnrollment)
            db.session.commit()
        else:
            flash('Wrong password')
        return redirect(url_for('admin.ResultDisplay', rollno=rollno))
    elif request.method == 'GET':
        form.rollno.data = rollno
        form.subject.data = subject
    return render_template('enrollnew.html', form=form)
