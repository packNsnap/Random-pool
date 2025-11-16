"""
Script to update the testing report email template with excused employee placeholders.
"""

import sqlite3

def update_template():
    conn = sqlite3.connect('pool_comms.db')
    cursor = conn.cursor()
    
    try:
        # Get current testing report template
        cursor.execute("""
            SELECT id, name, subject_template, body_template 
            FROM email_templates 
            WHERE template_type = 'testing_report'
        """)
        
        result = cursor.fetchone()
        
        if result:
            template_id, name, subject, body = result
            print(f"Found template: {name}")
            print(f"Subject: {subject}")
            print("\nCurrent body:")
            print(body)
            print("\n" + "="*80)
            
            # Check if excused placeholders are already in the template
            if "{{excused_count}}" in body or "{{excused_list}}" in body:
                print("\n✓ Template already includes excused placeholders!")
            else:
                print("\n⚠ Template needs to be updated with excused placeholders")
                print("\nPlease update the template through the UI to include:")
                print("  - {{excused_count}}: Number of excused employees")
                print("  - {{excused_list}}: List of excused employees")
                print("\nExample addition:")
                print("Excused Employees: {{excused_count}}")
                print("{{excused_list}}")
        else:
            print("No testing_report template found in database")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    update_template()
