from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Customers


@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
#create a new customer instance
    new_customer = Customers(**data)
    
    db.session.add(new_customer)
    
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#read customers route:
@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = db.session.query(Customers).all()
    return customer_schema.jsonify(customers), 200

#read individual customer route:
@customers_bp.route('/customers/<int:customers_id>', methods=['GET'])
def get_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    return customer_schema.jsonify(customer), 200

#delete customer route:
@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer deleted{customers_id}"}), 200

#UPDATE A USER
@customers_bp.route("/customers/<int:customers_id>", methods=["PUT"])
def update_user(customers_id):
  #Query the user by id
  user = db.session.get(Customers, customers_id) #Query for our user to update
  if not user: #Checking if I got a user with that id
    return jsonify({"message": "User not found"}), 404 
  #Validate and Deserialize the updates that they are sending in the body of the request
  try:
    user_data = customer_schema.load(request.json)
  except ValidationError as e:
    return jsonify({"message": e.messages}), 400
  # for each of the values that they are sending, we will change the value of the queried object

  # if user_data['email']:
  #   user.email = user_data["email"]

  for key, value in user_data.items():
    setattr(user, key, value) #setting object, Attribute, value to replace
  # commit the changes
  db.session.commit()
  # return a response
  return customer_schema.jsonify(user), 200