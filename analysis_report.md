# South African Tech Job Market Analysis

## 1. Project Overview

This analysis explores job listings collected from the Adzuna API
and stored in a SQLite database.

The goal is to examine data quality, job categories, locations,
job titles, and salary information.

## 2. Dataset Summary

- Total Adzuna records analysed: 20
- Job category: All 20 records are labelled "IT Jobs"
- Records missing company names: 10 (50%)
- Records with salary information: 2 (10%)
- Records missing titles, locations, dates, or URLs: 0

## 3. Geographic Distribution

- Johannesburg, Gauteng: 7 listings
- South Africa (unspecified location): 4 listings
- Cape Town City Centre, Cape Town Region: 3 listings
- Centurion, Tshwane: 2 listings
- Pretoria, Tshwane: 2 listings
- Port Elizabeth, Nelson Mandela Bay: 1 listing
- Stellenbosch, Cape Winelands: 1 listing

Johannesburg has the largest count among the identifiable
city-level locations in this dataset.

## 4. Job Titles

Senior Software Developer is the most frequent exact title,
appearing twice. Several other listings are variations of
senior software developer roles with different locations
and work arrangements.

## 5. Salary Coverage

Only 2 of the 20 records contain salary information.

- C# Software Developer, Johannesburg: 600,000
- Software Development Manager, Centurion: 700,000

Adzuna marks both salary records as not predicted. The salary
period has not yet been verified, so these values should not
be interpreted as annual or monthly salaries.

## 6. Data Limitations

- The dataset contains only 20 records.
- Half the listings have no company name.
- Salary information is available for only 10% of records.
- All records share the same broad job category.
- The results describe the collected listings, not the entire
  South African technology job market.

## 7. Next Improvements

- Collect a larger dataset.
- Standardise job titles into broader role categories.
- Improve missing-value reporting.
- Add automated tests for data quality.
- Develop further SQL queries and visualisations.
