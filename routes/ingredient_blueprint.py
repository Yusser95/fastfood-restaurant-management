from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

ingredient_blueprint = Blueprint("ingredient_blueprint",__name__)

from app import db



@ingredient_blueprint.route('/admin/ingredient/data')
@flask_login.login_required
def data():
	from db_models import IngredientModel, IngredientSectionModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(IngredientModel.id),
        ColumnDT(IngredientModel.name),
        ColumnDT(IngredientSectionModel.name),
        ColumnDT(IngredientModel.is_deleted),
        ColumnDT(IngredientModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(IngredientModel).order_by(IngredientModel.id).outerjoin(IngredientSectionModel, IngredientModel.section)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@ingredient_blueprint.route("/admin/ingredient/index" , methods =["GET"])
@flask_login.login_required
def index():
	return render_template('admin/ingredient/index.html')


@ingredient_blueprint.route("/admin/ingredient/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import IngredientModel
	item = IngredientModel.query.get(id)
	return render_template('admin/ingredient/show.html' , item = item)

@ingredient_blueprint.route("/admin/ingredient/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import IngredientModel
	print("deleted " , id)
	obj = IngredientModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1
		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/ingredient/index')

@ingredient_blueprint.route("/admin/ingredient/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import IngredientModel
	print(id)
	# edit
	if request.method == "POST":

		obj = IngredientModel.query.get(id)

		name = request.form.get('name')
		section_id = request.form.get('section_id')

		obj._update(name=name , section_id=section_id )


		
		db.session.commit()
		

		return redirect('/admin/ingredient/index')
	# show  one row
	elif request.method == "GET":

		item = IngredientModel.query.get(id)
		return render_template('/admin/ingredient/edit.html',item = item)
	return "404"


@ingredient_blueprint.route("/admin/ingredient/create" , methods =["GET" , "POST"])
@flask_login.login_required
def create():
	from db_models import IngredientModel
	# edit
	if request.method == "POST":

		name = request.form.get('name')
		section_id = request.form.get('section_id')

		obj = IngredientModel(name=name , section_id=section_id )
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/ingredient/index')
	# show  one row
	elif request.method == "GET":
		return render_template('/admin/ingredient/create.html')
	return "404"



@ingredient_blueprint.route("admin/ingredient/validator/uniquename" , methods =['GET',"POST"])
@flask_login.login_required
def unique_name_validator():

	from db_models import IngredientModel


	response = {'valid':'true'}
	name = request.args.get('name')
	print(name)

	# item = IngredientModel.query.filter_by(name=name).first()
	item = IngredientModel.query.filter(func.lower(IngredientModel.name) == func.lower(name)).first()

	if item:
		response['valid'] = 'false'


	return jsonify(response)


@ingredient_blueprint.route("/admin/ingredient/select", methods=['GET', "POST"])
@flask_login.login_required
def select():

	from db_models import IngredientModel

	params = request.args.to_dict()
	print(params)

	q= params['q']
	if q:
		ingredients = IngredientModel.query.filter(IngredientModel.name.like("%"+q+"%")).limit(50).all()
		db.session.commit()
		ingredients = [{"id": i.name, "text": i.name} for i in ingredients]
		ingredients.append({"id": q, "text": q})
		return jsonify(ingredients)

	ingredients = IngredientModel.query.limit(50).all()
	db.session.commit()
	ingredients = [{"id": i.name, "text": i.name} for i in ingredients]
	ingredients.append({"id": q, "text": q})
	return jsonify(ingredients)
