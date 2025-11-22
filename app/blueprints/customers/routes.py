from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash



#____________________________CREATE CUSTOMER ROUTE____________________________

@customers_bp.route("",methods=['POST'])
# @limiter.limit("200 per day")
def create_customer():
    try:
        data = customer_schema.load(request.json) #JSON > Python
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    
#create a new customer instance
    new_customer = Customers(**data) #Unpack the data dictionary into the Customer model
    
    db.session.add(new_customer)
    
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


#____________________________READ ALL CUSTOMERS ROUTE____________________________

@customers_bp.route("", methods=['GET'])
def get_customers():
    customers = db.session.query(Customers).all()
    return customers_schema.jsonify(customers), 200


#____________________________READ A SINGLE CUSTOMER ROUTE____________________________

@customers_bp.route('/<int:customers_id>', methods=['GET'])
# @limiter.limit("15 per hour")
def get_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    return customer_schema.jsonify(customer), 200


#____________________________DELETE CUSTOMER ROUTE____________________________

@customers_bp.route('/<int:customers_id>', methods=['DELETE'])
def delete_customer(customers_id):
    customer = db.session.get(Customers, customers_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer deleted {customers_id}"}), 200


#____________________________UPDATE CUSTOMER ROUTE____________________________

@customers_bp.route('/<int:customers_id>', methods=["PUT"])
def update_customer(customers_id):
    #Query the mechanic by id
    customer = db.session.get(Customers, customers_id) #Query for our mechanic to update
    if not customer: #Checking if I got a mechanic with that id
        return jsonify({"message": "Customer not found"}), 404 
    #Validate and Deserialize the updates that they are sending in the body of the request
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    # for each of the values that they are sending, we will change the value of the queried object
    
    # 
    
    for key, value in customer_data.items():
        setattr(customer, key, value)
    
    db.session.commit() #Save the changes to the database
    return customer_schema.jsonify(customer), 200