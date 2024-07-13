# Data Pipeline Project - Onefootball ⚽

## Overview

This project was developed to demonstrate data engineering skills, using codespaces, containers and data pipelines. The goal is to monitor a target directory's file system and record file sizes in a PostgreSQL database.

## Project Structure

- **devcontainer.json**: Configuration for the remote development environment (Codespace).
- **docker-compose.yml**: Configuration for Docker services.
- **Dockerfile**: Container build instructions for the application.
- **files_size_data.py**: Main script for the data pipeline.
- **requirements.txt**: Project dependencies.
- **.env**: Environment variables for database configuration.

## Usage Instructions

1. Create a codespace.

![create codespace](/images/create-codespace.png)

2. Wait for the codespace to be created.
3. Run `docker compose up`.
   - The `file_sizes_data.py` script will periodically store the data from the target repository on the database, as well as on the `result.csv` file.
   - The container and its dependencies can be viewed at the Docker tab

![alt text](/images/docker.png)

4. Connect to the database using `Ctrl`+`Shift`+`P` (or `⌘`+`Shift`+`P`) → `PostgreSQL: Add Connection`. Use the credentials in the `.env` file to connect to the database.

   - _Hostname_: `db`
   - _User_: `user`
   - _Password_: `0000`
   - _Port_: `5432`

5. Check the database.

   - On the PostgreSQL tab, view the table by right-clicking on the `file_sizes` table and selecting `New Query`, then run `SELECT * FROM file_sizes;`

   ![postgres table](/images/postgres.png)

   - Alternatively, open the `result.csv` file, use `Ctrl`+`Shift`+`P` (or `⌘`+`Shift`+`P`) → `Convert to table from CSV`
   
   ![csv](/images/csv.png)

   - Another method to access the result table's data is by using `psql`, running the following commands on the terminal:

   ```
    docker exec -it database bash

    psql -U user -d project_database

    SELECT * FROM file_sizes;
   ```

   ![psql table](/images/psql-table.png)

## Data Pipeline features

### Idempotency

The pipeline ensures idempotency by using the SQL `ON CONFLICT` clause in the `INSERT` statement. This updates the file size if the file path already exists in the database, preventing duplicate entries and ensuring consistent state across multiple runs.

### Incremental Data Ingestion

The pipeline handles incremental data ingestion by scanning the file system for changes and updating only the modified or new files in the database. This is achieved by recalculating file sizes and updating the database entries accordingly.

### File System Updates/Sync with Postgres Table

Updates on the file system are managed by continuously monitoring the target folder. The script recalculates file sizes and updates the database to reflect any new, modified, or deleted files. This ensures that the database remains synchronized with the file system.

## Time Invested

- Study: 3 hours
- Environment setup: 2 hours
- Pipeline development: 3 hours
- Documentation and adjustments: 6 hour

Total: 14 hours
