from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Client, EmailTemplate
from email_service import EmailService
from utils import get_current_quarter, get_quarter_dates, days_since
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_roster_template_by_type(db: Session, template_type: str):
    return db.query(EmailTemplate).filter(
        EmailTemplate.template_type == template_type,
        EmailTemplate.active == True
    ).first()

def check_and_send_roster_reminders():
    db = SessionLocal()
    try:
        logger.info("Running roster reminder check...")
        email_service = EmailService(db)
        today = date.today()
        current_quarter = get_current_quarter(today)
        
        quarter_start, quarter_end = get_quarter_dates(current_quarter)
        if not quarter_start or not quarter_end:
            logger.error(f"Invalid quarter: {current_quarter}")
            return
        
        days_until_quarter_end = (quarter_end - today).days
        remind_window_days = 14
        
        active_clients = db.query(Client).filter(Client.active == True).all()
        
        for client in active_clients:
            if client.roster_frequency != "quarterly":
                continue
            
            if days_until_quarter_end > remind_window_days:
                continue
            
            roster_received_this_quarter = False
            for roster in client.rosters:
                if roster.quarter == current_quarter:
                    roster_received_this_quarter = True
                    break
            
            if roster_received_this_quarter:
                continue
            
            days_since_last_request = days_since(client.last_roster_request_at) if client.last_roster_request_at else 999
            
            if days_since_last_request < 7:
                continue
            
            template = get_roster_template_by_type(db, "roster_request")
            if not template:
                logger.warning("No roster_request template found")
                continue
            
            variables = {
                "client_name": client.name,
                "contact_name": client.contact_name,
                "quarter": current_quarter,
                "due_date": quarter_end.strftime("%B %d, %Y")
            }
            
            attachment_paths = [os.path.join("uploads", "attachments", att.filename) for att in client.attachments]
            
            success, message = email_service.send_from_template(
                client=client,
                template=template,
                variables=variables,
                attachments=attachment_paths
            )
            
            if success:
                client.last_roster_request_at = datetime.utcnow()
                client.status = "Roster Request Sent"
                db.commit()
                logger.info(f"Sent roster reminder to {client.name}")
            else:
                logger.error(f"Failed to send roster reminder to {client.name}: {message}")
    
    except Exception as e:
        logger.error(f"Error in roster reminder check: {str(e)}")
    finally:
        db.close()

def check_and_send_follow_ups():
    db = SessionLocal()
    try:
        logger.info("Running follow-up check...")
        email_service = EmailService(db)
        today = date.today()
        current_quarter = get_current_quarter(today)
        
        active_clients = db.query(Client).filter(Client.active == True).all()
        
        for client in active_clients:
            roster_received_this_quarter = False
            for roster in client.rosters:
                if roster.quarter == current_quarter:
                    roster_received_this_quarter = True
                    break
            
            if roster_received_this_quarter:
                continue
            
            days_since_last_request = days_since(client.last_roster_request_at) if client.last_roster_request_at else None
            
            if days_since_last_request is None or days_since_last_request < 7:
                continue
            
            template = get_roster_template_by_type(db, "follow_up")
            if not template:
                logger.warning("No follow_up template found")
                continue
            
            variables = {
                "client_name": client.name,
                "contact_name": client.contact_name,
                "quarter": current_quarter,
                "days_overdue": days_since_last_request
            }
            
            attachment_paths = [os.path.join("uploads", "attachments", att.filename) for att in client.attachments]
            
            success, message = email_service.send_from_template(
                client=client,
                template=template,
                variables=variables,
                attachments=attachment_paths
            )
            
            if success:
                client.last_roster_request_at = datetime.utcnow()
                client.status = "Follow-up Sent"
                db.commit()
                logger.info(f"Sent follow-up to {client.name}")
            else:
                logger.error(f"Failed to send follow-up to {client.name}: {message}")
    
    except Exception as e:
        logger.error(f"Error in follow-up check: {str(e)}")
    finally:
        db.close()

def check_and_send_progress_updates():
    db = SessionLocal()
    try:
        logger.info("Running progress update check...")
        email_service = EmailService(db)
        
        active_clients = db.query(Client).filter(Client.active == True).all()
        
        for client in active_clients:
            days_since_last_update = days_since(client.last_progress_update_at) if client.last_progress_update_at else 999
            
            if days_since_last_update < client.progress_frequency_days:
                continue
            
            template = get_roster_template_by_type(db, "progress_update")
            if not template:
                logger.warning("No progress_update template found")
                continue
            
            variables = {
                "client_name": client.name,
                "contact_name": client.contact_name,
                "update_date": datetime.utcnow().strftime("%B %d, %Y")
            }
            
            success, message = email_service.send_from_template(
                client=client,
                template=template,
                variables=variables
            )
            
            if success:
                client.last_progress_update_at = datetime.utcnow()
                db.commit()
                logger.info(f"Sent progress update to {client.name}")
            else:
                logger.error(f"Failed to send progress update to {client.name}: {message}")
    
    except Exception as e:
        logger.error(f"Error in progress update check: {str(e)}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        func=check_and_send_roster_reminders,
        trigger="cron",
        hour=9,
        minute=0,
        id="roster_reminders"
    )
    
    scheduler.add_job(
        func=check_and_send_follow_ups,
        trigger="cron",
        hour=10,
        minute=0,
        id="follow_ups"
    )
    
    scheduler.add_job(
        func=check_and_send_progress_updates,
        trigger="cron",
        hour=11,
        minute=0,
        id="progress_updates"
    )
    
    scheduler.start()
    logger.info("Scheduler started successfully")
    
    return scheduler
