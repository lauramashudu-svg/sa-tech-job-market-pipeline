from src.transform.transform_jobs import transform_jobs


def test_transform_job_fields():
    raw_jobs = [
        {
            "id": 123,
            "title": "  Junior Data Engineer  ",
            "company": {"display_name": "Test Company"},
            "location": {"display_name": "Johannesburg"},
            "category": {"label": "IT Jobs"},
            "created": "2026-10-20T10:00:00Z",
            "salary_min": 15000,
            "salary_max": 20000,
            "salary_is_predicted": 0,
            "redirect_url": "https://example.com/job/123",
            "description": "  A data engineering role.  ",
        }
    ]

    result = transform_jobs(raw_jobs)

    assert len(result) == 1
    assert result[0]["job_id"] == "123"
    assert result[0]["job_title"] == "Junior Data Engineer"
    assert result[0]["company_name"] == "Test Company"
    assert result[0]["location"] == "Johannesburg"
    assert result[0]["salary_min"] == 15000
    assert result[0]["description"] == "A data engineering role."


def test_transform_empty_list():
    result = transform_jobs([])

    assert result == []


def test_transform_missing_optional_fields():
    raw_jobs = [
        {
            "id": 456,
            "title": "Data Analyst",
        }
    ]

    result = transform_jobs(raw_jobs)

    assert len(result) == 1
    assert result[0]["job_id"] == "456"
    assert result[0]["job_title"] == "Data Analyst"
    assert result[0]["company_name"] is None
    assert result[0]["location"] is None
    assert result[0]["salary_min"] is None
