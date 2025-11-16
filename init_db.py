from database import SessionLocal, init_db
from models import User, EmailTemplate
from auth import hash_password

def seed_database():
    init_db()
    
    db = SessionLocal()
    
    existing_admin = db.query(User).filter(User.username == "admin").first()
    if not existing_admin:
        admin_user = User(
            username="admin",
            password_hash=hash_password("admin123"),
            role="admin"
        )
        db.add(admin_user)
        print("Created default admin user (username: admin, password: admin123)")
    else:
        print("Admin user already exists")
    
    template_types = ["roster_request", "follow_up", "progress_update"]
    existing_templates = db.query(EmailTemplate).filter(EmailTemplate.template_type.in_(template_types)).all()
    existing_types = [t.template_type for t in existing_templates]
    
    if "roster_request" not in existing_types:
        roster_template = EmailTemplate(
            name="Quarterly Roster Request",
            subject_template="Action Required: {{quarter}} Roster Submission - {{client_name}}",
            body_template="""Dear {{contact_name}},

This is a reminder that the {{quarter}} roster submission is due soon.

Please submit your roster for {{client_name}} by {{due_date}}.

If you have any questions or need assistance, please don't hesitate to reach out.

Thank you for your prompt attention to this matter.

Best regards,
Pool Comms Team""",
            template_type="roster_request",
            active=True
        )
        db.add(roster_template)
        print("Created roster request template")
    
    if "follow_up" not in existing_types:
        follow_up_template = EmailTemplate(
            name="Roster Submission Follow-Up",
            subject_template="Follow-Up: {{quarter}} Roster Still Pending - {{client_name}}",
            body_template="""Dear {{contact_name}},

We noticed that we have not yet received the {{quarter}} roster for {{client_name}}.

This is a follow-up reminder. The roster was requested {{days_overdue}} days ago.

Please submit your roster at your earliest convenience to ensure compliance.

If you have already submitted it, please disregard this message. If you're experiencing any issues, please contact us.

Thank you,
Pool Comms Team""",
            template_type="follow_up",
            active=True
        )
        db.add(follow_up_template)
        print("Created follow-up template")
    
    if "progress_update" not in existing_types:
        progress_template = EmailTemplate(
            name="Biweekly Progress Update",
            subject_template="Progress Update - {{client_name}} - {{update_date}}",
            body_template="""Dear {{contact_name}},

This is your biweekly progress update for {{client_name}}.

Current Status:
- Program is running smoothly
- All testing procedures are being followed
- Compliance documentation is up to date

If you have any questions or concerns, please contact us.

Next scheduled update: In 14 days

Best regards,
Pool Comms Team""",
            template_type="progress_update",
            active=True
        )
        db.add(progress_template)
        print("Created progress update template")
    
    db.commit()
    db.close()
    
    print("\nDatabase initialization complete!")
    print("Login with: username=admin, password=admin123")
    print("IMPORTANT: Change the admin password after first login!")

if __name__ == "__main__":
    seed_database()
