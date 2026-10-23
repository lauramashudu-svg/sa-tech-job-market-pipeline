import json
from unittest.mock import patch

import main


def test_pipeline_integration(tmp_path):
    #Create one sample raw job.
    raw_jobs = [
        {
            "id": 12345,
            "title": "Junior Data Engineer",
            "company": {"display_name": "Test Company"},
            "location": {"display_name": "Johannesburg"},
            "category": {"label": "IT Jobs"},
            "created": "2026-10-20T10:00:00Z",
            "salary_min": 15000,
            "salary_max": 20000,
            "salary_is_predicted": 0,
            "redirect_url": "https://example.com/job/12345",
            "description": "A test data engineering role.",
        }
    ]

    # Save the output to a temporary file, not your real data.
    output_file = tmp_path / "jobs_clean.json"

    with (
        patch.object(
            main,
            "extract_adzuna_jobs",
            return_value=raw_jobs,
        ) as mock_extract,
        patch.object(
            main,
            "OUTPUT_FILE",
            output_file,
        ),
        patch.object(main, "load_jobs") as mock_load,
    ):
        main.main()

    #Confirm extraction and loading were called.
    mock_extract.assert_called_once()
    mock_load.assert_called_once()

    #Confirm the cleaned JSON was saved correctly.
    saved_jobs = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert len(saved_jobs) == 1
    assert saved_jobs[0]["job_id"] == "12345"
    assert saved_jobs[0]["job_title"] == "Junior Data Engineer"

    #Confirm the loader received the same cleaned records.
    assert mock_load.call_args.args[0] == saved_jobs
