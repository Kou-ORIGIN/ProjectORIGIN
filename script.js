// ============================================================
// ProjectORIGIN - AI OS Futuristic Interface
// Japanese Language, Hologram Style
// ============================================================

// ============================================================
// LOGIN SYSTEM
// ============================================================

const loginForm = document.getElementById('loginForm');
const loginContainer = document.getElementById('loginContainer');
const dashboard = document.getElementById('dashboard');
const logoutBtn = document.getElementById('logoutBtn');
const errorMessage = document.getElementById('errorMessage');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    
    // Validation
    if (!username) {
        showErrorMessage('ユーザー名を入力してください');
        return;
    }
    
    if (!password) {
        showErrorMessage('パスワードを入力してください');
        return;
    }
    
    if (username.length < 3) {
        showErrorMessage('ユーザー名は3文字以上で入力してください');
        return;
    }
    
    if (password.length < 6) {
        showErrorMessage('パスワードは6文字以上で入力してください');
        return;
    }
    
    // Simulate login
    loginContainer.style.display = 'none';
    dashboard.style.display = 'grid';
    localStorage.setItem('username', username);
    initializeChatScreen();
});

function showErrorMessage(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

logoutBtn.addEventListener('click', () => {
    if (confirm('ログアウトしますか？')) {
        dashboard.style.display = 'none';
        loginContainer.style.display = 'flex';
        loginForm.reset();
        errorMessage.style.display = 'none';
        localStorage.removeItem('username');
    }
});

// ============================================================
// CHAT SCREEN NAVIGATION
// ============================================================

const chatNavItems = document.querySelectorAll('.chat-nav-item');
const chatSections = document.querySelectorAll('.chat-section');

function setActiveSection(sectionName) {
    chatNavItems.forEach((nav) => {
        const isActive = nav.dataset.section === sectionName;
        nav.classList.toggle('active', isActive);
        nav.setAttribute('aria-pressed', String(isActive));
    });

    chatSections.forEach((section) => {
        const isActive = section.dataset.section === sectionName;
        section.classList.toggle('active', isActive);
        section.hidden = !isActive;
    });
}

chatNavItems.forEach((item) => {
    item.addEventListener('click', () => {
        setActiveSection(item.dataset.section);
    });
});

setActiveSection('chat');

// ============================================================
// CHAT FUNCTIONALITY
// ============================================================

const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessagesWrapper = document.getElementById('chatMessagesWrapper');

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const message = chatInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';
    chatInput.focus();
    
    // Simulate AI response
    setTimeout(() => {
        const responses = [
            'メッセージを受け取りました。処理中です...',
            'ご質問ありがとうございます。了解しました。',
            'その情報を記録しました。',
            'システムで確認しています...',
            'リクエストを処理中です。',
            'データを分析しています...',
            '確認いたしました。'
        ];
        
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        addMessage(randomResponse, 'ai');
    }, 500);
}

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    const pTag = document.createElement('p');
    pTag.textContent = text;
    messageDiv.appendChild(pTag);
    chatMessagesWrapper.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessagesWrapper.scrollTop = chatMessagesWrapper.scrollHeight;
}

// ============================================================
// INITIALIZE CHAT SCREEN
// ============================================================

function initializeChatScreen() {
    const username = localStorage.getItem('username');
    
    // Clear previous messages and add welcome message
    chatMessagesWrapper.innerHTML = '';
    addMessage(`こんにちは、${username}さん！ProjectORIGINへようこそ。本日はどのようなことでお役に立てますか？`, 'ai');
    
    // Set default tab to chat
    setActiveSection('chat');
    
    // Focus on input
    chatInput.focus();
}

// ============================================================
// SYSTEM ANIMATIONS
// ============================================================

setInterval(() => {
    const statusDots = document.querySelectorAll('.status-dot, .status-indicator');
    statusDots.forEach(dot => {
        dot.style.opacity = Math.random() > 0.5 ? 1 : 0.7;
    });
}, 500);

// Update system time
function updateSystemTime() {
    const statusElement = document.getElementById('systemStatus');
    if (statusElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ja-JP', { hour12: false });
        statusElement.textContent = `オンライン - ${timeString}`;
    }
}

setInterval(updateSystemTime, 1000);
updateSystemTime();

// ============================================================
// INITIALIZATION
// ============================================================

window.addEventListener('load', () => {
    console.log('ProjectORIGIN AI OS - Initialized successfully');
    
    // Check if user was previously logged in
    if (localStorage.getItem('username')) {
        loginContainer.style.display = 'none';
        dashboard.style.display = 'grid';
        initializeChatScreen();
    } else {
        loginContainer.style.display = 'flex';
        dashboard.style.display = 'none';
    }
});
