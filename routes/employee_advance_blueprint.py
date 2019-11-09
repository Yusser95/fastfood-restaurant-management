from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

employee_advance_blueprint = Blueprint("employee_advance_blueprint",__name__)

from app import db



@employee_advance_blueprint.route('/admin/employee_advance/data')
@employee_advance_blueprint.route('/admin/employee_advance/data/<employee_id>')
@flask_login.login_required
def data(employee_id=None):
	from db_models import EmployeeAdvanceModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(EmployeeAdvanceModel.id),
        ColumnDT(EmployeeAdvanceModel.employee_id),
        ColumnDT(EmployeeAdvanceModel.date_filter),
        ColumnDT(EmployeeAdvanceModel.amount),
        ColumnDT(EmployeeAdvanceModel.is_deleted),
        ColumnDT(EmployeeAdvanceModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(EmployeeAdvanceModel).order_by(EmployeeAdvanceModel.id)

	if employee_id is not None:
		query = query.filter_by(employee_id=employee_id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@employee_advance_blueprint.route("/admin/employee_advance/index" , methods =["GET"])
@employee_advance_blueprint.route("/admin/employee_advance/index/<employee_id>" , methods =["GET"])
@flask_login.login_required
def index(employee_id=None):
	return render_template('admin/employee_advance/index.html',employee_id=employee_id)


@employee_advance_blueprint.route("/admin/employee_advance/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import EmployeeAdvanceModel
	item = EmployeeAdvanceModel.query.get(id)
	return render_template('admin/employee_advance/show.html' , item = item)

@employee_advance_blueprint.route("/admin/employee_advance/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import EmployeeAdvanceModel
	print("deleted " , id)
	obj = EmployeeAdvanceModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1

		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/employee_advance/index')

@employee_advance_blueprint.route("/admin/employee_advance/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import EmployeeAdvanceModel
	print(id)
	# edit
	if request.method == "POST":

		obj = EmployeeAdvanceModel.query.get(id)

		employee_id = request.form.get('employee_id')
		amount = request.form.get('amount')

		obj._update(employee_id=employee_id , amount=amount )

		
		db.session.commit()
		

		return redirect('/admin/employee_advance/index')
	# show  one row
	elif request.method == "GET":

		item = EmployeeAdvanceModel.query.get(id)
		return render_template('/admin/employee_advance/edit.html',item = item)
	return "404"


@employee_advance_blueprint.route("/admin/employee_advance/create" , methods =["GET" , "POST"])
@employee_advance_blueprint.route("/admin/employee_advance/create/<employee_id>" , methods =["GET"])
@flask_login.login_required
def create(employee_id=None):
	from db_models import EmployeeAdvanceModel
	# edit
	if request.method == "POST":

		employee_id = request.form.get('employee_id')
		amount = request.form.get('amount')

		obj = EmployeeAdvanceModel(employee_id=employee_id , amount=amount )
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/employee_advance/index')
	# show  one row
	elif request.method == "GET":
		if employee_id is not None:
			return render_template('/admin/employee_advance/create.html',employee_id=employee_id)
	return "404"


