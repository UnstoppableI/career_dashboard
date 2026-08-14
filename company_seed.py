import sqlite3
import json
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

COMPANIES_DATA = [
    {
        "slug": "tcs",
        "name": "Tata Consultancy Services (TCS)",
        "logo_symbol": "💼",
        "category": "Service Based Giant",
        "tagline": "Building on Belief - India's largest IT Services company.",
        "description": "TCS conducts massive placement drives like TCS NQT (National Qualifier Test) offering roles in TCS Ninja (3.36 - 4.5 LPA), Digital (7 - 7.5 LPA), and Prime (9 - 11.5 LPA).",
        "required_skills": json.dumps(["C", "C++", "Java", "Python", "Data Structures", "SQL", "OOPs", "Aptitude", "Communication"]),
        "eligibility": "B.Tech / M.Tech / MCA / B.Sc / BCA with min 60% or 6.0 CGPA throughout 10th, 12th, and Graduation. Max 1 active backlog allowed at time of test.",
        "interview_process": json.dumps([
            "Round 1: TCS NQT Online Test (Aptitude, Verbal, Reasoning, Coding)",
            "Round 2: Technical Interview (Core CS, Coding, Project deep-dive)",
            "Round 3: HR & Managerial Interview (Situational, Behavioral, Willingness to relocate)"
        ]),
        "previous_questions": json.dumps([
            "Write a program to check if a number is Palindrome without converting to String.",
            "Explain the difference between Primary Key, Candidate Key, and Unique Key in SQL.",
            "What is OOPs polymorphism? Differentiate Method Overloading vs Overriding with code.",
            "Explain your final year project architecture and your specific contribution.",
            "How do you handle working in tight deadline projects under pressure?"
        ]),
        "salary_details": "Ninja: ₹3.36L - ₹4.5L | Digital: ₹7.0L - ₹7.5L | Prime: ₹9.0L - ₹11.5L PA",
        "hiring_trends": "Hiring peak: Aug - Oct via TCS NQT. High demand for Full-Stack, Java Microservices, Cloud (AWS/Azure), and Data Engineering skills.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 2 Years (Freshers & Junior Engineers)"
    },
    {
        "slug": "google",
        "name": "Google",
        "logo_symbol": "🔍",
        "category": "Product Giant (FAANG)",
        "tagline": "Organizing the world's information and making it universally accessible.",
        "description": "Google hires Software Development Engineers (SDE / SWE-1) via campus recruiting (STEP Internships, Girl Hackathon) and off-campus career portals.",
        "required_skills": json.dumps(["Data Structures & Algorithms", "System Design", "C++", "Python", "Java", "Graphs", "Dynamic Programming", "Concurrency"]),
        "eligibility": "B.Tech / M.Tech / Ph.D. in Computer Science or related STEM field. Strong problem-solving proficiency.",
        "interview_process": json.dumps([
            "Round 1: Online Coding Assessment (2 Hard DSA Questions on HackerEarth/Internal Platform)",
            "Round 2-4: 3x Technical Coding Rounds (Deep DSA, Graph Algorithms, DP, Time Complexity Optimization)",
            "Round 5: System Design & Googliness / Leadership Round"
        ]),
        "previous_questions": json.dumps([
            "Given a directed graph, find the shortest path containing at least one node of each color.",
            "Implement an LRU Cache with O(1) time complexity operations.",
            "Median of two sorted arrays of different sizes in O(log(min(N,M))) time.",
            "Design Google Drive or a scalable Rate Limiter service.",
            "Describe a situation where you had a disagreement with a team member and how you resolved it."
        ]),
        "salary_details": "Base: ₹18L - ₹26L | Stocks: $30k - $50k | Total CTC: ₹35L - ₹55L PA for SDE-1",
        "hiring_trends": "Heavy focus on algorithmic rigor, clean production-ready code execution, and Googliness values.",
        "min_cgpa": 7.5,
        "experience_req": "0 - 3 Years"
    },
    {
        "slug": "amazon",
        "name": "Amazon",
        "logo_symbol": "📦",
        "category": "Product Giant (FAANG)",
        "tagline": "Customer Obsession & Earth's Most Customer-Centric Company.",
        "description": "Amazon recruits SDE-1 and SDE Interns through Amazon WOW, HackOn, and campus placements across top engineering colleges.",
        "required_skills": json.dumps(["Data Structures", "Algorithms", "Java", "C++", "System Design", "AWS Basics", "Object-Oriented Design", "Amazon Leadership Principles"]),
        "eligibility": "B.E / B.Tech / M.Tech in CS/IT/ECE. No active backlogs during joining.",
        "interview_process": json.dumps([
            "Round 1: Online Assessment (2 Coding Questions + Work Simulation + Behavioral Assessment)",
            "Round 2: Technical Interview 1 (DSA Trees, Graphs, Hash Maps)",
            "Round 3: Technical Interview 2 (Dynamic Programming, OOD / System Design)",
            "Round 4: Bar Raiser Round (Deep Technical + 14 Amazon Leadership Principles)"
        ]),
        "previous_questions": json.dumps([
            "Serialize and Deserialize a Binary Tree.",
            "Find the top K frequent elements in a streaming dataset.",
            "Design an Elevator Control System using Object-Oriented Principles.",
            "Tell me about a time when you took Ownership of a project outside your responsibility.",
            "Give an instance where you had to make a decision without sufficient data (Bias for Action)."
        ]),
        "salary_details": "Base: ₹15.5L - ₹20L | Sign-on Bonus: ₹6L - ₹10L | CTC: ₹28L - ₹45L PA",
        "hiring_trends": "Strong emphasis on Amazon's 16 Leadership Principles combined with fast DSA problem solving.",
        "min_cgpa": 7.0,
        "experience_req": "0 - 2 Years"
    },
    {
        "slug": "microsoft",
        "name": "Microsoft",
        "logo_symbol": "🪟",
        "category": "Product Giant",
        "tagline": "Empower every person and every organization on the planet to achieve more.",
        "description": "Microsoft hires Software Engineers (SWE) through campus hiring, Microsoft Engage, and Code Without Barriers hackathons.",
        "required_skills": json.dumps(["C++", "C#", "Java", "Python", "Data Structures", "System Architecture", "OS Principles", "SQL"]),
        "eligibility": "B.Tech/M.Tech in CS/ECE/EE with min 70% or 7.0 CGPA throughout.",
        "interview_process": json.dumps([
            "Round 1: Online Assessment (3 Coding Questions on Codility)",
            "Round 2: Technical Round 1 (Problem Solving & Data Structures)",
            "Round 3: Technical Round 2 (Low-Level Design & System Fundamentals)",
            "Round 4: AA (Appropriate Authority / Hiring Manager) Round (Behavioral & Architecture)"
        ]),
        "previous_questions": json.dumps([
            "Reverse Nodes in k-Group in a Singly Linked List.",
            "Find minimum cost to connect N cities (Minimum Spanning Tree - Kruskal/Prim).",
            "Design a URL Shortening service like bit.ly.",
            "Explain virtual memory, paging, and deadlocks in Operating Systems.",
            "Why do you want to join Microsoft and which product team interests you most?"
        ]),
        "salary_details": "Base: ₹16L - ₹22L | Joining Bonus: ₹3L - ₹5L | Stocks: $25k | Total CTC: ₹40L - ₹50L PA",
        "hiring_trends": "Values growth mindset, clean architecture, operating system fundamentals, and teamwork.",
        "min_cgpa": 7.0,
        "experience_req": "0 - 2 Years"
    },
    {
        "slug": "infosys",
        "name": "Infosys",
        "logo_symbol": "🔷",
        "category": "Service Based Giant",
        "tagline": "Navigate your next - Global leader in next-generation digital services.",
        "description": "Infosys recruits through HackWithInfy, InfyTQ, and On-Campus drives for Systems Engineer (SE), Specialist Programmer (SP), and Digital Specialist Engineer (DSE).",
        "required_skills": json.dumps(["Java", "Python", "Database Management (DBMS)", "OOPs", "Web Technologies", "Data Structures", "Aptitude"]),
        "eligibility": "BE/B.Tech/ME/M.Tech/MCA/M.Sc with min 60% or 6.0 CGPA in X, XII, and Graduation.",
        "interview_process": json.dumps([
            "Round 1: Online Test (Aptitude, Logical, Verbal, Pseudocode, Puzzle)",
            "Round 2: Technical Interview (Core Java/Python, DBMS, OS, DBMS queries)",
            "Round 3: HR Interview (Communication skills, willingness to relocate, bond details)"
        ]),
        "previous_questions": json.dumps([
            "Explain ACID properties in DBMS with real-life banking example.",
            "Write SQL query to find 2nd highest salary of an employee.",
            "Difference between Interface and Abstract Class in Java.",
            "Demonstrate bubble sort or quick sort algorithm logic.",
            "Are you comfortable working in night shifts or changing project locations?"
        ]),
        "salary_details": "Systems Engineer: ₹3.6L PA | DSE: ₹6.25L PA | Specialist Programmer: ₹9.5L PA",
        "hiring_trends": "InfyTQ certification & HackWithInfy coding competition offer direct entry to high-tier roles.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 1 Year"
    },
    {
        "slug": "accenture",
        "name": "Accenture",
        "logo_symbol": "🅰️",
        "category": "Global Consulting & Tech",
        "tagline": "Let there be change - High performance delivered.",
        "description": "Accenture conducts nationwide hiring drives for Associate Software Engineer (ASE - 4.5 LPA) and Advanced ASE (AASE - 6.5 LPA).",
        "required_skills": json.dumps(["Python", "Java", "Cloud Basics", "SQL", "Pseudocode", "Critical Reasoning", "Communication Skills"]),
        "eligibility": "B.E/B.Tech/MCA/M.Sc with no active backlogs at time of recruitment drive.",
        "interview_process": json.dumps([
            "Stage 1: Cognitive & Technical Assessment (Logical, English, Math, Pseudocode, Networking)",
            "Stage 2: Coding Assessment (2 Moderate Coding Problems)",
            "Stage 3: Communication Assessment (Automated Voice Test)",
            "Stage 4: Virtual Interview (Technical + HR Combined)"
        ]),
        "previous_questions": json.dumps([
            "Given an array of integers, count pairs whose sum equals a target value.",
            "Explain Cloud Computing deployment models (IaaS, PaaS, SaaS).",
            "Write a function to check if two strings are Anagrams.",
            "Describe your role in your final year team project.",
            "How do you quickly adapt when asked to learn a completely new technology?"
        ]),
        "salary_details": "ASE Role: ₹4.5L PA | Advanced ASE Role: ₹6.5L PA",
        "hiring_trends": "Emphasis on clear English communication, pseudocode solving, and cloud/digital capabilities.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 2 Years"
    },
    {
        "slug": "wipro",
        "name": "Wipro",
        "logo_symbol": "🌐",
        "category": "Service Based Giant",
        "tagline": "Ambition Realized - Global Information Technology, Consulting and Business Services.",
        "description": "Wipro recruits freshers through Wipro Elite NTH (National Talent Hunt) and Wipro Turbo drives for Project Engineer roles.",
        "required_skills": json.dumps(["C", "C++", "Java", "Python", "Aptitude", "SQL", "Networking Fundamentals"]),
        "eligibility": "B.E/B.Tech/M.Tech with 60% or 6.0 CGPA throughout 10th, 12th, and Graduation.",
        "interview_process": json.dumps([
            "Round 1: Online Assessment (Logical, Quantitative, English, Essay Writing, Coding)",
            "Round 2: Technical Interview (Basic Programming, DSA basics, Project Qs)",
            "Round 3: HR Interview (Document Verification & Relocation confirmation)"
        ]),
        "previous_questions": json.dumps([
            "Write a program to check if a given matrix is Symmetric.",
            "Explain OSI Model 7 layers and functions of TCP vs UDP.",
            "What is a pointer in C/C++? Explain Dangling Pointer.",
            "Tell us about a challenge you faced during college projects.",
            "Where do you see yourself in 3 years at Wipro?"
        ]),
        "salary_details": "Elite Engineer: ₹3.5L - ₹4.0L PA | Turbo Engineer: ₹6.5L PA",
        "hiring_trends": "Regular mass recruitment in Q2 & Q3 with focus on strong foundational computing skills.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 1 Year"
    },
    {
        "slug": "deloitte",
        "name": "Deloitte",
        "logo_symbol": "🟢",
        "category": "Big 4 Consulting & Advisory",
        "tagline": "Making an impact that matters.",
        "description": "Deloitte USI recruits Analyst, Technology Consultant, and Solution Advisor roles from top campuses across India.",
        "required_skills": json.dumps(["SQL", "Python", "Data Analysis", "Java", "Cloud Computing", "Consulting Aptitude", "Business Communication"]),
        "eligibility": "B.E / B.Tech / MCA / MBA with min 60% or 6.5 CGPA with no active backlogs.",
        "interview_process": json.dumps([
            "Round 1: Online Aptitude & Technical MCQs (Quants, Verbal, CS Core)",
            "Round 2: Jam / Group Discussion / Case Study Round",
            "Round 3: Technical Interview (Database, Analytics, Coding)",
            "Round 4: Partner / HR Round"
        ]),
        "previous_questions": json.dumps([
            "Write SQL queries involving INNER JOIN, GROUP BY, and HAVING clauses.",
            "How would you migrate a legacy client database to AWS Cloud securely?",
            "Explain the difference between Data Science, Machine Learning, and Business Intelligence.",
            "How do you handle client requirement changes mid-way through a sprint?",
            "Solve this business logic puzzle: Estimate the number of smartphones sold in India per year."
        ]),
        "salary_details": "Analyst: ₹7.6L - ₹9.0L PA | Consultant: ₹12L - ₹16L PA",
        "hiring_trends": "High demand for Cloud (AWS/GCP), Cyber Security, Data Analytics, and strong consulting persona.",
        "min_cgpa": 6.5,
        "experience_req": "0 - 2 Years"
    },
    {
        "slug": "ibm",
        "name": "IBM",
        "logo_symbol": "🔵",
        "category": "Tech & Hybrid Cloud Giant",
        "tagline": "Let's create something that changes everything.",
        "description": "IBM hires Associate System Engineer (ASE) and Software Engineer freshers via IBM Code Challenge & campus drives.",
        "required_skills": json.dumps(["Java", "Python", "Docker", "Kubernetes", "Linux Shell", "Cloud Computing", "Data Structures"]),
        "eligibility": "B.E/B.Tech/MCA/M.Tech with 60% or 6.0 CGPA.",
        "interview_process": json.dumps([
            "Round 1: Cognitive Ability Test (Games-based assessment on IPAT platform)",
            "Round 2: Learning Agility & English Assessment",
            "Round 3: Coding Assessment (2 Problem Solving Questions)",
            "Round 4: Technical & HR Interview"
        ]),
        "previous_questions": json.dumps([
            "Implement Stack using Queues.",
            "Explain Docker containerization vs Virtual Machines.",
            "What is REST API? Explain HTTP methods (GET, POST, PUT, DELETE).",
            "Write a script to search for log patterns in Linux terminal.",
            "How do you keep yourself updated with cutting-edge tech trends?"
        ]),
        "salary_details": "ASE Role: ₹4.8L - ₹6.5L PA | R&D Engineer: ₹9L - ₹12L PA",
        "hiring_trends": "Strong preference for Hybrid Cloud, Red Hat OpenShift, AI/ML, and Open Source contributions.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 2 Years"
    },
    {
        "slug": "hcl",
        "name": "HCLTech",
        "logo_symbol": "🔷",
        "category": "Global Tech Services",
        "tagline": "Supercharging Progress for global enterprises.",
        "description": "HCLTech recruits freshers via First Careers Program and campus drives for Software Engineer and Infrastructure Engineer roles.",
        "required_skills": json.dumps(["C", "C++", "Java", "Networking", "Database Management", "Python", "Troubleshooting"]),
        "eligibility": "B.E / B.Tech / MCA / B.Sc (CS/IT) with 60% throughout.",
        "interview_process": json.dumps([
            "Round 1: Online Technical & Aptitude Assessment",
            "Round 2: Technical Interview (Core CS, DBMS, Basic Coding)",
            "Round 3: HR Interview"
        ]),
        "previous_questions": json.dumps([
            "Explain call by value vs call by reference in C/C++.",
            "Difference between TCP and UDP protocols.",
            "Write a program to count vowels and consonants in a string.",
            "What are your key strengths and area of improvement?",
            "Are you ready to sign a service agreement?"
        ]),
        "salary_details": "Software Engineer: ₹3.6L - ₹4.25L PA",
        "hiring_trends": "Recruits freshers for Cloud Infrastructure, Application Modernization, and Cybersecurity teams.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 1 Year"
    },
    {
        "slug": "cognizant",
        "name": "Cognizant",
        "logo_symbol": "⚙️",
        "category": "Global Tech & Consulting",
        "tagline": "Intuitive operations and engineering for the modern enterprise.",
        "description": "Cognizant conducts GenC, GenC Elevate, and GenC Pro drives for campus recruits across India.",
        "required_skills": json.dumps(["Java", "SQL", "Web Basics (HTML/CSS/JS)", "Python", "Data Structures", "Problem Solving"]),
        "eligibility": "B.E/B.Tech/MCA/M.Sc with 60% in X, XII & Graduation. Max 1 active backlog.",
        "interview_process": json.dumps([
            "Round 1: GenC Online Test (Communication, Aptitude, Analytical Coding)",
            "Round 2: Technical Interview (CS Fundamentals, Coding, SQL Queries)",
            "Round 3: HR Interview"
        ]),
        "previous_questions": json.dumps([
            "Write a query to find employees who joined in the last 6 months.",
            "Explain Exception Handling in Java with try, catch, finally, throw, throws.",
            "Implement Binary Search algorithm.",
            "Tell me about a team conflict and how you managed it.",
            "Are you willing to work in rotational shifts?"
        ]),
        "salary_details": "GenC: ₹4.0L PA | GenC Elevate: ₹5.4L PA | GenC Pro: ₹6.75L - ₹9.0L PA",
        "hiring_trends": "High demand for Full Stack Java, Salesforce, Data Engineering, and Automation Testing.",
        "min_cgpa": 6.0,
        "experience_req": "0 - 2 Years"
    }
]

def seed_companies():
    """Inserts initial company records if the companies table is empty."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM companies")
    count = cursor.fetchone()[0]
    
    if count == 0:
        for comp in COMPANIES_DATA:
            cursor.execute("""
                INSERT INTO companies (
                    slug, name, logo_symbol, category, tagline, description,
                    required_skills, eligibility, interview_process, previous_questions,
                    salary_details, hiring_trends, min_cgpa, experience_req
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                comp['slug'], comp['name'], comp['logo_symbol'], comp['category'],
                comp['tagline'], comp['description'], comp['required_skills'],
                comp['eligibility'], comp['interview_process'], comp['previous_questions'],
                comp['salary_details'], comp['hiring_trends'], comp['min_cgpa'], comp['experience_req']
            ))
        conn.commit()
        print(f"Successfully seeded {len(COMPANIES_DATA)} company profiles into database!")
    else:
        print(f"Company table already has {count} entries. Skipping seeding.")
        
    conn.close()

if __name__ == '__main__':
    seed_companies()
