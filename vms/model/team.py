from config import db
from vms.model.employee import Employee

team_employee = db.Table('team_employee',
                         db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
                         db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True)
                         )


class Team(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    employees = db.relationship('Employee', secondary=team_employee)
