from flask import Flask, jsonify, Blueprint, current_app, session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory
import flask_login
from datatables import ColumnDT, DataTables

recipe_tag_blueprint = Blueprint("recipe_tag_blueprint",__name__)

from app import db



@recipe_tag_blueprint.route('/admin/recipe_tag/data')
@flask_login.login_required
def data():
	from db_models import RecipeTagModel

	"""Return server side data."""
	# defining columns
	columns = [
        ColumnDT(RecipeTagModel.id),
        ColumnDT(RecipeTagModel.name),
        ColumnDT(RecipeTagModel.is_deleted),
        ColumnDT(RecipeTagModel.created_at),


    ]
    # defining the initial query depending on your purpose
	query = db.session.query().select_from(RecipeTagModel).order_by(RecipeTagModel.id)

	# GET parameters
	params = request.args.to_dict()
	# print(params)

	# instantiating a DataTable for the query and table needed
	rowTable = DataTables(params, query, columns)

	# returns what is needed by DataTable
	return jsonify(rowTable.output_result())


@recipe_tag_blueprint.route("/admin/recipe_tag/index" , methods =["GET"])
@flask_login.login_required
def index():
	return render_template('admin/recipe_tag/index.html')


@recipe_tag_blueprint.route("/admin/recipe_tag/show/<id>" , methods =["GET"])
@flask_login.login_required
def show(id):
	from db_models import RecipeTagModel
	item = RecipeTagModel.query.get(id)
	return render_template('admin/recipe_tag/show.html' , item = item)

@recipe_tag_blueprint.route("/admin/recipe_tag/delete/<id>" , methods =["GET"])
@flask_login.login_required
def delete(id):
	from db_models import RecipeTagModel
	print("deleted " , id)
	obj = RecipeTagModel.query.filter_by(id=id).first()
	if obj:
		if obj.is_deleted == 0:
			obj.is_deleted = 1
		else:
			obj.is_deleted = 0

	db.session.commit()
	return redirect('/admin/recipe_tag/index')

@recipe_tag_blueprint.route("/admin/recipe_tag/edit/<id>" , methods =["GET" , "POST"])
@flask_login.login_required
def edit(id):
	from db_models import RecipeTagModel
	print(id)
	# edit
	if request.method == "POST":

		obj = RecipeTagModel.query.get(id)

		name = request.form.get('name')

		obj._update(name=name)


		
		db.session.commit()
		

		return redirect('/admin/recipe_tag/index')
	# show  one row
	elif request.method == "GET":

		item = RecipeTagModel.query.get(id)
		return render_template('/admin/recipe_tag/edit.html',item = item)
	return "404"


@recipe_tag_blueprint.route("/admin/recipe_tag/create" , methods =["GET" , "POST"])
@flask_login.login_required
def create():
	from db_models import RecipeTagModel
	# edit
	if request.method == "POST":

		name = request.form.get('name')

		obj = RecipeTagModel(name=name)
		db.session.add(obj)
		db.session.commit()

		return redirect('/admin/recipe_tag/index')
	# show  one row
	elif request.method == "GET":
		return render_template('/admin/recipe_tag/create.html')
	return "404"





@recipe_tag_blueprint.route("/admin/recipe_tag/select", methods=['GET', "POST"])
@flask_login.login_required
def select():

	from db_models import RecipeTagModel

	params = request.args.to_dict()
	print(params)

	q= params['q']
	if q:
		categories = RecipeTagModel.query.filter(RecipeTagModel.name.like("%"+q+"%")).limit(50).all()
		db.session.commit()
		categories = [{"id": str(i.id), "text": i.name} for i in categories]
		# categories.append({"id": q, "text": q})
		return jsonify(categories)

	categories = RecipeTagModel.query.limit(50).all()
	db.session.commit()
	categories = [{"id": str(i.id), "text": i.name} for i in categories]
	# categories.append({"id": q, "text": q})
	return jsonify(categories)
