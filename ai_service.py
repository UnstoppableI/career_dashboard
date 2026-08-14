import os
import json
import re
import random
import urllib.request
import urllib.error

# Try importing google.generativeai safely across all Python versions (including Python 3.14+)
HAS_GEMINI_SDK = False
try:
    import google.generativeai as genai
    HAS_GEMINI_SDK = True
except Exception as err:
    print(f"Notice: google.generativeai SDK import skipped ({err}). Falling back to Direct REST API / Heuristic Engine.")


GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if HAS_GEMINI_SDK and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Gemini config error: {e}")

def call_gemini(prompt, system_instruction="You are an expert AI Career Coach and ATS Evaluator."):
    """Helper to query Gemini API via SDK or HTTP REST API, else returns None."""
    if not GEMINI_API_KEY:
        return None

    # Method 1: Try SDK if available
    if HAS_GEMINI_SDK:
        try:
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini SDK Call failed: {e}. Trying direct REST API...")

    # Method 2: Direct HTTP REST call to Gemini API (Python 3.14 compatible, no C-extension dependency)
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_instruction}\n\n{prompt}"}]
            }]
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as resp:
            res_data = json.loads(resp.read().decode('utf-8'))
            candidates = res_data.get('candidates', [])
            if candidates:
                parts = candidates[0].get('content', {}).get('parts', [])
                if parts:
                    return parts[0].get('text', '')
    except Exception as http_err:
        print(f"Gemini HTTP REST call failed: {http_err}")

    return None


# ==================== ATS RESUME CHECKER ==================== #

def analyze_resume_ats(resume_text, job_role="Software Developer"):
    """
    Analyzes resume text against a target job role.
    Returns a dict with: ats_score, summary, strengths, weaknesses, missing_skills, keywords, suggestions.
    """
    prompt = f"""
    Evaluate the following resume text for the target role: "{job_role}".
    
    Resume Text:
    \"\"\"{resume_text[:3000]}\"\"\"
    
    Return a strictly valid JSON object with the following keys:
    - "ats_score": an integer from 35 to 95 representing ATS compatibility score.
    - "summary": 2-3 sentence executive summary of the candidate's profile.
    - "strengths": array of 3-5 key strengths found in the resume.
    - "weaknesses": array of 2-4 areas needing improvement or structural issues.
    - "missing_skills": array of 4-6 essential tech/soft skills missing for a {job_role}.
    - "keywords": array of 6-8 recommended ATS keywords to add.
    - "suggestions": array of 4-5 concrete, actionable bullet points to boost the score.
    """

    ai_response = call_gemini(prompt)
    if ai_response:
        try:
            # Extract JSON block if wrapped in markdown
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception as e:
            print(f"JSON parsing error from Gemini ATS output: {e}")

    # Fallback Intelligent NLP-like Engine
    text_lower = resume_text.lower()
    
    # Common tech keywords check
    tech_keywords = {
        "python", "java", "javascript", "c++", "sql", "html", "css", "react", "node", 
        "git", "aws", "docker", "dsa", "oops", "dbms", "system design", "rest api", "flask", "django"
    }
    
    found_keywords = [kw.upper() for kw in tech_keywords if kw in text_lower]
    
    # Role specific required keywords
    role_skills_map = {
        "software developer": ["Data Structures", "OOPs", "Git", "SQL", "REST APIs", "Unit Testing", "Problem Solving"],
        "frontend developer": ["JavaScript", "React", "CSS3", "HTML5", "Responsive Design", "TypeScript", "Tailwind/Bootstrap"],
        "data analyst": ["Python", "SQL", "Pandas", "PowerBI/Tableau", "Excel", "Statistics", "Data Visualization"],
        "cloud engineer": ["AWS/Azure", "Docker", "Kubernetes", "Linux", "Terraform", "CI/CD", "Networking"]
    }
    
    target_lower = job_role.lower()
    expected_skills = role_skills_map.get(target_lower, role_skills_map["software developer"])
    
    missing = [skill for skill in expected_skills if skill.lower() not in text_lower]
    
    # Base score calculation
    base_score = 50 + (len(found_keywords) * 4) + (20 if len(resume_text) > 300 else 0)
    base_score = min(92, max(42, base_score))
    
    strengths = []
    if "project" in text_lower or "developed" in text_lower:
        strengths.append("Clear project descriptions with action-oriented language.")
    if len(found_keywords) >= 4:
        strengths.append(f"Strong technical keyword footprint including {', '.join(found_keywords[:3])}.")
    if "education" in text_lower or "b.tech" in text_lower or "bca" in text_lower:
        strengths.append("Solid educational qualifications highlighted clearly.")
    if not strengths:
        strengths.append("Structured format with recognizable section headers.")
        
    weaknesses = []
    if len(resume_text) < 400:
        weaknesses.append("Resume content is too brief. Elaborate on project details and responsibilities.")
    if not any(char.isdigit() for char in resume_text):
        weaknesses.append("Lacks quantifiable metrics (e.g., 'Improved performance by 25%', 'Handled 500+ users').")
    if missing:
        weaknesses.append(f"Missing core expected industry skills for {job_role}: {', '.join(missing[:3])}.")
        
    suggestions = [
        f"Incorporate measurable outcomes in project descriptions (e.g. reduced load time by 30%).",
        f"Add missing industry keywords: {', '.join(missing[:4])} under a dedicated 'Skills' section.",
        "Use strong action verbs like 'Architected', 'Engineered', 'Optimized', 'Spearheaded' at start of bullets.",
        "Ensure consistent formatting with clear bullet points and standard font sizes."
    ]
    
    return {
        "ats_score": base_score,
        "summary": f"Candidate profile evaluated for {job_role}. Possesses foundational experience with key technologies like {', '.join(found_keywords[:3]) if found_keywords else 'programming basics'}. Enhancing quantifiable project impact will significantly improve ATS ranking.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_skills": missing if missing else ["System Architecture", "CI/CD Pipelines", "Docker Containerization"],
        "keywords": [kw for kw in expected_skills if kw not in found_keywords] + ["Agile", "Git Hub", "Microservices"],
        "suggestions": suggestions
    }

# ==================== AI RESUME ENHANCER ==================== #

def enhance_bullet_point(bullet_text, role="Software Engineer"):
    """Enhances a raw bullet point to be ATS-friendly and high-impact."""
    prompt = f"Rewrite the following resume bullet point for a {role} to make it more professional, ATS-optimized, action-oriented, and impactful:\n'{bullet_text}'"
    ai_resp = call_gemini(prompt)
    if ai_resp:
        return ai_resp.strip().replace('"', '')
    
    # Fallback enhancement
    words = bullet_text.strip().capitalize()
    if not words.endswith('.'):
        words += '.'
    action_verbs = ["Architected and implemented", "Spearheaded development of", "Engineered scalable solution for", "Optimized performance of"]
    chosen_verb = random.choice(action_verbs)
    return f"{chosen_verb} {words.lower()} resulting in a 25% increase in operational efficiency and seamless deployment."

# ==================== AI COMPANY MATCHING & SKILL GAP ROADMAP ==================== #

def generate_company_match_and_roadmap(resume_skills, company_data):
    """
    Compares candidate skills with company requirements.
    Returns: match_percentage, missing_skills, matched_skills, learning_roadmap.
    """
    req_skills = json.loads(company_data.get('required_skills', '[]'))
    
    if isinstance(resume_skills, str):
        resume_skills_list = [s.strip().lower() for s in resume_skills.split(',') if s.strip()]
    else:
        resume_skills_list = [s.lower() for s in resume_skills]
        
    matched = []
    missing = []
    
    for skill in req_skills:
        skill_lower = skill.lower()
        if any(skill_lower in rs or rs in skill_lower for rs in resume_skills_list):
            matched.append(skill)
        else:
            missing.append(skill)
            
    total = len(req_skills) if req_skills else 1
    match_pct = int((len(matched) / total) * 100)
    match_pct = max(35, min(98, match_pct + 15 if matched else 40))
    
    prompt = f"""
    Candidate wants to target {company_data['name']} for the eligibility criteria '{company_data['eligibility']}'.
    The company requires: {', '.join(req_skills)}.
    Candidate missing skills: {', '.join(missing)}.
    
    Generate a 4-Week Skill Gap Learning Roadmap to help the student crack {company_data['name']}.
    Return a valid JSON array of 4 week objects:
    [
      {{ "week": 1, "topic": "...", "objective": "...", "tasks": ["...", "..."], "resource": "..." }},
      ...
    ]
    """
    
    ai_resp = call_gemini(prompt)
    if ai_resp:
        try:
            json_match = re.search(r'\[.*\]', ai_resp, re.DOTALL)
            if json_match:
                roadmap = json.loads(json_match.group())
                return {
                    "match_percentage": match_pct,
                    "matched_skills": matched,
                    "missing_skills": missing,
                    "roadmap": roadmap
                }
        except Exception as e:
            print(f"Error parsing Gemini roadmap JSON: {e}")

    # Fallback Roadmap Generator
    fallback_roadmap = [
        {
            "week": 1,
            "topic": f"Core Foundations ({missing[0] if missing else 'Data Structures & Algorithms'})",
            "objective": f"Master basic to intermediate concepts in {missing[0] if missing else 'DSA'}.",
            "tasks": [
                f"Solve 15-20 topic-wise practice questions on LeetCode / GeeksforGeeks.",
                f"Understand time and space complexity optimizations.",
                f"Review OOPs concepts and standard coding practices required by {company_data['name']}."
            ],
            "resource": "GeeksforGeeks / Striver's A2Z DSA Sheet"
        },
        {
            "week": 2,
            "topic": f"Advanced Concepts & DBMS/SQL ({missing[1] if len(missing)>1 else 'Database Systems'})",
            "objective": "Build solid database query writing skills and core computer science fundamentals.",
            "tasks": [
                "Practice complex SQL Joins, Aggregations, and Subqueries.",
                "Review Operating System concepts (Processes, Threads, Memory Management, Deadlocks).",
                "Learn basic Computer Networks (TCP/IP vs OSI model, HTTP methods)."
            ],
            "resource": "LeetCode SQL 50 & Gate Smashers YouTube Series"
        },
        {
            "week": 3,
            "topic": f"Company-Specific Problem Solving ({company_data['name']})",
            "objective": f"Practice real previous interview questions of {company_data['name']}.",
            "tasks": [
                f"Solve top 20 previous coding questions asked in {company_data['name']} campus drives.",
                "Take 2 timed mock aptitude & technical coding assessments.",
                "Refine project architecture explanations using the STAR method."
            ],
            "resource": f"{company_data['name']} Placement Archives on Career Lains AI"
        },
        {
            "week": 4,
            "topic": "Mock Interviews & HR Round Preparation",
            "objective": "Master technical articulation and HR behavioral questions.",
            "tasks": [
                f"Prepare answers for {company_data['name']} core values and behavioral scenarios.",
                "Conduct 2 interactive AI Mock Interview rounds on Career Lains AI.",
                "Perform final review of resume projects and custom GitHub links."
            ],
            "resource": "Career Lains AI Mock Interview Assistant"
        }
    ]
    
    return {
        "match_percentage": match_pct,
        "matched_skills": matched if matched else ["Basic Programming", "Aptitude"],
        "missing_skills": missing if missing else ["Advanced DSA", "System Design"],
        "roadmap": fallback_roadmap
    }

# ==================== AI MOCK INTERVIEW ASSISTANT ==================== #

def generate_interview_questions(company_name="TCS", role="Software Engineer", category="Technical"):
    """Generates 3 tailored interview questions with context."""
    prompt = f"""
    Generate 3 realistic {category} interview questions for candidate applying at {company_name} for the role of {role}.
    Return JSON array of strings: ["Question 1", "Question 2", "Question 3"]
    """
    ai_resp = call_gemini(prompt)
    if ai_resp:
        try:
            match = re.search(r'\[.*\]', ai_resp, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"Error parsing Gemini questions: {e}")

    # Fallback Question Store
    questions_bank = {
        "Technical": [
            f"Explain how memory is managed in Python/Java, and how garbage collection works during execution.",
            f"Write an efficient algorithm to detect a cycle in a Singly Linked List (Floyd's Cycle Finding algorithm).",
            f"Explain ACID properties in DBMS with a real-life banking system scenario.",
            f"How do you handle API rate limiting and CORS errors in modern web application development?"
        ],
        "HR": [
            f"Tell me about a time when your team project encountered a major setback and how you led the solution.",
            f"Why do you specifically want to join {company_name} over other competitors in the industry?",
            f"How do you prioritize multiple urgent deadlines when working under strict client pressure?",
            f"Describe a situation where you had a disagreement with a team member and how you reached consensus."
        ],
        "Managerial": [
            f"If you are assigned a technology stack you have zero experience in, how will you deliver in 2 weeks?",
            f"Where do you see yourself in 3 to 5 years, and how does {company_name} align with your career goals?",
            f"Explain your final year college project architecture to a non-technical stakeholder."
        ]
    }
    
    category_qs = questions_bank.get(category, questions_bank["Technical"])
    random.shuffle(category_qs)
    return category_qs[:3]

def evaluate_interview_answer(company_name, role, question, candidate_answer):
    """Evaluates candidate answer and provides score (0-100), feedback, and model answer."""
    prompt = f"""
    Evaluate the candidate's answer for this interview question at {company_name} for role {role}.
    
    Question: "{question}"
    Candidate Answer: "{candidate_answer}"
    
    Return a strictly valid JSON object with:
    - "score": integer 40-98.
    - "clarity": string rating ("Excellent", "Good", "Needs Improvement").
    - "technical_accuracy": string rating ("High", "Moderate", "Low").
    - "key_improvements": array of 2-3 specific feedback points.
    - "model_answer": 3-4 sentence exemplar answer using the STAR method where appropriate.
    """
    
    ai_resp = call_gemini(prompt)
    if ai_resp:
        try:
            match = re.search(r'\{.*\}', ai_resp, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as e:
            print(f"Error parsing Gemini evaluation: {e}")

    # Fallback Evaluation Engine
    length = len(candidate_answer.strip())
    words = candidate_answer.split()
    
    score = 60
    if length > 150:
        score += 20
    elif length > 60:
        score += 10
    else:
        score -= 10
        
    tech_keywords = ["because", "example", "result", "implemented", "used", "solution", "method", "data", "system"]
    keyword_hits = sum(1 for kw in tech_keywords if kw in candidate_answer.lower())
    score += min(15, keyword_hits * 3)
    score = min(95, max(45, score))
    
    return {
        "score": score,
        "clarity": "Good" if length > 100 else "Needs More Detail",
        "technical_accuracy": "High" if keyword_hits >= 3 else "Moderate",
        "key_improvements": [
            "Structure your response using the STAR method (Situation, Task, Action, Result).",
            "Quantify outcomes where possible (e.g. improved execution time, saved hours).",
            "Provide explicit real-world or project examples to substantiate your points."
        ],
        "model_answer": f"In a recent project, I encountered a similar scenario requiring a structured approach. I systematically analyzed the requirements, implemented standard industry best practices with clean modular code, tested edge cases thoroughly, and successfully delivered the feature on schedule with optimized performance."
    }

# ==================== AI CAREER CHATBOT ==================== #

def get_career_chatbot_response(user_message, user_context="Student"):
    """Generates intelligent career guidance chatbot response."""
    prompt = f"""
    You are 'CareerLanes Bot', an empathetic, highly knowledgeable AI Placement & Career Mentor.
    User context: {user_context}
    User Query: "{user_message}"
    
    Provide a clear, structured, encouraging, and actionable response (formatted in Markdown with bullet points where appropriate). Keep tone professional and supportive.
    """
    
    ai_resp = call_gemini(prompt)
    if ai_resp:
        return ai_resp

    # Fallback Intelligent Chatbot Logic
    msg = user_message.lower()
    
    if any(k in msg for k in ["resume", "cv", "ats", "format"]):
        return (
            "### 📄 ATS Resume Tips for Campus & Off-Campus Drives\n\n"
            "1. **Single-Column Clean Layout**: Use standard fonts (Inter, Arial, Calibri) with no complex graphics, tables, or text boxes that confuse ATS scanners.\n"
            "2. **Keyword Optimization**: Align your skills directly with job descriptions (e.g., *Java, React, SQL, REST APIs*).\n"
            "3. **Quantified Impact**: Use action-oriented bullet points: *'Developed X using Y which improved performance by Z%'*.\n"
            "4. **PDF Format**: Always export as standard searchable PDF using our **AI Resume Builder** tool!"
        )
    elif any(k in msg for k in ["tcs", "infosys", "wipro", "accenture", "nqt", "service"]):
        return (
            "### 🏢 Cracking Service-Based IT Companies (TCS, Infosys, Wipro, Accenture)\n\n"
            "- **Phase 1: Aptitude & Reasoning**: Daily 1-hour practice on Quants, Logical Reasoning, and Verbal Ability.\n"
            "- **Phase 2: Coding Round**: Focus on basic array/string manipulations, palindrome, prime factors, and sorting algorithms.\n"
            "- **Phase 3: Core CS Subjects**: Prepare DBMS (SQL queries), OOPs concepts (Inheritance, Polymorphism), and OS basics.\n"
            "👉 *Check out our **Company Placement Dataset** module for company-specific interview archives!*"
        )
    elif any(k in msg for k in ["google", "amazon", "microsoft", "product", "faang", "dsa"]):
        return (
            "### 🚀 Cracking Product Giants & Top Tech Companies\n\n"
            "1. **Master Data Structures**: Arrays, Strings, HashMaps, Two Pointers, Trees, Graphs, and Dynamic Programming.\n"
            "2. **Clean Coding & Complexity**: Practice writing bug-free code while explaining Time ($O(N)$) & Space complexities ($O(1)$).\n"
            "3. **System Design & LLD**: Learn Object-Oriented Design principles (SOLID) and basic scalability patterns.\n"
            "4. **Behavioral Preparation**: For Amazon, study the 16 Leadership Principles carefully."
        )
    elif any(k in msg for k in ["salary", "package", "ctc", "negotiate"]):
        return (
            "### 💰 Salary Negotiation & CTC Insights\n\n"
            "- **Freshers (Campus Placement)**: Packages are generally fixed based on tiers (e.g., Ninja vs Digital vs Prime at TCS).\n"
            "- **Off-Campus / Experienced**: Research market standard ranges on Glassdoor & AmbitionBox before the HR call.\n"
            "- **Understand Fixed vs Variable**: Always verify Base Salary vs Variable Bonus vs Stocks (RSUs) vesting schedule."
        )
    else:
        return (
            f"Hello! I am your **CareerLanes AI Counselor**. 🎯\n\n"
            f"I can help you with:\n"
            f"- **Resume Building & ATS Optimization**\n"
            f"- **Company-Specific Placement Guides (TCS, Google, Amazon, Infosys, etc.)**\n"
            f"- **Technical & HR Interview Question Practice**\n"
            f"- **Skill Gap Roadmaps & Career Transitions**\n\n"
            f"How can I assist your placement preparation today?"
        )
