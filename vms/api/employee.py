from config import db, session
from vms.core.session import get_all
from vms.model.employee import Employee, EmployeeSchema
from sqlalchemy.sql import text

from vms.model.vacation import Vacation


def employees_get_list(**kwargs):
    employees = get_all(Employee, kwargs)
    employee_schema = EmployeeSchema(many=True)
    data = employee_schema.dump(employees)
    return data


def employee_get_by_id(id):
    employee = Employee.query.get(id)
    employee_schema = EmployeeSchema()
    data = employee_schema.dump(employee)
    return data


def employees_post(**kwargs):
    del(kwargs['body'])
    employee = Employee(**kwargs)
    db.session.add(employee)
    db.session.commit()
    employee_schema = EmployeeSchema()
    data = employee_schema.dump(employee)
    return data


def employee_patch(id, **kwargs):
    employee_updated = Employee.query.get(id)
    del (kwargs['body'])
    for att, value in kwargs.items():
        setattr(employee_updated, att, value)
    db.session.commit()
    employee_schema = EmployeeSchema()
    data = employee_schema.dump(Employee.query.get(id))
    return data


def employee_delete(id):
    employee = Employee.query.get(id)
    employee_vacations_list = Vacation.query.filter_by(employee_id=id)
    result = Employee.query.filter_by(id=id).delete()
    if result:
        employee_vacations_list.delete()
    # db.session.query(Employee).filter(Employee.id == id).delete()
    employee_schema = EmployeeSchema()
    data = employee_schema.dump(employee)
    db.session.commit()
    return data
