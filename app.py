import os
import json
import sqlite3
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, 
    session, jsonify, flash, g
)
from werkzeug.security import generate_password_hash, check_password_hash

import db
import company_seed
import ai_service

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "career_lains_ai_super_secret_key_2026")

# Initialize database and seed company data
with app.app_context():
    db.init_db(app)
    company_seed.seed_companies()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please sign in / log in to access this feature.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.query_db('SELECT * FROM users WHERE id = ?', [user_id], one=True)

# ==================== LANDING & AUTHENTICATION ROUTES ==================== #

@app.route('/')
def index():
    """Landing Page displaying Welcome to Career Lains AI with Sign In / Sign Up CTAs."""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        target_role = request.form.get('target_role', 'Software Engineer')
        experience_level = request.form.get('experience_level', 'Fresher / Student')
        
        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('signup.html')
            
        existing = db.query_db('SELECT id FROM users WHERE email = ?', [email], one=True)
        if existing:
            flash('An account with this email already exists. Please log in.', 'danger')
            return render_template('login.html')
            
        pwd_hash = generate_password_hash(password)
        user_id = db.execute_db(
            'INSERT INTO users (name, email, password_hash, target_role, experience_level) VALUES (?, ?, ?, ?, ?)',
            [name, email, pwd_hash, target_role, experience_level]
        )
        
        default_personal = json.dumps({"name": name, "email": email, "phone": "", "linkedin": "", "github": ""})
        db.execute_db('INSERT INTO resumes (user_id, title, personal_info) VALUES (?, ?, ?)', [user_id, 'My Primary Resume', default_personal])
        
        session['user_id'] = user_id
        session['user_name'] = name
        flash('Account created successfully! Welcome to Career Lains AI.', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        user = db.query_db('SELECT * FROM users WHERE email = ?', [email], one=True)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash(f"Welcome back to Career Lains AI, {user['name']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        target_role = request.form.get('target_role', 'Software Engineer')
        experience_level = request.form.get('experience_level', 'Fresher / Student')
        bio = request.form.get('bio', '')
        
        db.execute_db(
            'UPDATE users SET name = ?, target_role = ?, experience_level = ?, bio = ? WHERE id = ?',
            [name, target_role, experience_level, bio, g.user['id']]
        )
        session['user_name'] = name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
        
    return render_template('profile.html', user=g.user)

# ==================== DASHBOARD ==================== #

@app.route('/dashboard')
@login_required
def dashboard():
    ats_logs = db.query_db(
        'SELECT * FROM ats_reports WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        [g.user['id']]
    )
    resume = db.query_db('SELECT * FROM resumes WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1', [g.user['id']], one=True)
    companies = db.query_db('SELECT * FROM companies ORDER BY name ASC LIMIT 6')
    
    recent_ats = ats_logs[0]['ats_score'] if ats_logs else 0
    interview_count = db.query_db('SELECT COUNT(*) as cnt FROM interview_sessions WHERE user_id = ?', [g.user['id']], one=True)['cnt']
    
    return render_template(
        'dashboard.html', 
        user=g.user, 
        ats_logs=ats_logs, 
        recent_ats=recent_ats, 
        resume=resume,
        companies=companies,
        interview_count=interview_count
    )

# ==================== RESUME BUILDER ==================== #

@app.route('/resume-builder')
@login_required
def resume_builder():
    resume = db.query_db('SELECT * FROM resumes WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1', [g.user['id']], one=True)
    if not resume:
        default_personal = json.dumps({"name": g.user['name'], "email": g.user['email'], "phone": "", "linkedin": "", "github": ""})
        res_id = db.execute_db('INSERT INTO resumes (user_id, title, personal_info) VALUES (?, ?, ?)', [g.user['id'], 'My Primary Resume', default_personal])
        resume = db.query_db('SELECT * FROM resumes WHERE id = ?', [res_id], one=True)
        
    return render_template('resume_builder.html', resume=resume, user=g.user)

@app.route('/api/resume/save', methods=['POST'])
@login_required
def save_resume():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    resume_id = data.get('id')
    title = data.get('title', 'My Resume')
    personal_info = json.dumps(data.get('personal_info', {}))
    summary = data.get('summary', '')
    education = json.dumps(data.get('education', []))
    experience = json.dumps(data.get('experience', []))
    projects = json.dumps(data.get('projects', []))
    skills = json.dumps(data.get('skills', []))
    certifications = json.dumps(data.get('certifications', []))
    theme = data.get('theme', 'modern')
    
    if resume_id:
        db.execute_db(
            '''UPDATE resumes SET title = ?, personal_info = ?, summary = ?, education = ?, 
               experience = ?, projects = ?, skills = ?, certifications = ?, theme = ?, updated_at = CURRENT_TIMESTAMP 
               WHERE id = ? AND user_id = ?''',
            [title, personal_info, summary, education, experience, projects, skills, certifications, theme, resume_id, g.user['id']]
        )
    else:
        resume_id = db.execute_db(
            '''INSERT INTO resumes (user_id, title, personal_info, summary, education, experience, projects, skills, certifications, theme) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            [g.user['id'], title, personal_info, summary, education, experience, projects, skills, certifications, theme]
        )
        
    return jsonify({"success": True, "resume_id": resume_id, "message": "Resume saved successfully!"})

@app.route('/api/resume/enhance', methods=['POST'])
@login_required
def enhance_resume_bullet():
    data = request.get_json()
    text = data.get('text', '')
    role = data.get('role', g.user['target_role'])
    
    if not text:
        return jsonify({"success": False, "message": "Text is required"}), 400
        
    enhanced = ai_service.enhance_bullet_point(text, role)
    return jsonify({"success": True, "enhanced_text": enhanced})

# ==================== ATS CHECKER ==================== #

@app.route('/ats-checker')
@login_required
def ats_checker():
    reports = db.query_db('SELECT * FROM ats_reports WHERE user_id = ? ORDER BY created_at DESC', [g.user['id']])
    return render_template('ats_checker.html', reports=reports, user=g.user)

@app.route('/api/ats/analyze', methods=['POST'])
@login_required
def analyze_ats():
    job_role = request.form.get('job_role', g.user['target_role'])
    resume_text = request.form.get('resume_text', '').strip()
    
    file = request.files.get('resume_file')
    file_name = "Pasted Resume Text"
    
    if file and file.filename:
        file_name = file.filename
        ext = file.filename.split('.')[-1].lower()
        if ext == 'pdf':
            try:
                import pypdf
                reader = pypdf.PdfReader(file)
                extracted = ""
                for page in reader.pages:
                    extracted += page.extract_text() or ""
                if extracted.strip():
                    resume_text = extracted
            except Exception as e:
                print(f"PDF extraction error: {e}")
        elif ext in ['txt', 'md']:
            resume_text = file.read().decode('utf-8', errors='ignore')

    if not resume_text:
        return jsonify({"success": False, "message": "Please provide resume text or upload a valid file."}), 400

    analysis = ai_service.analyze_resume_ats(resume_text, job_role)
    
    report_id = db.execute_db(
        '''INSERT INTO ats_reports (user_id, file_name, job_role, ats_score, summary, strengths, weaknesses, missing_skills, keywords, suggestions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        [
            g.user['id'], file_name, job_role, analysis['ats_score'], analysis['summary'],
            json.dumps(analysis['strengths']), json.dumps(analysis['weaknesses']),
            json.dumps(analysis['missing_skills']), json.dumps(analysis['keywords']),
            json.dumps(analysis['suggestions'])
        ]
    )
    
    analysis['id'] = report_id
    analysis['file_name'] = file_name
    analysis['job_role'] = job_role
    return jsonify({"success": True, "analysis": analysis})

# ==================== COMPANY DATASET & MATCHING ==================== #

@app.route('/companies')
def company_list():
    category = request.args.get('category', '')
    query = request.args.get('q', '').strip()
    
    sql = 'SELECT * FROM companies WHERE 1=1'
    params = []
    
    if category:
        sql += ' AND category LIKE ?'
        params.append(f'%{category}%')
    if query:
        sql += ' AND (name LIKE ? OR required_skills LIKE ? OR description LIKE ?)'
        params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])
        
    sql += ' ORDER BY name ASC'
    companies = db.query_db(sql, params)
    
    user_skills = []
    if g.user:
        latest_resume = db.query_db('SELECT skills FROM resumes WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1', [g.user['id']], one=True)
        user_skills = json.loads(latest_resume['skills']) if latest_resume and latest_resume['skills'] else []
    
    return render_template('companies.html', companies=companies, category=category, query=query, user_skills=user_skills)

@app.route('/company/<slug>')
def company_detail(slug):
    company = db.query_db('SELECT * FROM companies WHERE slug = ?', [slug], one=True)
    if not company:
        flash('Company not found.', 'danger')
        return redirect(url_for('company_list'))
        
    user_skills = []
    if g.user:
        latest_resume = db.query_db('SELECT skills FROM resumes WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1', [g.user['id']], one=True)
        user_skills = json.loads(latest_resume['skills']) if latest_resume and latest_resume['skills'] else []
    
    match_result = ai_service.generate_company_match_and_roadmap(user_skills, dict(company))
    
    return render_template(
        'company_detail.html', 
        company=company, 
        user_skills=user_skills, 
        match_result=match_result,
        required_skills=json.loads(company['required_skills']),
        interview_process=json.loads(company['interview_process']),
        previous_questions=json.loads(company['previous_questions'])
    )

@app.route('/api/company/match', methods=['POST'])
@login_required
def match_company():
    data = request.get_json()
    company_id = data.get('company_id')
    custom_skills = data.get('skills', [])
    
    company = db.query_db('SELECT * FROM companies WHERE id = ?', [company_id], one=True)
    if not company:
        return jsonify({"success": False, "message": "Company not found"}), 404
        
    match_data = ai_service.generate_company_match_and_roadmap(custom_skills, dict(company))
    return jsonify({"success": True, "data": match_data})

# ==================== INTERVIEW ASSISTANT ==================== #

@app.route('/interview-prep')
@login_required
def interview_prep():
    companies = db.query_db('SELECT name, slug FROM companies ORDER BY name ASC')
    recent_sessions = db.query_db('SELECT * FROM interview_sessions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5', [g.user['id']])
    return render_template('interview.html', companies=companies, recent_sessions=recent_sessions, user=g.user)

@app.route('/api/interview/generate', methods=['POST'])
@login_required
def generate_interview():
    data = request.get_json()
    company_name = data.get('company', 'TCS')
    role = data.get('role', g.user['target_role'])
    category = data.get('category', 'Technical')
    
    questions = ai_service.generate_interview_questions(company_name, role, category)
    return jsonify({"success": True, "questions": questions})

@app.route('/api/interview/evaluate', methods=['POST'])
@login_required
def evaluate_interview():
    data = request.get_json()
    company_name = data.get('company', 'TCS')
    role = data.get('role', g.user['target_role'])
    category = data.get('category', 'Technical')
    question = data.get('question', '')
    candidate_answer = data.get('answer', '')
    
    if not question or not candidate_answer:
        return jsonify({"success": False, "message": "Question and Answer are required"}), 400
        
    eval_result = ai_service.evaluate_interview_answer(company_name, role, question, candidate_answer)
    
    db.execute_db(
        '''INSERT INTO interview_sessions (user_id, company_name, role, category, question, user_answer, score, feedback, sample_answer)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        [
            g.user['id'], company_name, role, category, question, candidate_answer,
            eval_result['score'], json.dumps(eval_result), eval_result['model_answer']
        ]
    )
    
    return jsonify({"success": True, "evaluation": eval_result})

# ==================== CAREER CHATBOT ==================== #

@app.route('/chatbot')
@login_required
def chatbot():
    history = db.query_db('SELECT * FROM chat_messages WHERE user_id = ? ORDER BY timestamp ASC', [g.user['id']])
    return render_template('chatbot.html', history=history, user=g.user)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"success": False, "message": "Empty message"}), 400
        
    db.execute_db('INSERT INTO chat_messages (user_id, sender, message) VALUES (?, ?, ?)', [g.user['id'], 'user', message])
    
    user_ctx = f"Role: {g.user['target_role']}, Level: {g.user['experience_level']}"
    bot_response = ai_service.get_career_chatbot_response(message, user_ctx)
    
    db.execute_db('INSERT INTO chat_messages (user_id, sender, message) VALUES (?, ?, ?)', [g.user['id'], 'ai', bot_response])
    
    return jsonify({"success": True, "response": bot_response})

if __name__ == '__main__':
    print("Starting Career Lains AI Flask Application on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
