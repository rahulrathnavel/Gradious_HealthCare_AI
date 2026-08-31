const questions = [
    { id: 'fever', text: 'Do you have a fever?' },
    { id: 'cough', text: 'Do you have a cough?' },
    { id: 'breathlessness', text: 'Do you have difficulty breathing or breathlessness?' },
    { id: 'chest_pain', text: 'Do you have chest pain?' },
    { id: 'headache', text: 'Do you have a headache?' },
    { id: 'digestive_problem', text: 'Do you have stomach or digestive problems?' },
    { id: 'joint_or_muscle_problem', text: 'Do you have joint or muscle pain/problems?' },
    { id: 'skin_problem', text: 'Do you have a skin problem such as a rash or itching?' },
    { id: 'urinary_problem', text: 'Do you have a urinary problem?' },
    { id: 'fatigue', text: 'Do you feel unusually tired or weak?' }
];

let currentQuestionIndex = 0;
let answers = {}; // Store answers as { id: 1/0 }

const appContainer = document.getElementById('app-container');

function renderQuestion() {
    if (currentQuestionIndex >= questions.length) {
        renderReview();
        return;
    }

    const question = questions[currentQuestionIndex];
    const progress = ((currentQuestionIndex) / questions.length) * 100;

    appContainer.innerHTML = `
        <div class="card">
            <div class="progress-header">
                <span>Question ${currentQuestionIndex + 1} of ${questions.length}</span>
                <span>${Math.round(progress)}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progress}%"></div>
            </div>
            
            <h3 class="question-text">${question.text}</h3>
            
            <div class="options">
                <button class="btn-option" onclick="handleAnswer(1)">YES</button>
                <button class="btn-option" onclick="handleAnswer(0)">NO</button>
            </div>
            
            ${currentQuestionIndex > 0 ? `<button class="btn-nav" onclick="goBack()">← Back</button>` : ''}
        </div>
    `;
}

function handleAnswer(value) {
    const question = questions[currentQuestionIndex];
    answers[question.id] = value;
    currentQuestionIndex++;
    renderQuestion();
}

function goBack() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderQuestion();
    }
}

function goToQuestion(index) {
    currentQuestionIndex = index;
    renderQuestion();
}

function renderReview() {
    let historyHtml = '<div class="history-list">';
    
    questions.forEach((q, index) => {
        const answerVal = answers[q.id];
        const answerText = answerVal === 1 ? 'Yes' : 'No';
        
        historyHtml += `
            <div class="history-item">
                <div class="history-question">${q.text}</div>
                <div class="history-answer">${answerText}</div>
                <button class="btn-edit" onclick="goToQuestion(${index})">✎</button>
            </div>
        `;
    });
    
    historyHtml += '</div>';

    appContainer.innerHTML = `
        <div class="card">
            <h3 class="question-text" style="margin-bottom: 20px;">Review your answers</h3>
            
            ${historyHtml}
            
            <button class="btn-primary mt-20" id="btn-recommend" onclick="getRecommendation()">Get Recommendation</button>
            <button class="btn-nav mt-20" onclick="goToQuestion(0)">← Start Over</button>
        </div>
    `;
}

async function getRecommendation() {
    const btn = document.getElementById('btn-recommend');
    btn.textContent = 'Analyzing...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(answers)
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }
        
        const data = await response.json();
        renderResult(data);
    } catch (error) {
        alert('Error getting recommendation: ' + error.message);
        btn.textContent = 'Get Recommendation';
        btn.disabled = false;
    }
}

function renderResult(data) {
    const topMatch = data.top_matches[0];
    const otherMatches = data.top_matches.slice(1);
    
    let otherMatchesHtml = '';
    otherMatches.forEach(match => {
        const percent = Math.round(match.probability * 100);
        otherMatchesHtml += `
            <div class="match-item">
                <div class="match-header">
                    <span>${match.specialty}</span>
                    <span>${percent}%</span>
                </div>
                <div class="match-bar-bg">
                    <div class="match-bar-fill" style="width: ${percent}%"></div>
                </div>
            </div>
        `;
    });

    appContainer.innerHTML = `
        <div class="card">
            <div class="result-title">Recommended medical specialty</div>
            
            <div class="main-recommendation">
                <div class="specialty-name">${topMatch.specialty}</div>
                <div class="specialty-prob">${Math.round(topMatch.probability * 100)}%</div>
            </div>
            
            <div class="other-matches">
                <h3>Other possible matches</h3>
                ${otherMatchesHtml}
            </div>
            
            <div class="disclaimer">
                Based on the symptoms you entered.<br><br>
                This is a proof-of-concept specialty recommendation and is not a medical diagnosis.
            </div>
            
            <button class="btn-primary mt-20" onclick="resetApp()">Start Again</button>
        </div>
    `;
}

function resetApp() {
    currentQuestionIndex = 0;
    answers = {};
    renderQuestion();
}

// Initialize
renderQuestion();

