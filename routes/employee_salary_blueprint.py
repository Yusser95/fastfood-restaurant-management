from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

employee_salary_blueprint = Blueprint("employee_salary_blueprint",__name__)

from app import db



@employee_salary_blueprint.route('/admin/employee_salary/data')
@employee_salary_blueprint.route('/admin/employee_salary/data/<employee_id>')
@flask_login.login_required
def data(employee_id=None):
	from db_models import EmployeeSalaryModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(EmployeeSalaryModel.id),
        ColumnDT(EmployeeSalaryModel.employee_id),
        ColumnDT(EmployeeSalaryModel.date_filter),
        ColumnDT(EmployeeSalaryModel.amount),
        ColumnDT(EmployeeSalaryModel.is_deleted),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(EmployeeSalaryModel).order_by(EmployeeSalaryModel.id)

	if employee_id is not None:
		query = query.filter_by(employee_id=employee_id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@employee_salary_blueprint.route("/admin/employee_salary/index" , methods =["GET"])
@employee_salary_blueprint.route("/admin/employee_salary/index/<employee_id>" , methods =["GET"])
@flask_login.login_required
def index(employee_id=None):
	return render_template('admin/employee_salary/index.html',employee_id=employee_id)


@employee_salary_blueprint.route("/admin/employee_salary/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import EmployeeSalaryModel
	item = EmployeeSalaryModel.query.get(id)
	return render_template('admin/employee_salary/show.html' , item = item)

@employee_salary_blueprint.route("/admin/employee_salary/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import EmployeeSalaryModel
	print("deleted " , id)
	obj = EmployeeSalaryModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1

		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/employee_salary/index')

@employee_salary_blueprint.route("/admin/employee_salary/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import EmployeeSalaryModel
	print(id)
	# edit
	if request.method == "POST":

		obj = EmployeeSalaryModel.query.get(id)

		obj.employee_id = request.form.get('employee_id')
		obj.amount = request.form.get('amount')

		
		db.session.commit()
		

		return redirect('/admin/employee_salary/index')
	# show  one row
	elif request.method == "GET":

		item = EmployeeSalaryModel.query.get(id)
		return render_template('/admin/employee_salary/edit.html',item = item)
	return "404"


@employee_salary_blueprint.route("/admin/employee_salary/create" , methods =["GET" , "POST"])
@employee_salary_blueprint.route("/admin/employee_salary/create/<employee_id>" , methods =["GET"])
@flask_login.login_required
def create(employee_id=None):
	from db_models import EmployeeSalaryModel
	# edit
	if request.method == "POST":

		employee_id = request.form.get('employee_id')
		amount = request.form.get('amount')

		obj = EmployeeSalaryModel(employee_id=employee_id , amount=amount )
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/employee_salary/index')
	# show  one row
	elif request.method == "GET":
		if employee_id is not None:
			return render_template('/admin/employee_salary/create.html',employee_id=employee_id)
	return "404"


