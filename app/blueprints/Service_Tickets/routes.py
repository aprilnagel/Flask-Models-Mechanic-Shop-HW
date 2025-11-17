from app.blueprints.Service_Tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Service_Tickets


@service_tickets_bp.route('/service_tickets', methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
#create a new service ticket instance
    new_service_ticket = Service_Tickets(**data)
    
    db.session.add(new_service_ticket)
    
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201

#read service tickets route:
@service_tickets_bp.route('/service_tickets', methods=['GET'])
def get_service_tickets():
    service_tickets = db.session.query(Service_Tickets).all()
    return service_tickets_schema.jsonify(service_tickets), 200

#read individual service ticket route:
@service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    return service_ticket_schema.jsonify(service_ticket), 200

#delete service ticket route:
@service_tickets_bp.route('/service_tickets/<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(Service_Tickets, service_ticket_id)
    if not service_ticket:
        return jsonify({"message": "Service Ticket not found"}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f"Service Ticket deleted {service_ticket_id}"}), 200

#UPDATE A SERVICE TICKET
@service_tickets_bp.route("/service_tickets/<int:service_ticket_id>", methods=["PUT"])
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