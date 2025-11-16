# Random Pool Comms Console

## Overview
A Python-based client communication management system for automating quarterly roster requests and biweekly progress updates with email scheduling and tracking.

## Tech Stack
- **Backend**: Python 3.11 + FastAPI
- **Frontend**: Jinja2 templates + Bootstrap 5
- **Database**: SQLite
- **Email**: SMTP (Gmail/Outlook configurable)
- **Scheduler**: APScheduler

## Features
- User authentication system
- Client and contact management
- Roster tracking with file upload capability
- Email template management with placeholders
- Configurable email provider (Gmail/Outlook)
- Automated scheduling for roster reminders and progress updates
- Dashboard with client status overview
- Email logs with filtering

## Default Credentials
- Username: `admin`
- Password: `admin123`
- **IMPORTANT**: Change password after first login

## Project Structure
- `main.py` - FastAPI application with all routes
- `models.py` - SQLAlchemy database models
- `database.py` - Database configuration
- `auth.py` - Authentication and authorization
- `email_service.py` - Configurable email service (Gmail/Outlook)
- `scheduler.py` - Background job scheduler
- `utils.py` - Utility functions
- `init_db.py` - Database initialization script
- `templates/` - Jinja2 HTML templates
- `uploads/rosters/` - Uploaded roster files

## Email Configuration
The system supports both Gmail and Outlook/Office 365:

### Gmail Setup
1. Enable 2-Step Verification
2. Generate App Password
3. Use App Password in settings

### Outlook Setup
1. Use account email and password
2. Ensure SMTP is enabled

## Available Placeholders for Email Templates
- `{{client_name}}` - Client organization name
- `{{contact_name}}` - Contact person name
- `{{quarter}}` - Current quarter (e.g., 2025-Q1)
- `{{due_date}}` - Formatted due date
- `{{days_overdue}}` - Days since last request
- `{{update_date}}` - Current date

## Recent Changes
- 2025-01-16: Initial project setup with all core features
- Configured for Gmail/Outlook switching capability
- Created default email templates for roster requests, follow-ups, and progress updates
