import csv


def extract_jobs(file_path):
    """Read raw job data from a CSV file."""

    jobs = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            jobs.append(row)

    return jobs


if __name__ == "__main__":
    data = extract_jobs("data/raw/jobs.csv")

    print("SA Tech Job Market Pipeline")
    print("---------------------------")
    print(f"Jobs extracted: {len(data)}")
    print()

    for job in data[:5]:
        print(job)