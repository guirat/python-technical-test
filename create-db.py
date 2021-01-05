import datetime
import os
import random

from config import db
from vms.model.employee import Employee
from vms.model.team import Team, team_employee
from vms.model.vacation import Vacation
from faker import Faker


fake = Faker()

if os.path.exists('vms.db'):
    os.remove('vms.db')

db.create_all()


def add_team():
    for _ in range(3):
        team = Team(
            name=fake.color_name()
        )
        db.session.add(team)


def add_employees():
    for _ in range(10):
        customer = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.street_address(),
            postcode=fake.postcode(),
            email=fake.email(),
            phone=fake.phone_number()
        )
        db.session.add(customer)


def add_team_employee():
    teams = Team.query.all()
    employees = Employee.query.all()

    for team in teams:
        k = random.randint(1, 3)
        employee = random.sample(employees, k)
        team.employees.extend(employee)

    db.session.commit()


def add_vacations():
    employees = Employee.query.all()
    for _ in range(5):
        employee = random.choice(employees)
        start_dates = []
        for i in range(1,10):
            if len(start_dates) > 0:
                start = start_dates.pop()
                start_date = fake.date_between_dates(date_start=start+datetime.timedelta(days=1), date_end=start+datetime.timedelta(days=15))
            else:
                start_date = fake.date_between(start_date='-1y', end_date='today')
            end_date = fake.date_between_dates(date_start=start_date, date_end=start_date+datetime.timedelta(days=10))
            start_dates.append(end_date)
            vacation_type = random.choices(['NORMALE', 'UNPAID', 'RTT'], [60, 5, 25])[0]

            vacation = Vacation(
                employee_id=employee.id,
                start_date=start_date,
                end_date=end_date,
                type=vacation_type
            )
            db.session.add(vacation)


add_team()
add_employees()
add_team_employee()
add_vacations()
db.session.commit()
