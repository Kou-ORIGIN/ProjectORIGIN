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
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const chatMessagesWrapper = document.getElementById('chatMessagesWrapper');

sendBtn.addEventListener('click', sendMessage);
clearHistoryBtn.addEventListener('click', clearChatHistory);

// Enterキーでの送信制御
chatInput.addEventListener('keydown', (e) => {
    // 日本語入力の変換中は処理しない
    if (e.isComposing || e.keyCode === 229) {
        return;
    }
    
    if (e.key === 'Enter') {
        // Shift+Enterの場合は改行を許可
        if (e.shiftKey) {
            return;
        }
        
        // 通常のEnterキー - デフォルト動作を阻止して送信
        e.preventDefault();
        
        // 入力欄が無効化されている場合は送信しない（ORIGIN入力中）
        if (chatInput.disabled) {
            return;
        }
        
        sendMessage();
    }
});

// textareaの自動拡張機能
chatInput.addEventListener('input', () => {
    // スクロールハイトを使用してtextareaの高さを調整
    chatInput.style.height = 'auto';
    const scrollHeight = chatInput.scrollHeight;
    // 最大高さ（120px）を超えないようにクリップ
    if (scrollHeight > 120) {
        chatInput.style.height = '120px';
    } else {
        chatInput.style.height = scrollHeight + 'px';
    }
});

let chatHistory = [];

function getChatHistoryKey() {
    const username = localStorage.getItem('username') || 'guest';
    // ユーザー名を小文字で正規化してキーを生成（大文字小文字の違いは同じユーザーとして扱う）
    return `ProjectORIGIN_chat_history_${username.toLowerCase()}`;
}

function loadChatHistory() {
    const historyJson = localStorage.getItem(getChatHistoryKey());
    if (!historyJson) {
        return false;
    }

    try {
        const storedHistory = JSON.parse(historyJson);
        if (!Array.isArray(storedHistory)) {
            return false;
        }

        chatHistory = storedHistory;
        chatMessagesWrapper.innerHTML = '';
        chatHistory.forEach((item) => {
            createMessageElement(item.text, item.sender === 'user' ? 'user' : 'ai', item.time);
        });
        return true;
    } catch (error) {
        console.error('チャット履歴の読み込みに失敗しました', error);
        return false;
    }
}

function saveChatHistory() {
    localStorage.setItem(getChatHistoryKey(), JSON.stringify(chatHistory));
}

function clearChatHistory() {
    if (!confirm('本当にチャット履歴を削除しますか？')) {
        return;
    }

    localStorage.removeItem(getChatHistoryKey());
    chatHistory = [];
    chatMessagesWrapper.innerHTML = '';

    const username = localStorage.getItem('username') || 'ゲスト';
    addMessage(`こんにちは、${username}さん！ProjectORIGINへようこそ。本日はどのようなことでお役に立てますか？`, 'ai');
}

function sendMessage() {
    const message = chatInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Add user message
    addMessage(message, 'user');
    chatInput.value = '';
    // textareaの高さをリセット
    chatInput.style.height = 'auto';
    
    // Disable input during typing
    chatInput.disabled = true;
    sendBtn.disabled = true;
    
    // Show typing indicator
    const typingElement = showTypingIndicator();
    
    // Respond based on input intent
    const delayMs = 800 + Math.random() * 400; // 0.8～1.2秒
    setTimeout(() => {
        // Remove typing indicator
        if (typingElement && typingElement.parentNode) {
            typingElement.parentNode.removeChild(typingElement);
        }
        
        const response = getAiResponse(message);
        addMessage(response, 'ai');
        
        // Re-enable input
        chatInput.disabled = false;
        sendBtn.disabled = false;
        chatInput.focus();
    }, delayMs);
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message message-typing';
    typingDiv.setAttribute('aria-label', 'ORIGINが入力中');
    
    const dotsSpan = document.createElement('span');
    dotsSpan.className = 'typing-dots';
    dotsSpan.innerHTML = '<span>.</span><span>.</span><span>.</span>';
    
    typingDiv.appendChild(dotsSpan);
    chatMessagesWrapper.appendChild(typingDiv);
    
    // Scroll to bottom
    chatMessagesWrapper.scrollTop = chatMessagesWrapper.scrollHeight;
    
    return typingDiv;
}

function getAiResponse(message) {
    const text = message.trim().toLowerCase();

    if (text === 'こんにちは') {
        return 'こんにちは！本日はどのようなご用件でしょうか？';
    }
    if (text === 'おはよう') {
        return 'おはようございます！今日もよろしくお願いいたします。';
    }
    if (text === 'こんばんは') {
        return 'こんばんは！本日のご相談をどうぞ。';
    }
    if (text === '時間') {
        const now = new Date();
        return `現在の時刻は ${now.toLocaleTimeString('ja-JP', { hour12: false })} です。`;
    }
    if (text === '日付') {
        const today = new Date();
        return `今日の日付は ${today.toLocaleDateString('ja-JP')} です。`;
    }
    if (text === 'projectoriginとは' || text === 'projectoriginとは？' || text === 'projectoriginとは。') {
        return 'ProjectORIGINは、AIアシスタントと未来的なインターフェースを備えた次世代のAI OSです。';
    }

    return '内容を確認しました。もう少し詳しく教えてください。';
}

function createMessageElement(text, type, time = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    const pTag = document.createElement('p');
    pTag.textContent = text;
    messageDiv.appendChild(pTag);
    
    // 時刻情報を表示
    if (time) {
        const timeSpan = document.createElement('span');
        timeSpan.className = 'message-time';
        timeSpan.textContent = time;
        messageDiv.appendChild(timeSpan);
    }
    
    chatMessagesWrapper.appendChild(messageDiv);
}

function addMessage(text, type) {
    const messageType = type === 'user' ? 'user' : 'ai';
    // 現在時刻を「HH:mm」形式で取得
    const now = new Date();
    const time = now.toLocaleTimeString('ja-JP', { hour12: false, hour: '2-digit', minute: '2-digit' });
    
    chatHistory.push({ sender: messageType, text, time });
    saveChatHistory();

    createMessageElement(text, messageType, time);
    
    // Scroll to bottom
    chatMessagesWrapper.scrollTop = chatMessagesWrapper.scrollHeight;
}

// ============================================================
// INITIALIZE CHAT SCREEN
// ============================================================

function initializeChatScreen() {
    const username = localStorage.getItem('username');
    
    chatMessagesWrapper.innerHTML = '';
    chatHistory = [];

    const hasHistory = loadChatHistory();
    if (!hasHistory) {
        addMessage(`こんにちは、${username}さん！ProjectORIGINへようこそ。本日はどのようなことでお役に立てますか？`, 'ai');
    }

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
