from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, Float, ForeignKey, Table, Column
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

ticket_inventory = Table(
    "ticket_inventory",
    Base.metadata,
    Column("ticket_id", ForeignKey("service_tickets.id"), primary_key=True),
    Column("inventory_id", ForeignKey("inventory.id"), primary_key=True),
)
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
    inventories = relationship("Inventory", secondary=ticket_inventory, back_populates="service_tickets")
    parts = relationship("Part", back_populates="service_ticket")


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
    
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    service_tickets = relationship("ServiceTickets", secondary="ticket_mechanics", back_populates="mechanics")
    
    def set_password(self, raw_password: str) -> None:
        self.password = generate_password_hash(raw_password)
        
    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)
    

class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    service_tickets = relationship(
        "ServiceTickets",
        secondary=ticket_inventory,
        back_populates="inventories",
    )
    parts = relationship("Part", back_populates="inventory", cascade="all, delete-orphan")


class Part(Base):
    __tablename__ = "parts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"), nullable=False)
    ticket_id: Mapped[int | None] = mapped_column(ForeignKey("service_tickets.id"), nullable=True)

    inventory = relationship("Inventory", back_populates="parts")
    service_ticket = relationship("ServiceTickets", back_populates="parts")