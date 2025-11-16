import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from models import EmailLog, Client, EmailTemplate, Settings
from utils import render_template_string

class EmailConfig:
    def __init__(self, db: Session):
        self.db = db
        self.load_config()
    
    def load_config(self):
        self.provider = self.get_setting("email_provider", "gmail")
        self.smtp_host = self.get_setting("smtp_host", "smtp.gmail.com")
        self.smtp_port = int(self.get_setting("smtp_port", "587"))
        self.smtp_username = self.get_setting("smtp_username", "")
        self.smtp_password = self.get_setting("smtp_password", "")
        self.from_email = self.get_setting("from_email", "")
        self.from_name = self.get_setting("from_name", "Pool Comms Console")
    
    def get_setting(self, key: str, default: str = "") -> str:
        setting = self.db.query(Settings).filter(Settings.key == key).first()
        return setting.value if setting else default
    
    def save_setting(self, key: str, value: str):
        setting = self.db.query(Settings).filter(Settings.key == key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = Settings(key=key, value=value)
            self.db.add(setting)
        self.db.commit()
    
    def configure_gmail(self, username: str, password: str, from_email: str):
        self.save_setting("email_provider", "gmail")
        self.save_setting("smtp_host", "smtp.gmail.com")
        self.save_setting("smtp_port", "587")
        self.save_setting("smtp_username", username)
        self.save_setting("smtp_password", password)
        self.save_setting("from_email", from_email)
        self.load_config()
    
    def configure_outlook(self, username: str, password: str, from_email: str):
        self.save_setting("email_provider", "outlook")
        self.save_setting("smtp_host", "smtp-mail.outlook.com")
        self.save_setting("smtp_port", "587")
        self.save_setting("smtp_username", username)
        self.save_setting("smtp_password", password)
        self.save_setting("from_email", from_email)
        self.load_config()

class EmailService:
    def __init__(self, db: Session):
        self.db = db
        self.config = EmailConfig(db)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        client_id: Optional[int] = None,
        template_id: Optional[int] = None,
        cc_emails: Optional[List[str]] = None
    ) -> tuple[bool, str]:
        log = EmailLog(
            client_id=client_id,
            template_id=template_id,
            recipient_email=to_email,
            subject=subject,
            body=body,
            status="pending"
        )
        self.db.add(log)
        self.db.commit()
        
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.config.from_name} <{self.config.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            
            msg.attach(MIMEText(body, 'plain'))
            
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            if not self.config.smtp_username or not self.config.smtp_password:
                raise Exception("Email not configured. Please configure SMTP settings.")
            
            server = smtplib.SMTP(self.config.smtp_host, self.config.smtp_port)
            server.starttls()
            server.login(self.config.smtp_username, self.config.smtp_password)
            server.send_message(msg)
            server.quit()
            
            log.status = "sent"
            log.sent_at = datetime.utcnow()
            self.db.commit()
            
            return True, "Email sent successfully"
        
        except Exception as e:
            error_msg = str(e)
            log.status = "failed"
            log.error_message = error_msg
            self.db.commit()
            return False, error_msg
    
    def send_from_template(
        self,
        client: Client,
        template: EmailTemplate,
        variables: dict,
        attachments: Optional[List[str]] = None
    ) -> tuple[bool, str]:
        subject = render_template_string(template.subject_template, variables)
        body = render_template_string(template.body_template, variables)
        
        cc_emails = [cc.email for cc in client.cc_emails] if client.cc_emails else None
        
        return self.send_email(
            to_email=client.contact_email,
            subject=subject,
            body=body,
            attachments=attachments,
            client_id=client.id,
            template_id=template.id,
            cc_emails=cc_emails
        )
    
    def get_config(self) -> EmailConfig:
        return self.config
