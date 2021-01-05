from werkzeug.exceptions import Forbidden, Conflict

from config import db
from vms.core.helpers import format_date, verify_dates, \
    get_periods_intersection
from vms.model.vacation import Vacation, VacationSchema
from vms.core.session import get_all, get_specific_instance


def vacations_get_list(*args, **kwargs):
    vacations = get_all(Vacation, kwargs, "start_date")
    if "employee_id" in kwargs and len(kwargs['employee_id']) > 1:
        vacations_intersect = []
        for i in range(len(vacations) - 1):
            period = get_periods_intersection([[vacations[i].start_date,
                                                vacations[i].end_date],
                                               [vacations[i + 1].start_date,
                                                vacations[i + 1].end_date]])
            if period and [i for i in period]:
                vacations_intersect.append(period)
        return {'count': len(vacations_intersect),
                'results': vacations_intersect}
    vacation_schema = VacationSchema(many=True)
    data = vacation_schema.dump(vacations)
    response = {'count': len(data), 'results': data}
    return response


def vacations_post(**kwargs):
    del (kwargs['body'])
    kwargs['start_date'] = format_date(kwargs['start_date'])
    kwargs['end_date'] = format_date(kwargs['end_date'])
    verify_dates([kwargs['start_date'], kwargs['end_date']])
    if get_specific_instance(Vacation, kwargs):
        raise Conflict("Vacation already exist !")
    vacation_post = Vacation()
    vacations = get_all(Vacation, {"employee_id": [kwargs['employee_id']]})
    create_new_vacation = len(vacations) == 0
    for vacation in vacations:
        if vacation.start_date > kwargs['end_date'] or \
                kwargs['start_date'] > vacation.end_date:
            create_new_vacation = True
        elif vacation.type == kwargs['type']:
            create_new_vacation = False
            start_date = min(vacation.start_date, kwargs['start_date'])
            end_date = max(vacation.end_date, kwargs['end_date'])
            if vacation.start_date == start_date and \
                    vacation.end_date == end_date:
                vacation_post = vacation
            if vacation.start_date == start_date:
                if vacation.end_date == end_date:
                    vacation_post = vacation
                else:
                    vac = Vacation.query.get(vacation.id)
                    vac.end_date = kwargs['end_date']
                    vacation_post = vac
            elif vacation.end_date == end_date:
                vac = Vacation.query.get(vacation.id)
                vac.start_date = kwargs['start_date']
                vacation_post = vac
            else:
                create_new_vacation = True
            break
        else:
            raise Forbidden("Two overlapped vacations must have the same type")
    if create_new_vacation:
        vacation_post = Vacation(**kwargs)
        db.session.add(vacation_post)
    db.session.commit()
    employee_schema = VacationSchema()
    data = employee_schema.dump(vacation_post)
    return data


def vacation_get_by_id(id):
    vacation = Vacation.query.get(id)
    vacation_schema = VacationSchema()
    data = vacation_schema.dump(vacation)
    return data


def vacation_patch(id, **kwargs):
    vacation_updated = Vacation.query.get(id)
    del (kwargs['body'])
    kwargs['start_date'] = format_date(kwargs['start_date'])
    kwargs['end_date'] = format_date(kwargs['end_date'])
    verify_dates([kwargs['start_date'], kwargs['end_date']])
    for att, value in kwargs.items():
        setattr(vacation_updated, att, value)
    db.session.commit()
    vacation_schema = VacationSchema()
    data = vacation_schema.dump(Vacation.query.get(id))
    return data


def vacation_delete(id):
    vacation = Vacation.query.get(id)
    Vacation.query.filter_by(id=id).delete()
    vacation_schema = VacationSchema()
    data = vacation_schema.dump(vacation)
    db.session.commit()
    return data
