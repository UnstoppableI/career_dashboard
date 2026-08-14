-- Career Lains AI Database Schema

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    target_role TEXT DEFAULT 'Software Engineer',
    experience_level TEXT DEFAULT 'Fresher / Student',
    bio TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL DEFAULT 'My Resume',
    personal_info TEXT DEFAULT '{}',
    summary TEXT DEFAULT '',
    education TEXT DEFAULT '[]',
    experience TEXT DEFAULT '[]',
    projects TEXT DEFAULT '[]',
    skills TEXT DEFAULT '[]',
    certifications TEXT DEFAULT '[]',
    theme TEXT DEFAULT 'modern',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ats_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    job_role TEXT DEFAULT 'Software Developer',
    ats_score INTEGER NOT NULL,
    summary TEXT DEFAULT '',
    strengths TEXT DEFAULT '[]',
    weaknesses TEXT DEFAULT '[]',
    missing_skills TEXT DEFAULT '[]',
    keywords TEXT DEFAULT '[]',
    suggestions TEXT DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    logo_symbol TEXT DEFAULT '🏢',
    category TEXT NOT NULL, -- Service Based, Product Based, Tech Giant, Consulting
    tagline TEXT DEFAULT '',
    description TEXT DEFAULT '',
    required_skills TEXT DEFAULT '[]',
    eligibility TEXT DEFAULT '',
    interview_process TEXT DEFAULT '[]',
    previous_questions TEXT DEFAULT '[]',
    salary_details TEXT DEFAULT '',
    hiring_trends TEXT DEFAULT '',
    min_cgpa REAL DEFAULT 6.0,
    experience_req TEXT DEFAULT '0-2 Years'
);

CREATE TABLE IF NOT EXISTS interview_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    company_name TEXT NOT NULL,
    role TEXT NOT NULL,
    category TEXT NOT NULL, -- Technical, HR, Managerial
    question TEXT NOT NULL,
    user_answer TEXT DEFAULT '',
    score INTEGER DEFAULT 0,
    feedback TEXT DEFAULT '{}',
    sample_answer TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sender TEXT NOT NULL, -- 'user' or 'ai'
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
