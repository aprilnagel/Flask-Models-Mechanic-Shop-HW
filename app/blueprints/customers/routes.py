from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema, login_customer_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Customers
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.utility.auth import encode_token, token_required

@customers_bp.route('/customers/login', methods=['POST'])
@limiter.limit("5 per 10 minutes")
def login_customer():
  try:
    data = login_customer_schema.load(request.json)#JSON > Python
  except ValidationError as err:
    return jsonify(err.messages), 400 #return the error messages and a 400 status code if validation fails
  
  customer = db.session.query(Customers).where(Customers.email == data['email']).first()

  if customer and check_password_hash(customer.password, data['password']):
    #create token for customer
    token = encode_token(customer.id, role=customer.role)
    return jsonify({
      "message": f"Welcome {customer.first_name} {customer.last_name}",
      "token": token
    })

@customers_bp.route('/customers', methods=['POST'])
@limiter.limit("200 per day")
def create_customer():
    try:
        data = customer_schema.load(request.json) #JSON > Python
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    data['password'] = generate_password_hash(data['password']) #resetting the key value to the hash of the current value. hash the password before storing it in the database
    
#create a new customer instance
    new_customer = Customers(**data)
    
    db.session.add(new_customer)
    
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

#read customers route:
@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200

#read individual customer route:
@customers_bp.route('/customers/<int:customers_id>', methods=['GET'])
@limiter.limit("15 per hour")
def get_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    return customer_schema.jsonify(customer), 200

#delete customer route:
@customers_bp.route('/customers/<int:customer_id>', methods=['DELETE'])
@limiter.limit("5 per day")
@token_required #created in auth.py. This decorator will ensure that a valid token is provided before allowing access to this route.
def delete_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer deleted{customers_id}"}), 200

#UPDATE A USER
@customers_bp.route("/customers/<int:customers_id>", methods=["PUT"])
@limiter.limit("1 per month")
def update_user(customers_id):
  #Query the user by id
  customer = db.session.get(Customers, customers_id) #Query for our user to update
  if not customer: #Checking if I got a user with that id
    return jsonify({"message": "User not found"}), 404 
  #Validate and Deserialize the updates that they are sending in the body of the request
  try:
    customer_data = customer_schema.load(request.json)
  except ValidationError as e:
    return jsonify({"message": e.messages}), 400
  # for each of the values that they are sending, we will change the value of the queried object

  # if user_data['email']:
  #   user.email = user_data["email"]

  for key, value in customer_data.items():
    setattr(customer, key, value) #setting object, Attribute, value to replace
  # commit the changes
  db.session.commit()
  # return a response
  return customer_schema.jsonify(customer), 200