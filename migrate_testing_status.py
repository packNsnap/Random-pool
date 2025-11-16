"""
Migration script to add testing_status field to RosterEntry
and migrate data from has_tested boolean field.
"""

import sqlite3
from datetime import datetime

def migrate():
    conn = sqlite3.connect('pool_comms.db')
    cursor = conn.cursor()
    
    try:
        print("Starting migration...")
        
        # Check if testing_status column already exists
        cursor.execute("PRAGMA table_info(roster_entries)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'testing_status' not in columns:
            # Add testing_status column with default value
            print("Adding testing_status column...")
            cursor.execute("""
                ALTER TABLE roster_entries 
                ADD COLUMN testing_status TEXT DEFAULT 'not_tested' NOT NULL
            """)
            conn.commit()
            print("✓ Column added")
        else:
            print("✓ testing_status column already exists")
        
        # Check if has_tested column exists (for migration)
        if 'has_tested' in columns:
            print("Migrating data from has_tested to testing_status...")
            
            # Update testing_status based on has_tested value
            cursor.execute("""
                UPDATE roster_entries 
                SET testing_status = CASE 
                    WHEN has_tested = 1 THEN 'tested'
                    ELSE 'not_tested'
                END
            """)
            
            rows_updated = cursor.rowcount
            conn.commit()
            print(f"✓ Migrated {rows_updated} rows")
            
            # Drop the old has_tested column
            # SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
            print("Removing old has_tested column...")
            cursor.execute("""
                CREATE TABLE roster_entries_new (
                    id INTEGER PRIMARY KEY,
                    roster_id INTEGER NOT NULL,
                    client_id INTEGER NOT NULL,
                    employee_name TEXT NOT NULL,
                    employee_id TEXT,
                    position TEXT,
                    department TEXT,
                    testing_status TEXT DEFAULT 'not_tested' NOT NULL,
                    test_date DATETIME,
                    notes TEXT,
                    created_at DATETIME,
                    updated_at DATETIME,
                    FOREIGN KEY (roster_id) REFERENCES rosters(id),
                    FOREIGN KEY (client_id) REFERENCES clients(id)
                )
            """)
            
            cursor.execute("""
                INSERT INTO roster_entries_new 
                SELECT id, roster_id, client_id, employee_name, employee_id, position, 
                       department, testing_status, test_date, notes, created_at, updated_at
                FROM roster_entries
            """)
            
            cursor.execute("DROP TABLE roster_entries")
            cursor.execute("ALTER TABLE roster_entries_new RENAME TO roster_entries")
            
            conn.commit()
            print("✓ Removed has_tested column")
        else:
            print("✓ No has_tested column to migrate")
        
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
