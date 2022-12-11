from flask import Flask, request, Response, jsonify
import flask
from flask_marshmallow import Marshmallow
from sqlalchemy.dialects.postgresql import UUID


from db import *
from users import Users, users_schema,user_schema
from orders import Orders, orders_schema, order_schema
from products import Products, products_schema, product_schema
from categories import Categories, categories_schema, category_schema
from product_category_association import product_category_association_table
from product_order_association import product_association_schema


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://Amee@localhost:5432/amee"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
ma = Marshmallow(app)

def create_all():
  with app.app_context():
    print("Creating tables...")
    db.create_all()
    print("All done!")

def populate_object(obj, data_dictionary):
  fields = data_dictionary.keys()
  for field in fields:
    if getattr(obj, field): 
      setattr(obj, field, data_dictionary[field])

@app.route("/user/add", methods=["POST"])
def user_add():
  post_data = request.json

  if not post_data:
    post_data = request.post
  
  first_name = post_data.get('first_name')
  last_name = post_data.get('last_name')
  phone = post_data.get('phone')
  email = post_data.get('email')
  street_address = post_data.get('street_address')
  city = post_data.get('city')
  state = post_data.get('state')
  postal_code = post_data.get('postal_code')
  active = post_data.get('active')

  add_user(first_name, last_name, phone, email, street_address, city, state, postal_code, active)

  return jsonify("Client created"), 201

def add_user(first_name, last_name, phone, email, street_address, city, state, postal_code, active): 
  new_user = Users(first_name, last_name, phone, email, street_address, city, state, postal_code, active)
  
  db.session.add(new_user)
  db.session.commit()

@app.route('/users/get', methods=['GET'] )
def get_users():
  results = db.session.query(Users).filter(Users.active == True).all()

  if results:
    return jsonify(users_schema.dump(results)), 200
  
  else:
    return jsonify('No User Found'), 404

@app.route('/user/update', methods=['POST', 'PUT'] )
def user_update():
  post_data = request.get_json()
  user_id = post_data.get("user_id")
  if user_id == None:
    return jsonify("ERROR: user_id missing"), 400
  first_name = post_data.get('first_name')
  last_name = post_data.get('last_name')
  phone = post_data.get('phone')
  email = post_data.get('email')
  street_address = post_data.get('street_address')
  city = post_data.get('city')
  state = post_data.get('state')
  postal_code = post_data.get('postal_code')
  active = post_data.get('active')

  if active == None:
    active = True
    
    user_data = None

    if user_id != None:
      user_data = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_data:
      user_id = user_data.user_id
      if first_name:
        user_data.first_name = first_name
      if last_name is not None:
        user_data.last_name = last_name
      if phone is not None:
        user_data.phone = phone
      if email is not None:
        user_data.email = email
      if street_address is not None:
        user_data.street_address = street_address
      if city is not None:
        user_data.city = city
      if state is not None:
        user_data.state = state
      if postal_code is not None:
        user_data.postal_code = postal_code
      if active is not None:
        user_data.active = active

      db.session.commit()

      return jsonify('User Information Updated'), 200
    else:
      return jsonify("User Not Found"), 404
  else:
    return jsonify("ERROR: request must be in JSON format"), 400


@app.route("/order/add", methods=["POST"])
def order_add():
  post_data = request.json

  if not post_data:
    post_data = request.post
  
  user_id = post_data.get('user_id')
  order_total_price = post_data.get('order_total_price')
  order_completed = post_data.get('order_completed')  

  add_order(user_id, order_total_price, order_completed)

  return jsonify("Order created"), 201

def add_order(user_id, order_total_price, order_completed): 
  new_order = Orders(user_id, order_total_price, order_completed)
  
  db.session.add(new_order)
  db.session.commit()

@app.route('/orders/get', methods=['GET'] )
def get_orders():
  results = db.session.query(Orders).filter(Orders.order_completed == True).all()

  if results:
    return jsonify(orders_schema.dump(results)), 200
  
  else:
    return jsonify('No Orders Found'), 404

@app.route('/order/update', methods=['POST', 'PUT'] )
def order_update():
  post_data = request.get_json()
  order_id = post_data.get("order_id")
  if order_id == None:
    return jsonify("ERROR: order_id missing"), 400
  user_id = post_data.get('user_id')
  order_date = post_data.get('order_date')
  ship_date = post_data.get('ship_date')
  order_total_price = post_data.get('order_total_price')
  order_completed = post_data.get('order_completed')
  quantity = post_data.get('quantity')
  product_id = post_data.get('product_id')

  if order_completed == None:
    order_completed = True
    
    order_data = None

    if order_id != None:
      order_data = db.session.query(Orders).filter(Orders.order_id == order_id).first()

    if order_data:
      order_id = order_data.order_id
      if user_id:
        order_data.user_id = user_id
      if order_date is not None:
        order_data.order_date = order_date
      if ship_date is not None:
        order_data.ship_date = ship_date
      if order_total_price is not None:
        order_data.order_total_price = order_total_price
      if order_completed is not None:
        order_data.order_completed = order_completed
      if quantity is not None:
        order_data.quantity = quantity
      if product_id != None or product_id != '':
        product = db.session.query(Products).filter(Products.product_id == product_id).first()
        if product != None:
          product.order.append(order_data)

      db.session.commit()

      return jsonify('Order Information Updated'), 200
    else:
      return jsonify("Order Not Found"), 404
  else:
    return jsonify("ERROR: request must be in JSON format"), 400


@app.route("/product/add", methods=["POST"])
def product_add():
  post_data = request.json

  if not post_data:
    post_data = request.post
  
  product_name = post_data.get('product_name')
  product_descripton = post_data.get('product_descripton')
  product_total_price = post_data.get('product_total_price')
  active = post_data.get('active')
  category_id = post_data.get('category_id')
  
  

  add_product(product_name, product_descripton, product_total_price, active, category_id)

  return jsonify("Product created"), 201

def add_product(product_name, product_descripton, product_total_price, active, category_id): 
  new_product = Products(product_name, product_descripton, product_total_price, active)
  category = db.session.query(Categories).filter(Categories.category_id == category_id).first()  
  db.session.add(new_product)
  if category != None:
    new_product.category.append(category)
    db.session.flush()
  db.session.commit()

@app.route('/product/get/<product_id>', methods=['GET'] )
def get_product(product_id):
  results = db.session.query(Products).filter(Products.product_id == product_id).first()

  if results:
    return jsonify(products_schema.dump(results)), 200
  
  else:
    return jsonify('No Product Found'), 404

@app.route('/product/update', methods=['POST', 'PUT'] )
def product_update():
  post_data = request.get_json()
  product_id = post_data.get("product_id")
  if product_id == None:
    return jsonify("ERROR: product_id missing"), 400
  product_id = post_data.get('product_id')
  product_name = post_data.get('product_name')
  product_descripton = post_data.get('product_descripton')
  product_total_price = post_data.get('product_total_price')
  active = post_data.get('active')
  order_id = post_data.get('order_id')
  category_id = post_data.get('category_id')

  if active == None:
    active = True
    
    product_data = None

    if product_id != None:
      product_data = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product_data:
      product_id = product_data.product_id
      if product_name:
        product_data.product_name = product_name
      if product_descripton is not None:
        product_data.product_descripton = product_descripton
      if product_total_price is not None:
        product_data.product_total_price = product_total_price
      if active is not None:
        product_data.active = active
      if order_id != None or order_id != '':
        product = db.session.query(Orders).filter(Orders.order_id == order_id).first()
        if product != None:
          product.product.append(product_data)
      if category_id != None or category_id != '':
        category = db.session.query(Categories).filter(Categories.category_id == category_id).first()
        if category!= None:
          category.product.append(product_data)

      db.session.commit()

      return jsonify('Product Information Updated'), 200
    else:
      return jsonify("Product Not Found"), 404
  else:
    return jsonify("ERROR: request must be in JSON format"), 400


@app.route('/products/get', methods=['GET'] )
def get_products():
  results = db.session.query(Products).filter(Products.active == True).all()

  if results:
    return jsonify(products_schema.dump(results)), 200
  
  else:
    return jsonify('No Products Found'), 404
  

@app.route('/user/delete/<user_id>', methods=['DELETE'] )
def user_delete(user_id):
  results = db.session.query(Users).filter(Users.user_id == user_id).first()
  db.session.delete(results)
  db.session.commit()
  return jsonify('User Deleted'), 200

@app.route("/category/add", methods=["POST"])
def category_add():
  post_data = request.json

  
  category_id = post_data.get('category_id')
  name = post_data.get('name')
  category_description = post_data.get('category_description')
  active = post_data.get('active') 

  add_category(category_id, name, category_description, active)

  return jsonify("category created"), 201

def add_category(category_id, name, category_description, active): 
  new_category = Categories(category_id, name, category_description, active)
  
  db.session.add(new_category)
  db.session.commit()

@app.route('/category/get/<category_id>', methods=['GET'] )
def get_category(category_id):
  results = db.session.query(Categories).filter(Categories.category_id == category_id).first()

  if results:
    return jsonify(category_schema.dump(results)), 200
  
  else:
    return jsonify('No Category Found'), 404

@app.route('/admin/categories/get', methods=['GET'] )
def get_categories():
  results = db.session.query(Categories).filter(Categories.active == True).all()

  if results:
    return jsonify(categories_schema.dump(results)), 200
  
  else:
    return jsonify('No Categories Found'), 404


# @app.route('/user/categories/get', methods = ['GET'])
# def user_get_categories():
#   results = db.session.query(Users).filter(Users.active == True).all()

#   if results:
#     return jsonify(users_category_schema.dump(results)), 200

#   else: return jsonify('No Categories Found'), 404


# @app.route("/opperation/add", methods=["POST"])
# def opperation_add():
#   post_data = request.json

#   if not post_data:
#     post_data = request.post
  
#   name = post_data.get('name')
#   description = post_data.get('description')
#   active = post_data.get('active')
  

#   add_opperation(name, description, active)

#   return jsonify("Opperation created"), 201

# def add_opperation(name, description, active): 
#   new_opperation = OpperationInfo(name, description, active)
  
#   db.session.add(new_opperation)
#   db.session.commit()

# @app.route('/opperations/get', methods=['GET'] )
# def get_opperations():
#   results = db.session.query(OpperationInfo).filter(OpperationInfo.active == True).all()

#   if results:
#     return jsonify(opperations_info_schema.dump(results)), 200
  
#   else:
#     return jsonify('No Opperations Found'), 404

# @app.route('/opperation/update', methods=['POST', 'PUT'] )
# def opperation_update():
#   post_data = request.get_json()
#   opperation_id = post_data.get("opperation_id")
#   if opperation_id == None:
#     return jsonify("ERROR: opperation_id missing"), 400
#   name = post_data.get('name')
#   description = post_data.get('description')
#   active = post_data.get('active')

#   if active == None:
#     active = True
    
#     pet_type_data = None

#     if opperation_id != None:
#       pet_type_data = db.session.query(OpperationInfo).filter(OpperationInfo.opperation_id == opperation_id).first()

#     if pet_type_data:
#       opperation_id = pet_type_data.opperation_id
#       if name:
#         pet_type_data.name = name
#       if description is not None:
#         pet_type_data.description = description
#       if active is not None:
#         pet_type_data.active = active

#       db.session.commit()

#       return jsonify('Opperaton Information Updated'), 200
#     else:
#       return jsonify("Opperaton Not Found"), 404
#   else:
#     return jsonify("ERROR: request must be in JSON format"), 400



# @app.route("/vaccine/add", methods=["POST"])
# def vaccine_add():
#   post_data = request.json

#   if not post_data:
#     post_data = request.post
  
#   name = post_data.get('name')
#   description = post_data.get('description')
#   active = post_data.get('active')
  

#   add_vaccine(name, description, active)

#   return jsonify("Vaccine created"), 201

# def add_vaccine(name, description, active): 
#   new_vaccine = VaccineInfo(name, description, active)
  
#   db.session.add(new_vaccine)
#   db.session.commit()

# @app.route('/vaccine/get', methods=['GET'] )
# def get_vaccine():
#   results = db.session.query(VaccineInfo).filter(VaccineInfo.active == True).all()

#   if results:
#     return jsonify(vaccines_info_schema.dump(results)), 200
  
#   else:
#     return jsonify('No Vaccines Found'), 404

# @app.route('/vaccine/update', methods=['POST', 'PUT'] )
# def vaccine_update():
#   post_data = request.get_json()
#   vaccine_id = post_data.get("vaccine_id")
#   if vaccine_id == None:
#     return jsonify("ERROR: vaccine_id missing"), 400
#   name = post_data.get('name')
#   description = post_data.get('description')
#   active = post_data.get('active')

#   if active == None:
#     active = True
    
#     pet_type_data = None

#     if vaccine_id != None:
#       pet_type_data = db.session.query(VaccineInfo).filter(VaccineInfo.vaccine_id == vaccine_id).first()

#     if pet_type_data:
#       vaccine_id = pet_type_data.vaccine_id
#       if name:
#         pet_type_data.name = name
#       if description is not None:
#         pet_type_data.description = description
#       if active is not None:
#         pet_type_data.active = active

#       db.session.commit()

#       return jsonify('Vaccine Information Updated'), 200
#     else:
#       return jsonify("Vaccine Not Found"), 404
#   else:
#     return jsonify("ERROR: request must be in JSON format"), 400





if __name__ == '__main__':
  create_all()
  app.run(host='0.0.0.0', port="8089")