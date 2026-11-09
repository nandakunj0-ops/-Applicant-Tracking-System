import sqlite3
 
from datetime import datetime
 
 
 
DB = "ats_database.db"
 
 
 
 
 
# ==========================================
 
# DATABASE CONNECTION AND TABLE CREATION
 
# ==========================================
 
 
 
def connect():
 
    con = sqlite3.connect(DB)
 
    con.execute("PRAGMA foreign_keys = ON")
 
    return con
 
 
 
 
 
def setup_database():
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    CREATE TABLE IF NOT EXISTS jobs(
 
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        title TEXT NOT NULL,
 
        department TEXT,
 
        skills TEXT,
 
        experience INTEGER,
 
        vacancies INTEGER
 
    )
 
    """)
 
 
 
    cur.execute("""
 
    CREATE TABLE IF NOT EXISTS applicants(
 
        applicant_id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        name TEXT NOT NULL,
 
        email TEXT UNIQUE NOT NULL,
 
        phone TEXT,
 
        skills TEXT,
 
        experience INTEGER,
 
        resume TEXT
 
    )
 
    """)
 
 
 
    cur.execute("""
 
    CREATE TABLE IF NOT EXISTS applications(
 
        application_id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        applicant_id INTEGER,
 
        job_id INTEGER,
 
        status TEXT DEFAULT 'Applied',
 
        applied_date TEXT,
 
        FOREIGN KEY(applicant_id)
 
            REFERENCES applicants(applicant_id)
 
            ON DELETE CASCADE,
 
        FOREIGN KEY(job_id)
 
            REFERENCES jobs(job_id)
 
            ON DELETE CASCADE,
 
        UNIQUE(applicant_id, job_id)
 
    )
 
    """)
 
 
 
    cur.execute("""
 
    CREATE TABLE IF NOT EXISTS interviews(
 
        interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
 
        application_id INTEGER,
 
        interview_date TEXT,
 
        interview_mode TEXT,
 
        result TEXT DEFAULT 'Pending',
 
        FOREIGN KEY(application_id)
 
            REFERENCES applications(application_id)
 
            ON DELETE CASCADE
 
    )
 
    """)
 
 
 
    con.commit()
 
    con.close()
 
 
 
 
 
# ==========================================
 
# JOB MANAGEMENT
 
# ==========================================
 
 
 
def add_job():
 
    print("\\n--- ADD NEW JOB ---")
 
 
 
    title = input("Job Title: ").strip()
 
    department = input("Department: ").strip()
 
    skills = input("Required Skills (comma separated): ").strip()
 
 
 
    try:
 
        experience = int(input("Required Experience: "))
 
        vacancies = int(input("Number of Vacancies: "))
 
 
 
        if experience < 0 or vacancies <= 0:
 
            print("Invalid experience or vacancy count.")
 
            return
 
 
 
    except ValueError:
 
        print("Enter valid numeric values.")
 
        return
 
 
 
    if not title:
 
        print("Job title is required.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    INSERT INTO jobs(title,department,skills,experience,vacancies)
 
    VALUES(?,?,?,?,?)
 
    """, (title, department, skills, experience, vacancies))
 
 
 
    con.commit()
 
    con.close()
 
 
 
    print("Job added successfully!")
 
 
 
 
 
def view_jobs():
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("SELECT * FROM jobs")
 
    jobs = cur.fetchall()
 
 
 
    print("\\n--- AVAILABLE JOBS ---")
 
 
 
    if not jobs:
 
        print("No jobs available.")
 
 
 
    for job in jobs:
 
        print("\\nJob ID:", job[0])
 
        print("Title:", job[1])
 
        print("Department:", job[2])
 
        print("Required Skills:", job[3])
 
        print("Experience:", job[4], "years")
 
        print("Vacancies:", job[5])
 
 
 
    con.close()
 
 
 
 
 
def delete_job():
 
    try:
 
        job_id = int(input("Enter Job ID: "))
 
    except ValueError:
 
        print("Invalid Job ID.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("DELETE FROM jobs WHERE job_id=?", (job_id,))
 
    con.commit()
 
 
 
    print("Job deleted." if cur.rowcount else "Job not found.")
 
    con.close()
 
 
 
 
 
# ==========================================
 
# APPLICANT MANAGEMENT
 
# ==========================================
 
 
 
def add_applicant():
 
    print("\\n--- APPLICANT REGISTRATION ---")
 
 
 
    name = input("Name: ").strip()
 
    email = input("Email: ").strip()
 
    phone = input("Phone: ").strip()
 
    skills = input("Skills (comma separated): ").strip()
 
    resume = input("Resume Summary: ").strip()
 
 
 
    try:
 
        experience = int(input("Experience in years: "))
 
        if experience < 0:
 
            print("Experience cannot be negative.")
 
            return
 
    except ValueError:
 
        print("Enter valid experience.")
 
        return
 
 
 
    if not name or not email:
 
        print("Name and email are required.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    try:
 
        cur.execute("""
 
        INSERT INTO applicants
 
        (name,email,phone,skills,experience,resume)
 
        VALUES(?,?,?,?,?,?)
 
        """, (name,email,phone,skills,experience,resume))
 
 
 
        con.commit()
 
        print("Applicant registered successfully!")
 
 
 
    except sqlite3.IntegrityError:
 
        print("This email is already registered.")
 
 
 
    con.close()
 
 
 
 
 
def view_applicants():
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("SELECT * FROM applicants")
 
    records = cur.fetchall()
 
 
 
    print("\\n--- REGISTERED APPLICANTS ---")
 
 
 
    if not records:
 
        print("No applicants found.")
 
 
 
    for a in records:
 
        print("\\nApplicant ID:", a[0])
 
        print("Name:", a[1])
 
        print("Email:", a[2])
 
        print("Phone:", a[3])
 
        print("Skills:", a[4])
 
        print("Experience:", a[5], "years")
 
        print("Resume:", a[6])
 
 
 
    con.close()
 
 
 
 
 
def search_applicant():
 
    keyword = input("Enter name, email or skill: ").strip()
 
    pattern = "%" + keyword + "%"
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    SELECT * FROM applicants
 
    WHERE name LIKE ? OR email LIKE ? OR skills LIKE ?
 
    """, (pattern, pattern, pattern))
 
 
 
    records = cur.fetchall()
 
 
 
    if records:
 
        for a in records:
 
            print("\\nID:", a[0], "| Name:", a[1])
 
            print("Email:", a[2], "| Skills:", a[4])
 
            print("Experience:", a[5])
 
    else:
 
        print("No matching applicant found.")
 
 
 
    con.close()
 
 
 
 
 
def delete_applicant():
 
    try:
 
        aid = int(input("Enter Applicant ID: "))
 
    except ValueError:
 
        print("Invalid ID.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute(
 
        "DELETE FROM applicants WHERE applicant_id=?", (aid,)
 
    )
 
 
 
    con.commit()
 
    print("Applicant deleted." if cur.rowcount else "Applicant not found.")
 
    con.close()
 
 
 
 
 
# ==========================================
 
# JOB APPLICATION
 
# ==========================================
 
 
 
def apply_for_job():
 
    try:
 
        aid = int(input("Enter Applicant ID: "))
 
        jid = int(input("Enter Job ID: "))
 
    except ValueError:
 
        print("Enter valid IDs.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    INSERT INTO applications
 
    (applicant_id,job_id,applied_date)
 
    VALUES(?,?,?)
 
    """, (aid, jid, datetime.now().strftime("%Y-%m-%d")))
 
 
 
    try:
 
        con.commit()
 
        print("Application submitted successfully!")
 
 
 
    except sqlite3.IntegrityError:
 
        print("Invalid applicant/job ID or duplicate application.")
 
        con.rollback()
 
 
 
    con.close()
 
 
 
 
 
def view_applications():
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    SELECT a.application_id, p.name, j.title,
 
           a.status, a.applied_date
 
    FROM applications a
 
    JOIN applicants p
 
        ON a.applicant_id = p.applicant_id
 
    JOIN jobs j
 
        ON a.job_id = j.job_id
 
    ORDER BY a.application_id
 
    """)
 
 
 
    records = cur.fetchall()
 
 
 
    print("\\n--- APPLICATION RECORDS ---")
 
 
 
    if not records:
 
        print("No applications found.")
 
 
 
    for r in records:
 
        print("\\nApplication ID:", r[0])
 
        print("Applicant:", r[1])
 
        print("Job:", r[2])
 
        print("Status:", r[3])
 
        print("Applied Date:", r[4])
 
 
 
    con.close()
 
 
 
 
 
# ==========================================
 
# SKILL MATCHING SYSTEM
 
# ==========================================
 
 
 
def skill_matching():
 
    try:
 
        aid = int(input("Enter Applicant ID: "))
 
        jid = int(input("Enter Job ID: "))
 
    except ValueError:
 
        print("Invalid ID.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    SELECT p.name,p.skills,p.experience,
 
           j.title,j.skills,j.experience
 
    FROM applicants p, jobs j
 
    WHERE p.applicant_id=? AND j.job_id=?
 
    """, (aid, jid))
 
 
 
    record = cur.fetchone()
 
 
 
    if not record:
 
        print("Applicant or job not found.")
 
        con.close()
 
        return
 
 
 
    name, candidate_skills, exp, title, required, required_exp = record
 
 
 
    candidate = {
 
        s.strip().lower()
 
        for s in (candidate_skills or "").split(",")
 
        if s.strip()
 
    }
 
 
 
    requirements = {
 
        s.strip().lower()
 
        for s in (required or "").split(",")
 
        if s.strip()
 
    }
 
 
 
    if requirements:
 
        matched = candidate.intersection(requirements)
 
        score = round(len(matched) / len(requirements) * 100)
 
    else:
 
        matched = set()
 
        score = 0
 
 
 
    print("\\n--- CANDIDATE MATCHING REPORT ---")
 
    print("Applicant:", name)
 
    print("Applied Position:", title)
 
    print("Matched Skills:", ", ".join(sorted(matched)) or "None")
 
    print("Skill Match:", str(score) + "%")
 
    print("Experience:", exp, "years")
 
    print("Required Experience:", required_exp, "years")
 
 
 
    if score >= 70 and exp >= required_exp:
 
        print("Recommendation: Good Match")
 
    elif score >= 40:
 
        print("Recommendation: Partial Match")
 
    else:
 
        print("Recommendation: Low Match")
 
 
 
    con.close()
 
 
 
 
 
# ==========================================
 
# APPLICATION STATUS MANAGEMENT
 
# ==========================================
 
 
 
def update_status():
 
    try:
 
        app_id = int(input("Enter Application ID: "))
 
    except ValueError:
 
        print("Invalid ID.")
 
        return
 
 
 
    statuses = {
 
        "1": "Applied",
 
        "2": "Shortlisted",
 
        "3": "Interview",
 
        "4": "Selected",
 
        "5": "Rejected"
 
    }
 
 
 
    print("\\n1. Applied")
 
    print("2. Shortlisted")
 
    print("3. Interview")
 
    print("4. Selected")
 
    print("5. Rejected")
 
 
 
    choice = input("Select new status: ")
 
 
 
    if choice not in statuses:
 
        print("Invalid status.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    UPDATE applications SET status=?
 
    WHERE application_id=?
 
    """, (statuses[choice], app_id))
 
 
 
    con.commit()
 
 
 
    print("Status updated." if cur.rowcount else "Application not found.")
 
    con.close()
 
 
 
 
 
# ==========================================
 
# INTERVIEW MANAGEMENT
 
# ==========================================
 
 
 
def schedule_interview():
 
    try:
 
        app_id = int(input("Enter Application ID: "))
 
    except ValueError:
 
        print("Invalid application ID.")
 
        return
 
 
 
    date = input("Interview Date (YYYY-MM-DD): ").strip()
 
    mode = input("Interview Mode (Online/Offline): ").strip()
 
 
 
    try:
 
        datetime.strptime(date, "%Y-%m-%d")
 
    except ValueError:
 
        print("Invalid date format.")
 
        return
 
 
 
    if mode.lower() not in ("online", "offline"):
 
        print("Choose Online or Offline.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    SELECT application_id FROM applications
 
    WHERE application_id=?
 
    """, (app_id,))
 
 
 
    if not cur.fetchone():
 
        print("Application not found.")
 
        con.close()
 
        return
 
 
 
    cur.execute("""
 
    INSERT INTO interviews
 
    (application_id,interview_date,interview_mode)
 
    VALUES(?,?,?)
 
    """, (app_id, date, mode.title()))
 
 
 
    cur.execute("""
 
    UPDATE applications SET status='Interview'
 
    WHERE application_id=?
 
    """, (app_id,))
 
 
 
    con.commit()
 
    con.close()
 
 
 
    print("Interview scheduled successfully!")
 
 
 
 
 
def view_interviews():
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    SELECT i.interview_id,p.name,j.title,
 
           i.interview_date,i.interview_mode,i.result
 
    FROM interviews i
 
    JOIN applications a ON i.application_id=a.application_id
 
    JOIN applicants p ON a.applicant_id=p.applicant_id
 
    JOIN jobs j ON a.job_id=j.job_id
 
    """)
 
 
 
    records = cur.fetchall()
 
 
 
    print("\\n--- INTERVIEW SCHEDULE ---")
 
 
 
    if not records:
 
        print("No interviews scheduled.")
 
 
 
    for r in records:
 
        print("\\nInterview ID:", r[0])
 
        print("Applicant:", r[1])
 
        print("Position:", r[2])
 
        print("Date:", r[3])
 
        print("Mode:", r[4])
 
        print("Result:", r[5])
 
 
 
    con.close()
 
 
 
 
 
def update_interview_result():
 
    try:
 
        iid = int(input("Enter Interview ID: "))
 
    except ValueError:
 
        print("Invalid ID.")
 
        return
 
 
 
    print("1. Pending")
 
    print("2. Passed")
 
    print("3. Failed")
 
 
 
    choice = input("Select result: ")
 
 
 
    results = {
 
        "1": "Pending",
 
        "2": "Passed",
 
        "3": "Failed"
 
    }
 
 
 
    if choice not in results:
 
        print("Invalid choice.")
 
        return
 
 
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    cur.execute("""
 
    UPDATE interviews SET result=?
 
    WHERE interview_id=?
 
    """, (results[choice], iid))
 
 
 
    con.commit()
 
    print("Interview result updated." if cur.rowcount else "Interview not found.")
 
 
 
    con.close()
 
 
 
 
 
# ==========================================
 
# RECRUITMENT REPORT
 
# ==========================================
 
 
 
def recruitment_report():
 
    con = connect()
 
    cur = con.cursor()
 
 
 
    print("\\n========== RECRUITMENT REPORT ==========")
 
 
 
    cur.execute("SELECT COUNT(*) FROM applicants")
 
    print("Total Applicants:", cur.fetchone()[0])
 
 
 
    cur.execute("SELECT COUNT(*) FROM jobs")
 
    print("Total Job Vacancies:", cur.fetchone()[0])
 
 
 
    cur.execute("SELECT COUNT(*) FROM applications")
 
    print("Total Applications:", cur.fetchone()[0])
 
 
 
    cur.execute("""
 
    SELECT status,COUNT(*)
 
    FROM applications
 
    GROUP BY status
 
    """)
 
 
 
    print("\\n--- APPLICATION STATUS ---")
 
 
 
    for status, count in cur.fetchall():
 
        print(status + ":", count)
 
 
 
    cur.execute("""
 
    SELECT title,COUNT(a.application_id)
 
    FROM jobs j
 
    LEFT JOIN applications a ON j.job_id=a.job_id
 
    GROUP BY j.job_id
 
    """)
 
 
 
    print("\\n--- JOB-WISE APPLICATIONS ---")
 
 
 
    for title, count in cur.fetchall():
 
        print(title + ":", count)
 
 
 
    con.close()
 
 
 
 
 
# ==========================================
 
# MAIN MENU
 
# ==========================================
 
 
 
def main():
 
    setup_database()
 
 
 
    while True:
 
        print("\\n==========================================")
 
        print("       APPLICANT TRACKING SYSTEM")
 
        print("==========================================")
 
 
 
        print("1.  Add Job")
 
        print("2.  View Jobs")
 
        print("3.  Delete Job")
 
        print("4.  Register Applicant")
 
        print("5.  View Applicants")
 
        print("6.  Search Applicant")
 
        print("7.  Delete Applicant")
 
        print("8.  Apply for Job")
 
        print("9.  View Applications")
 
        print("10. Skill Matching")
 
        print("11. Update Application Status")
 
        print("12. Schedule Interview")
 
        print("13. View Interviews")
 
        print("14. Update Interview Result")
 
        print("15. Recruitment Report")
 
        print("16. Exit")
 
 
 
        choice = input("\\nEnter your choice: ")
 
 
 
        menu = {
 
            "1": add_job,
 
            "2": view_jobs,
 
            "3": delete_job,
 
            "4": add_applicant,
 
            "5": view_applicants,
 
            "6": search_applicant,
 
            "7": delete_applicant,
 
            "8": apply_for_job,
 
            "9": view_applications,
 
            "10": skill_matching,
 
            "11": update_status,
 
            "12": schedule_interview,
 
            "13": view_interviews,
 
            "14": update_interview_result,
 
            "15": recruitment_report
 
        }
 
 
 
        if choice == "16":
 
            print("Thank you for using ATS!")
 
            break
 
 
 
        elif choice in menu:
 
            menu[choice]()
 
 
 
        else:
 
            print("Invalid choice! Try again.")
 
 
 
 
 
if __name__ == "__main__":
 
    setup_database()
 
    main()
