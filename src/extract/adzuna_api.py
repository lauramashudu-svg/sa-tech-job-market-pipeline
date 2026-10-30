#Extract South African technology job listings from the Adzuna API.

import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


#Find the main project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#Load credentials from the .env file in the project root.
load_dotenv(PROJECT_ROOT / ".env")

#Read credentials without displaying them.
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

#Adzuna's South African job search endpoint.
API_URL = "https://api.adzuna.com/v1/api/jobs/za/search/1"


def extract_adzuna_jobs():
    #Fetch one page of software developer jobs and save the raw response.

    if not APP_ID or not APP_KEY:
        raise ValueError(
            "Adzuna credentials are missing. Check the .env file "
            "in your project root."
        )

    #Request a maximum of 10 jobs to keep the first test small.
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "what": "software developer",
        "content-type": "application/json",
    }

    print("Connecting to the Adzuna API...")

    response = requests.get(
        API_URL,
        params=params,
        timeout=20,
    )

    #Raise an error if the API returns an unsuccessful HTTP status.
    response.raise_for_status()

    #Convert the JSON response into Python data.
    data = response.json()

    #Save the original API response for later transformation.
    output_file = PROJECT_ROOT / "data" / "raw" / "adzuna_jobs.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    jobs = data.get("results", [])

    print(f"Jobs returned: {len(jobs)}")
    print(f"Raw response saved to: {output_file.relative_to(PROJECT_ROOT)}")

    return jobs


if __name__ == "__main__":
    try:
        extract_adzuna_jobs()
    except requests.exceptions.HTTPError as error:
        print(f"Adzuna returned an HTTP error: {error.response.status_code}")
        print("Check your API access, credentials and request parameters.")
    except requests.exceptions.RequestException as error:
        print(f"Could not connect to Adzuna: {error}")
    except ValueError as error:
        print(f"Configuration or response error: {error}")
