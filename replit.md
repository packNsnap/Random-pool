# Random Pool Management

## Overview
A Python-based client communication management system for automating quarterly roster requests and biweekly progress updates with email scheduling and tracking. The system aims to streamline the management of employee rosters, track testing statuses, and automate client communications for random pool selections, ultimately enhancing efficiency and compliance.

## User Preferences
I prefer detailed explanations.
I want iterative development.
Ask before making major changes.
Do not make changes to the folder `Z`.
Do not make changes to the file `Y`.

## System Architecture
The application is built with Python 3.11, utilizing FastAPI for the backend and Jinja2 templates with Bootstrap 5 for a responsive, modern UI/UX. Data is stored in an SQLite database. Email services are handled via SMTP, configurable for Gmail or Outlook, and background tasks are managed by APScheduler.

Key architectural decisions and features include:
- **Modular Design**: Separation of concerns with dedicated modules for authentication, database, email, and scheduling.
- **Role-Based Access Control**: Comprehensive user management with admin and regular user roles, granular permissions (can_send_emails, can_manage_clients, can_view_reports), and secure admin-only quick action enforcement.
- **Dynamic Content Management**: Ability to create, edit, and delete custom email templates and dynamically generate quick action buttons based on active templates.
- **Robust Roster Management**: Supports CSV/XLSX uploads and exports for employee rosters with extensive fields (12+ fields including Primary ID, Last Name, First Name, Company, Modality, Location, Division, Supervisor Name, Alternate IDs).
- **Dual Roster & Selections Management**: Distinct management of "Roster" (reference data) and "Selections" (testing status data) with separate upload and viewing interfaces.
- **Three-State Testing Status**: Tracks employees as tested, not tested, or excused, with status cycling functionality.
- **BAT Dual-Tracking**: Independent tracking of Drug Testing and BAT (Breath Alcohol Testing) for employees in selections, with per-employee BAT requirement toggle and separate status management.
- **Automated Communication**: Scheduled email delivery for roster requests, reminders, progress updates, weekly testing reports, and quarterly selections.
- **Configurable Reminders**: Per-client reminder preferences with custom frequencies (daily, weekly, biweekly, monthly, custom days).
- **Attachment Management**: Client-specific attachment uploads categorized for different email types (roster requests, reminders, updates, quarterly selections), with automated inclusion in emails.
- **CC Email Support**: Allows adding multiple CC recipients per client for automatic inclusion in all automated emails.
- **Real-time Reporting**: Automated email reports with roster statistics and auto-generated CSV attachments containing complete testing status.

## External Dependencies
- **FastAPI**: Web framework for building the API.
- **Jinja2**: Templating engine for dynamic HTML generation.
- **Bootstrap 5**: Frontend framework for responsive design.
- **SQLite**: Database for data storage.
- **SMTP (Gmail/Outlook)**: Email sending service.
- **APScheduler**: Python library for scheduling background jobs.
- **SQLAlchemy**: ORM for database interaction.

## Recent Changes
- 2025-11-17: Deployment Health Check Architecture (Production Ready)
  - **Clean Endpoint Separation**: `/` (health check only, always 200 JSON) and `/dashboard` (authenticated application interface)
  - **Database-Free Health Checks**: Root endpoint never touches database - works even when database is unavailable
  - **Multi-Worker Scheduler Lock**: File-based fcntl lock ensures only ONE scheduler runs when using `--workers 2` with gunicorn
  - **Instant Startup**: Scheduler starts immediately in background thread - no 5-second delay, fast health checks
  - **Bulletproof Health Detection**: Returns 200 for ALL health check scenarios (no headers, Accept */*, Accept text/html, any User-Agent including AWS ELB, Google HC)
  - **Fast Response**: Health checks respond in <3ms without database dependency
  - **Login Flow Update**: After authentication, users redirect to `/dashboard` instead of `/`
  - **Deployment Command**: `gunicorn main:app --bind 0.0.0.0:5000 --workers 2 --worker-class uvicorn.workers.UvicornWorker`
  - **Health Check Endpoints**: `GET /` (200 JSON), `HEAD /` (200), `GET /health` (200 JSON with timestamp)
- 2025-11-17: BAT (Breath Alcohol Testing) Dual-Tracking Feature (Production Ready)
  - **Per-Employee BAT Toggle**: One-click button to enable/disable BAT requirement for individual employees in selections
  - **Independent Status Management**: Separate drug and BAT status cycling (not_tested → tested → excused → not_tested)
  - **Dual Status Display**: Separate columns showing drug test status and BAT status with color-coded badges
  - **Separate Test Dates**: Independent tracking of drug test date and BAT test date timestamps
  - **BAT-Specific Stats**: When BAT is required, displays separate stat cards showing BAT completion rates (tested/not tested/excused)
  - **Visual Indicators**: Droplet icon (💧) for BAT toggle button, clear tooltips for all actions
  - **Database Fields**: Added bat_required (boolean), bat_status (string), bat_test_date (datetime) to RosterEntry model
  - **Migration Script**: migrate_bat_fields.py for safe database schema updates
  - **DOT Compliance Ready**: Aligns with DOT MIS form requirements for separate drug and alcohol testing reporting
- 2025-11-17: Dashboard Overhaul - Executive Command Center (Production Ready)
  - **KPI Metrics Cards**: 4 modern cards showing Active Clients, Pending Rosters, Testing Completion %, and Overdue Items
  - **Smart Action Items**: Urgent (red, 21+ days) and Warning (yellow, 14-21 days or <50% testing) alerts with inline client links
  - **Visual Analytics**: Chart.js doughnut chart displaying testing progress with tested vs. pending breakdown
  - **Enhanced Client Table**: Color-coded rows (red/yellow for overdue), progress bars for testing completion, inline actions
  - **Recent Activity Feed**: Last 10 email logs with status badges and timestamps
  - **Upcoming Automations**: Shows 5 enabled schedules sorted by least recently sent (displays frequencies and client names)
  - **Roster Detection Fix**: Pending rosters now correctly filters by roster_type="roster" only (selections don't count)
  - **Responsive Design**: Bootstrap 5 with shadow effects, proper spacing, mobile-friendly layout
  - **Balanced UX**: Quick visibility into urgent items while maintaining detailed client overview table
- 2025-11-17: User Management & Role-Based Access Control (Production Ready)
  - **User Roles**: Admin and regular user roles with distinct permissions
  - **Granular Permissions**: can_send_emails, can_manage_clients, can_view_reports flags for fine-grained access control
  - **Admin-Only Quick Actions**: All quick action email sends (roster requests, reminders, updates, quarterly selections) restricted to administrators
  - **User Management UI**: Complete /users interface for admins to add, edit, delete users and toggle permissions
  - **Enhanced User Model**: Added email, full_name, active status, last_login tracking, and permission fields
  - **Secure Authentication**: Password hashing with bcrypt, session-based auth, 403 forbidden responses for unauthorized access
  - **Database Migration**: migrate_user_table.py script to safely add new User fields to existing database
  - **Defense-in-Depth**: Quick action restrictions enforced at both UI (template) and API (route dependencies) layers
  - **Navigation Security**: User Management link visible only to admin users in main navigation
- 2025-11-17: Bulk File Upload with Drag & Drop
  - **Drag & Drop Interface**: New bulk upload modal with intuitive drag-and-drop zone for multiple files
  - **Multiple File Selection**: Upload multiple attachments at once instead of one-by-one
  - **Visual Feedback**: Real-time file preview with size display and remove buttons before uploading
  - **Progress Tracking**: Animated progress bar shows upload status for bulk operations
  - **Smart Defaults**: Pre-selects "Quarterly Selections" category for quick quarterly mailing uploads
  - **Error Handling**: Comprehensive error messages for individual file failures with detailed feedback
  - **Auto-Refresh**: Page automatically reloads after successful bulk upload to show new attachments
  - **File Validation**: Individual 3MB file size validation with clear error messages
  - **Bulk Upload Button**: New green "Bulk Upload" button in Quarterly Mailing Attachments section
- 2025-11-17: Scheduler Integration with Automation Settings
  - **Full Scheduler Integration**: All scheduler functions now use ClientTemplateSchedule settings
  - **Auto-Bootstrap Schedules**: System automatically creates default ClientTemplateSchedule entries when none exist
  - **Helper Functions**: Centralized should_send_email() and mark_email_sent() functions handle all interval logic
  - **Production Ready**: Scheduler respects per-client, per-template automation settings with flexible intervals