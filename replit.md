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
- **CSV Roster Management** - Upload roster CSV files to import employee data
- **Three-State Testing Status** - Track employees as tested/not tested/excused with dates
- **Roster Entry Management** - View and manage individual roster entries per client with status cycling
- **Client-specific attachment management** - Upload passports, certifications, and other documents (max 3MB per file)
- **Attachment categorization** - Separate attachments for roster requests, reminders, updates, and quarterly selections
- Automated attachment inclusion in category-specific emails
- **Quarterly Selections Quick Action** - Send random pool quarterly selection emails with multiple attachments
- **Weekly Testing Reports** - Automated email reports showing tested vs not tested employees
- Email template management with placeholders
- Configurable email provider (Gmail/Outlook)
- **Enhanced Reminder Settings** - Per-client reminder preferences with custom frequencies
- Automated scheduling for roster reminders, follow-ups, and progress updates
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
- `uploads/attachments/` - Client-specific attachment files

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
### General Templates
- `{{client_name}}` - Client organization name
- `{{contact_name}}` - Contact person name
- `{{quarter}}` - Current quarter (e.g., 2025-Q1)
- `{{due_date}}` - Formatted due date
- `{{days_overdue}}` - Days since last request
- `{{update_date}}` - Current date

### Testing Report Templates
- `{{roster_quarter}}` - Roster quarter
- `{{total_employees}}` - Total number of employees
- `{{tested_count}}` - Number who have tested
- `{{not_tested_count}}` - Number who haven't tested
- `{{excused_count}}` - Number who are excused from testing
- `{{tested_percentage}}` - Percentage tested
- `{{tested_list}}` - List of employees who have tested
- `{{not_tested_list}}` - List of employees who haven't tested
- `{{excused_list}}` - List of employees who are excused
- `{{report_date}}` - Report generation date

## Recent Changes
- 2025-11-16: Quarterly selections quick action added
  - **New Email Type**: Quarterly Selections email template with roster metrics
  - **Quick Action Button**: Send quarterly selections with multiple attachments
  - **New Attachment Category**: quarterly_selections for organizing selection documents
  - **Email Placeholders**: {{quarter}}, {{roster_quarter}}, {{total_employees}}, {{tested_count}}, {{not_tested_count}}, {{excused_count}}, {{send_date}}
- 2025-11-16: Three-state testing status implementation
  - **Excused Status Added**: Employees can now be marked as tested/not tested/excused
  - **Status Cycling**: Click to cycle through all three statuses (not tested → tested → excused → repeat)
  - **Enhanced Reports**: Weekly testing reports now include excused employees in a separate section
  - **Database Migration**: Migrated from boolean has_tested to string testing_status field
  - **Updated Placeholders**: Added {{excused_count}} and {{excused_list}} to email templates
- 2025-11-16: Major feature additions
  - **CSV Roster Import**: Upload CSV files to import employee rosters with automatic parsing
  - **Testing Status Tracking**: Mark individual employees as tested/not tested with dates
  - **Roster Management UI**: View all roster entries with testing statistics
  - **Weekly Testing Reports**: Automated scheduler job sends testing status reports every Monday
  - **Enhanced Reminder Settings**: Per-client preferences for reminders and reports
    - Enable/disable automated reminders per client
    - Custom reminder frequency in days
    - Enable/disable weekly testing reports per client
    - Choose day of week for testing reports
  - **Attachment Categorization**: Separate attachments for roster requests, reminders, and updates
  - Three separate email buttons for different communication types
  - Secure file handling with UUID-based storage and path validation
- 2025-01-16: Initial project setup with all core features
- Configured for Gmail/Outlook switching capability
- Created default email templates for roster requests, follow-ups, progress updates, and testing reports
