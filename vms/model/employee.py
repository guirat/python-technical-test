from config import db, ma
from vms.model.vacation import Vacation
from marshmallow import fields


class Employee(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    postcode = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)

    vacations = db.relationship('Vacation', backref='employee', cascade='all, delete, delete-orphan', passive_deletes=True)


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        sqla_session = db.session

    vacations = fields.Nested("EmployeeVacationSchema", default=[], many=True)


class EmployeeVacationSchema(ma.SQLAlchemyAutoSchema):

    id = fields.Int()
    start_date = fields.Date()
    end_date = fields.Date()
    type = fields.Str()
    employee_id = fields.Int()
