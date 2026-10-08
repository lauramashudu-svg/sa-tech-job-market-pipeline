import re
from typing import Any, Dict, List


def extract_skills(description: str) -> List[str]:
     #Parse skill tags from the description text
    known_skills = [
        "python", "java", "sql", "postgresql", "mysql", "aws", 
        "docker", "kubernetes", "linux", "terraform", "react", 
        "javascript", "html", "css", "spring", "git", "power bi", "excel"
    ]
    desc_lower = description.lower()
    found_skills = [skill.title() for skill in known_skills if re.search(rf"\b{re.escape(skill)}\b", desc_lower)]
    return sorted(list(set(found_skills)))


def classify_seniority(title: str) -> str:
    #Categorize role ranking based on title keywords
    title_lower = title.lower()
    if "junior" in title_lower or "intern" in title_lower or "graduate" in title_lower:
        return "Junior"
    elif "senior" in title_lower or "lead" in title_lower or "principal" in title_lower:
        return "Senior"
    return "Mid-Level"


def classify_domain(title: str) -> str:
    #Classify the technical discipline
    title_lower = title.lower()
    if "data engineer" in title_lower:
        return "Data Engineering"
    elif "data analyst" in title_lower or "analytics" in title_lower:
        return "Data Analytics"
    elif "cloud" in title_lower or "devops" in title_lower:
        return "Cloud & DevOps"
    elif "frontend" in title_lower or "backend" in title_lower or "developer" in title_lower:
        return "Software Development"
    return "Other"


def transform_jobs(raw_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    #Transform and enrich raw job records
    processed_jobs = []

    for job in raw_jobs:
        skills = extract_skills(job.get("description", ""))
        
        cleaned = {
            "job_id": int(job["job_id"]),
            "title": job["title"].strip(),
            "company": job["company"].strip(),
            "location": job["location"].strip(),
            "date_posted": job["date_posted"].strip(),
            "seniority": classify_seniority(job.get("title", "")),
            "domain": classify_domain(job.get("title", "")),
            "skills": ", ".join(skills),
            "skill_count": len(skills),
        }
        processed_jobs.append(cleaned)

    return processed_jobs


if __name__ == "__main__":
    sample_data = [
        {"job_id": "1", "title": "Junior Java Developer", "company": "Tech Solutions", 
         "location": "Johannesburg", "description": "Java SQL Git Docker", "date_posted": "2026-09-15"},
        {"job_id": "4", "title": "Junior Data Engineer", "company": "Analytics SA", 
         "location": "Johannesburg", "description": "Python SQL PostgreSQL Docker", "date_posted": "2026-09-12"}
    ]
    transformed = transform_jobs(sample_data)
    for t in transformed:
        print(t)