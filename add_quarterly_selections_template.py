"""
Script to add the quarterly selections email template to the database.
"""

import sqlite3

def add_template():
    conn = sqlite3.connect('pool_comms.db')
    cursor = conn.cursor()
    
    try:
        # Check if template already exists
        cursor.execute("""
            SELECT id FROM email_templates 
            WHERE template_type = 'quarterly_selections'
        """)
        
        existing = cursor.fetchone()
        
        if existing:
            print("✓ Quarterly selections template already exists")
            return
        
        subject = "{{quarter}} Random Pool Selections - {{client_name}}"
        
        body = """Dear {{contact_name}},

We are pleased to send you the quarterly random pool selections for {{client_name}}.

QUARTER: {{roster_quarter}}

TESTING SUMMARY:
================
Total Employees in Pool: {{total_employees}}
Tested: {{tested_count}}
Not Tested: {{not_tested_count}}
Excused: {{excused_count}}

Please find the attached documents which include:
- Random pool selection results
- Testing requirements and guidelines
- Any additional documentation for this quarter

All employees selected for the random pool must complete their required testing by the deadline specified in the attached documents.

If you have any questions or need assistance, please don't hesitate to contact us.

Best regards,
Pool Communications Team

Generated: {{send_date}}"""
        
        cursor.execute("""
            INSERT INTO email_templates (name, subject_template, body_template, template_type, active)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "Quarterly Pool Selections",
            subject,
            body,
            "quarterly_selections",
            True
        ))
        
        conn.commit()
        print("✅ Successfully added quarterly selections email template")
        print("   Template type: quarterly_selections")
        print("   Supports multiple attachments from the 'quarterly_selections' category")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_template()
