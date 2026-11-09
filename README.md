# Applicant Tracking System (ATS)

**A Python and SQLite Based Recruitment Management System**

## 1. Project Overview

The Applicant Tracking System (ATS) is a console-based recruitment management application developed using Python and SQLite.

It is designed to simplify the recruitment process by managing job vacancies, applicant information, job applications, candidate skill matching, interview scheduling and recruitment reports.

## 2. Objectives

- To automate basic recruitment activities.
- To maintain applicant and job records.
- To simplify application tracking.
- To evaluate candidates based on skill matching.
- To manage interview schedules and results.
- To generate recruitment reports.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application development |
| SQLite3 | Database management |
| SQL | Database operations |
| Sublime Text | Code editor |
| GitHub | Source code management |

## 4. Key Features

1. Job Management – Add, view and delete jobs.
2. Applicant Registration – Store candidate details.
3. Applicant Management – View, search and delete applicants.
4. Job Applications – Apply for available jobs.
5. Skill Matching – Calculate candidate skill match percentage.
6. Application Status – Track application progress.
7. Interview Management – Schedule interviews.
8. Interview Results – Update interview outcomes.
9. Recruitment Reports – Generate recruitment statistics.

## 5. Database Design

The system contains four main database tables:

- **jobs:** Stores job details and vacancy information.
- **applicants:** Stores candidate details and skills.
- **applications:** Maintains applicant-job relationships.
- **interviews:** Stores interview schedules and results.

## 6. Application Status

- Applied
- Shortlisted
- Interview
- Selected
- Rejected

## 7. Interview Results

- Pending
- Passed
- Failed

## 8. Installation and Execution

### Requirements
- Python 3.x
- SQLite3 (included with Python)

### Steps

1. Clone or download this repository.
2. Open the project folder in Terminal.
3. Run the following command:

```bash
python3 ats.py
```

4. The database will be created automatically.
5. Use the interactive menu to access the system.

## 9. Skill Matching Logic

The system compares candidate skills with the required job skills.

**Skill Match Percentage:**

Matched Skills / Total Required Skills × 100

The system also considers candidate experience when generating recommendations.

## 10. Future Scope

- Graphical User Interface (GUI).
- Resume file upload and parsing.
- Advanced candidate filtering.
- Email notifications.
- User authentication and role management.
- Advanced recruitment analytics.

## 11. Conclusion

The Applicant Tracking System provides a simple and structured way to manage recruitment activities. It demonstrates the practical implementation of Python programming, database connectivity, SQL queries and CRUD operations.

## 12. Author

**Name:** [Your Name]  
**Course:** [Your Course]  
**College:** [Your College Name]  
**Project:** Applicant Tracking System
