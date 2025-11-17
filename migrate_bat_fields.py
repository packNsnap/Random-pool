"""
Migration script to add BAT (Breath Alcohol Testing) fields to roster_entries table.
Run this once to update your existing database.
"""
import sqlite3
from datetime import datetime

def migrate_bat_fields():
    conn = sqlite3.connect('pool_comms.db')
    cursor = conn.cursor()
    
    try:
        print("Starting BAT fields migration...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(roster_entries)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'bat_required' not in columns:
            print("Adding bat_required column...")
            cursor.execute("""
                ALTER TABLE roster_entries 
                ADD COLUMN bat_required BOOLEAN DEFAULT 0 NOT NULL
            """)
            print("✓ bat_required column added")
        else:
            print("✓ bat_required column already exists")
        
        if 'bat_status' not in columns:
            print("Adding bat_status column...")
            cursor.execute("""
                ALTER TABLE roster_entries 
                ADD COLUMN bat_status VARCHAR DEFAULT 'not_tested' NOT NULL
            """)
            print("✓ bat_status column added")
        else:
            print("✓ bat_status column already exists")
        
        if 'bat_test_date' not in columns:
            print("Adding bat_test_date column...")
            cursor.execute("""
                ALTER TABLE roster_entries 
                ADD COLUMN bat_test_date DATETIME
            """)
            print("✓ bat_test_date column added")
        else:
            print("✓ bat_test_date column already exists")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        print("You can now use BAT dual-tracking features.")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_bat_fields()
