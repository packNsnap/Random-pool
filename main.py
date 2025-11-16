from fastapi import FastAPI, Request, Depends, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
from typing import Optional

from database import get_db, init_db
from models import User, Client, Roster, EmailTemplate, EmailLog, Settings
from auth import authenticate_user, require_login, get_current_user, hash_password
from email_service import EmailService
from scheduler import start_scheduler
from utils import get_current_quarter, format_datetime, days_since, render_template_string

app = FastAPI(title="Random Pool Comms Console")

SESSION_SECRET = os.getenv("SESSION_SECRET")
if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET environment variable must be set")

app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

templates = Jinja2Templates(directory="templates")
templates.env.filters['format_datetime'] = format_datetime
templates.env.filters['days_since'] = days_since

os.makedirs("static", exist_ok=True)
os.makedirs("uploads/rosters", exist_ok=True)

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    pass

@app.on_event("startup")
async def startup_event():
    init_db()
    start_scheduler()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    clients = db.query(Client).filter(Client.active == True).all()
    current_quarter = get_current_quarter()
    
    client_data = []
    for client in clients:
        roster_received = any(r.quarter == current_quarter for r in client.rosters)
        days_last_contact = days_since(client.last_roster_request_at)
        
        client_data.append({
            "client": client,
            "roster_received": roster_received,
            "days_last_contact": days_last_contact
        })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "client_data": client_data,
        "current_quarter": current_quarter
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password"
        })
    
    request.session["user_id"] = user.id
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/clients", response_class=HTMLResponse)
async def list_clients(request: Request, user: User = Depends(require_login), db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return templates.TemplateResponse("clients.html", {
        "request": request,
        "user": user,
        "clients": clients
    })

@app.get("/clients/new", response_class=HTMLResponse)
async def new_client_form(request: Request, user: User = Depends(require_login)):
    return templates.TemplateResponse("client_form.html", {
        "request": request,
        "user": user,
        "client": None
    })

@app.post("/clients/new")
async def create_client(
    request: Request,
    name: str = Form(...),
    contact_name: str = Form(...),
    contact_email: str = Form(...),
    program_type: str = Form("DOT"),
    progress_frequency_days: int = Form(14),
    active: bool = Form(True),
    notes: Optional[str] = Form(None),
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    client = Client(
        name=name,
        contact_name=contact_name,
        contact_email=contact_email,
        program_type=program_type,
        progress_frequency_days=progress_frequency_days,
        active=active,
        notes=notes
    )
    db.add(client)
    db.commit()
    return RedirectResponse(url="/clients", status_code=303)

@app.get("/clients/{client_id}", response_class=HTMLResponse)
async def client_detail(
    request: Request,
    client_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    rosters = sorted(client.rosters, key=lambda r: r.received_at, reverse=True)
    email_logs = db.query(EmailLog).filter(EmailLog.client_id == client_id).order_by(EmailLog.sent_at.desc()).limit(10).all()
    
    return templates.TemplateResponse("client_detail.html", {
        "request": request,
        "user": user,
        "client": client,
        "rosters": rosters,
        "email_logs": email_logs,
        "current_quarter": get_current_quarter()
    })

@app.get("/clients/{client_id}/edit", response_class=HTMLResponse)
async def edit_client_form(
    request: Request,
    client_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return templates.TemplateResponse("client_form.html", {
        "request": request,
        "user": user,
        "client": client
    })

@app.post("/clients/{client_id}/edit")
async def update_client(
    request: Request,
    client_id: int,
    name: str = Form(...),
    contact_name: str = Form(...),
    contact_email: str = Form(...),
    program_type: str = Form("DOT"),
    progress_frequency_days: int = Form(14),
    active: bool = Form(True),
    notes: Optional[str] = Form(None),
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client.name = name
    client.contact_name = contact_name
    client.contact_email = contact_email
    client.program_type = program_type
    client.progress_frequency_days = progress_frequency_days
    client.active = active
    client.notes = notes
    db.commit()
    
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)

@app.post("/clients/{client_id}/send_roster_request")
async def send_roster_request(
    client_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    template = db.query(EmailTemplate).filter(
        EmailTemplate.template_type == "roster_request",
        EmailTemplate.active == True
    ).first()
    
    if not template:
        raise HTTPException(status_code=404, detail="No roster request template found")
    
    current_quarter = get_current_quarter()
    variables = {
        "client_name": client.name,
        "contact_name": client.contact_name,
        "quarter": current_quarter,
        "due_date": datetime.utcnow().strftime("%B %d, %Y")
    }
    
    email_service = EmailService(db)
    success, message = email_service.send_from_template(client, template, variables)
    
    if success:
        client.last_roster_request_at = datetime.utcnow()
        client.status = "Roster Request Sent"
        db.commit()
    
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)

@app.post("/clients/{client_id}/mark_roster_received")
async def mark_roster_received(
    client_id: int,
    quarter: str = Form(...),
    file: Optional[UploadFile] = File(None),
    notes: Optional[str] = Form(None),
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    file_path = None
    if file and file.filename:
        file_path = f"uploads/rosters/{client_id}_{quarter}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    
    roster = Roster(
        client_id=client_id,
        quarter=quarter,
        file_path=file_path,
        notes=notes
    )
    db.add(roster)
    
    client.last_roster_received_at = datetime.utcnow()
    client.status = "Roster Received"
    db.commit()
    
    return RedirectResponse(url=f"/clients/{client_id}", status_code=303)

@app.get("/templates", response_class=HTMLResponse)
async def list_templates(request: Request, user: User = Depends(require_login), db: Session = Depends(get_db)):
    templates_list = db.query(EmailTemplate).all()
    return templates.TemplateResponse("templates.html", {
        "request": request,
        "user": user,
        "templates": templates_list
    })

@app.get("/templates/new", response_class=HTMLResponse)
async def new_template_form(request: Request, user: User = Depends(require_login)):
    return templates.TemplateResponse("template_form.html", {
        "request": request,
        "user": user,
        "template": None
    })

@app.post("/templates/new")
async def create_template(
    request: Request,
    name: str = Form(...),
    subject_template: str = Form(...),
    body_template: str = Form(...),
    template_type: str = Form(...),
    active: bool = Form(True),
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    template = EmailTemplate(
        name=name,
        subject_template=subject_template,
        body_template=body_template,
        template_type=template_type,
        active=active
    )
    db.add(template)
    db.commit()
    return RedirectResponse(url="/templates", status_code=303)

@app.get("/templates/{template_id}/edit", response_class=HTMLResponse)
async def edit_template_form(
    request: Request,
    template_id: int,
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return templates.TemplateResponse("template_form.html", {
        "request": request,
        "user": user,
        "template": template
    })

@app.post("/templates/{template_id}/edit")
async def update_template(
    template_id: int,
    name: str = Form(...),
    subject_template: str = Form(...),
    body_template: str = Form(...),
    template_type: str = Form(...),
    active: bool = Form(True),
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.name = name
    template.subject_template = subject_template
    template.body_template = body_template
    template.template_type = template_type
    template.active = active
    db.commit()
    
    return RedirectResponse(url="/templates", status_code=303)

@app.get("/logs", response_class=HTMLResponse)
async def email_logs(
    request: Request,
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    query = db.query(EmailLog).order_by(EmailLog.sent_at.desc())
    
    if client_id:
        query = query.filter(EmailLog.client_id == client_id)
    if status:
        query = query.filter(EmailLog.status == status)
    
    logs = query.limit(100).all()
    clients = db.query(Client).all()
    
    return templates.TemplateResponse("logs.html", {
        "request": request,
        "user": user,
        "logs": logs,
        "clients": clients,
        "selected_client_id": client_id,
        "selected_status": status
    })

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, user: User = Depends(require_login), db: Session = Depends(get_db)):
    email_service = EmailService(db)
    config = email_service.get_config()
    
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "user": user,
        "config": config
    })

@app.post("/settings/email")
async def update_email_settings(
    provider: str = Form(...),
    smtp_username: str = Form(...),
    smtp_password: str = Form(...),
    from_email: str = Form(...),
    from_name: str = Form("Pool Comms Console"),
    user: User = Depends(require_login),
    db: Session = Depends(get_db)
):
    email_service = EmailService(db)
    
    if provider == "gmail":
        email_service.config.configure_gmail(smtp_username, smtp_password, from_email)
    elif provider == "outlook":
        email_service.config.configure_outlook(smtp_username, smtp_password, from_email)
    
    email_service.config.save_setting("from_name", from_name)
    
    return RedirectResponse(url="/settings", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
