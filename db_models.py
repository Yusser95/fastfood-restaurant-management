
from app import db
import datetime
from datetime import datetime, timedelta



class EmployeeModel(db.Model):
    __tablename__ = "employee"
    id = db.Column(db.Integer , primary_key=True)
    firstname = db.Column(db.String(40), nullable=True)
    lastname = db.Column(db.String(40), nullable=True)
    nickname = db.Column(db.String(40), nullable=True)
    address = db.Column(db.String(40), nullable=True)
    phone_number = db.Column(db.String(40), nullable=True)
    price_per_hour = db.Column(db.Float, nullable=True)
    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)

    def __init__(self,firstname,lastname,nickname,address,phone_number,price_per_hour):
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.address = address
        self.phone_number = phone_number
        self.price_per_hour = price_per_hour
        self.created_at = datetime.utcnow()


    def _update(self,firstname,lastname,nickname,address,phone_number,price_per_hour):
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.address = address
        self.phone_number = phone_number
        self.price_per_hour = price_per_hour
        self.updated_at = datetime.utcnow()


    def get_salary_by_month(self,date_filter):
        amount = 0
        objs = EmployeeSalaryModel.query.filter_by(employee_id=self.id,date_filter=date_filter,is_deleted=0).all()#self.salaries.any(EmployeeSalaryModel.date_filter == date_filter)#.filter_by(date_filter = date_filter ,is_deleted=0).first()
        if objs:
            for obj in objs:
                amount += obj.amount

        amount += self.get_advances_by_month(date_filter)

        return amount


    def get_advances_by_month(self,date_filter):
        amount = 0
        objs = EmployeeAdvanceModel.query.filter_by(employee_id=self.id,date_filter=date_filter,is_deleted=0).all()#self.advances.any(EmployeeAdvanceModel.date_filter == date_filter)#.filter_by(date_filter = date_filter ,is_deleted=0).all()
        if objs:
            for obj in objs:
                amount += obj.amount

        return amount


    def get_hours_by_month(self,date_filter):
        hours = 0
        objs = EmployeeHoursModel.query.filter_by(employee_id=self.id,date_filter=date_filter,is_deleted=0).all() #self.hours.any(EmployeeHoursModel.date_filter == date_filter)#.filter_by(date_filter = date_filter ,is_deleted=0).all()
        if objs:
            for obj in objs:
                hours += obj.hours

        return hours

    def calculate_salary_by_month(self, date_filter):
        amount = self.get_hours_by_month(date_filter) * self.price_per_hour - self.get_advances_by_month(date_filter)
        return amount



    # to do access month salary ,month advance ,month hour



class EmployeeSalaryModel(db.Model):
    __tablename__ = "employee_salary"
    id = db.Column(db.Integer , primary_key=True)
    date_filter = db.Column(db.String(40), nullable=True)

    amount = db.Column(db.Float, nullable=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'),
        nullable=True)
    employee = db.relationship('EmployeeModel', lazy=True,
        backref=db.backref('salaries', lazy=True))

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)

    is_deleted = db.Column(db.Integer , default=0)


    def __init__(self,amount,employee_id):
        self.amount = amount
        self.employee_id = employee_id
        self.created_at = datetime.utcnow()
        self.date_filter = "{}-{}".format(str(self.created_at.year), str(self.created_at.month))


    def _update(self,amount,employee_id):
        self.amount = amount
        self.employee_id = employee_id
        self.updated_at = datetime.utcnow()


class EmployeeAdvanceModel(db.Model):
    __tablename__ = "employee_advance"
    id = db.Column(db.Integer , primary_key=True)
    date_filter = db.Column(db.String(40), nullable=True)

    amount = db.Column(db.Float, nullable=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'),
        nullable=True)
    employee = db.relationship('EmployeeModel', lazy=True,
        backref=db.backref('advances', lazy=True))

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)

    is_deleted = db.Column(db.Integer , default=0)


    def __init__(self,amount,employee_id):
        self.amount = amount
        self.employee_id = employee_id
        self.created_at = datetime.utcnow()
        self.date_filter = "{}-{}".format(str(self.created_at.year), str(self.created_at.month))


    def _update(self,amount,employee_id):
        self.amount = amount
        self.employee_id = employee_id
        self.updated_at = datetime.utcnow()


class EmployeeHoursModel(db.Model):
    __tablename__ = "employee_day_hours"
    id = db.Column(db.Integer , primary_key=True)
    date_filter = db.Column(db.String(40), nullable=True)

    started_at  = db.Column( db.DateTime , nullable=True)
    finished_at = db.Column( db.DateTime , nullable=True)
    hours = db.Column(db.Float, nullable=True)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'),
        nullable=True)
    employee = db.relationship('EmployeeModel', lazy=True,
        backref=db.backref('hours', lazy=True))

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)

    is_deleted = db.Column(db.Integer , default=0)


    def __init__(self,started_at,finished_at,employee_id):
        started_at = datetime.strptime(started_at, '%m/%d/%Y %I:%M %p')
        finished_at = datetime.strptime(finished_at, '%m/%d/%Y %I:%M %p')
        self.started_at = started_at
        self.finished_at = finished_at

        self.hours = 0
        if finished_at > started_at:
            tmp = finished_at - started_at
            self.hours = tmp.seconds / 60 / 60

        self.employee_id = employee_id
        self.created_at = datetime.utcnow()

        self.date_filter = "{}-{}".format(str(self.created_at.year), str(self.created_at.month))


    def _update(self,started_at,finished_at,employee_id):
        started_at = datetime.strptime(started_at, '%m/%d/%Y %I:%M %p')
        finished_at = datetime.strptime(finished_at, '%m/%d/%Y %I:%M %p')
        self.started_at = started_at
        self.finished_at = finished_at
        
        self.hours = 0
        if finished_at > started_at:
            tmp = finished_at - started_at
            self.hours = tmp.seconds / 60 / 60

        self.employee_id = employee_id
        self.updated_at = datetime.utcnow()
 
