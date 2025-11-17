#!/usr/bin/env python3
"""
Database migration script to add new columns to users table
"""
import sqlite3

def migrate_database():
    conn = sqlite3.connect('pool_comms.db')
    cursor = conn.cursor()
    
    try:
        # Add new columns to users table
        columns_to_add = [
            ("email", "TEXT"),
            ("full_name", "TEXT"),
            ("active", "BOOLEAN DEFAULT 1"),
            ("can_send_emails", "BOOLEAN DEFAULT 0"),
            ("can_manage_clients", "BOOLEAN DEFAULT 0"),
            ("can_view_reports", "BOOLEAN DEFAULT 1"),
            ("last_login_at", "TIMESTAMP"),
        ]
        
        for column_name, column_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {column_name} {column_type}")
                print(f"✓ Added column: {column_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"- Column already exists: {column_name}")
                else:
                    raise
        
        # Update existing admin user to have all permissions
        cursor.execute("""
            UPDATE users 
            SET role = 'admin', 
                active = 1,
                can_send_emails = 1,
                can_manage_clients = 1,
                can_view_reports = 1
            WHERE id = 1
        """)
        print("✓ Updated admin user permissions")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
