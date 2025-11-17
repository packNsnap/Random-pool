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
- **Dynamic Content Management**: Ability to create, edit, and delete custom email templates and dynamically generate quick action buttons based on active templates.
- **Robust Roster Management**: Supports CSV/XLSX uploads and exports for employee rosters with extensive fields (12+ fields including Primary ID, Last Name, First Name, Company, Modality, Location, Division, Supervisor Name, Alternate IDs).
- **Dual Roster & Selections Management**: Distinct management of "Roster" (reference data) and "Selections" (testing status data) with separate upload and viewing interfaces.
- **Three-State Testing Status**: Tracks employees as tested, not tested, or excused, with status cycling functionality.
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