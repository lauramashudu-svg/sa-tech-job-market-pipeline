import sqlite3
import json

from src.load import load_jobs as load_module


def sample_job(job_id="12345", title="Junior Data Engineer"):
    """Return one cleaned job record for testing."""
    return {
        "job_id": job_id,
        "job_title": title,
        "company_name": "Test Company",
        "location": "Johannesburg",
        "category": "IT Jobs",
        "date_posted": "2026-10-20T10:00:00Z",
        "salary_min": 15000,
        "salary_max": 20000,
        "salary_is_predicted": "0",
        "job_url": "https://example.com/job/12345",
        "description": "Test job description.",
    }


def setup_test_database(tmp_path, monkeypatch):
    """Direct the loader to a temporary database."""
    test_database = tmp_path / "test_jobs.db"
    monkeypatch.setattr(load_module, "DATABASE_FILE", test_database)
    return test_database


def test_load_inserts_job(tmp_path, monkeypatch):
    database = setup_test_database(tmp_path, monkeypatch)

    load_module.load_jobs([sample_job()])

    connection = sqlite3.connect(database)
    try:
        result = connection.execute(
            "SELECT adzuna_id, title, company, location "
            "FROM adzuna_jobs"
        ).fetchone()
    finally:
        connection.close()

    assert result == (
        "12345",
        "Junior Data Engineer",
        "Test Company",
        "Johannesburg",
    )


def test_load_skips_duplicate_job(tmp_path, monkeypatch, capsys):
    database = setup_test_database(tmp_path, monkeypatch)
    job = sample_job()

    load_module.load_jobs([job])
    load_module.load_jobs([job])

    output = capsys.readouterr().out

    assert "New Adzuna jobs inserted: 0" in output
    assert "Duplicate jobs skipped: 1" in output

    connection = sqlite3.connect(database)
    try:
        count = connection.execute(
            "SELECT COUNT(*) FROM adzuna_jobs"
        ).fetchone()[0]
    finally:
        connection.close()

    assert count == 1


def test_load_skips_job_without_id_or_title(
    tmp_path, monkeypatch, capsys
):
    database = setup_test_database(tmp_path, monkeypatch)

    invalid_jobs = [
        sample_job(job_id=""),
        sample_job(job_id="67890", title=""),
    ]

    load_module.load_jobs(invalid_jobs)

    output = capsys.readouterr().out

    assert output.count("Skipping a job") == 2

    connection = sqlite3.connect(database)
    try:
        count = connection.execute(
            "SELECT COUNT(*) FROM adzuna_jobs"
        ).fetchone()[0]
    finally:
        connection.close()

    assert count == 0


import json


def test_read_cleaned_jobs(tmp_path, monkeypatch):
    cleaned_file = tmp_path / "jobs.json"

    jobs = [
        {
            "job_id": "12345",
            "job_title": "Junior Data Engineer",
        }
    ]

    cleaned_file.write_text(
        json.dumps(jobs),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        load_module,
        "DATA_FILE",
        cleaned_file,
    )

    result = load_module.read_cleaned_jobs()

    assert result == jobs


def test_read_cleaned_jobs_missing_file(tmp_path, monkeypatch):
    missing_file = tmp_path / "missing.json"

    monkeypatch.setattr(
        load_module,
        "DATA_FILE",
        missing_file,
    )

    try:
        load_module.read_cleaned_jobs()
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass

