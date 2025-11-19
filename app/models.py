
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Table
from datetime import date

#Base Class
class Base(DeclarativeBase):
    pass

#instantiate the databases
db = SQLAlchemy(model_class=Base) 
#I dont really understand this line of code.

#junction table object
#many to many relationship between mechanics and service tickets
mechanic_service_ticket = Table(
    "mechanic_service_ticket", 
    db.metadata,
    Column("mechanic_id", Integer, ForeignKey("mechanics.id")),
    Column("service_ticket_id", Integer, ForeignKey("service_tickets.id"))
)

class Customers(db.Model):
    __tablename__ = "customers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    
    #relationships
    #one to many with service tickets
    service_tickets_customer: Mapped[list["Service_Tickets"]] = relationship("Service_Tickets", back_populates="customer")

class Service_Tickets(db.Model):
    __tablename__ = "service_tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column (Integer, ForeignKey("customers.id"), nullable=False)
    vehicle_make: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_model: Mapped[str] = mapped_column(String(100), nullable=False)
    vehicle_year: Mapped[int] = mapped_column(nullable=False)
    service_description: Mapped[str] = mapped_column(String(500), nullable=False)
    date_created: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Pending")
    
    #relationships
    #many to one with customers
    customer: Mapped[list["Customers"]] = relationship("Customers", back_populates="service_tickets_customer")
    #many to many with mechanics
    mechanics_service_tickets: Mapped[list["Mechanics"]] = relationship("Mechanics", secondary=mechanic_service_ticket, back_populates="service_tickets_mechanics")
    
class Mechanics(db.Model):
    __tablename__ = "mechanics"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    specialty: Mapped[str] = mapped_column(String(200), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    
    #relationships
    #many to many with service tickets
    service_tickets_mechanics: Mapped[list["Service_Tickets"]] = relationship("Service_Tickets", secondary=mechanic_service_ticket, back_populates="mechanics_service_tickets")





