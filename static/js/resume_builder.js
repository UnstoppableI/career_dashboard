document.addEventListener('DOMContentLoaded', () => {
    // Tab switching logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.style.display = 'none');
            
            btn.classList.add('active');
            const target = btn.dataset.target;
            document.getElementById(target).style.display = 'block';
        });
    });

    // Experience Items Manager
    const experienceContainer = document.getElementById('experienceContainer');
    const addExpBtn = document.getElementById('addExpBtn');

    function createExpRow(title = '', company = '', duration = '', bullets = '') {
        const div = document.createElement('div');
        div.className = 'exp-item glass-card';
        div.style.padding = '16px';
        div.style.marginBottom = '12px';
        div.style.background = 'rgba(0,0,0,0.2)';
        
        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong style="color: var(--primary-cyan);">Position / Role</strong>
                <button type="button" class="btn btn-secondary remove-exp-btn" style="padding: 2px 8px; font-size: 11px; color: #f87171;">Remove</button>
            </div>
            <div class="grid-2">
                <input type="text" class="form-control exp-title" placeholder="Software Engineer Intern" value="${title}">
                <input type="text" class="form-control exp-company" placeholder="Tech Company Inc." value="${company}">
            </div>
            <div class="form-group" style="margin-top: 8px;">
                <input type="text" class="form-control exp-duration" placeholder="Jan 2025 - Present" value="${duration}">
            </div>
            <div class="form-group" style="margin-bottom: 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <label class="form-label" style="font-size: 12px;">Key Achievements / Bullets</label>
                    <button type="button" class="ai-enhance-bullet-btn btn btn-purple" style="padding: 2px 8px; font-size: 11px;">✨ AI Polish</button>
                </div>
                <textarea class="form-control exp-bullets" placeholder="• Architected RESTful microservices reducing response latency by 35%...">${bullets}</textarea>
            </div>
        `;

        div.querySelector('.remove-exp-btn').addEventListener('click', () => {
            div.remove();
            updateLivePreview();
        });

        div.querySelector('.ai-enhance-bullet-btn').addEventListener('click', async () => {
            const txtArea = div.querySelector('.exp-bullets');
            if (!txtArea.value.strip && !txtArea.value.trim()) return;
            
            const btn = div.querySelector('.ai-enhance-bullet-btn');
            btn.innerHTML = '⏳ Polishing...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/resume/enhance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: txtArea.value })
                });
                const data = await res.json();
                if (data.success) {
                    txtArea.value = data.enhanced_text;
                    updateLivePreview();
                }
            } catch (err) {
                console.error(err);
            } finally {
                btn.innerHTML = '✨ AI Polish';
                btn.disabled = false;
            }
        });

        div.querySelectorAll('input, textarea').forEach(el => el.addEventListener('input', updateLivePreview));
        experienceContainer.appendChild(div);
    }

    addExpBtn.addEventListener('click', () => {
        createExpRow();
        updateLivePreview();
    });

    // Projects Manager
    const projectsContainer = document.getElementById('projectsContainer');
    const addProjBtn = document.getElementById('addProjBtn');

    function createProjRow(name = '', tech = '', details = '') {
        const div = document.createElement('div');
        div.className = 'proj-item glass-card';
        div.style.padding = '16px';
        div.style.marginBottom = '12px';
        div.style.background = 'rgba(0,0,0,0.2)';

        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong style="color: var(--primary-cyan);">Project</strong>
                <button type="button" class="btn btn-secondary remove-proj-btn" style="padding: 2px 8px; font-size: 11px; color: #f87171;">Remove</button>
            </div>
            <div class="grid-2">
                <input type="text" class="form-control proj-name" placeholder="E-Commerce AI Platform" value="${name}">
                <input type="text" class="form-control proj-tech" placeholder="Python, Flask, React, SQLite" value="${tech}">
            </div>
            <div class="form-group" style="margin-top: 8px; margin-bottom: 0;">
                <textarea class="form-control proj-details" placeholder="• Built scalable full-stack application with real-time notifications...">${details}</textarea>
            </div>
        `;

        div.querySelector('.remove-proj-btn').addEventListener('click', () => {
            div.remove();
            updateLivePreview();
        });

        div.querySelectorAll('input, textarea').forEach(el => el.addEventListener('input', updateLivePreview));
        projectsContainer.appendChild(div);
    }

    addProjBtn.addEventListener('click', () => {
        createProjRow();
        updateLivePreview();
    });

    // Education Manager
    const educationContainer = document.getElementById('educationContainer');
    const addEduBtn = document.getElementById('addEduBtn');

    function createEduRow(degree = '', college = '', year = '', score = '') {
        const div = document.createElement('div');
        div.className = 'edu-item glass-card';
        div.style.padding = '16px';
        div.style.marginBottom = '12px';
        div.style.background = 'rgba(0,0,0,0.2)';

        div.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                <strong style="color: var(--primary-cyan);">Education Degree</strong>
                <button type="button" class="btn btn-secondary remove-edu-btn" style="padding: 2px 8px; font-size: 11px; color: #f87171;">Remove</button>
            </div>
            <div class="grid-2">
                <input type="text" class="form-control edu-degree" placeholder="B.Tech in Computer Science" value="${degree}">
                <input type="text" class="form-control edu-college" placeholder="National Institute of Tech" value="${college}">
            </div>
            <div class="grid-2" style="margin-top: 8px;">
                <input type="text" class="form-control edu-year" placeholder="2021 - 2025" value="${year}">
                <input type="text" class="form-control edu-score" placeholder="CGPA: 8.5 / 10" value="${score}">
            </div>
        `;

        div.querySelector('.remove-edu-btn').addEventListener('click', () => {
            div.remove();
            updateLivePreview();
        });

        div.querySelectorAll('input').forEach(el => el.addEventListener('input', updateLivePreview));
        educationContainer.appendChild(div);
    }

    addEduBtn.addEventListener('click', () => {
        createEduRow();
        updateLivePreview();
    });

    // Populate Initial Data if available
    if (typeof INITIAL_RESUME_DATA !== 'undefined') {
        const pInfo = INITIAL_RESUME_DATA.personal_info || {};
        document.getElementById('resName').value = pInfo.name || '';
        document.getElementById('resEmail').value = pInfo.email || '';
        document.getElementById('resPhone').value = pInfo.phone || '';
        document.getElementById('resLocation').value = pInfo.location || '';
        document.getElementById('resLinkedin').value = pInfo.linkedin || '';
        document.getElementById('resGithub').value = pInfo.github || '';

        document.getElementById('resSummary').value = INITIAL_RESUME_DATA.summary || '';

        const exps = INITIAL_RESUME_DATA.experience || [];
        if (exps.length > 0) {
            exps.forEach(e => createExpRow(e.title, e.company, e.duration, e.bullets));
        } else {
            createExpRow("Software Development Intern", "TechCorp Solutions", "Jun 2024 - Aug 2024", "• Engineered backend API endpoints in Python Flask handling 10k daily requests.\n• Reduced database query response times by 40% through indexing.");
        }

        const projs = INITIAL_RESUME_DATA.projects || [];
        if (projs.length > 0) {
            projs.forEach(p => createProjRow(p.name, p.tech, p.details));
        } else {
            createProjRow("AI Placement Preparation Platform", "Flask, SQLite, HTML5, CSS3, Gemini AI", "• Developed end-to-end career portal with AI ATS scoring and company skill gap roadmaps.");
        }

        const edus = INITIAL_RESUME_DATA.education || [];
        if (edus.length > 0) {
            edus.forEach(ed => createEduRow(ed.degree, ed.college, ed.year, ed.score));
        } else {
            createEduRow("B.Tech in Computer Science & Engineering", "XYZ Institute of Technology", "2021 - 2025", "CGPA: 8.4 / 10");
        }

        const skillsList = INITIAL_RESUME_DATA.skills || [];
        document.getElementById('resSkillsLanguages').value = skillsList.join(', ') || "Python, Java, C++, JavaScript, SQL";
        document.getElementById('resSkillsTools').value = "Flask, React, Git, AWS, Docker";
        document.getElementById('resCertifications').value = INITIAL_RESUME_DATA.certifications || "• AWS Certified Cloud Practitioner";
    }

    // Real-time Live Preview Updater
    function updateLivePreview() {
        const name = document.getElementById('resName').value || 'Rahul Sharma';
        const email = document.getElementById('resEmail').value || 'rahul@example.com';
        const phone = document.getElementById('resPhone').value || '+91 9876543210';
        const loc = document.getElementById('resLocation').value || 'Bengaluru, India';
        const linkedin = document.getElementById('resLinkedin').value || 'linkedin.com/in/rahul';
        const github = document.getElementById('resGithub').value || 'github.com/rahul';

        document.getElementById('pvName').innerText = name;
        document.getElementById('pvContact').innerHTML = `
            <span><i class="fa-solid fa-envelope"></i> ${email}</span>
            <span><i class="fa-solid fa-phone"></i> ${phone}</span>
            <span><i class="fa-solid fa-location-dot"></i> ${loc}</span>
            <span><i class="fa-brands fa-linkedin"></i> ${linkedin}</span>
            <span><i class="fa-brands fa-github"></i> ${github}</span>
        `;

        document.getElementById('pvSummary').innerText = document.getElementById('resSummary').value || 'No summary provided.';

        // Render Experience
        const expList = document.getElementById('pvExperienceList');
        expList.innerHTML = '';
        document.querySelectorAll('.exp-item').forEach(item => {
            const title = item.querySelector('.exp-title').value;
            const company = item.querySelector('.exp-company').value;
            const duration = item.querySelector('.exp-duration').value;
            const bullets = item.querySelector('.exp-bullets').value;

            if (title || company) {
                const div = document.createElement('div');
                div.style.marginBottom = '12px';
                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1e293b;">
                        <span>${title} ${company ? '| ' + company : ''}</span>
                        <span style="font-size: 12px; color: #64748b;">${duration}</span>
                    </div>
                    <div style="color: #334155; white-space: pre-line; margin-top: 4px;">${bullets}</div>
                `;
                expList.appendChild(div);
            }
        });

        // Render Projects
        const projList = document.getElementById('pvProjectsList');
        projList.innerHTML = '';
        document.querySelectorAll('.proj-item').forEach(item => {
            const name = item.querySelector('.proj-name').value;
            const tech = item.querySelector('.proj-tech').value;
            const details = item.querySelector('.proj-details').value;

            if (name) {
                const div = document.createElement('div');
                div.style.marginBottom = '12px';
                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1e293b;">
                        <span>${name} <span style="font-size: 12px; color: #0284c7; font-weight: 500;">(${tech})</span></span>
                    </div>
                    <div style="color: #334155; white-space: pre-line; margin-top: 4px;">${details}</div>
                `;
                projList.appendChild(div);
            }
        });

        // Render Education
        const eduList = document.getElementById('pvEducationList');
        eduList.innerHTML = '';
        document.querySelectorAll('.edu-item').forEach(item => {
            const degree = item.querySelector('.edu-degree').value;
            const college = item.querySelector('.edu-college').value;
            const year = item.querySelector('.edu-year').value;
            const score = item.querySelector('.edu-score').value;

            if (degree || college) {
                const div = document.createElement('div');
                div.style.marginBottom = '8px';
                div.innerHTML = `
                    <div style="display: flex; justify-content: space-between; font-weight: 700; color: #1e293b;">
                        <span>${degree} - <span style="font-weight: 400;">${college}</span></span>
                        <span style="font-size: 12px; color: #64748b;">${year} | ${score}</span>
                    </div>
                `;
                eduList.appendChild(div);
            }
        });

        // Render Skills
        document.getElementById('pvSkillsLangs').innerHTML = `<strong>Languages:</strong> ${document.getElementById('resSkillsLanguages').value}`;
        document.getElementById('pvSkillsTools').innerHTML = `<strong>Tools & Frameworks:</strong> ${document.getElementById('resSkillsTools').value}`;
        document.getElementById('pvCertifications').innerHTML = `<strong>Certifications:</strong> ${document.getElementById('resCertifications').value}`;
    }

    // Attach listeners to input fields
    document.querySelectorAll('#resumeForm input, #resumeForm textarea').forEach(el => {
        el.addEventListener('input', updateLivePreview);
    });

    updateLivePreview();

    // Theme selector
    const themeCards = document.querySelectorAll('.theme-card');
    themeCards.forEach(card => {
        card.addEventListener('click', () => {
            themeCards.forEach(c => {
                c.classList.remove('active');
                c.style.borderColor = 'var(--border-glass)';
            });
            card.classList.add('active');
            card.style.borderColor = 'var(--primary-cyan)';
            const theme = card.dataset.theme;
            document.getElementById('previewThemeBadge').innerText = `Theme: ${theme.toUpperCase()}`;
        });
    });

    // Save Resume to Server
    document.getElementById('saveResumeBtn').addEventListener('click', async () => {
        const id = document.getElementById('resumeId').value;
        const title = document.getElementById('resTitle').value;

        const personal_info = {
            name: document.getElementById('resName').value,
            email: document.getElementById('resEmail').value,
            phone: document.getElementById('resPhone').value,
            location: document.getElementById('resLocation').value,
            linkedin: document.getElementById('resLinkedin').value,
            github: document.getElementById('resGithub').value
        };

        const summary = document.getElementById('resSummary').value;

        const experience = [];
        document.querySelectorAll('.exp-item').forEach(item => {
            experience.push({
                title: item.querySelector('.exp-title').value,
                company: item.querySelector('.exp-company').value,
                duration: item.querySelector('.exp-duration').value,
                bullets: item.querySelector('.exp-bullets').value
            });
        });

        const projects = [];
        document.querySelectorAll('.proj-item').forEach(item => {
            projects.push({
                name: item.querySelector('.proj-name').value,
                tech: item.querySelector('.proj-tech').value,
                details: item.querySelector('.proj-details').value
            });
        });

        const education = [];
        document.querySelectorAll('.edu-item').forEach(item => {
            education.push({
                degree: item.querySelector('.edu-degree').value,
                college: item.querySelector('.edu-college').value,
                year: item.querySelector('.edu-year').value,
                score: item.querySelector('.edu-score').value
            });
        });

        const skillsStr = document.getElementById('resSkillsLanguages').value;
        const skills = skillsStr.split(',').map(s => s.trim()).filter(Boolean);
        const certifications = document.getElementById('resCertifications').value;

        try {
            const res = await fetch('/api/resume/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    id, title, personal_info, summary, experience, projects, education, skills, certifications
                })
            });
            const data = await res.json();
            if (data.success) {
                alert('✅ Resume saved successfully!');
            }
        } catch (err) {
            alert('Failed to save resume');
        }
    });

    // PDF Download Generator using html2pdf.js
    document.getElementById('downloadPdfBtn').addEventListener('click', () => {
        const element = document.getElementById('resumePreviewContainer');
        const name = document.getElementById('resName').value || 'Resume';
        
        const opt = {
            margin:       0.3,
            filename:     `${name.replace(/\s+/g, '_')}_Resume.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };

        html2pdf().set(opt).from(element).save();
    });
});
