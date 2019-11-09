from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

employee_blueprint = Blueprint("employee_blueprint",__name__)

from app import db



@employee_blueprint.route('/admin/employee/data')
@flask_login.login_required
def data():
	from db_models import EmployeeModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(EmployeeModel.id),
        ColumnDT(EmployeeModel.firstname),
        ColumnDT(EmployeeModel.lastname),
        ColumnDT(EmployeeModel.nickname),
        ColumnDT(EmployeeModel.is_deleted),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(EmployeeModel).order_by(EmployeeModel.id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@employee_blueprint.route("/admin/employee/index" , methods =["GET"])
@flask_login.login_required
def index():
	return render_template('admin/employee/index.html')


@employee_blueprint.route("/admin/employee/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import EmployeeModel
	item = EmployeeModel.query.get(id)
	return render_template('admin/employee/show.html' , item = item)

@employee_blueprint.route("/admin/employee/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import EmployeeModel
	print("deleted " , id)
	obj = EmployeeModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1
			for o in obj.salaries:
				o.is_deleted = 1
			for o in obj.advances:
				o.is_deleted = 1
			for o in obj.hours:
				o.is_deleted = 1
		else:
			obj.is_deleted = 0
			for o in obj.salaries:
				o.is_deleted = 0
			for o in obj.advances:
				o.is_deleted = 0
			for o in obj.hours:
				o.is_deleted = 0

	db.session.commit()
	return redirect('/admin/employee/index')

@employee_blueprint.route("/admin/employee/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import EmployeeModel
	print(id)
	# edit
	if request.method == "POST":

		obj = EmployeeModel.query.get(id)

		obj.firstname = request.form.get('firstname')
		obj.lastname = request.form.get('lastname')
		obj.nickname = request.form.get('nickname')
		obj.address = request.form.get('address')
		obj.phone_number = request.form.get('phone_number')
		obj.price_per_hour = request.form.get('price_per_hour')

		
		db.session.commit()
		

		return redirect('/admin/employee/index')
	# show  one row
	elif request.method == "GET":

		item = EmployeeModel.query.get(id)
		return render_template('/admin/employee/edit.html',item = item)
	return "404"


@employee_blueprint.route("/admin/employee/create" , methods =["GET" , "POST"])
@flask_login.login_required
def create():
	from db_models import EmployeeModel
	# edit
	if request.method == "POST":

		firstname = request.form.get('firstname')
		lastname = request.form.get('lastname')
		nickname = request.form.get('nickname')
		address = request.form.get('address')
		phone_number = request.form.get('phone_number')
		price_per_hour = request.form.get('price_per_hour')

		obj = EmployeeModel(firstname=firstname , lastname=lastname , nickname=nickname , address=address , phone_number=phone_number , price_per_hour=price_per_hour)
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/employee/index')
	# show  one row
	elif request.method == "GET":
		return render_template('/admin/employee/create.html')
	return "404"



@employee_blueprint.route("/admin/employee/business/<business_type>/<employee_id>" , methods =["POST"])
@flask_login.login_required
def business(business_type,employee_id):
	from db_models import EmployeeModel
	# edit
	response = {'status':'fail'}

	obj = EmployeeModel.query.get(employee_id)
	if obj:
		date_filter = request.form.get('date_filter')
		print(date_filter)
		if date_filter:
			if business_type == 'hours':
				response['result'] = obj.get_hours_by_month(date_filter)
			elif business_type == 'advance':
				response['result'] = obj.get_advances_by_month(date_filter)
			elif business_type == 'salary_without_advance':
				response['result'] = obj.calculate_salary_by_month(date_filter)
			elif business_type == 'salary_with_advance':
				response['result'] = obj.get_salary_by_month(date_filter)

				
			response['status'] = 'success'
		


	return jsonify(response)



