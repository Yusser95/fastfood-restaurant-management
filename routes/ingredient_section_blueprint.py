from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

ingredient_section_blueprint = Blueprint("ingredient_section_blueprint",__name__)

from app import db



@ingredient_section_blueprint.route('/admin/ingredient_section/data')
@flask_login.login_required
def data():
	from db_models import IngredientSectionModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(IngredientSectionModel.id),
        ColumnDT(IngredientSectionModel.name),
        ColumnDT(IngredientSectionModel.is_deleted),
        ColumnDT(IngredientSectionModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(IngredientSectionModel).order_by(IngredientSectionModel.id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@ingredient_section_blueprint.route("/admin/ingredient_section/index" , methods =["GET"])
@flask_login.login_required
def index():
	return render_template('admin/ingredient_section/index.html')


@ingredient_section_blueprint.route("/admin/ingredient_section/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import IngredientSectionModel
	item = IngredientSectionModel.query.get(id)
	return render_template('admin/ingredient_section/show.html' , item = item)

@ingredient_section_blueprint.route("/admin/ingredient_section/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import IngredientSectionModel
	print("deleted " , id)
	obj = IngredientSectionModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1
		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/ingredient_section/index')

@ingredient_section_blueprint.route("/admin/ingredient_section/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import IngredientSectionModel
	print(id)
	# edit
	if request.method == "POST":

		obj = IngredientSectionModel.query.get(id)

		name = request.form.get('name')

		obj._update(name=name)


		
		db.session.commit()
		

		return redirect('/admin/ingredient_section/index')
	# show  one row
	elif request.method == "GET":

		item = IngredientSectionModel.query.get(id)
		return render_template('/admin/ingredient_section/edit.html',item = item)
	return "404"


@ingredient_section_blueprint.route("/admin/ingredient_section/create" , methods =["GET" , "POST"])
@flask_login.login_required
def create():
	from db_models import IngredientSectionModel
	# edit
	if request.method == "POST":

		name = request.form.get('name')

		obj = IngredientSectionModel(name=name)
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/ingredient_section/index')
	# show  one row
	elif request.method == "GET":
		return render_template('/admin/ingredient_section/create.html')
	return "404"



@ingredient_section_blueprint.route("/admin/ingredient_section/select", methods=['GET', "POST"])
@flask_login.login_required
def select():

	from db_models import IngredientSectionModel

	params = request.args.to_dict()
	print(params)

	q= params['q']
	if q:
		categories = IngredientSectionModel.query.filter(IngredientSectionModel.name.like("%"+q+"%")).limit(50).all()
		db.session.commit()
		categories = [{"id": str(i.id), "text": i.name} for i in categories]
		# categories.append({"id": q, "text": q})
		return jsonify(categories)

	categories = IngredientSectionModel.query.limit(50).all()
	db.session.commit()
	categories = [{"id": str(i.id), "text": i.name} for i in categories]
	# categories.append({"id": q, "text": q})
	return jsonify(categories)


