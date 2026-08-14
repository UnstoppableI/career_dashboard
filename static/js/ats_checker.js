document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resumeFileInput');
    const fileNameDisplay = document.getElementById('dropFileName');
    const atsForm = document.getElementById('atsForm');
    const atsAnalyzeBtn = document.getElementById('atsAnalyzeBtn');
    
    const placeholder = document.getElementById('atsPlaceholder');
    const resultsCard = document.getElementById('atsResultsCard');

    // Drag and Drop handlers
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary-cyan)';
        dropZone.style.background = 'rgba(0, 242, 254, 0.08)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--border-glass-hover)';
        dropZone.style.background = 'rgba(0, 0, 0, 0.2)';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--border-glass-hover)';
        dropZone.style.background = 'rgba(0, 0, 0, 0.2)';
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            fileNameDisplay.innerText = `Selected File: ${e.dataTransfer.files[0].name}`;
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameDisplay.innerText = `Selected File: ${fileInput.files[0].name}`;
        }
    });

    // Form Submission
    atsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const resumeText = document.getElementById('atsResumeText').value.trim();
        const fileSelected = fileInput.files.length > 0;

        if (!resumeText && !fileSelected) {
            alert('Please select a PDF file or paste your resume text to evaluate.');
            return;
        }

        atsAnalyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing Resume with AI...';
        atsAnalyzeBtn.disabled = true;

        const formData = new FormData(atsForm);

        try {
            const res = await fetch('/api/ats/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            if (data.success) {
                renderAtsResults(data.analysis);
            } else {
                alert(data.message || 'Evaluation failed.');
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred during evaluation.');
        } finally {
            atsAnalyzeBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> Run AI ATS Evaluation';
            atsAnalyzeBtn.disabled = false;
        }
    });

    function renderAtsResults(analysis) {
        placeholder.style.display = 'none';
        resultsCard.style.display = 'block';

        document.getElementById('atsRoleBadge').innerText = analysis.job_role;
        document.getElementById('atsFileTitle').innerText = `${analysis.file_name} Report`;

        // Update Score Gauge Circle
        const scoreCircle = document.getElementById('atsScoreCircle');
        const scoreVal = document.getElementById('atsScoreVal');
        scoreCircle.style.setProperty('--score', analysis.ats_score);
        scoreVal.innerText = analysis.ats_score;

        if (analysis.ats_score >= 80) {
            scoreCircle.style.background = `conic-gradient(var(--accent-emerald) calc(${analysis.ats_score} * 1%), rgba(255, 255, 255, 0.08) 0)`;
        } else if (analysis.ats_score >= 65) {
            scoreCircle.style.background = `conic-gradient(var(--primary-cyan) calc(${analysis.ats_score} * 1%), rgba(255, 255, 255, 0.08) 0)`;
        } else {
            scoreCircle.style.background = `conic-gradient(var(--accent-amber) calc(${analysis.ats_score} * 1%), rgba(255, 255, 255, 0.08) 0)`;
        }

        // Summary
        document.getElementById('atsSummary').innerText = analysis.summary;

        // Strengths
        const strengthsUl = document.getElementById('atsStrengthsList');
        strengthsUl.innerHTML = analysis.strengths.map(s => `<li>${s}</li>`).join('');

        // Weaknesses
        const weaknessesUl = document.getElementById('atsWeaknessesList');
        weaknessesUl.innerHTML = analysis.weaknesses.map(w => `<li>${w}</li>`).join('');

        // Keywords & Missing Skills Badges
        const kwContainer = document.getElementById('atsKeywordsContainer');
        kwContainer.innerHTML = '';
        analysis.missing_skills.forEach(skill => {
            kwContainer.innerHTML += `<span class="badge badge-amber"><i class="fa-solid fa-plus"></i> ${skill}</span>`;
        });
        analysis.keywords.forEach(kw => {
            kwContainer.innerHTML += `<span class="badge badge-cyan">${kw}</span>`;
        });

        // Suggestions List
        const sugContainer = document.getElementById('atsSuggestionsList');
        sugContainer.innerHTML = analysis.suggestions.map((sug, idx) => `
            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-glass); padding: 12px 16px; border-radius: var(--radius-md); font-size: 13px; color: var(--text-secondary); display: flex; gap: 12px; align-items: flex-start;">
                <span style="font-weight: 700; color: var(--primary-cyan); font-size: 14px;">${idx + 1}.</span>
                <span>${sug}</span>
            </div>
        `).join('');
    }
});
