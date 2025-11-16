from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="admin")
    created_at = Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    program_type = Column(String, default="DOT")
    active = Column(Boolean, default=True)
    roster_frequency = Column(String, default="quarterly")
    progress_frequency_days = Column(Integer, default=14)
    reminder_enabled = Column(Boolean, default=True)
    reminder_frequency_days = Column(Integer, default=7)
    testing_report_enabled = Column(Boolean, default=True)
    testing_report_day_of_week = Column(Integer, default=1)
    last_roster_request_at = Column(DateTime, nullable=True)
    last_roster_received_at = Column(DateTime, nullable=True)
    last_progress_update_at = Column(DateTime, nullable=True)
    last_testing_report_at = Column(DateTime, nullable=True)
    status = Column(String, default="Active")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    rosters = relationship("Roster", back_populates="client", cascade="all, delete-orphan")
    email_logs = relationship("EmailLog", back_populates="client", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="client", cascade="all, delete-orphan")
    cc_emails = relationship("CCEmail", back_populates="client", cascade="all, delete-orphan")

class Roster(Base):
    __tablename__ = "rosters"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    quarter = Column(String, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    client = relationship("Client", back_populates="rosters")
    entries = relationship("RosterEntry", back_populates="roster", cascade="all, delete-orphan")

class RosterEntry(Base):
    __tablename__ = "roster_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    roster_id = Column(Integer, ForeignKey("rosters.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Basic employee info
    primary_id = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    employee_name = Column(String, nullable=False)
    employee_id = Column(String, nullable=True)
    
    # Work details
    company = Column(String, nullable=True)
    position = Column(String, nullable=True)
    department = Column(String, nullable=True)
    division = Column(String, nullable=True)
    modality = Column(String, nullable=True)
    location = Column(String, nullable=True)
    supervisor_name = Column(String, nullable=True)
    
    # Alternate IDs
    alternate_id = Column(String, nullable=True)
    alternate_id_type = Column(String, nullable=True)
    alternate_id_2 = Column(String, nullable=True)
    alternate_id_2_type = Column(String, nullable=True)
    
    # Testing status
    testing_status = Column(String, default="not_tested", nullable=False)
    test_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    roster = relationship("Roster", back_populates="entries")
    client = relationship("Client")

class EmailTemplate(Base):
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    subject_template = Column(Text, nullable=False)
    body_template = Column(Text, nullable=False)
    template_type = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    email_logs = relationship("EmailLog", back_populates="template")

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=True)
    recipient_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    error_message = Column(Text, nullable=True)
    
    client = relationship("Client", back_populates="email_logs")
    template = relationship("EmailTemplate", back_populates="email_logs")

class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Attachment(Base):
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    category = Column(String, default="roster_request", nullable=False)
    description = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="attachments")

class CCEmail(Base):
    __tablename__ = "cc_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    email = Column(String, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="cc_emails")
