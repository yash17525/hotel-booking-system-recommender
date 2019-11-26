from project import app, db
from project.model import Users, Hotels, Rooms, Facilities,Room_allotted,Drafts,Handler

if __name__ == '__main__':
    app.run(debug=True)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Hotels':Hotels, 'Rooms': Rooms, 'Facilities': Facilities, 'Users':Users,'Room_allotted':Room_allotted,'Drafts':Drafts,'Handler':Handler}