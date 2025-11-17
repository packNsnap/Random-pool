# Random Pool Management

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
- **Roster Upload (CSV/XLSX)** - Upload roster files in CSV or Excel format to import employee data with 12+ fields
- **Enhanced Import** - Supports Primary ID, Last Name, First Name, Company, Modality, Location, Division, Supervisor Name, and Alternate IDs
- **Roster Export (CSV/XLSX)** - Download complete roster data in CSV or Excel format with all fields and testing status
- **Toggle Roster Status** - Quick button to mark roster as received/not received
- **Roster Version Control** - Delete entire roster versions when no longer needed
- **Three-State Testing Status** - Track employees as tested/not tested/excused with dates
- **Roster Entry Management** - View and manage individual roster entries per client with status cycling
- **Manual Employee Management** - Add or remove individual employees from rosters directly
- **Client-specific attachment management** - Upload passports, certifications, and other documents (max 3MB per file)
- **Attachment categorization** - Separate attachments for roster requests, reminders, updates, and quarterly selections
- Automated attachment inclusion in category-specific emails
- **Quarterly Selections Quick Action** - Send random pool quarterly selection emails with multiple attachments
- **CC Email Support** - Add multiple CC email recipients per client for automatic inclusion in all automated emails
- **Weekly Testing Reports** - Automated email reports showing tested vs not tested employees
- **Progress Updates with CSV Export** - Biweekly progress emails include roster statistics and auto-generated CSV attachments with complete testing status
- **Dynamic Email Templates** - Create, edit, and delete custom email templates
- **Dynamic Quick Actions** - Active templates automatically appear as quick action buttons on client pages
- Email template management with placeholders and attachment integration
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

### Roster Statistics Templates (Testing Reports & Progress Updates)
- `{{roster_quarter}}` - Roster quarter
- `{{total_employees}}` - Total number of employees
- `{{tested_count}}` - Number who have tested
- `{{not_tested_count}}` - Number who haven't tested
- `{{excused_count}}` - Number who are excused from testing
- `{{tested_percentage}}` - Percentage tested (auto-calculated)
- `{{tested_list}}` - Formatted list of employees who have tested
- `{{not_tested_list}}` - Formatted list of employees who haven't tested
- `{{excused_list}}` - Formatted list of employees who are excused
- `{{report_date}}` - Report generation date

## Recent Changes
- 2025-11-17: Excel (XLSX) Support Added
  - **XLSX Upload**: Roster upload now accepts both CSV and XLSX (Excel) files for maximum flexibility
  - **XLSX Export**: Added Excel download option alongside CSV export with formatted headers and auto-adjusted column widths
  - **Dual Format Support**: Users can choose between CSV and XLSX for both uploading and downloading rosters
  - **Enhanced File Parsing**: Smart detection of file type with appropriate parsing for each format
- 2025-11-16: Enhanced Roster Management Features
  - **Roster Status Toggle**: Added quick toggle button on client detail page to mark roster as received/not received with visual indicators
  - **Multi-Format Export**: Download buttons on roster view export complete roster data with all 18 fields including Primary ID, Last Name, First Name, Company, Modality, Location, Division, Supervisor Name, Alternate IDs, testing status, and test dates
  - **Enhanced Import**: File upload now supports 12 additional fields beyond basic employee info:
    - Primary ID, Last Name, First Name (auto-combines to employee name)
    - Company, Modality, Location, Division
    - Supervisor Name
    - Alternate ID + Type, Alternate ID 2 + Type
  - **Database Migration**: Added 12 new columns to roster_entries table to store extended employee information
- 2025-11-16: Enhanced Progress Update Emails
  - **Real Roster Data**: Progress update emails now include actual testing statistics (total employees, tested count, not tested count, excused count, percentage tested)
  - **Employee Lists**: Detailed lists of employees in each testing status category included in email body
  - **CSV Export**: Automatic CSV attachment generation with complete roster data (employee name, ID, position, department, testing status, test date)
  - **Template Variables**: Added {{tested_percentage}}, {{tested_list}}, {{not_tested_list}}, {{excused_list}} placeholders
  - **Updated Default Template**: Progress update template now shows comprehensive roster statistics
- 2025-11-16: Dynamic Template & Quick Action System
  - **Template CRUD**: Create, edit, and delete email templates with full management interface
  - **Dynamic Quick Actions**: Active templates automatically generate quick action buttons on client detail pages
  - **Generic Send Route**: Universal email sending route works with any template type
  - **Enhanced Template UI**: Reorganized template management with helpful sidebars showing placeholders, template types, and attachment categories
  - **Automatic Attachment Linking**: Template types automatically determine which attachments to include in emails
  - **Template Status Control**: Toggle templates active/inactive to show/hide quick action buttons
- 2025-11-16: Roster Management Enhancements
  - **Delete Roster Versions**: Added delete button in roster management section to remove entire rosters
  - **Manual Employee Add**: Add individual employees to existing rosters via modal form
  - **Manual Employee Remove**: Delete individual employees from rosters with confirmation
  - **Improved UI**: Streamlined action buttons in roster view with icon-only buttons
- 2025-11-16: CC Email Support Implementation
  - **CCEmail Database Model**: Store multiple CC email addresses per client with optional names
  - **Automatic Inclusion**: CC recipients automatically included in all automated emails (roster requests, reminders, updates, quarterly selections, testing reports)
  - **Management UI**: Add and remove CC email addresses from client detail page
  - **Email Service Integration**: Updated email service to support CC field in SMTP messages
  - **User-Friendly Interface**: Simple modal form for adding CC recipients with email and optional name fields
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
