from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Mechanics

@mechanics_bp.route('/mechanics', methods=['POST'])
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    #create a new mechanic instance
    new_mechanic = Mechanics(**data)
    
    db.session.add(new_mechanic)
    
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

#read mechanics route:
@mechanics_bp.route('/mechanics', methods=['GET'])
def get_mechanics():
    mechanics = db.session.query(Mechanics).all()
    return mechanics_schema.jsonify(mechanics), 200

#read individual mechanic route:
@mechanics_bp.route('/mechanics/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    return mechanic_schema.jsonify(mechanic), 200

#delete mechanic route:
@mechanics_bp.route('/mechanics/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic deleted {mechanic_id}"}), 200

#UPDATE A MECHANIC
@mechanics_bp.route("/mechanics/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    #Query the mechanic by id
    mechanic = db.session.get(Mechanics, mechanic_id) #Query for our mechanic to update
    if not mechanic: #Checking if I got a mechanic with that id
        return jsonify({"message": "Mechanic not found"}), 404 
    #Validate and Deserialize the updates that they are sending in the body of the request
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    # for each of the values that they are sending, we will change the value of the queried object
    
    # 
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit() #Save the changes to the database
    return mechanic_schema.jsonify(mechanic), 200