// Configuration
const API_URL = '/api';
let currentToken = localStorage.getItem('token');
let currentUser = JSON.parse(localStorage.getItem('user') || 'null');

// Navigation
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
    document.getElementById(`page-${pageId}`).classList.remove('hidden');
    
    if (currentToken && pageId !== 'login' && pageId !== 'register') {
        document.getElementById('navbar').classList.remove('hidden');
    } else {
        document.getElementById('navbar').classList.add('hidden');
    }

    if (pageId === 'dashboard') loadDashboard();
}

// Toast
function showToast(message, type='success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), 3000);
}

// Authentication
async function apiFetch(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json' };
    if (currentToken) headers['Authorization'] = `Bearer ${currentToken}`;
    
    if (options.body instanceof FormData) {
        delete headers['Content-Type']; // Let browser set boundary
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: { ...headers, ...options.headers }
        });
        const data = await response.json();
        if (!response.ok || !data.success) {
            throw new Error(data.error?.message || 'API Error');
        }
        return data.data;
    } catch (e) {
        showToast(e.message, 'error');
        if (e.message.includes('token') || e.message.includes('Authentication')) {
            logout();
        }
        throw e;
    }
}

document.getElementById('login-form').onsubmit = async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    try {
        const data = await apiFetch('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
        loginSuccess(data);
    } catch (e) {}
};

document.getElementById('register-form').onsubmit = async (e) => {
    e.preventDefault();
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    try {
        const data = await apiFetch('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ name, email, password })
        });
        loginSuccess(data);
    } catch (e) {}
};

function loginSuccess(data) {
    currentToken = data.token;
    currentUser = data.user;
    localStorage.setItem('token', currentToken);
    localStorage.setItem('user', JSON.stringify(currentUser));
    document.getElementById('user-name').textContent = currentUser.name;
    showPage('dashboard');
}

function logout() {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    showPage('login');
}

// Dashboard
async function loadDashboard() {
    if (!currentUser) return logout();
    document.getElementById('user-name').textContent = currentUser.name;
    
    const list = document.getElementById('appointments-list');
    list.innerHTML = 'Loading...';
    try {
        const appointments = await apiFetch('/appointments');
        if (appointments.length === 0) {
            list.innerHTML = '<p class="text-muted">No appointments found.</p>';
            return;
        }
        list.innerHTML = appointments.map(a => `
            <div class="list-item">
                <div class="appt-header">
                    <h4>${a.doctor_name} <span class="text-muted text-sm">(${a.specialty})</span></h4>
                    <span class="status text-muted">${a.status}</span>
                </div>
                <p>Date: ${a.date} at ${a.time}</p>
                <p>Patient: ${a.patient_name}</p>
            </div>
        `).join('');
    } catch (e) {
        list.innerHTML = 'Failed to load appointments.';
    }
}

// Questionnaire
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
let currentQ = 0;
let answers = {};

function startQuestionnaire() {
    currentQ = 0;
    answers = {};
    renderQuestion();
    showPage('questionnaire');
}

function renderQuestion() {
    if (currentQ >= questions.length) {
        renderReview();
        return;
    }
    const q = questions[currentQ];
    document.getElementById('question-text').textContent = q.text;
    document.getElementById('q-progress-text').textContent = `Question ${currentQ + 1} of 10`;
    const pct = ((currentQ) / 10) * 100;
    document.getElementById('q-progress-pct').textContent = `${pct}%`;
    document.getElementById('q-progress-fill').style.width = `${pct}%`;
}

function handleAnswer(val) {
    answers[questions[currentQ].id] = val;
    currentQ++;
    renderQuestion();
}

function goBackQ() {
    if (currentQ > 0) {
        currentQ--;
        renderQuestion();
    }
}

function editAnswer(idx) {
    currentQ = idx;
    showPage('questionnaire');
    renderQuestion();
}

function renderReview() {
    const list = document.getElementById('review-list');
    list.innerHTML = questions.map((q, idx) => `
        <div class="history-item">
            <span>${q.text}</span>
            <div>
                <strong>${answers[q.id] ? 'Yes' : 'No'}</strong>
                <button class="btn-edit" onclick="editAnswer(${idx})">✎</button>
            </div>
        </div>
    `).join('');
    showPage('review');
}

async function getRecommendation() {
    const btn = document.getElementById('btn-recommend');
    
    // Check if all answers are 0
    const allNo = Object.values(answers).every(val => val === 0);
    if (allNo) {
        showPage('zero-symptoms');
        return;
    }

    btn.textContent = 'Analyzing...';
    btn.disabled = true;
    try {
        const result = await apiFetch('/recommendations', {
            method: 'POST',
            body: JSON.stringify(answers)
        });
        
        document.getElementById('rec-specialty').textContent = result.recommended_specialty;
        document.getElementById('rec-prob').textContent = `${Math.round(result.top_matches[0].probability * 100)}%`;
        
        const others = result.top_matches.slice(1);
        document.getElementById('rec-other').innerHTML = others.map(m => `
            <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                <span>${m.specialty}</span>
                <span>${Math.round(m.probability * 100)}%</span>
            </div>
        `).join('');

        showPage('recommendation');
        loadDoctors(result.recommended_specialty, 'doctors-list');
    } catch (e) {
    } finally {
        btn.textContent = 'Get Recommendation';
        btn.disabled = false;
    }
}

async function loadDoctors(specialty = '', targetElement = 'doctors-list') {
    const list = document.getElementById(targetElement);
    list.innerHTML = 'Finding available doctors...';
    try {
        let url = '/doctors';
        if (specialty) url += `?specialty=${specialty}`;
        const doctors = await apiFetch(url);
        if (doctors.length === 0) {
            list.innerHTML = '<p>No doctors found.</p>';
            return;
        }
        list.innerHTML = doctors.map(d => `
            <div class="list-item">
                <div class="doctor-header">
                    <div>
                        <h4>${d.name} <span class="text-sm text-muted">(${d.specialty})</span></h4>
                        <p class="text-muted">${d.experience} experience</p>
                    </div>
                </div>
                <p style="margin: 10px 0;">${d.bio}</p>
                <div>
                    ${d.availability.map(t => `<span class="time-slot" onclick="openBooking('${d._id}', '${d.name}', '${t}')">${t}</span>`).join('')}
                </div>
            </div>
        `).join('');
    } catch (e) {
        list.innerHTML = 'Failed to load doctors.';
    }
}

function loadAllDoctors() {
    showPage('all-doctors');
    loadDoctors('', 'all-doctors-list');
}

function filterDoctors() {
    const specialty = document.getElementById('filter-specialty').value;
    loadDoctors(specialty, 'all-doctors-list');
}

// Booking Modal
function openBooking(docId, docName, time) {
    document.getElementById('booking-modal').classList.remove('hidden');
    document.getElementById('book-doctor-id').value = docId;
    document.getElementById('book-doctor-name').textContent = `Booking with ${docName} at ${time}`;
    document.getElementById('book-time').innerHTML = `<option value="${time}">${time}</option>`;
    
    // Set min date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('book-date').min = today;
    document.getElementById('book-date').value = today;
}

function closeModal() {
    document.getElementById('booking-modal').classList.add('hidden');
    document.getElementById('booking-form').reset();
}

document.getElementById('booking-form').onsubmit = async (e) => {
    e.preventDefault();
    const payload = {
        doctor_id: document.getElementById('book-doctor-id').value,
        date: document.getElementById('book-date').value,
        time: document.getElementById('book-time').value,
        patient_name: document.getElementById('book-patient-name').value,
        notes: document.getElementById('book-notes').value
    };
    
    try {
        await apiFetch('/appointments', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        showToast('Appointment booked successfully!');
        closeModal();
        showPage('dashboard');
    } catch (e) {}
};

// AI Assistant
document.getElementById('ai-form').onsubmit = async (e) => {
    e.preventDefault();
    const text = document.getElementById('ai-text').value;
    const fileInput = document.getElementById('ai-file');
    const btn = document.getElementById('btn-ai-analyze');
    
    const formData = new FormData();
    if (text) formData.append('text', text);
    if (fileInput.files.length > 0) formData.append('file', fileInput.files[0]);
    
    if (!text && fileInput.files.length === 0) {
        return showToast('Please enter text or upload a file', 'error');
    }
    
    btn.textContent = 'Processing...';
    btn.disabled = true;
    document.getElementById('ai-result').classList.add('hidden');
    
    try {
        const result = await apiFetch('/medical-assistant/analyze', {
            method: 'POST',
            body: formData
        });
        
        // Basic Markdown parsing (assuming marked.js is loaded)
        document.getElementById('ai-content').innerHTML = marked.parse(result.analysis);
        document.getElementById('ai-result').classList.remove('hidden');
    } catch (e) {
    } finally {
        btn.textContent = 'Analyze';
        btn.disabled = false;
    }
};

// Init
if (currentToken) showPage('dashboard');
else showPage('login');
