from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, Float, ForeignKey
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Customers(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    
    service_tickets = relationship("ServiceTickets", back_populates="customer")


class ServiceTickets(Base):
    __tablename__ = 'service_tickets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    service_desc: Mapped[str] = mapped_column(String(1000), nullable=False)
    VIN: Mapped[str] = mapped_column(String(50), nullable=False)
    service_date: Mapped[date] = mapped_column(Date, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    customer = relationship("Customers", back_populates="service_tickets")
    mechanics = relationship("Mechanic", secondary="ticket_mechanics", back_populates="service_tickets")


class TicketMechanics(Base):
    __tablename__ = 'ticket_mechanics'
    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.id"), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("mechanics.id"), primary_key=True)
    
    
class Mechanic(Base):
    __tablename__ = 'mechanics'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    address: Mapped[str] = mapped_column(String(500), nullable=True)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    
    service_tickets = relationship("ServiceTickets", secondary="ticket_mechanics", back_populates="mechanics")