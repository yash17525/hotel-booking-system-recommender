from project import app, db
from project.model import Result, Enrollments, Teachers, Student

if __name__ == '__main__':
    app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student':Student, 'Result': Result, 'Teachers': Teachers, 'Enrollments': Enrollments}