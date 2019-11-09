from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

unit_blueprint = Blueprint("unit_blueprint",__name__)

from app import db



@unit_blueprint.route('/admin/unit/data')
@flask_login.login_required
def data():
	from db_models import UnitModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(UnitModel.id),
        ColumnDT(UnitModel.name),
        ColumnDT(UnitModel.value_per_kg),
        ColumnDT(UnitModel.is_deleted),
        ColumnDT(UnitModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(UnitModel).order_by(UnitModel.id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@unit_blueprint.route("/admin/unit/index" , methods =["GET"])
@flask_login.login_required
def index():
	return render_template('admin/unit/index.html')


@unit_blueprint.route("/admin/unit/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import UnitModel
	item = UnitModel.query.get(id)
	return render_template('admin/unit/show.html' , item = item)

@unit_blueprint.route("/admin/unit/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import UnitModel
	print("deleted " , id)
	obj = UnitModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1
		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/unit/index')

@unit_blueprint.route("/admin/unit/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import UnitModel
	print(id)
	# edit
	if request.method == "POST":

		obj = UnitModel.query.get(id)

		name = request.form.get('name')
		value_per_kg = request.form.get('value_per_kg')

		obj._update(name=name , value_per_kg=value_per_kg )


		
		db.session.commit()
		

		return redirect('/admin/unit/index')
	# show  one row
	elif request.method == "GET":

		item = UnitModel.query.get(id)
		return render_template('/admin/unit/edit.html',item = item)
	return "404"


@unit_blueprint.route("/admin/unit/create" , methods =["GET" , "POST"])
@flask_login.login_required
def create():
	from db_models import UnitModel
	# edit
	if request.method == "POST":

		name = request.form.get('name')
		value_per_kg = request.form.get('value_per_kg')

		obj = UnitModel(name=name , value_per_kg=value_per_kg )
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/unit/index')
	# show  one row
	elif request.method == "GET":
		return render_template('/admin/unit/create.html')
	return "404"



@unit_blueprint.route("/admin/unit/select", methods=['GET', "POST"])
@flask_login.login_required
def select():

	from db_models import UnitModel

	params = request.args.to_dict()
	print(params)

	q= params['q']
	if q:
		units = UnitModel.query.filter(UnitModel.name.like("%"+q+"%")).limit(50).all()
		db.session.commit()
		units = [{"id": i.id, "text": i.name} for i in units]
		# units.append({"id": q, "text": q})
		return jsonify(units)

	units = UnitModel.query.limit(50).all()
	db.session.commit()
	units = [{"id": i.id, "text": i.name} for i in units]
	# units.append({"id": q, "text": q})
	return jsonify(units)


