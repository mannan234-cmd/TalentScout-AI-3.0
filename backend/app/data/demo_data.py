"""
Seeds the in-memory demo store with:
  - an admin account and a sample student account (so the app is usable
    immediately after `uvicorn app.main:app --reload`)
  - a handful of active opportunities
  - one already-submitted, already-processed sample student so the
    dashboards aren't empty on first load

Only runs when DATA_PROVIDER=demo, and only once (guarded by a flag) even
if --reload triggers startup twice.
"""
import uuid
from datetime import datetime

from app.providers import get_data_provider
from app.api.auth import hash_password
from app.services.orchestrator import run_intake_pipeline

_SEEDED = False


def seed_demo_data():
    global _SEEDED
    if _SEEDED:
        return
    data = get_data_provider()

    # --- accounts ---
    admin = {
        "id": str(uuid.uuid4()),
        "full_name": "Admin Reviewer",
        "email": "admin@talentscout.ai",
        "hashed_password": hash_password("admin123"),
        "role": "admin",
        "student_id": None,
        "created_at": datetime.utcnow(),
    }
    data.create_user(admin)

    student_user = {
        "id": str(uuid.uuid4()),
        "full_name": "Sara Khan",
        "email": "sara@student.com",
        "hashed_password": hash_password("student123"),
        "role": "student",
        "student_id": None,
        "created_at": datetime.utcnow(),
    }
    data.create_user(student_user)

    # --- opportunities ---
    opportunities = [
        {
            "title": "Data Analyst Intern",
            "organization": "Nexora Analytics",
            "type": "internship",
            "description": "Support the BI team with dashboards, SQL reporting, and data cleaning.",
            "required_skills": ["sql", "excel", "data analysis", "power bi"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "careers@nexora-analytics.example.com",
        },
        {
            "title": "Junior Python Developer",
            "organization": "Bytework Labs",
            "type": "job",
            "description": "Build and maintain internal tools using Python and FastAPI.",
            "required_skills": ["python", "fastapi", "sql", "git"],
            "location": "Lahore, Pakistan",
            "is_active": True,
            "contact_email": "hiring@bytework-labs.example.com",
        },
        {
            "title": "AI Research Scholarship",
            "organization": "Frontier Institute",
            "type": "scholarship",
            "description": "Fund a semester of independent research in applied machine learning.",
            "required_skills": ["python", "machine learning", "research", "pytorch"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "scholarships@frontier-institute.example.com",
        },
        {
            "title": "Frontend Engineering Intern",
            "organization": "Pixelforge",
            "type": "internship",
            "description": "Build UI features with React and collaborate with designers on UX.",
            "required_skills": ["react", "javascript", "css", "figma"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "team@pixelforge.example.com",
        },
        # --- non-tech opportunities (Business, Media, Education, Healthcare, Law) ---
        {
            "title": "Digital Marketing Intern",
            "organization": "Brandloom Agency",
            "type": "internship",
            "description": "Plan and run social media campaigns and basic SEO for client brands.",
            "required_skills": ["digital marketing", "social media management", "seo", "content writing"],
            "location": "Karachi, Pakistan",
            "is_active": True,
            "contact_email": "careers@brandloom.example.com",
        },
        {
            "title": "Content Writer & Journalist",
            "organization": "Qalam Media House",
            "type": "job",
            "description": "Write and edit articles, interview sources, and manage an editorial calendar.",
            "required_skills": ["content writing", "journalism", "writing", "research"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "editorial@qalam-media.example.com",
        },
        {
            "title": "HR & Recruitment Intern",
            "organization": "Meridian Textiles",
            "type": "internship",
            "description": "Support hiring, onboarding, and employee engagement initiatives.",
            "required_skills": ["human resources", "recruitment", "communication", "negotiation"],
            "location": "Faisalabad, Pakistan",
            "is_active": True,
            "contact_email": "hr@meridian-textiles.example.com",
        },
        {
            "title": "Graphic Design Intern",
            "organization": "Studio Rung",
            "type": "internship",
            "description": "Design social media creatives, brand assets, and print collateral.",
            "required_skills": ["graphic design", "photoshop", "illustrator", "figma"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "hello@studio-rung.example.com",
        },
        {
            "title": "Teaching Assistant — Mathematics",
            "organization": "Horizon Academy",
            "type": "job",
            "description": "Assist lead teachers with lesson planning, grading, and tutoring sessions.",
            "required_skills": ["teaching", "tutoring", "communication", "curriculum design"],
            "location": "Lahore, Pakistan",
            "is_active": True,
            "contact_email": "staff@horizon-academy.example.com",
        },
        {
            "title": "Public Health Research Scholarship",
            "organization": "Sehat Foundation",
            "type": "scholarship",
            "description": "Fund a research project studying community health outcomes.",
            "required_skills": ["public health", "research", "academic research", "writing"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "grants@sehat-foundation.example.com",
        },
        {
            "title": "Legal Research Intern",
            "organization": "Adalat Chambers",
            "type": "internship",
            "description": "Assist lawyers with case research, drafting, and documentation.",
            "required_skills": ["law", "legal research", "paralegal", "writing"],
            "location": "Islamabad, Pakistan",
            "is_active": True,
            "contact_email": "intern@adalat-chambers.example.com",
        },
        {
            "title": "Event Management Intern",
            "organization": "Mehfil Events",
            "type": "internship",
            "description": "Coordinate logistics, vendors, and on-ground execution for client events.",
            "required_skills": ["event management", "hospitality", "communication", "project management"],
            "location": "Remote",
            "is_active": True,
            "contact_email": "team@mehfil-events.example.com",
        },
    ]
    for opp in opportunities:
        record = {"id": str(uuid.uuid4()), **opp, "created_at": datetime.utcnow()}
        data.create_opportunity(record)

    # --- one sample processed student, so dashboards have data on first load ---
    sample_student = {
        "id": str(uuid.uuid4()),
        "user_id": student_user["id"],
        "full_name": "Sara Khan",
        "email": "sara@student.com",
        "university": "University of the Punjab",
        "degree_program": "BS Computer Science",
        "graduation_year": 2026,
        "skills": ["python", "sql", "data analysis"],
        "bio": "Final-year CS student passionate about data-driven decision making.",
        "portfolio_url": "https://github.com/sara-khan-demo",
        "evidence_text": (
            "Built a Power BI dashboard analyzing university enrollment trends using SQL and Python.\n\n"
            "Completed a Kaggle data analysis project cleaning and visualizing e-commerce sales data with pandas.\n\n"
            "Interned part-time doing Excel-based reporting for a local retail business."
        ),
        "status": "new",
        "category": None,
        "potential_score": None,
        "is_high_potential": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": None,
    }
    data.create_student(sample_student)
    run_intake_pipeline(sample_student)
    student_user["student_id"] = sample_student["id"]

    # --- a second demo account: a NON-TECH student, to prove the platform
    # matches every field equally, not just Computer Science ---
    biz_user = {
        "id": str(uuid.uuid4()),
        "full_name": "Ayesha Raza",
        "email": "ayesha@student.com",
        "hashed_password": hash_password("student123"),
        "role": "student",
        "student_id": None,
        "created_at": datetime.utcnow(),
    }
    data.create_user(biz_user)

    biz_student = {
        "id": str(uuid.uuid4()),
        "user_id": biz_user["id"],
        "full_name": "Ayesha Raza",
        "email": "ayesha@student.com",
        "university": "Lahore School of Economics",
        "degree_program": "BBA Marketing",
        "graduation_year": 2026,
        "skills": ["digital marketing", "social media management", "content writing"],
        "bio": "Marketing student who loves building brand campaigns and writing copy.",
        "portfolio_url": "https://linkedin.com/in/ayesha-raza-demo",
        "evidence_text": (
            "Ran a 3-month Instagram growth campaign for a local cafe using content writing and social media management, growing followers by 40%.\n\n"
            "Wrote SEO-optimized blog posts for a university club's website.\n\n"
            "Led a team of 4 in a business plan competition, presenting the marketing strategy."
        ),
        "status": "new",
        "category": None,
        "potential_score": None,
        "is_high_potential": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "reviewed_by": None,
        "reviewed_at": None,
        "review_notes": None,
    }
    data.create_student(biz_student)
    run_intake_pipeline(biz_student)
    biz_user["student_id"] = biz_student["id"]

    _SEEDED = True
