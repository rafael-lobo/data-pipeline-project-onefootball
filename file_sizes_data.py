import os
import psycopg2
from psycopg2 import sql

def connect_to_db():
    try:
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', '5432')
        )
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        exit(1)

def get_file_sizes(target_folder_path):
    print("Fetching file sizes...")

    file_sizes = []

    for root, _, files in os.walk(target_folder_path):
        for file in files:
            try:
                path = os.path.join(root, file)
                size = os.path.getsize(path)
                file_sizes.append((path, size))
            except OSError:
                continue
    return file_sizes

def insert_records(cursor, file_sizes):
    for path, size in file_sizes:
        cursor.execute(
            sql.SQL("INSERT INTO file_sizes (path, size) VALUES (%s, %s) ON CONFLICT (path) DO UPDATE SET size = EXCLUDED.size"),
            (path, size)
        )

def export_to_csv(cursor):
    with open('result.csv', 'w') as f:
        cursor.copy_expert('COPY file_sizes TO STDOUT WITH CSV HEADER', f)
        print("Table exported to result.csv.")

def write_to_database(database, file_sizes):
    try:
        cursor = database.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_sizes (
                path TEXT PRIMARY KEY,
                size BIGINT
            )
        ''')

        insert_records(cursor, file_sizes)
        database.commit()

        print("Data stored in database.")

        export_to_csv(cursor)
        cursor.close()
    except Exception as e:
        print(f"Error writing to database: {e}")

def main():
    database = connect_to_db()
    target_folder_path = os.getenv('FILES_FOLDER_PATH')
    file_sizes = get_file_sizes(target_folder_path)
    write_to_database(database, file_sizes)

if __name__ == "__main__":
    print("Starting script...")
    main()
    print("Script finished!")
