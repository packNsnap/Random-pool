from sqlalchemy import Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="user")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    can_send_emails: Mapped[bool] = mapped_column(Boolean, default=False)
    can_manage_clients: Mapped[bool] = mapped_column(Boolean, default=False)
    can_view_reports: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class Client(Base):
    __tablename__ = "clients"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    contact_name: Mapped[str] = mapped_column(String, nullable=False)
    contact_email: Mapped[str] = mapped_column(String, nullable=False)
    program_type: Mapped[str] = mapped_column(String, default="DOT")
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    roster_frequency: Mapped[str] = mapped_column(String, default="quarterly")
    progress_frequency_days: Mapped[int] = mapped_column(Integer, default=14)
    reminder_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    reminder_frequency_days: Mapped[int] = mapped_column(Integer, default=7)
    testing_report_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    testing_report_day_of_week: Mapped[int] = mapped_column(Integer, default=1)
    last_roster_request_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_roster_received_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_progress_update_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_testing_report_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default="Active")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    rosters: Mapped[List["Roster"]] = relationship("Roster", back_populates="client", cascade="all, delete-orphan")
    email_logs: Mapped[List["EmailLog"]] = relationship("EmailLog", back_populates="client", cascade="all, delete-orphan")
    attachments: Mapped[List["Attachment"]] = relationship("Attachment", back_populates="client", cascade="all, delete-orphan")
    cc_emails: Mapped[List["CCEmail"]] = relationship("CCEmail", back_populates="client", cascade="all, delete-orphan")
    template_schedules: Mapped[List["ClientTemplateSchedule"]] = relationship("ClientTemplateSchedule", cascade="all, delete-orphan")

class Roster(Base):
    __tablename__ = "rosters"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    quarter: Mapped[str] = mapped_column(String, nullable=False)
    roster_type: Mapped[str] = mapped_column(String, default="roster", nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    file_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    client: Mapped["Client"] = relationship("Client", back_populates="rosters")
    entries: Mapped[List["RosterEntry"]] = relationship("RosterEntry", back_populates="roster", cascade="all, delete-orphan")

class RosterEntry(Base):
    __tablename__ = "roster_entries"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    roster_id: Mapped[int] = mapped_column(Integer, ForeignKey("rosters.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    
    primary_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    employee_name: Mapped[str] = mapped_column(String, nullable=False)
    employee_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    company: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    division: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    modality: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    supervisor_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    alternate_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    alternate_id_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    alternate_id_2: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    alternate_id_2_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    testing_status: Mapped[str] = mapped_column(String, default="not_tested", nullable=False)
    test_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    bat_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bat_status: Mapped[str] = mapped_column(String, default="not_tested", nullable=False)
    bat_test_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    roster: Mapped["Roster"] = relationship("Roster", back_populates="entries")
    client: Mapped["Client"] = relationship("Client")

class EmailTemplate(Base):
    __tablename__ = "email_templates"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subject_template: Mapped[str] = mapped_column(Text, nullable=False)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)
    template_type: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    email_logs: Mapped[List["EmailLog"]] = relationship("EmailLog", back_populates="template")

class EmailLog(Base):
    __tablename__ = "email_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    template_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("email_templates.id"), nullable=True)
    recipient_email: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String, default="pending")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    client: Mapped["Client"] = relationship("Client", back_populates="email_logs")
    template: Mapped[Optional["EmailTemplate"]] = relationship("EmailTemplate", back_populates="email_logs")

class Settings(Base):
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Attachment(Base):
    __tablename__ = "attachments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(String, default="roster_request", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    client: Mapped["Client"] = relationship("Client", back_populates="attachments")

class CCEmail(Base):
    __tablename__ = "cc_emails"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    client: Mapped["Client"] = relationship("Client", back_populates="cc_emails")

class ClientTemplateSchedule(Base):
    __tablename__ = "client_template_schedules"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    template_type: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    interval_type: Mapped[str] = mapped_column(String, default="weekly", nullable=False)
    interval_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    client: Mapped["Client"] = relationship("Client", overlaps="template_schedules")
