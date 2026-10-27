# South African Tech Job Market Pipeline

## Project Overview

The **South African Tech Job Market Pipeline** is a Python ETL (Extract, Transform, Load) project that collects technology job listings from the Adzuna API, cleans and standardises the data, and stores the results in a SQLite database for analysis.

The project demonstrates data extraction, data transformation, database loading, automated testing, and SQL-based analysis.

## Project Objectives

- Extract technology job listings using the Adzuna API.
- Clean and standardise job listing data.
- Save raw and transformed data as JSON files.
- Store job listings in a SQLite database.
- Prevent duplicate job records from being inserted.
- Validate pipeline behaviour with automated tests.
- Analyse job titles, locations, categories, and salary availability.

## Technologies Used

- Python
- Adzuna API
- SQLite
- SQL
- pytest
- pandas (for tabular data display and analysis where used)
- Git and GitHub

## ETL Pipeline

The pipeline follows three main stages:

1. **Extract:** Retrieve job listings from the Adzuna API.
2. **Transform:** Clean and standardise the extracted records.
3. **Load:** Store valid records in the SQLite database while skipping duplicates.

The main pipeline entry point is `main.py`.

## Project Structure

```text
sa-tech-job-market-pipeline/
├── data/
│   ├── raw/
│   │   └── adzuna_jobs.json
│   └── processed/
│       ├── adzuna_jobs_clean.json
│       └── jobs.db
├── src/
│   ├── extract/
│   ├── transform/
│   └── load/
├── tests/
│   ├── test_load.py
│   ├── test_pipeline_integration.py
│   └── test_transform.py
├── analysis_report.md
├── analyze_job_categories.py
├── analyze_job_data.py
├── analyze_job_locations.py
├── analyze_job_salaries.py
├── analyze_job_titles.py
├── inspect_database.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

Some generated files and local configuration files may be excluded from version control.

## Setup and Installation

### 1. Clone the repository

```powershell
git clone https://github.com/lauramashudu-svg/sa-tech-job-market-pipeline.git
cd sa-tech-job-market-pipeline
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this in the same terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Configure API credentials

Create a local `.env` file in the project root and configure the Adzuna API credentials required by the extraction module.

Use the environment variable names expected by the project's code.

**Security:** Never commit your `.env` file or expose API keys in screenshots, videos, or public repositories.

## Running the ETL Pipeline

Make sure the virtual environment is activated and the required API credentials are configured.

Run:

```powershell
python main.py
```

The pipeline executes the extraction, transformation, and loading stages.

**Important:** Running the main pipeline may make live API requests and consume API calls. Use the existing saved data and analysis scripts when you only need to demonstrate the database or run tests.

## Running Automated Tests

Run the test suite from the project root:

```powershell
python -m pytest -v
```

The tests check behaviours such as:

- Inserting valid job records.
- Skipping duplicate records.
- Rejecting records without required fields.
- Transforming and cleaning job data.
- Handling missing files and optional fields.
- Testing the pipeline's integration and failure handling.

A successful run reports the number of tests passed and failed.

## Viewing the SQLite Database

The SQLite database is located at:

```text
data/processed/jobs.db
```

### Option 1: View database tables using Python in the terminal

First, start Python from the activated PowerShell terminal:

```powershell
python
```

At the Python `>>>` prompt, connect to the database:

```python
import sqlite3
c = sqlite3.connect("data/processed/jobs.db")
```

### List all tables

```python
print(c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
```

### View the first 10 job listings

```python
rows = c.execute("""
SELECT title, location, salary_min, salary_max
FROM adzuna_jobs
LIMIT 10
""").fetchall()

print("TITLE | LOCATION | MINIMUM SALARY | MAXIMUM SALARY")
for row in rows:
    print(row)
```

### Count the stored Adzuna jobs

```python
print(c.execute("SELECT COUNT(*) FROM adzuna_jobs").fetchone())
```

### Check for duplicate Adzuna IDs

```python
print(c.execute("""
SELECT adzuna_id, COUNT(*)
FROM adzuna_jobs
GROUP BY adzuna_id
HAVING COUNT(*) > 1
""").fetchall())
```

An empty result means this query found no duplicate IDs.

### View the database schema

```python
print(c.execute("PRAGMA table_info(adzuna_jobs)").fetchall())
```

When finished, close the connection:

```python
c.close()
```

To leave the Python prompt, type:

```python
exit()
```

**Note:** SQL statements are executed through Python's built-in `sqlite3` library. You do not need the separate SQLite command-line application for these examples.

## Running the Analysis Scripts

Run these commands from the project root in the activated virtual environment:

```powershell
python analyze_job_data.py
```

```powershell
python analyze_job_categories.py
```

```powershell
python analyze_job_locations.py
```

```powershell
python analyze_job_salaries.py
```

```powershell
python analyze_job_titles.py
```

These scripts analyse the saved database data. Review `analysis_report.md` for the findings and limitations.

## Current Analysis and Limitations

The analysis of the saved dataset found:

- 20 Adzuna job records in the database at the time of analysis.
- Job listings across several South African locations.
- Missing company names in some records.
- Salary information for only 2 of the 20 records.

The dataset is relatively small and does not represent the entire South African technology job market. Salary values should not be interpreted as monthly or annual amounts unless their pay period has been verified.

Results may change when new data is extracted.

## Data Quality and Reliability

The pipeline includes transformation and loading checks to improve data quality. The database loader skips duplicate records and records that do not have the required job ID or title.

Automated tests help verify expected behaviour and catch regressions when the code changes.

## Future Improvements

Possible future enhancements include:

- Adding a job freshness filter to identify expired listings.
- Scheduling automated pipeline runs.
- Expanding SQL analytics.
- Building an interactive analytics dashboard.
- Exploring PostgreSQL as an alternative database.

## Author

**Mashudu**

GitHub: https://github.com/lauramashudu-svg

