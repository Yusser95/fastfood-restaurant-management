from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

employee_hours_blueprint = Blueprint("employee_hours_blueprint",__name__)

from app import db



@employee_hours_blueprint.route('/admin/employee_hours/data')
@employee_hours_blueprint.route('/admin/employee_hours/data/<employee_id>')
@flask_login.login_required
def data(employee_id=None):
	from db_models import EmployeeHoursModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(EmployeeHoursModel.id),
        ColumnDT(EmployeeHoursModel.employee_id),
        ColumnDT(EmployeeHoursModel.date_filter),
        ColumnDT(EmployeeHoursModel.started_at),
        ColumnDT(EmployeeHoursModel.finished_at),
        ColumnDT(EmployeeHoursModel.hours),
        ColumnDT(EmployeeHoursModel.is_deleted),
        ColumnDT(EmployeeHoursModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(EmployeeHoursModel).order_by(EmployeeHoursModel.id)

	if employee_id is not None:
		query = query.filter_by(employee_id=employee_id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@employee_hours_blueprint.route("/admin/employee_hours/index" , methods =["GET"])
@employee_hours_blueprint.route("/admin/employee_hours/index/<employee_id>" , methods =["GET"])
@flask_login.login_required
def index(employee_id=None):
	return render_template('admin/employee_hours/index.html',employee_id=employee_id)


@employee_hours_blueprint.route("/admin/employee_hours/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import EmployeeHoursModel
	item = EmployeeHoursModel.query.get(id)
	return render_template('admin/employee_hours/show.html' , item = item)

@employee_hours_blueprint.route("/admin/employee_hours/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import EmployeeHoursModel
	print("deleted " , id)
	obj = EmployeeHoursModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1

		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/employee_hours/index')

@employee_hours_blueprint.route("/admin/employee_hours/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import EmployeeHoursModel
	print(id)
	# edit
	if request.method == "POST":

		obj = EmployeeHoursModel.query.get(id)

		obj.employee_id = request.form.get('employee_id')
		obj.started_at = request.form.get('started_at')
		obj.finished_at = request.form.get('finished_at')

		
		db.session.commit()
		

		return redirect('/admin/employee_hours/index')
	# show  one row
	elif request.method == "GET":

		item = EmployeeHoursModel.query.get(id)
		return render_template('/admin/employee_hours/edit.html',item = item)
	return "404"


@employee_hours_blueprint.route("/admin/employee_hours/create" , methods =["GET" , "POST"])
@employee_hours_blueprint.route("/admin/employee_hours/create/<employee_id>" , methods =["GET"])
@flask_login.login_required
def create(employee_id=None):
	from db_models import EmployeeHoursModel
	# edit
	if request.method == "POST":

		employee_id = request.form.get('employee_id')
		started_at = request.form.get('started_at')
		finished_at = request.form.get('finished_at')

		obj = EmployeeHoursModel(employee_id=employee_id , started_at=started_at , finished_at=finished_at )
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/employee_hours/index')
	# show  one row
	elif request.method == "GET":
		if employee_id is not None:
			return render_template('/admin/employee_hours/create.html',employee_id=employee_id)
	return "404"


