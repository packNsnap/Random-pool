"""
Script to update the testing report email template with excused employee section.
"""

import sqlite3

def update_template():
    conn = sqlite3.connect('pool_comms.db')
    cursor = conn.cursor()
    
    try:
        new_body = """Dear {{contact_name}},

This is your weekly testing status report for {{client_name}}.

Roster: {{roster_quarter}}

TESTING SUMMARY:
================
Total Employees: {{total_employees}}
Tested: {{tested_count}} ({{tested_percentage}}%)
Not Tested: {{not_tested_count}}
Excused: {{excused_count}}

EMPLOYEES WHO HAVE TESTED:
{{tested_list}}

EMPLOYEES WHO HAVE NOT TESTED:
{{not_tested_list}}

EXCUSED EMPLOYEES:
{{excused_list}}

Please ensure all employees who have not been excused complete their required testing as soon as possible.

If you have any questions, please don't hesitate to contact us.

Best regards,
Pool Comms Team"""
        
        cursor.execute("""
            UPDATE email_templates 
            SET body_template = ?
            WHERE template_type = 'testing_report'
        """, (new_body,))
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Successfully updated testing report template")
            print(f"   Added placeholders: {{excused_count}}, {{excused_list}}")
        else:
            print("⚠ No template was updated")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_template()
