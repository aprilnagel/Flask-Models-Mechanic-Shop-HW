from app.blueprints.Service_Tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, Mechanics, db, Service_Tickets
from app.extensions import limiter, cache


#__________________CREATE SERVICE TICKET ROUTE____________________#

@service_tickets_bp.route('', methods=['POST'])

def create_service_ticket():
    #Validate and Deserialize the data
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    
    #Create a new Service Ticket object
    new_service_ticket = Service_Tickets(**service_ticket_data)
    
    #Add to the database
    db.session.add(new_service_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_service_ticket), 201


#__________________READ SERVICE TICKETS ROUTE____________________#

@service_tickets_bp.route('', methods=['GET'])
@cache.cached(timeout=30)
def get_service_tickets():
    service_tickets = db.session.query(Service_Tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200


#____________________________READ A SINGLE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________DELETE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket deleted {service_ticket_id}"}), 200


#____________________________UPDATE SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route("/<int:service_ticket_id>", methods=["PUT"])
# @limiter.limit("5 per day")
def update_service_ticket(service_ticket_id):
    
    #Query the service ticket by id
    service_ticket = db.session.get(Service_Tickets, service_ticket_id) #Query for our service ticket to update
    if not service_ticket: #Checking if I got a service ticket with that id
        return jsonify({"message": "Service Ticket not found"}), 404 
    #Validate and Deserialize the updates that they are sending in the body of the request
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"message": e.messages}), 400
    # for each of the values that they are sending, we will change the value of the queried object
    
    # if service_ticket_data['description']:
    #   service_ticket.description = service_ticket_data["description"]

    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value)
        
    # commit the changes
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________ASSIGN MECHANIC TO SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic_to_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    service_ticket.mechanics_service_tickets.append(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200


#____________________________REMOVE MECHANIC FROM SERVICE TICKET ROUTE____________________________#

@service_tickets_bp.route('/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic_from_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    
    mechanic = db.session.get(Mechanics, mechanic_id)
    
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    service_ticket.mechanics_service_tickets.remove(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(service_ticket), 200

