from config import db
from vms.core.helpers import format_date


def get_all(model, filter, order_by=None):
    query = db.session.query(model)
    for attr, value in filter.items():
        if attr == "start_date":
            query = query.filter(getattr(model, attr) >= format_date(value))
        elif attr == "end_date":
            query = query.filter(getattr(model, attr) <= format_date(value))
        elif attr == "employee_id":
            query = query.filter(getattr(model, attr).in_(value))
        else:
            query = query.filter(getattr(model, attr) == value)
    if order_by:
        results = query.order_by(getattr(model, order_by)).all()
    else:
        results = query.all()
    return results


def get_specific_instance(model, filter):
    query = db.session.query(model)
    for attr, value in filter.items():
        query = query.filter(getattr(model, attr) == value)
    results = query.all()
    return results
