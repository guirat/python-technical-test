from config import db, ma
from marshmallow import fields


class Vacation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id',
                                                      ondelete='CASCADE'))


class VacationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vacation
        sqla_session = db.session

    employee = fields.Nested("VacationEmployeeSchema", default=[])


class VacationEmployeeSchema(ma.SQLAlchemyAutoSchema):

    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    address = fields.Str()
    postcode = fields.Str()
    email = fields.Str()
    phone = fields.Str()
