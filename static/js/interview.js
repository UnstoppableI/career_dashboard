document.addEventListener('DOMContentLoaded', () => {
    const intGenerateBtn = document.getElementById('intGenerateBtn');
    const intPracticeCard = document.getElementById('intPracticeCard');
    const intQuestionText = document.getElementById('intQuestionText');
    const intAnswerText = document.getElementById('intAnswerText');
    const intSubmitAnswerBtn = document.getElementById('intSubmitAnswerBtn');
    const intNextQBtn = document.getElementById('intNextQBtn');
    const intCategoryBadge = document.getElementById('intCategoryBadge');
    const intQuestionIndex = document.getElementById('intQuestionIndex');

    const evalPlaceholder = document.getElementById('intEvalPlaceholder');
    const evalCard = document.getElementById('intEvalCard');

    let currentQuestions = [];
    let currentIndex = 0;

    intGenerateBtn.addEventListener('click', async () => {
        const company = document.getElementById('intCompany').value;
        const role = document.getElementById('intRole').value;
        const category = document.getElementById('intCategory').value;

        intGenerateBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Generating Questions...';
        intGenerateBtn.disabled = true;

        try {
            const res = await fetch('/api/interview/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company, role, category })
            });

            const data = await res.json();
            if (data.success && data.questions.length > 0) {
                currentQuestions = data.questions;
                currentIndex = 0;
                displayCurrentQuestion();
                intPracticeCard.style.display = 'block';
            } else {
                alert('Could not generate questions.');
            }
        } catch (err) {
            console.error(err);
            alert('Failed to generate interview questions.');
        } finally {
            intGenerateBtn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> Generate AI Interview Questions';
            intGenerateBtn.disabled = false;
        }
    });

    function displayCurrentQuestion() {
        if (currentIndex < currentQuestions.length) {
            const category = document.getElementById('intCategory').value;
            intCategoryBadge.innerText = `${category} Round`;
            intQuestionIndex.innerText = `Question ${currentIndex + 1} of ${currentQuestions.length}`;
            intQuestionText.innerText = `Q: "${currentQuestions[currentIndex]}"`;
            intAnswerText.value = '';
        } else {
            alert('All questions in this set completed!');
            intPracticeCard.style.display = 'none';
        }
    }

    intNextQBtn.addEventListener('click', () => {
        currentIndex++;
        displayCurrentQuestion();
    });

    intSubmitAnswerBtn.addEventListener('click', async () => {
        const company = document.getElementById('intCompany').value;
        const role = document.getElementById('intRole').value;
        const category = document.getElementById('intCategory').value;
        const question = currentQuestions[currentIndex];
        const answer = intAnswerText.value.trim();

        if (!answer) {
            alert('Please type an answer before submitting.');
            return;
        }

        intSubmitAnswerBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Evaluating...';
        intSubmitAnswerBtn.disabled = true;

        try {
            const res = await fetch('/api/interview/evaluate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company, role, category, question, answer })
            });

            const data = await res.json();
            if (data.success) {
                renderEvaluation(data.evaluation);
            }
        } catch (err) {
            console.error(err);
            alert('Failed to evaluate answer.');
        } finally {
            intSubmitAnswerBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Submit & Evaluate Answer';
            intSubmitAnswerBtn.disabled = false;
        }
    });

    function renderEvaluation(evalResult) {
        evalPlaceholder.style.display = 'none';
        evalCard.style.display = 'block';

        const circle = document.getElementById('intScoreCircle');
        const scoreVal = document.getElementById('intScoreVal');
        circle.style.setProperty('--score', evalResult.score);
        scoreVal.innerText = evalResult.score;

        document.getElementById('intClarityVal').innerText = evalResult.clarity;
        document.getElementById('intAccuracyVal').innerText = evalResult.technical_accuracy;

        const fbList = document.getElementById('intFeedbackList');
        fbList.innerHTML = evalResult.key_improvements.map(i => `<li>${i}</li>`).join('');

        document.getElementById('intModelAnswer').innerText = evalResult.model_answer;
    }
});
