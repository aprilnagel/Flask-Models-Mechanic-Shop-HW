from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_mechanic_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Mechanics
from werkzeug.security import generate_password_hash, check_password_hash
from app.utility.auth import encode_token, token_required


#________________________#MECHANIC LOGIN ROUTE________________________

@mechanics_bp.route('/login', methods=['POST'])
# @limiter.limit("5 per 10 minutes")
def login():
  try:
    data = login_mechanic_schema.load(request.json)#JSON > Python
  except ValidationError as err:
    return jsonify(err.messages), 400 #return the error messages and a 400 status code if validation fails
  
  mechanic = db.session.query(Mechanics).where(Mechanics.email == data['email']).first()

  if mechanic and check_password_hash(mechanic.password, data['password']):
    #create token for customer
    token = encode_token(mechanic.id)
    return jsonify({
      "message": f"Welcome {mechanic.first_name} {mechanic.last_name}",
      "token": token,
    }), 200
    
    
#_______________________#CREATE MECHANIC ROUTE________________________

@mechanics_bp.route('', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    data['password'] = generate_password_hash(data['password'])
    #create a new mechanic instance
    new_mechanic = Mechanics(**data)
    
    db.session.add(new_mechanic)
    
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201
  

#________________________#READ MECHANICS ROUTES________________________

@mechanics_bp.route('', methods=['GET'])
def get_mechanics():
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200

#read individual mechanic route:
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    return mechanic_schema.jsonify(mechanic), 200
  
  
#________________________#DELETE A MECHANIC ROUTE________________________

@mechanics_bp.route("", methods=['DELETE']) #Deleted the ID in the route so that users can only delete their own account
# @limiter.limit("5 per day")
@token_required #created in auth.py. This decorator will ensure that a valid token is provided before allowing access to this route.
def delete_mechanic():
    token_id = request.logged_in_mechanic_id
    mechanic = db.session.get(Mechanics, token_id)
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {token_id}"}), 200
  

#________________________#UPDATE A MECHANIC ROUTE________________________

@mechanics_bp.route("", methods=["PUT"]) #No ID in the route. Users can only update their own info
# @limiter.limit("500 per month")
@token_required
def update_mechanic():
  #Query the user by id
  mechanic_id = request.logged_in_mechanic_id
  mechanic = db.session.get(Mechanics, mechanic_id) #Query for our user to update
  if not mechanic: #Checking if I got a user with that id
    return jsonify({"message": "Mechanic not found"}), 404 
  #Validate and Deserialize the updates that they are sending in the body of the request
  try:
    mechanic_data = mechanic_schema.load(request.json)
  except ValidationError as e:
    return jsonify({"message": e.messages}), 400
  # for each of the values that they are sending, we will change the value of the queried object
  
  mechanic_data['password'] = generate_password_hash(mechanic_data['password'])
  # if user_data['email']:
  #   user.email = user_data["email"]

  for key, value in mechanic_data.items():
    setattr(mechanic, key, value) #setting object, Attribute, value to replace
  # commit the changes
  db.session.commit()
  # return a response
  return mechanic_schema.jsonify(mechanic), 200