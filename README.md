WTC-V4RF645G

## South African Tech Job Market Pipeline

A Python ETL (Extract, Transform, Load) project that collects technology job listings from the Adzuna API, cleans and standardises the data, stores it in SQLite, and analyses job-market trends using SQL.

The project demonstrates data engineering fundamentals, API integration, data quality checks, database management, automated testing, and colourful terminal reporting.

## Project Demonstration

Watch the project demonstration video:

[South African Tech Job Market Pipeline – Demo Video](https://youtu.be/pykj6qG665U)

##  Project Overview

The **South African Tech Job Market Pipeline** is designed to process technology job listings and make the resulting data easier to inspect and analyse.

The pipeline follows three main stages:

1. **Extract:** Retrieve job listings from the Adzuna API.
2. **Transform:** Clean and standardise job records.
3. **Load:** Store job records in a SQLite database while handling duplicate and invalid records.

Rich is used to improve terminal output with colourful headings, panels, tables, and status messages.

##  Project Objectives

- Extract technology job listings using the Adzuna API.
- Save raw and transformed job data as JSON files.
- Clean and standardise job listing fields.
- Store job records in a SQLite database.
- Prevent duplicate records from being inserted.
- Handle missing required fields and optional values.
- Validate pipeline behaviour using automated tests.
- Analyse job titles, locations, categories, and salary availability.
- Present analysis results in readable terminal tables.

## Technologies Used

Python — ETL pipeline, data processing, and analysis.

Adzuna API — Source of technology job listings.

SQLite — Storing and managing job records.

SQL — Querying and analysing job-market data.

pytest — Automated testing and validation.

Rich — Colourful terminal output, panels, and tables.

Git and GitHub — Version control and project hosting.

##  ETL Pipeline

### 1. Extract

The extraction module retrieves job listings from the Adzuna API and saves raw data for further processing.

### 2. Transform

The transformation module cleans and standardises fields such as job titles, company names, locations, dates, salary information, URLs, and descriptions.

### 3. Load

The loading module inserts eligible records into SQLite. It handles duplicate job IDs and skips records that do not meet the required ID and title checks.

The main entry point is `main.py`.

##  Project Structure

```text
sa-tech-job-market-pipeline/
├── data/
│   ├── raw/
│   │   └── adzuna_jobs.json
│   └── processed/
│       ├── adzuna_jobs_clean.json
│       └── jobs_recovered.db
├── src/
│   ├── extract/
│   │   └── adzuna_api.py
│   ├── transform/
│   │   └── transform_jobs.py
│   ├── load/
│   │   └── load_jobs.py
│   └── terminal_style.py
├── tests/
│   ├── test_load.py
│   ├── test_pipeline_integration.py
│   └── test_transform.py
├── analyze_job_categories.py
├── analyze_job_data.py
├── analyze_job_locations.py
├── analyze_job_salaries.py
├── analyze_job_titles.py
├── inspect_database.py
├── recover_database.py
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The structure above highlights the main project files. Other local files, such as virtual environments and generated database backups, may also exist.

**Security note:** The `.env` file is local configuration and must not be committed to the public repository. It is shown above to explain its role, not as a file to publish.

##  Setup and Installation

### 1. Clone the repository

```powershell
git clone https://github.com/lauramashudu-svg/sa-tech-job-market-pipeline.git
cd sa-tech-job-market-pipeline
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The project uses Rich for styled terminal output and pytest for automated testing. Make sure these packages are included in `requirements.txt`.

If needed, install them in your active virtual environment:

```powershell
python -m pip install rich pytest
```

### 5. Configure Adzuna API credentials

Create a local `.env` file in the project root and provide the credentials required by the extraction module.

Use the environment variable names expected by the project's code.

Never commit `.env`, expose API keys in screenshots, or include credentials in demonstration videos.

##  Running the ETL Pipeline

With your virtual environment activated and API credentials configured, run:

```powershell
python main.py
```

The pipeline runs the extraction, transformation, and loading stages, with styled terminal output.

**Important:** Running `main.py` can make live API requests and consume API calls. The analysis scripts and automated tests can be run separately when you do not need to retrieve fresh data.

##  Running Automated Tests

Run the test suite from the project root:

```powershell
python -m pytest -v
```

The latest verified test run reported:

**13 passed, 0 failed.**

The tests cover behaviours including:

- Inserting valid job records.
- Skipping duplicate records.
- Skipping records with missing required fields.
- Reading cleaned job
