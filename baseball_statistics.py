#This is a database of Major league batting and hitting statistics dating back to 1871. The database includes fielding statistics, postseason data, and other data. Lastly it includes statistics from the Negro Leagues.

import sqlite3
import csv
import os

def import_csv_to_sqlite(csv_file, sqlite_db, table_name=None):
    """
    Import a CSV file into a SQLite database
    """
    
    # Use filename as table name if not specified
    if table_name is None:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        # Remove spaces and special characters
        table_name = table_name.replace(' ', '_').replace('-', '_')
    
    print(f"Importing {csv_file} into table '{table_name}'...")
    
    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        # Get headers from first row
        headers = next(reader)
        headers = [h.strip().replace(' ', '_').replace('-', '_') for h in headers]
        
        print(f"  Columns: {', '.join(headers)}")
        
        # Create table (drop if exists)
        cursor.execute(f"DROP TABLE IF EXISTS [{table_name}]")
        
        # Create table with TEXT columns (SQLite will handle types dynamically)
        columns = ', '.join([f"[{h}] TEXT" for h in headers])
        cursor.execute(f"CREATE TABLE [{table_name}] ({columns})")
        
        # Insert data
        placeholders = ', '.join(['?' for _ in headers])
        insert_sql = f"INSERT INTO [{table_name}] VALUES ({placeholders})"
        
        row_count = 0
        for row in reader:
            cursor.execute(insert_sql, row)
            row_count += 1
        
        print(f"  ✓ Imported {row_count} rows")
    
    conn.commit()
    conn.close()
    print(f"✓ Successfully imported to {sqlite_db}\n")

def import_multiple_csvs(csv_folder, sqlite_db):
    """
    Import all CSV files from a folder into SQLite
    """
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {csv_folder}")
        return
    
    print(f"Found {len(csv_files)} CSV files to import:\n")
    
    for csv_file in csv_files:
        csv_path = os.path.join(csv_folder, csv_file)
        import_csv_to_sqlite(csv_path, sqlite_db)
    
    print(f"✓ All files imported to {sqlite_db}")

if __name__ == "__main__":
    CSV_FOLDER = "C:/Users/wzhoo/OneDrive/Documents/Resume/Sabermetrics/lahman_1871-2024u_csv"
    SQLITE_DB = "database2.db"
    import_multiple_csvs(CSV_FOLDER, SQLITE_DB)