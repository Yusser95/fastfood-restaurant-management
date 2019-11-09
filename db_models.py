
from app import db
import datetime
from datetime import datetime, timedelta



class IngredientSectionModel(db.Model):
    __tablename__ = 'ingredient_sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)

    def __init__(self,name):
        self.name = name
        self.created_at = datetime.utcnow()


    def _update(self,name):
        self.name = name
        self.updated_at = datetime.utcnow()



class RecipeTagModel(db.Model):
    __tablename__ = 'recipe_tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)


    def __init__(self,name):
        self.name = name
        self.created_at = datetime.utcnow()


    def _update(self,name):
        self.name = name
        self.updated_at = datetime.utcnow()




class UnitModel(db.Model):
    __tablename__ = 'unit'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    value_per_kg = db.Column(db.String(50), nullable=False)

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)


    def __init__(self,name,value_per_kg):
        self.name = name
        self.value_per_kg = value_per_kg
        self.created_at = datetime.utcnow()


    def _update(self,name,value_per_kg):
        self.name = name
        self.value_per_kg = value_per_kg
        self.updated_at = datetime.utcnow()


class RecipeModel(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('recipe_tags.id', ondelete='CASCADE'),
        nullable=True)
    tag = db.relationship('RecipeTagModel',lazy=True)

    name = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(300), nullable=True)
    direction = db.Column(db.String(1000), nullable=False)

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)

    def __init__(self,name,image,direction,tag_id,ingredients,amounts,units):
        self.name = name
        self.image = image
        self.direction = direction
        self.tag_id = tag_id
        self.created_at = datetime.utcnow()

        for i in range(len(ingredients)):
            Ingr = RecipeIngredientModel(amount=amounts[i],unit_id=units[i])

            temp_ingr = IngredientModel.query.filter_by(name=ingredients[i]).first()
            if not temp_ingr:
                temp_ingr = IngredientModel(name=ingredients[i])
            Ingr.ingredient = temp_ingr

            self.ingredients.append(Ingr)


    def _update(self,name,image,direction,tag_id,ingredients,amounts,units):
        self.name = name
        self.image = image
        self.direction = direction
        self.tag_id = tag_id
        self.updated_at = datetime.utcnow()

        for ing in self.ingredients:
            if ing.ingredient.name not in ingredients:
                db.session.delete(ing)
            else:
                flag = True
                for i in range(len(ingredients)):
                    if ing.ingredient.name == ingredients[i] and ing.unit_id == units[i] and str(ing.amount) == str(amounts[i]):
                        print("found")
                        ingredients.pop(i)
                        units.pop(i)
                        amounts.pop(i)
                        flag =False
                        break
                if flag:
                    db.session.delete(ing)



        for i in range(len(ingredients)):
            Ingr = RecipeIngredientModel(amount=amounts[i],unit_id=units[i])

            temp_ingr = IngredientModel.query.filter_by(name=ingredients[i]).first()
            if not temp_ingr:
                temp_ingr = IngredientModel(name=ingredients[i])
            Ingr.ingredient = temp_ingr


            self.ingredients.append(Ingr)





class RecipeIngredientModel(db.Model):
    __tablename__ = 'recipe_has_ingredient'

    id = db.Column(db.Integer, primary_key=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', ondelete='CASCADE'),
        nullable=True)
    recipe = db.relationship('RecipeModel',lazy=True,
        backref=db.backref('ingredients', lazy=True))

    ingr_id = db.Column("ingredient_id",db.Integer, db.ForeignKey('ingredient.id', ondelete='CASCADE'),
        nullable=True)
    ingredient = db.relationship('IngredientModel',lazy=True,
        backref=db.backref('recipes_ingr', lazy=True))

    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id', ondelete='CASCADE'),
        nullable=True)
    unit = db.relationship('UnitModel',lazy=True,
        backref=db.backref('recipes_ingr', lazy=True))

    amount = db.Column(db.Float, unique=False, nullable=True)

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)

    def __init__(self  ,amount,unit_id):
        # self.ingr_name = ingr_name
        self.amount = amount
        self.unit_id = unit_id
        self.created_at = datetime.utcnow()

    def _update(self  ,amount,unit_id):
        # self.ingr_name = ingr_name
        self.amount = amount
        self.unit_id = unit_id
        self.updated_at = datetime.utcnow()



class IngredientModel(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    section_id = db.Column(db.Integer, db.ForeignKey('ingredient_sections.id', ondelete='CASCADE'),
        nullable=True)
    section = db.relationship('IngredientSectionModel',lazy=True)

    created_at = db.Column( db.DateTime , nullable=True)
    updated_at = db.Column( db.DateTime , nullable=True)
    is_deleted = db.Column(db.Integer , default=0)

    def __init__(self,name,section_id):
        self.name = name
        self.section_id = section_id
        self.created_at = datetime.utcnow()


    def _update(self,name,section_id):
        self.name = name
        self.section_id = section_id
        self.updated_at = datetime.utcnow()








#####################################################################################

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
        amount = self.get_hours_by_month(date_filter) * self.price_per_hour - self.get_salary_by_month(date_filter)
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
 
