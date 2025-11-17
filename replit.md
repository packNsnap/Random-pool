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