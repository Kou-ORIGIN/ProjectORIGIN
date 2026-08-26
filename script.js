// ============================================================
// ProjectORIGIN - AI OS Futuristic Interface
// Japanese Language, Hologram Style
// ============================================================

// ============================================================
// LOGIN SYSTEM
// ============================================================

const loginForm = document.getElementById('loginForm');
const loginContainer = document.getElementById('loginContainer');
const topPage = document.getElementById('topPage');
const dashboard = document.getElementById('dashboard');
const dashboardTopPageBtn = document.getElementById('dashboardTopPageBtn');
const desktopLogoutBtn = document.getElementById('desktopLogoutBtn');
const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
const errorMessage = document.getElementById('errorMessage');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const dashboardHeader = document.querySelector('.dashboard-header');
const logoutConfirmOverlay = document.getElementById('logoutConfirmOverlay');
const logoutConfirmDialog = logoutConfirmOverlay?.querySelector('.logout-confirm-dialog') || null;
const logoutConfirmCancelBtn = document.getElementById('logoutConfirmCancelBtn');
const logoutConfirmSubmitBtn = document.getElementById('logoutConfirmSubmitBtn');
const desktopSidebarMediaQuery = window.matchMedia('(min-width: 993px)');

const HEADER_TOP_REVEAL_THRESHOLD = 24;
const HEADER_SCROLL_TOGGLE_THRESHOLD = 32;
const HEADER_VISIBILITY_STORAGE_KEY = 'ProjectORIGIN_header_visibility';

let lastKnownScrollY = window.scrollY;
let lastHeaderToggleScrollY = window.scrollY;
let headerVisibilityLocked = false;
let isHeaderVisible = getStoredHeaderVisibility();
let scrollTicking = false;
let logoutConfirmOpen = false;
const modalStack = [];
const modalManagedInertElements = new Set();
const FOCUSABLE_SELECTOR = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
].join(',');

function isVisibleFocusableElement(element) {
    if (!(element instanceof HTMLElement) || element.hidden || element.closest('[hidden]')) {
        return false;
    }

    const style = window.getComputedStyle(element);
    return style.display !== 'none'
        && style.visibility !== 'hidden'
        && element.getClientRects().length > 0;
}

function getModalFocusableElements(dialog) {
    if (!dialog) {
        return [];
    }

    return Array.from(dialog.querySelectorAll(FOCUSABLE_SELECTOR)).filter(isVisibleFocusableElement);
}

function getTopModalEntry() {
    return modalStack[modalStack.length - 1] || null;
}

function clearManagedBackgroundInert() {
    modalManagedInertElements.forEach((element) => {
        element.inert = false;
    });
    modalManagedInertElements.clear();
}

function setModalBackgroundInert(activeOverlay) {
    clearManagedBackgroundInert();

    if (!activeOverlay) {
        return;
    }

    let activeBranch = activeOverlay;
    let parent = activeBranch.parentElement;

    while (parent) {
        Array.from(parent.children).forEach((sibling) => {
            if (sibling !== activeBranch && sibling instanceof HTMLElement && !sibling.inert) {
                sibling.inert = true;
                modalManagedInertElements.add(sibling);
            }
        });

        if (parent === document.body) {
            break;
        }

        activeBranch = parent;
        parent = parent.parentElement;
    }
}

function syncModalInteractionState() {
    const topModal = getTopModalEntry();
    setModalBackgroundInert(topModal?.overlay || null);
}

function activateModal(id, overlay, dialog, trigger) {
    const existingIndex = modalStack.findIndex((entry) => entry.id === id);
    if (existingIndex !== -1) {
        modalStack.splice(existingIndex, 1);
    }

    modalStack.push({
        id,
        overlay,
        dialog,
        trigger: trigger instanceof HTMLElement ? trigger : null
    });
    syncModalInteractionState();
}

function deactivateModal(id) {
    const entryIndex = modalStack.findIndex((entry) => entry.id === id);
    if (entryIndex === -1) {
        return null;
    }

    const [entry] = modalStack.splice(entryIndex, 1);
    syncModalInteractionState();
    return entry;
}

function restoreModalTriggerFocus(entry, fallback = null) {
    const trigger = entry?.trigger;
    const focusTarget = trigger?.isConnected && isVisibleFocusableElement(trigger) ? trigger : fallback;
    if (focusTarget instanceof HTMLElement && !focusTarget.inert && isVisibleFocusableElement(focusTarget)) {
        focusTarget.focus({ preventScroll: true });
    }
}

function containFocusWithinTopModal(event) {
    const topModal = getTopModalEntry();
    if (!topModal?.dialog) {
        return;
    }

    const focusableElements = getModalFocusableElements(topModal.dialog);
    if (focusableElements.length === 0) {
        event.preventDefault();
        return;
    }

    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    const activeElement = document.activeElement;

    if (!topModal.dialog.contains(activeElement)) {
        event.preventDefault();
        (event.shiftKey ? lastFocusable : firstFocusable).focus();
        return;
    }

    if (event.shiftKey && activeElement === firstFocusable) {
        event.preventDefault();
        lastFocusable.focus();
    } else if (!event.shiftKey && activeElement === lastFocusable) {
        event.preventDefault();
        firstFocusable.focus();
    }
}

function redirectEscapedModalFocus(event) {
    const topModal = getTopModalEntry();
    if (!topModal?.dialog || topModal.dialog.contains(event.target)) {
        return;
    }

    const [firstFocusable] = getModalFocusableElements(topModal.dialog);
    firstFocusable?.focus({ preventScroll: true });
}

if (dashboardHeader && !isHeaderVisible) {
    dashboardHeader.classList.add('header-hidden');
}

function setLoginFieldInvalid(input, invalid) {
    input.setAttribute('aria-invalid', String(invalid));
}

function clearLoginValidationState() {
    setLoginFieldInvalid(usernameInput, false);
    setLoginFieldInvalid(passwordInput, false);
}

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    errorMessage.style.display = 'none';
    errorMessage.textContent = '';
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    const usernameInvalid = !username || username.length < 3;
    const passwordInvalid = !password || password.length < 6;

    setLoginFieldInvalid(usernameInput, usernameInvalid);
    setLoginFieldInvalid(passwordInput, passwordInvalid);
    
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

    clearLoginValidationState();
    
    // Simulate login
    loginContainer.style.display = 'none';
    dashboard.style.display = 'grid';
    localStorage.setItem('username', username);
    initializeChatScreen();
    requestAnimationFrame(refreshHeaderLayout);
});

function showErrorMessage(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function getStoredHeaderVisibility() {
    try {
        return localStorage.getItem(HEADER_VISIBILITY_STORAGE_KEY) !== 'hidden';
    } catch (error) {
        return true;
    }
}

function persistHeaderVisibility(visible) {
    try {
        localStorage.setItem(HEADER_VISIBILITY_STORAGE_KEY, visible ? 'visible' : 'hidden');
    } catch (error) {
        // Ignore localStorage access errors.
    }
}

function clearHeaderBootState() {
    document.documentElement.classList.remove('header-boot-hidden');
}

function clearAuthCheckingState() {
    document.documentElement.classList.remove('auth-checking');
}

function hasPersistedLogin() {
    try {
        const storedUsername = localStorage.getItem('username');
        return typeof storedUsername === 'string' && storedUsername.trim() !== '';
    } catch (error) {
        return false;
    }
}

function applyAuthView(isLoggedIn) {
    if (isLoggedIn) {
        loginContainer.style.display = 'none';
        dashboard.style.display = 'grid';
        initializeChatScreen();
        refreshHeaderLayout();
    } else {
        loginContainer.style.display = 'flex';
        dashboard.style.display = 'none';
        resetHeaderScrollState();
    }

    clearAuthCheckingState();
}

function executeLogout() {
    closeMobileNavDrawer({ restoreFocus: false, immediate: true });
    dashboard.style.display = 'none';
    loginContainer.style.display = 'flex';
    loginForm.reset();
    clearLoginValidationState();
    errorMessage.style.display = 'none';
    localStorage.removeItem('username');
    favoriteIncidentIds = new Set();
    lockHeaderVisibility(true);
}

function openLogoutConfirmDialog(trigger = document.activeElement) {
    if (!logoutConfirmOverlay || logoutConfirmOpen) {
        return;
    }

    logoutConfirmOpen = true;
    logoutConfirmOverlay.hidden = false;
    activateModal('logout-confirm', logoutConfirmOverlay, logoutConfirmDialog, trigger);
    lockBodyScroll('logout-confirm');

    if (logoutConfirmCancelBtn) {
        logoutConfirmCancelBtn.focus();
    }
}

function closeLogoutConfirmDialog(options = {}) {
    if (!logoutConfirmOverlay || !logoutConfirmOpen) {
        return;
    }

    const shouldRestoreFocus = options.restoreFocus !== false;
    logoutConfirmOpen = false;
    logoutConfirmOverlay.hidden = true;
    const modalEntry = deactivateModal('logout-confirm');
    unlockBodyScroll('logout-confirm');

    if (shouldRestoreFocus) {
        restoreModalTriggerFocus(modalEntry);
    }
}

if (desktopLogoutBtn) {
    desktopLogoutBtn.addEventListener('click', (event) => {
        openLogoutConfirmDialog(event.currentTarget);
    });
}

if (mobileLogoutBtn) {
    mobileLogoutBtn.addEventListener('click', (event) => {
        openLogoutConfirmDialog(event.currentTarget);
    });
}

if (logoutConfirmCancelBtn) {
    logoutConfirmCancelBtn.addEventListener('click', () => {
        closeLogoutConfirmDialog();
    });
}

if (logoutConfirmSubmitBtn) {
    logoutConfirmSubmitBtn.addEventListener('click', () => {
        closeLogoutConfirmDialog({ restoreFocus: false });
        executeLogout();
    });
}

if (logoutConfirmOverlay) {
    logoutConfirmOverlay.addEventListener('click', (event) => {
        if (event.target === logoutConfirmOverlay) {
            closeLogoutConfirmDialog();
        }
    });
}

// ============================================================
// CHAT SCREEN NAVIGATION
// ============================================================

const desktopNavMenu = document.getElementById('desktopNavMenu');
let desktopNavItems = [];
const chatSections = document.querySelectorAll('.chat-section');
const mobileNavToggleBtn = document.getElementById('mobileNavToggleBtn');
const mobileNavOverlay = document.getElementById('mobileNavOverlay');
const mobileNavDrawer = document.getElementById('mobileNavDrawer');
const mobileNavCloseBtn = document.getElementById('mobileNavCloseBtn');
const mobileNavMenu = document.getElementById('mobileNavMenu');
const originAssistantPanel = document.getElementById('originAssistantPanel');
const ACTIVE_SECTION_STORAGE_KEY = 'ProjectORIGIN_active_section';
const MOBILE_NAV_TRANSITION_MS = 260;

const navigationConfig = [
    { section: 'chat', label: 'チャット' },
    { section: 'incident-file', label: '事件ファイル' },
    { section: 'origin-map', label: 'ORIGIN MAP' },
    { section: 'timeline', label: 'タイムライン' },
    { section: 'favorites', label: 'お気に入り' },
    { section: 'info', label: '情報' }
];
const topPageNavItems = topPage ? Array.from(topPage.querySelectorAll('.top-page-nav-button')) : [];

let mobileNavItems = [];
let mobileNavHideTimerId = null;
let mobileNavReturnFocus = null;
const bodyScrollLockReasons = new Set();
let bodyScrollLockY = 0;

function normalizeSectionName(sectionName) {
    if (sectionName === 'incidents') {
        return 'incident-file';
    }
    if (sectionName === 'map') {
        return 'origin-map';
    }
    return sectionName;
}

function getStoredSectionName() {
    const storedSection = localStorage.getItem(ACTIVE_SECTION_STORAGE_KEY);
    if (!storedSection) {
        return 'chat';
    }

    const normalizedSection = normalizeSectionName(storedSection);
    const validSections = navigationConfig.map((item) => item.section);
    return validSections.includes(normalizedSection) ? normalizedSection : 'chat';
}

function persistActiveSection(sectionName) {
    const normalizedSection = normalizeSectionName(sectionName);
    const storageValue = normalizedSection === 'incident-file' ? 'incidents' : normalizedSection === 'origin-map' ? 'map' : normalizedSection;
    localStorage.setItem(ACTIVE_SECTION_STORAGE_KEY, storageValue);
}

function getCombinedNavItems() {
    return [...desktopNavItems, ...mobileNavItems];
}

function handleSectionSetup(sectionName) {
    if (sectionName === 'incident-file') {
        initializeIncidentArchive();
    }
    if (sectionName === 'origin-map') {
        initializeOriginMap();
    }
    if (sectionName === 'favorites') {
        initializeFavoritesView();
    }
}

function navigateToSection(sectionName, options = {}) {
    const normalizedSection = normalizeSectionName(sectionName);
    const shouldPersist = options.persist !== false;
    const shouldCloseMobileDrawer = options.closeMobileDrawer !== false;

    setActiveSection(normalizedSection, { persist: shouldPersist });
    handleSectionSetup(normalizedSection);

    if (shouldCloseMobileDrawer) {
        closeMobileNavDrawer({ restoreFocus: false });
    }
}

function focusDashboardSection(sectionName) {
    const normalizedSection = normalizeSectionName(sectionName);
    const destinationSection = Array.from(chatSections)
        .find((section) => section.dataset.section === normalizedSection);

    if (!destinationSection || destinationSection.hidden) {
        return;
    }

    destinationSection.setAttribute('tabindex', '-1');
    destinationSection.focus({ preventScroll: true });
    destinationSection.addEventListener('blur', () => {
        destinationSection.removeAttribute('tabindex');
    }, { once: true });
}

function navigateFromTopPage(sectionName) {
    if (!topPage || topPage.hidden) {
        return;
    }

    topPage.hidden = true;
    loginContainer.style.display = 'none';
    dashboard.style.display = 'grid';
    navigateToSection(sectionName);

    requestAnimationFrame(() => {
        refreshHeaderLayout();
        focusDashboardSection(sectionName);
    });
}

function showTopPageFromDashboard() {
    if (!topPage) {
        return;
    }

    closeMobileNavDrawer({ restoreFocus: false, immediate: true });
    dashboard.style.display = 'none';
    initializeTopFeaturedRecords();
    topPage.hidden = false;
    requestTopFeaturedRecordUpdate();
    window.scrollTo({ top: 0, left: 0, behavior: 'auto' });

    const encounterHeading = document.getElementById('topEncounterHeading');
    if (!encounterHeading) {
        return;
    }

    encounterHeading.setAttribute('tabindex', '-1');
    requestAnimationFrame(() => {
        encounterHeading.focus({ preventScroll: true });
    });
    encounterHeading.addEventListener('blur', () => {
        encounterHeading.removeAttribute('tabindex');
    }, { once: true });
}

if (dashboardTopPageBtn) {
    dashboardTopPageBtn.addEventListener('click', showTopPageFromDashboard);
}

topPageNavItems.forEach((item) => {
    item.addEventListener('click', () => {
        navigateFromTopPage(item.dataset.section);
    });
});

function setActiveSection(sectionName, options = {}) {
    const normalizedSection = normalizeSectionName(sectionName);
    const shouldPersist = options.persist !== false;

    if (shouldPersist) {
        persistActiveSection(normalizedSection);
    }

    getCombinedNavItems().forEach((nav) => {
        const isActive = nav.dataset.section === normalizedSection;
        nav.classList.toggle('active', isActive);
        nav.setAttribute('aria-pressed', String(isActive));
    });

    chatSections.forEach((section) => {
        const isActive = section.dataset.section === normalizedSection;
        section.classList.toggle('active', isActive);
        section.hidden = !isActive;
    });

    if (originAssistantPanel) {
        originAssistantPanel.classList.toggle('is-chat-context', normalizedSection === 'chat');
    }
}

function renderDesktopNavItems() {
    if (!desktopNavMenu) {
        return;
    }

    desktopNavMenu.innerHTML = '';
    const fragment = document.createDocumentFragment();

    navigationConfig.forEach((item) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'chat-nav-item';
        button.setAttribute('data-section', item.section);
        button.setAttribute('aria-pressed', 'false');
        button.textContent = item.label;
        fragment.appendChild(button);
    });

    desktopNavMenu.appendChild(fragment);
    desktopNavItems = Array.from(desktopNavMenu.querySelectorAll('.chat-nav-item'));

    desktopNavItems.forEach((item) => {
        item.addEventListener('click', () => {
            navigateToSection(item.dataset.section, { closeMobileDrawer: false });
        });
    });
}

function isIncidentModalOpen() {
    return Boolean(incidentModalOverlay && !incidentModalOverlay.hidden);
}

function isMobileNavigationViewport() {
    return !desktopSidebarMediaQuery.matches;
}

function lockBodyScroll(reason) {
    if (!reason || bodyScrollLockReasons.has(reason)) {
        return;
    }

    if (bodyScrollLockReasons.size === 0) {
        bodyScrollLockY = window.scrollY || window.pageYOffset || 0;
        document.body.style.top = `-${bodyScrollLockY}px`;
        document.body.classList.add('body-scroll-locked');
    }

    bodyScrollLockReasons.add(reason);
}

function unlockBodyScroll(reason) {
    if (!reason || !bodyScrollLockReasons.has(reason)) {
        return;
    }

    bodyScrollLockReasons.delete(reason);

    if (bodyScrollLockReasons.size > 0) {
        return;
    }

    document.body.classList.remove('body-scroll-locked');
    document.body.style.top = '';
    window.scrollTo({ top: bodyScrollLockY, left: 0, behavior: 'auto' });
}

function renderMobileNavItems() {
    if (!mobileNavMenu) {
        return;
    }

    mobileNavMenu.innerHTML = '';
    const fragment = document.createDocumentFragment();

    navigationConfig.forEach((item) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'mobile-nav-item';
        button.setAttribute('data-section', item.section);
        button.setAttribute('aria-pressed', 'false');
        button.textContent = item.label;

        button.addEventListener('click', () => {
            navigateToSection(item.section);
        });

        fragment.appendChild(button);
    });

    mobileNavMenu.appendChild(fragment);
    mobileNavItems = Array.from(mobileNavMenu.querySelectorAll('.mobile-nav-item'));
}

function openMobileNavDrawer() {
    if (!mobileNavOverlay || !mobileNavDrawer || !mobileNavToggleBtn) {
        return;
    }

    if (!isMobileNavigationViewport()) {
        closeMobileNavDrawer({ restoreFocus: false, immediate: true });
        return;
    }

    if (isIncidentModalOpen()) {
        return;
    }

    if (!mobileNavOverlay.hidden && mobileNavOverlay.classList.contains('is-open')) {
        return;
    }

    if (mobileNavHideTimerId !== null) {
        window.clearTimeout(mobileNavHideTimerId);
        mobileNavHideTimerId = null;
    }

    mobileNavOverlay.hidden = false;
    mobileNavDrawer.setAttribute('aria-hidden', 'false');
    mobileNavToggleBtn.setAttribute('aria-expanded', 'true');
    mobileNavReturnFocus = document.activeElement instanceof HTMLElement ? document.activeElement : mobileNavToggleBtn;
    activateModal('mobile-nav', mobileNavOverlay, mobileNavDrawer, mobileNavReturnFocus);

    requestAnimationFrame(() => {
        mobileNavOverlay.classList.add('is-open');
    });

    lockBodyScroll('mobile-nav');
    lockHeaderVisibility(true);

    if (mobileNavCloseBtn) {
        mobileNavCloseBtn.focus();
    }
}

function closeMobileNavDrawer(options = {}) {
    if (!mobileNavOverlay || !mobileNavDrawer || !mobileNavToggleBtn) {
        return;
    }

    if (mobileNavOverlay.hidden) {
        return;
    }

    const shouldRestoreFocus = options.restoreFocus !== false;
    const shouldCloseImmediately = options.immediate === true;
    const modalEntry = deactivateModal('mobile-nav');

    mobileNavOverlay.classList.remove('is-open');
    mobileNavDrawer.setAttribute('aria-hidden', 'true');
    mobileNavToggleBtn.setAttribute('aria-expanded', 'false');
    unlockBodyScroll('mobile-nav');

    if (!isIncidentModalOpen()) {
        lockHeaderVisibility(false);
    }

    if (mobileNavHideTimerId !== null) {
        window.clearTimeout(mobileNavHideTimerId);
    }

    if (shouldCloseImmediately) {
        mobileNavOverlay.hidden = true;
        mobileNavHideTimerId = null;

        if (shouldRestoreFocus) {
            restoreModalTriggerFocus(modalEntry, mobileNavToggleBtn);
        }
        mobileNavReturnFocus = null;
        return;
    }

    mobileNavHideTimerId = window.setTimeout(() => {
        mobileNavOverlay.hidden = true;
        mobileNavHideTimerId = null;
    }, MOBILE_NAV_TRANSITION_MS);

    if (shouldRestoreFocus) {
        restoreModalTriggerFocus(modalEntry, mobileNavToggleBtn);
    }
    mobileNavReturnFocus = null;
}

if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', () => {
        if (!isMobileNavigationViewport()) {
            closeMobileNavDrawer({ restoreFocus: false, immediate: true });
            return;
        }

        if (mobileNavOverlay && !mobileNavOverlay.hidden) {
            closeMobileNavDrawer();
            return;
        }

        openMobileNavDrawer();
    });
}

if (mobileNavCloseBtn) {
    mobileNavCloseBtn.addEventListener('click', () => {
        closeMobileNavDrawer();
    });
}

if (mobileNavOverlay) {
    mobileNavOverlay.addEventListener('click', (event) => {
        if (event.target === mobileNavOverlay) {
            closeMobileNavDrawer();
        }
    });
}

renderDesktopNavItems();
renderMobileNavItems();

setActiveSection(getStoredSectionName(), { persist: false });

// ============================================================
// INCIDENT ARCHIVE
// ============================================================

function createIncidentCardBackgroundDataUrl(incidentLabel, colors) {
        const svg = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice">
    <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="${colors[0]}"/>
            <stop offset="55%" stop-color="${colors[1]}"/>
            <stop offset="100%" stop-color="${colors[2]}"/>
        </linearGradient>
        <radialGradient id="halo" cx="70%" cy="30%" r="55%">
            <stop offset="0%" stop-color="rgba(0,240,255,0.38)"/>
            <stop offset="100%" stop-color="rgba(0,0,0,0)"/>
        </radialGradient>
    </defs>
    <rect width="1200" height="800" fill="url(#bg)"/>
    <rect width="1200" height="800" fill="url(#halo)"/>
    <g stroke="rgba(255,255,255,0.16)" stroke-width="1" fill="none">
        <path d="M-20 120 H1220"/>
        <path d="M-20 220 H1220"/>
        <path d="M-20 320 H1220"/>
        <path d="M-20 420 H1220"/>
        <path d="M-20 520 H1220"/>
        <path d="M-20 620 H1220"/>
        <path d="M120 0 V800"/>
        <path d="M300 0 V800"/>
        <path d="M480 0 V800"/>
        <path d="M660 0 V800"/>
        <path d="M840 0 V800"/>
        <path d="M1020 0 V800"/>
    </g>
    <g fill="rgba(255,255,255,0.2)">
        <circle cx="220" cy="170" r="54"/>
        <circle cx="920" cy="580" r="72"/>
        <circle cx="680" cy="240" r="34"/>
    </g>
    <text x="52" y="740" fill="rgba(255,255,255,0.38)" font-size="44" font-family="monospace">${incidentLabel}</text>
</svg>`;

        return `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;
}

const incidentStatusLabelMap = {
    '調査継続中': 'ACTIVE',
    '一部解明': 'PARTIAL',
    '研究継続中': 'ANALYZING',
    '未解明': 'UNKNOWN',
    '機密扱い': 'CLASSIFIED',
    '確認済み': 'CONFIRMED'
};

function getIncidentId(incident) {
    return incident?.id ?? null;
}

function getIncidentCaseName(incident) {
    return incident?.name ?? null;
}

function getIncidentEnglishName(incident) {
    return incident?.englishName ?? null;
}

function getIncidentCategory(incident) {
    return incident?.category ?? null;
}

function getIncidentClass(incident) {
    return incident?.class ?? null;
}

function getIncidentStatus(incident) {
    return incident?.status ?? null;
}

function getIncidentStatusDisplay(incident) {
    const status = getIncidentStatus(incident);
    if (status === null) {
        return '—';
    }

    if (incidentStatusLabelMap[status]) {
        return incidentStatusLabelMap[status];
    }

    return String(status).trim().toUpperCase() || 'UNKNOWN';
}

function getIncidentRiskLevel(incident) {
    return incident?.riskLevel ?? null;
}

function getIncidentRiskLevelDisplay(incident) {
    const riskLevel = getIncidentRiskLevel(incident);
    return riskLevel === null ? '—' : String(riskLevel);
}

function getIncidentTags(incident) {
    return Array.isArray(incident?.tags) ? incident.tags : [];
}

function formatIncidentDisplayId(incidentId) {
    const rawId = String(incidentId || '').trim();
    const match = rawId.match(/^FILE-(\d+)$/i);
    if (!match) {
        return rawId;
    }

    return `FILE ${match[1].padStart(4, '0')}`;
}

function getIncidentCaseCardImagePath(incident) {
    const caseCardImage = incident?.caseCardImage;
    if (!caseCardImage || typeof caseCardImage !== 'object' || Array.isArray(caseCardImage)) {
        return null;
    }

    if (typeof caseCardImage.path !== 'string') {
        return null;
    }

    const path = caseCardImage.path.trim();
    return path || null;
}

function getIncidentSearchText(incident) {
    return [
        getIncidentId(incident),
        getIncidentCaseName(incident),
        incident.region,
        incident.era,
        getIncidentCategory(incident),
        getIncidentStatus(incident),
        ...incident.facts,
        ...incident.theories,
        ...incident.legends
    ].join(' ').toLowerCase();
}

function applyIncidentCaseCardImage(card, incident) {
    if (!card) {
        return;
    }

    const imagePath = getIncidentCaseCardImagePath(incident);
    if (!imagePath) {
        return;
    }

    card.classList.add('has-case-card-image');
    card.style.setProperty('--incident-card-image', `url(${JSON.stringify(imagePath)})`);
}

const incidentList = document.getElementById('incidentList');
const incidentModalOverlay = document.getElementById('incidentModalOverlay');
const incidentModalPanel = incidentModalOverlay ? incidentModalOverlay.querySelector('.incident-modal') : null;
const incidentModalFile = document.getElementById('incidentModalFile');
const incidentModalStatus = document.getElementById('incidentModalStatus');
const incidentModalTitle = document.getElementById('incidentModalTitle');
const incidentModalEnglishTitle = document.getElementById('incidentModalEnglishTitle');
const incidentModalIntro = document.getElementById('incidentModalIntro');
const incidentModalRegion = document.getElementById('incidentModalRegion');
const incidentModalYear = document.getElementById('incidentModalYear');
const incidentModalStatusRecord = document.getElementById('incidentModalStatusRecord');
const incidentModalCategory = document.getElementById('incidentModalCategory');
const incidentModalClass = document.getElementById('incidentModalClass');
const incidentModalCategoryRow = document.getElementById('incidentModalCategoryRow');
const incidentModalClassRow = document.getElementById('incidentModalClassRow');
const incidentModalRisk = document.getElementById('incidentModalRisk');
const incidentModalRiskGauge = document.getElementById('incidentModalRiskGauge');
const incidentModalBodyCopy = document.getElementById('incidentModalBodyCopy');
const incidentCloseBtn = document.getElementById('incidentCloseBtn');
const incidentModalCornerCloseBtn = document.getElementById('incidentModalCornerCloseBtn');
const incidentViewOnMapBtn = document.getElementById('incidentViewOnMapBtn');
const incidentSearchInput = document.getElementById('incidentSearchInput');
const incidentCategoryFilter = document.getElementById('incidentCategoryFilter');
const incidentDangerFilter = document.getElementById('incidentDangerFilter');
const incidentResetBtn = document.getElementById('incidentResetBtn');
const incidentFilterSummary = document.getElementById('incidentFilterSummary');
const favoritesList = document.getElementById('favoritesList');
const favoritesSummary = document.getElementById('favoritesSummary');
const originWorldMap = document.getElementById('originWorldMap');
const originMapInfo = document.getElementById('originMapInfo');
const topFeaturedRecordsTrack = document.getElementById('topFeaturedRecordsTrack');
const INCIDENT_FILTER_STORAGE_KEY = 'ProjectORIGIN_incident_filters';
const FAVORITES_STORAGE_PREFIX = 'ProjectORIGIN_favorites_';
let activeTopFeaturedRecord = null;
let topFeaturedUpdateFrameId = null;

function createTopFeaturedRecord(incident) {
    const record = document.createElement('article');
    record.className = 'top-featured-record';

    const visual = document.createElement('div');
    visual.className = 'top-featured-record-visual';

    const imagePath = getIncidentCaseCardImagePath(incident);
    if (imagePath) {
        const image = document.createElement('img');
        image.className = 'top-featured-record-image';
        image.src = imagePath;
        image.alt = '';
        image.loading = 'lazy';
        image.decoding = 'async';
        visual.appendChild(image);
    } else {
        const placeholder = document.createElement('div');
        placeholder.className = 'top-featured-record-placeholder';
        placeholder.setAttribute('aria-hidden', 'true');
        placeholder.textContent = 'VISUAL RECORD PENDING';
        visual.appendChild(placeholder);
    }

    const copy = document.createElement('div');
    copy.className = 'top-featured-record-copy';

    const incidentId = document.createElement('p');
    incidentId.className = 'top-featured-record-id';
    incidentId.textContent = formatIncidentDisplayId(getIncidentId(incident));

    const title = document.createElement('h3');
    title.className = 'top-featured-record-title';
    title.textContent = getIncidentCaseName(incident);

    copy.appendChild(incidentId);
    copy.appendChild(title);
    record.appendChild(visual);
    record.appendChild(copy);
    return record;
}

function updateTopFeaturedRecord() {
    topFeaturedUpdateFrameId = null;
    if (!topFeaturedRecordsTrack) {
        return;
    }

    const trackBounds = topFeaturedRecordsTrack.getBoundingClientRect();
    if (trackBounds.width <= 0) {
        return;
    }

    const trackCenter = trackBounds.left + (trackBounds.width / 2);
    const records = Array.from(topFeaturedRecordsTrack.querySelectorAll('.top-featured-record'));
    let closestRecord = null;
    let closestDistance = Number.POSITIVE_INFINITY;

    records.forEach((record) => {
        const recordBounds = record.getBoundingClientRect();
        const recordCenter = recordBounds.left + (recordBounds.width / 2);
        const distanceFromCenter = Math.abs(trackCenter - recordCenter);

        if (distanceFromCenter < closestDistance) {
            closestRecord = record;
            closestDistance = distanceFromCenter;
        }
    });

    if (!closestRecord || closestRecord === activeTopFeaturedRecord) {
        return;
    }

    activeTopFeaturedRecord?.classList.remove('is-featured');
    closestRecord.classList.add('is-featured');
    activeTopFeaturedRecord = closestRecord;
}

function requestTopFeaturedRecordUpdate() {
    if (topFeaturedUpdateFrameId !== null) {
        return;
    }

    topFeaturedUpdateFrameId = requestAnimationFrame(updateTopFeaturedRecord);
}

function initializeTopFeaturedRecords() {
    if (!topFeaturedRecordsTrack || topFeaturedRecordsTrack.dataset.initialized) {
        return;
    }

    const fragment = document.createDocumentFragment();
    incidentData.slice(0, 5).forEach((incident) => {
        fragment.appendChild(createTopFeaturedRecord(incident));
    });

    topFeaturedRecordsTrack.replaceChildren(fragment);
    topFeaturedRecordsTrack.dataset.initialized = 'true';
    topFeaturedRecordsTrack.addEventListener('scroll', requestTopFeaturedRecordUpdate, { passive: true });
    window.addEventListener('resize', requestTopFeaturedRecordUpdate);
    requestTopFeaturedRecordUpdate();
}

let favoriteIncidentIds = new Set();
let activeOriginMapIncidentId = null;
let activeIncidentModalId = null;
let incidentModalReturnFocus = null;

const originMapMarkerPositions = {
    'FILE-001': { left: 22, top: 40 },
    'FILE-002': { left: 62, top: 24 },
    'FILE-003': { left: 30, top: 67 },
    'FILE-004': { left: 21, top: 42 },
    'FILE-005': { left: 22, top: 46 },
    'FILE-006': { left: 49, top: 33 },
    'FILE-007': { left: 48, top: 31 },
    'FILE-008': { left: 69, top: 23 },
    'FILE-009': { left: 53, top: 49 },
    'FILE-010': { left: 56, top: 44 },
    'FILE-011': { left: 40, top: 42 },
    'FILE-012': { left: 31, top: 43 }
};

// Preparation boundary only: flat-map positions are intentionally not projected
// onto the Top Earth until a formally approved projection rule exists.
function prepareTopEarthIncidentIds() {
    return Object.freeze(incidentData
        .map((incident) => getIncidentId(incident))
        .filter((incidentId) => Boolean(incidentId && originMapMarkerPositions[incidentId]))
    );
}

const incidentFilterState = {
    search: '',
    category: 'all',
    danger: 'all'
};

function getDefaultIncidentFilterState() {
    return {
        search: '',
        category: 'all',
        danger: 'all'
    };
}

function loadIncidentFilterState() {
    const defaults = getDefaultIncidentFilterState();
    const storedValue = localStorage.getItem(INCIDENT_FILTER_STORAGE_KEY);
    if (!storedValue) {
        return defaults;
    }

    try {
        const parsedValue = JSON.parse(storedValue);
        return {
            search: typeof parsedValue.search === 'string' ? parsedValue.search : defaults.search,
            category: typeof parsedValue.category === 'string' ? parsedValue.category : defaults.category,
            danger: typeof parsedValue.danger === 'string' ? parsedValue.danger : defaults.danger
        };
    } catch (error) {
        console.error('事件フィルター状態の読み込みに失敗しました', error);
        return defaults;
    }
}

function saveIncidentFilterState() {
    localStorage.setItem(INCIDENT_FILTER_STORAGE_KEY, JSON.stringify(incidentFilterState));
}

function syncIncidentFilterControls() {
    if (incidentSearchInput) {
        incidentSearchInput.value = incidentFilterState.search;
    }
    if (incidentCategoryFilter) {
        incidentCategoryFilter.value = incidentFilterState.category;
    }
    if (incidentDangerFilter) {
        incidentDangerFilter.value = incidentFilterState.danger;
    }
}

function populateIncidentCategoryOptions() {
    if (!incidentCategoryFilter) {
        return;
    }

    const categories = [...new Set(
        incidentData
            .map((incident) => getIncidentCategory(incident))
            .filter((category) => category !== null)
    )];
    const currentValue = incidentCategoryFilter.value || 'all';

    incidentCategoryFilter.innerHTML = categories.length > 0
        ? '<option value="all">ALL CATEGORIES</option>'
        : '<option value="all">CATEGORY — NOT ASSIGNED</option>';

    categories.forEach((category) => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        incidentCategoryFilter.appendChild(option);
    });

    const nextValue = categories.includes(incidentFilterState.category) ? incidentFilterState.category : 'all';
    incidentFilterState.category = nextValue === 'all' && currentValue !== 'all' && categories.includes(currentValue) ? currentValue : nextValue;
    incidentCategoryFilter.value = incidentFilterState.category;
    incidentCategoryFilter.disabled = categories.length === 0;
    incidentCategoryFilter.closest('.incident-filter-group')?.classList.toggle('is-filter-unavailable', categories.length === 0);
}

function updateIncidentRiskFilterAvailability() {
    if (!incidentDangerFilter) {
        return;
    }

    const hasFormalRiskLevel = incidentData.some((incident) => {
        const riskLevel = getIncidentRiskLevel(incident);
        return Number.isInteger(riskLevel) && riskLevel >= 1 && riskLevel <= 5;
    });
    incidentDangerFilter.innerHTML = hasFormalRiskLevel
        ? `
            <option value="all">ALL RISK LEVELS</option>
            <option value="1">1以上</option>
            <option value="2">2以上</option>
            <option value="3">3以上</option>
            <option value="4">4以上</option>
            <option value="5">5以上</option>
        `
        : '<option value="all">RISK — NOT ASSIGNED</option>';

    if (!hasFormalRiskLevel) {
        incidentFilterState.danger = 'all';
    }

    incidentDangerFilter.disabled = !hasFormalRiskLevel;
    incidentDangerFilter.closest('.incident-filter-group')?.classList.toggle('is-filter-unavailable', !hasFormalRiskLevel);
}

function getFilteredIncidents() {
    const searchText = incidentFilterState.search.trim().toLowerCase();
    const selectedCategory = incidentFilterState.category;
    const selectedDanger = incidentFilterState.danger;
    const minimumDanger = selectedDanger === 'all' ? null : Number(selectedDanger);

    return incidentData.filter((incident) => {
        const matchesCategory = selectedCategory === 'all' || getIncidentCategory(incident) === selectedCategory;
        const incidentRiskLevel = getIncidentRiskLevel(incident);
        const matchesDanger = minimumDanger === null
            || (incidentRiskLevel !== null && incidentRiskLevel >= minimumDanger);

        if (!matchesCategory || !matchesDanger) {
            return false;
        }

        if (!searchText) {
            return true;
        }

        return getIncidentSearchText(incident).includes(searchText);
    });
}

function updateIncidentFilterSummary(filteredIncidents) {
    if (!incidentFilterSummary) {
        return;
    }

    const activeFilters = [];
    if (incidentFilterState.search.trim()) {
        activeFilters.push(`検索: ${incidentFilterState.search.trim()}`);
    }
    if (incidentFilterState.category !== 'all') {
        activeFilters.push(`分類: ${incidentFilterState.category}`);
    }
    if (incidentFilterState.danger !== 'all') {
        activeFilters.push(`危険度: ${incidentFilterState.danger}以上`);
    }

    const baseSummary = `TOTAL CASES ${incidentData.length}  /  VISIBLE CASES ${filteredIncidents.length}  /  FAVORITES ${favoriteIncidentIds.size}`;
    incidentFilterSummary.textContent = activeFilters.length > 0
        ? `${baseSummary} | ${activeFilters.join(' / ')}`
        : baseSummary;
}

function renderIncidentEmptyState() {
    if (!incidentList) {
        return;
    }

    const emptyState = document.createElement('div');
    emptyState.className = 'incident-empty-state';
    emptyState.textContent = '条件に一致する事件ファイルは見つかりませんでした。';
    incidentList.appendChild(emptyState);
}

function getCurrentUsernameNormalized() {
    const username = localStorage.getItem('username');
    if (typeof username !== 'string') {
        return 'guest';
    }

    const normalizedUsername = username.trim().toLowerCase();
    return normalizedUsername || 'guest';
}

function getFavoritesStorageKey() {
    return `${FAVORITES_STORAGE_PREFIX}${getCurrentUsernameNormalized()}`;
}

function loadFavoriteIncidentIds() {
    const validIncidentIds = new Set(incidentData.map((incident) => getIncidentId(incident)));
    const storedValue = localStorage.getItem(getFavoritesStorageKey());

    if (!storedValue) {
        favoriteIncidentIds = new Set();
        return;
    }

    try {
        const parsedValue = JSON.parse(storedValue);
        if (!Array.isArray(parsedValue)) {
            favoriteIncidentIds = new Set();
            return;
        }

        favoriteIncidentIds = new Set(
            parsedValue.filter((id) => typeof id === 'string' && validIncidentIds.has(id))
        );
    } catch (error) {
        console.error('お気に入り状態の読み込みに失敗しました', error);
        favoriteIncidentIds = new Set();
    }
}

function saveFavoriteIncidentIds() {
    localStorage.setItem(getFavoritesStorageKey(), JSON.stringify([...favoriteIncidentIds]));
}

function isIncidentFavorite(incidentId) {
    return favoriteIncidentIds.has(incidentId);
}

function updateFavoriteButtonState(button, incidentName, active) {
    button.textContent = active ? '★' : '☆';
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
    button.setAttribute('aria-label', active
        ? `${incidentName}をお気に入りから解除`
        : `${incidentName}をお気に入りに登録`
    );
}

function refreshFavoriteUiAcrossSections() {
    renderIncidentCards();
    renderFavoriteCards();

    if (activeOriginMapIncidentId) {
        const activeIncident = getIncidentById(activeOriginMapIncidentId);
        if (activeIncident) {
            renderOriginMapInfoCard(activeIncident);
        }
    }
}

function toggleIncidentFavorite(incidentId) {
    if (isIncidentFavorite(incidentId)) {
        favoriteIncidentIds.delete(incidentId);
    } else {
        favoriteIncidentIds.add(incidentId);
    }

    saveFavoriteIncidentIds();
    refreshFavoriteUiAcrossSections();
}

function getIncidentById(incidentId) {
    return incidentData.find((incident) => getIncidentId(incident) === incidentId) || null;
}

function createOriginMapSvg() {
    if (!originWorldMap) {
        return;
    }

    const svgNamespace = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(svgNamespace, 'svg');
    svg.classList.add('origin-world-map-svg');
    svg.setAttribute('viewBox', '0 0 1000 520');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', '世界地図ベース');

    const continents = [
        'M66,140 L150,80 L286,86 L354,138 L338,214 L262,238 L188,206 L124,212 L78,182 Z',
        'M246,252 L296,268 L322,332 L306,444 L256,506 L208,474 L190,394 L214,318 Z',
        'M392,110 L468,88 L596,104 L702,96 L788,126 L826,188 L790,238 L714,250 L636,226 L584,240 L540,214 L478,222 L438,190 L404,160 Z',
        'M552,250 L610,262 L640,324 L624,384 L590,430 L550,420 L530,356 L536,304 Z',
        'M768,312 L818,296 L874,316 L906,358 L884,410 L834,434 L784,402 L754,356 Z',
        'M844,176 L878,160 L920,178 L934,208 L914,234 L878,230 L852,204 Z'
    ];

    continents.forEach((pathData) => {
        const path = document.createElementNS(svgNamespace, 'path');
        path.classList.add('origin-world-map-land');
        path.setAttribute('d', pathData);
        svg.appendChild(path);
    });

    originWorldMap.appendChild(svg);
}

function updateOriginMapMarkerActiveState() {
    if (!originWorldMap) {
        return;
    }

    const markers = originWorldMap.querySelectorAll('.origin-map-marker');
    markers.forEach((marker) => {
        const isActive = marker.getAttribute('data-id') === activeOriginMapIncidentId;
        marker.classList.toggle('active', isActive);
        marker.setAttribute('aria-pressed', String(isActive));
    });
}

function renderOriginMapInfoCard(incident) {
    if (!originMapInfo || !incident) {
        return;
    }

    originMapInfo.innerHTML = '';

    const card = createIncidentCard(incident, {
        enableCardModalOpen: true,
        cardClassName: 'origin-map-info-card',
        showDetailButton: false
    });
    originMapInfo.appendChild(card);
}

function handleOriginMapMarkerSelect(incidentId) {
    const incident = getIncidentById(incidentId);
    if (!incident) {
        return;
    }

    activeOriginMapIncidentId = incidentId;
    updateOriginMapMarkerActiveState();
    renderOriginMapInfoCard(incident);
}

function createOriginMapMarkers() {
    if (!originWorldMap) {
        return;
    }

    incidentData.forEach((incident) => {
        const incidentId = getIncidentId(incident);
        const incidentName = getIncidentCaseName(incident);
        const position = originMapMarkerPositions[incidentId];
        if (!position) {
            return;
        }

        const marker = document.createElement('button');
        marker.type = 'button';
        marker.className = 'origin-map-marker';
        marker.setAttribute('data-id', incidentId);
        marker.setAttribute('aria-label', `${incidentName}の地点`);
        marker.setAttribute('aria-controls', 'originMapInfo');
        marker.setAttribute('aria-pressed', 'false');
        marker.setAttribute('draggable', 'false');
        marker.style.left = `${position.left}%`;
        marker.style.top = `${position.top}%`;
        // Keep each marker pulse out of phase for a natural scanning feel.
        const pulseSeed = incidentId.split('').reduce((sum, char) => sum + char.charCodeAt(0), 0);
        marker.style.setProperty('--pulse-duration', `${3.6 + (pulseSeed % 7) * 0.2}s`);
        marker.style.setProperty('--pulse-delay', `${-(pulseSeed % 11) * 0.32}s`);

        marker.addEventListener('click', () => {
            handleOriginMapMarkerSelect(incidentId);
        });

        marker.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                handleOriginMapMarkerSelect(incidentId);
            }
        });

        originWorldMap.appendChild(marker);
    });
}

function initializeOriginMap() {
    if (!originWorldMap || !originMapInfo) {
        return;
    }

    if (!originWorldMap.dataset.initialized) {
        createOriginMapSvg();
        createOriginMapMarkers();
        originWorldMap.dataset.initialized = 'true';
    }

    if (!activeOriginMapIncidentId) {
        activeOriginMapIncidentId = getIncidentId(incidentData[0]);
    }

    handleOriginMapMarkerSelect(activeOriginMapIncidentId);
}

function handleIncidentCardActivate(incident) {
    openIncidentModal(incident);
}

function bindIncidentCardInteractions(card, incident, options = {}) {
    if (options.enableCardModalOpen === false) {
        return;
    }

    card.addEventListener('click', () => {
        handleIncidentCardActivate(incident);
    });

    card.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
            event.preventDefault();
            handleIncidentCardActivate(incident);
        }
    });

    card.addEventListener('mousedown', (event) => {
        const target = event.target;
        if (!(target instanceof Element)) {
            return;
        }

        if (target.closest('.incident-favorite-btn')) {
            return;
        }

        event.preventDefault();
    });
}

function createIncidentCard(incident, options = {}) {
    const settings = {
        enableCardModalOpen: true,
        showDetailButton: false,
        cardClassName: '',
        ...options
    };

    const incidentId = getIncidentId(incident);
    const incidentName = getIncidentCaseName(incident);
    const incidentEnglishName = getIncidentEnglishName(incident);
    const incidentCategory = getIncidentCategory(incident);
    const incidentClass = getIncidentClass(incident);
    const incidentRiskLevel = getIncidentRiskLevel(incident);
    const incidentTags = getIncidentTags(incident);

    const card = document.createElement('article');
    card.className = settings.cardClassName
        ? `incident-card ${settings.cardClassName}`
        : 'incident-card';
    card.setAttribute('data-id', incidentId);

    applyIncidentCaseCardImage(card, incident);

    if (settings.enableCardModalOpen) {
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.setAttribute('aria-label', `${incidentName}の詳細を表示`);
    }

    const imageRegion = document.createElement('div');
    imageRegion.className = 'incident-card-image';

    const imageDescription = document.createElement('span');
    imageDescription.className = 'incident-card-image-description';
    imageDescription.setAttribute('role', 'img');

    if (card.classList.contains('has-case-card-image')) {
        imageDescription.setAttribute('aria-label', `${incidentName}の事件画像`);
    } else {
        card.classList.add('has-case-card-placeholder');
        imageDescription.setAttribute('aria-label', `${incidentName}の画像は未設定です`);

        const placeholderLabel = document.createElement('span');
        placeholderLabel.className = 'incident-card-image-placeholder-label';
        placeholderLabel.textContent = 'VISUAL RECORD PENDING';
        imageRegion.appendChild(placeholderLabel);
    }

    imageRegion.appendChild(imageDescription);

    const cardContent = document.createElement('div');
    cardContent.className = 'incident-card-content';

    card.appendChild(imageRegion);
    card.appendChild(cardContent);

    const favoriteButton = document.createElement('button');
    favoriteButton.type = 'button';
    favoriteButton.className = 'incident-favorite-btn';
    updateFavoriteButtonState(favoriteButton, incidentName, isIncidentFavorite(incidentId));

    favoriteButton.addEventListener('click', (event) => {
        event.stopPropagation();
        toggleIncidentFavorite(incidentId);
    });

    imageRegion.appendChild(favoriteButton);

    const header = document.createElement('div');
    header.className = 'incident-card-header';

    const idElement = document.createElement('span');
    idElement.className = 'incident-id';
    idElement.textContent = formatIncidentDisplayId(incidentId);

    header.appendChild(idElement);
    const statusElement = document.createElement('span');
    statusElement.className = 'incident-status';
    statusElement.textContent = `STATUS ${getIncidentStatusDisplay(incident)}`;
    statusElement.classList.toggle('is-unset', getIncidentStatus(incident) === null);

    header.appendChild(statusElement);
    cardContent.appendChild(header);

    const title = document.createElement('h4');
    title.className = 'incident-name';
    title.textContent = incidentName;
    cardContent.appendChild(title);

    if (incidentEnglishName) {
        const englishTitle = document.createElement('p');
        englishTitle.className = 'incident-english-name';
        englishTitle.textContent = incidentEnglishName;
        cardContent.appendChild(englishTitle);
    }

    const classification = document.createElement('div');
    classification.className = 'incident-classification';

    const metaFields = [
        { label: 'CATEGORY', value: incidentCategory },
        { label: 'CLASS', value: incidentClass }
    ].filter((field) => field.value !== null);

    metaFields.forEach((field) => {
        const meta = document.createElement('div');
        meta.className = 'incident-meta';

        const label = document.createElement('span');
        label.className = 'incident-meta-label';
        label.textContent = field.label;

        const value = document.createElement('span');
        value.className = 'incident-meta-value';
        value.textContent = field.value;

        meta.appendChild(label);
        meta.appendChild(value);
        classification.appendChild(meta);
    });

    if (incidentTags.length > 0) {
        const tags = document.createElement('div');
        tags.className = 'incident-tags';
        tags.setAttribute('aria-label', 'Case tags');

        incidentTags.forEach((tag) => {
            const tagElement = document.createElement('span');
            tagElement.className = 'incident-tag';
            tagElement.textContent = tag;
            tags.appendChild(tagElement);
        });

        classification.appendChild(tags);
    }

    if (classification.childElementCount > 0) {
        cardContent.appendChild(classification);
    }

    const danger = document.createElement('div');
    danger.className = 'incident-danger';

    const dangerLabel = document.createElement('span');
    dangerLabel.className = 'incident-danger-label';
    dangerLabel.textContent = `RISK LEVEL : ${getIncidentRiskLevelDisplay(incident)}`;

    const gauge = document.createElement('div');
    gauge.className = 'danger-gauge';
    gauge.setAttribute('aria-label', `Risk level ${getIncidentRiskLevelDisplay(incident)}`);
    if (incidentRiskLevel !== null) {
        gauge.classList.add(`risk-level-${incidentRiskLevel}`);
    } else {
        gauge.classList.add('is-unset');
    }

    for (let index = 0; index < 5; index += 1) {
        const segment = document.createElement('span');
        segment.className = 'danger-gauge-segment';
        if (incidentRiskLevel !== null && index < incidentRiskLevel) {
            segment.classList.add('active');
        }
        gauge.appendChild(segment);
    }

    danger.appendChild(dangerLabel);
    danger.appendChild(gauge);
    cardContent.appendChild(danger);

    if (settings.showDetailButton) {
        const detailButton = document.createElement('button');
        detailButton.type = 'button';
        detailButton.className = 'origin-map-detail-btn';
        detailButton.textContent = '詳細を見る';
        detailButton.addEventListener('click', (event) => {
            event.stopPropagation();
            handleIncidentCardActivate(incident);
        });
        card.appendChild(detailButton);
    }

    bindIncidentCardInteractions(card, incident, settings);

    return card;
}

function renderIncidentCards() {
    if (!incidentList) {
        return;
    }

    incidentList.innerHTML = '';

    const filteredIncidents = getFilteredIncidents();
    updateIncidentFilterSummary(filteredIncidents);

    if (filteredIncidents.length === 0) {
        renderIncidentEmptyState();
        return;
    }

    const fragment = document.createDocumentFragment();

    filteredIncidents.forEach((incident) => {
        fragment.appendChild(createIncidentCard(incident, { cardClassName: 'incident-file-card' }));
    });

    incidentList.appendChild(fragment);
}

function renderFavoriteCards() {
    if (!favoritesList) {
        return;
    }

    favoritesList.innerHTML = '';

    const favoriteIncidents = incidentData.filter((incident) => favoriteIncidentIds.has(getIncidentId(incident)));
    if (favoritesSummary) {
        favoritesSummary.textContent = `SAVED CASES ${favoriteIncidents.length}  /  ARCHIVE TOTAL ${incidentData.length}`;
    }

    if (favoriteIncidents.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'incident-empty-state personal-collection-empty';

        const emptyLabel = document.createElement('p');
        emptyLabel.className = 'personal-collection-empty-label';
        emptyLabel.textContent = 'NO SAVED CASE RECORDS';

        const emptyTitle = document.createElement('h4');
        emptyTitle.textContent = '保存された事件ファイルはまだありません';

        const emptyDescription = document.createElement('p');
        emptyDescription.textContent = '事件ファイルで星印を選択すると、ここから同じCaseへ戻れます。';

        emptyState.appendChild(emptyLabel);
        emptyState.appendChild(emptyTitle);
        emptyState.appendChild(emptyDescription);
        favoritesList.appendChild(emptyState);
        return;
    }

    const fragment = document.createDocumentFragment();
    favoriteIncidents.forEach((incident) => {
        fragment.appendChild(createIncidentCard(incident));
    });

    favoritesList.appendChild(fragment);
}

function initializeFavoritesView() {
    renderFavoriteCards();
}

function resolveIncidentModalBackground(incident) {
    const modalBackground = incident?.modalBackground;
    const fallbackImage = createIncidentCardBackgroundDataUrl(
        modalBackground?.fallbackLabel || getIncidentId(incident) || 'UNRESOLVED',
        modalBackground?.fallbackColors || ['#081124', '#163043', '#050a14']
    );

    return {
        image: typeof modalBackground?.imagePath === 'string' && modalBackground.imagePath.trim().length > 0
            ? `url("${modalBackground.imagePath.trim()}")`
            : fallbackImage,
        desktopPosition: modalBackground?.desktopPosition || 'center center',
        mobilePosition: modalBackground?.mobilePosition || modalBackground?.desktopPosition || 'center center'
    };
}

function applyIncidentModalBackground(modalElement, incident) {
    if (!modalElement) {
        return;
    }

    const backgroundConfig = resolveIncidentModalBackground(incident);
    modalElement.style.setProperty('--incident-modal-bg-image', backgroundConfig.image);
    modalElement.style.setProperty('--incident-modal-bg-position-desktop', backgroundConfig.desktopPosition);
    modalElement.style.setProperty('--incident-modal-bg-position-mobile', backgroundConfig.mobilePosition);
}

function updateIncidentModalBackgroundFade(modalElement) {
    if (!modalElement) {
        return;
    }

    const maxScroll = modalElement.scrollHeight - modalElement.clientHeight;
    const progress = maxScroll > 0
        ? Math.min(Math.max(modalElement.scrollTop / maxScroll, 0), 1)
        : 0;
    const fade = Math.min(0.9, Math.pow(progress, 0.82) * 0.9);
    modalElement.style.setProperty('--incident-modal-scroll-fade', fade.toFixed(3));
}

function getIncidentOverview(incident) {
    return incident.facts[0] || incident.theories[0] || incident.legends[0] || '記録可能な概要情報はありません。';
}

function renderIncidentBodyCopy(container, incident) {
    if (!container) {
        return;
    }

    container.innerHTML = '';

    const sectionDefinitions = [
        {
            heading: 'FACTS',
            items: incident.facts.filter((text) => typeof text === 'string' && text.trim().length > 0)
        },
        {
            heading: 'THEORIES',
            items: [...incident.theories, ...incident.legends].filter((text) => typeof text === 'string' && text.trim().length > 0)
        },
        {
            heading: 'EVIDENCE',
            items: Array.isArray(incident.evidence)
                ? incident.evidence.filter((text) => typeof text === 'string' && text.trim().length > 0)
                : []
        },
        {
            heading: 'REFERENCES',
            items: Array.isArray(incident.references)
                ? incident.references.filter((text) => typeof text === 'string' && text.trim().length > 0)
                : []
        }
    ];

    const visibleSections = sectionDefinitions.filter((section) => section.items.length > 0);

    if (visibleSections.length === 0) {
        const emptyParagraph = document.createElement('p');
        emptyParagraph.className = 'incident-modal-body-paragraph';
        emptyParagraph.textContent = '詳細な本文記録は現在アーカイブされていません。';
        container.appendChild(emptyParagraph);
        return;
    }

    const fragment = document.createDocumentFragment();

    visibleSections.forEach((section) => {
        const block = document.createElement('section');
        block.className = `incident-modal-copy-section is-${section.heading.toLowerCase()}`;

        const heading = document.createElement('h5');
        heading.className = 'incident-modal-copy-heading';
        heading.textContent = section.heading;
        block.appendChild(heading);

        const body = document.createElement('div');
        body.className = 'incident-modal-copy-content';

        section.items.forEach((sectionText) => {
            const paragraph = document.createElement('p');
            paragraph.className = 'incident-modal-body-paragraph';
            paragraph.textContent = sectionText;
            body.appendChild(paragraph);
        });

        block.appendChild(body);
        fragment.appendChild(block);
    });

    container.appendChild(fragment);
}

function renderIncidentRiskGauge(container, dangerLevel) {
    if (!container) {
        return;
    }

    container.innerHTML = '';
    container.className = 'danger-gauge incident-modal-risk-gauge';
    if (dangerLevel !== null) {
        container.classList.add(`risk-level-${dangerLevel}`);
    } else {
        container.classList.add('is-unset');
    }

    const fragment = document.createDocumentFragment();
    for (let index = 0; index < 5; index += 1) {
        const segment = document.createElement('span');
        segment.className = 'danger-gauge-segment';
        if (dangerLevel !== null && index < dangerLevel) {
            segment.classList.add('active');
        }
        fragment.appendChild(segment);
    }

    container.appendChild(fragment);
}

function lockBackgroundScrollForModal() {
    document.body.classList.add('modal-open');
    lockBodyScroll('incident-modal');
}

function unlockBackgroundScrollForModal() {
    document.body.classList.remove('modal-open');
    unlockBodyScroll('incident-modal');
}

function openIncidentModal(incident) {
    if (!incidentModalOverlay || !incidentModalFile || !incidentModalTitle) {
        return;
    }

    closeMobileNavDrawer({ restoreFocus: false });

    applyIncidentModalBackground(incidentModalPanel || incidentModalOverlay, incident);
    incidentModalFile.textContent = formatIncidentDisplayId(getIncidentId(incident));
    if (incidentModalStatus) {
        incidentModalStatus.textContent = `STATUS ${getIncidentStatusDisplay(incident)}`;
        incidentModalStatus.classList.toggle('is-unset', getIncidentStatus(incident) === null);
    }
    incidentModalTitle.textContent = getIncidentCaseName(incident);
    if (incidentModalEnglishTitle) {
        const englishName = getIncidentEnglishName(incident);
        incidentModalEnglishTitle.textContent = englishName ?? '';
        incidentModalEnglishTitle.hidden = !englishName;
    }
    if (incidentModalIntro) {
        incidentModalIntro.textContent = getIncidentOverview(incident);
    }
    if (incidentModalRegion) {
        incidentModalRegion.textContent = incident.region;
    }
    if (incidentModalYear) {
        incidentModalYear.textContent = incident.era;
    }
    if (incidentModalStatusRecord) {
        incidentModalStatusRecord.textContent = getIncidentStatusDisplay(incident);
    }
    const incidentCategory = getIncidentCategory(incident);
    if (incidentModalCategory) {
        incidentModalCategory.textContent = incidentCategory ?? '';
    }
    if (incidentModalCategoryRow) {
        incidentModalCategoryRow.hidden = incidentCategory === null;
    }
    const incidentClass = getIncidentClass(incident);
    if (incidentModalClass) {
        incidentModalClass.textContent = incidentClass ?? '';
    }
    if (incidentModalClassRow) {
        incidentModalClassRow.hidden = incidentClass === null;
    }
    if (incidentModalRisk) {
        incidentModalRisk.textContent = getIncidentRiskLevelDisplay(incident);
    }
    renderIncidentRiskGauge(incidentModalRiskGauge, getIncidentRiskLevel(incident));
    renderIncidentBodyCopy(incidentModalBodyCopy, incident);
    activeIncidentModalId = getIncidentId(incident);
    incidentModalReturnFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    incidentModalOverlay.hidden = false;
    activateModal('incident-modal', incidentModalOverlay, incidentModalPanel, incidentModalReturnFocus);
    updateIncidentModalBackgroundFade(incidentModalPanel || incidentModalOverlay);
    lockBackgroundScrollForModal();
    lockHeaderVisibility(true);
    incidentModalCornerCloseBtn?.focus({ preventScroll: true });
}

function closeIncidentModal(options = {}) {
    if (!incidentModalOverlay) {
        return;
    }

    incidentModalOverlay.hidden = true;
    const modalEntry = deactivateModal('incident-modal');
    unlockBackgroundScrollForModal();
    lockHeaderVisibility(false);
    activeIncidentModalId = null;
    if (options.restoreFocus !== false) {
        restoreModalTriggerFocus(modalEntry, incidentModalReturnFocus);
    }
    incidentModalReturnFocus = null;
}

if (incidentCloseBtn) {
    incidentCloseBtn.addEventListener('click', closeIncidentModal);
}

if (incidentModalCornerCloseBtn) {
    incidentModalCornerCloseBtn.addEventListener('click', closeIncidentModal);
}

if (incidentViewOnMapBtn) {
    incidentViewOnMapBtn.addEventListener('click', () => {
        const incidentId = activeIncidentModalId;
        if (!incidentId || !getIncidentById(incidentId) || !originMapMarkerPositions[incidentId]) {
            return;
        }

        closeIncidentModal({ restoreFocus: false });
        navigateToSection('origin-map');
        handleOriginMapMarkerSelect(incidentId);
        document.querySelector(`.origin-map-marker[data-id="${incidentId}"]`)?.focus({ preventScroll: true });
    });
}

if (incidentModalOverlay) {
    incidentModalOverlay.addEventListener('click', (event) => {
        if (event.target === incidentModalOverlay) {
            closeIncidentModal();
        }
    });
}

if (incidentModalPanel) {
    incidentModalPanel.addEventListener('scroll', () => {
        updateIncidentModalBackgroundFade(incidentModalPanel);
    }, { passive: true });
}

document.addEventListener('focusin', redirectEscapedModalFocus);

document.addEventListener('keydown', (event) => {
    if (event.key === 'Tab' && getTopModalEntry()) {
        containFocusWithinTopModal(event);
        return;
    }

    if (event.key === 'Escape' && logoutConfirmOpen) {
        closeLogoutConfirmDialog();
        return;
    }

    if (event.key === 'Escape' && incidentModalOverlay && !incidentModalOverlay.hidden) {
        closeIncidentModal();
        return;
    }

    if (event.key === 'Escape' && mobileNavOverlay && !mobileNavOverlay.hidden) {
        closeMobileNavDrawer();
    }
});

function initializeIncidentArchive() {
    const incidentListNode = document.getElementById('incidentList');
    if (!incidentListNode) {
        return;
    }

    Object.assign(incidentFilterState, getDefaultIncidentFilterState(), loadIncidentFilterState());
    populateIncidentCategoryOptions();
    updateIncidentRiskFilterAvailability();
    syncIncidentFilterControls();
    renderIncidentCards();
}

initializeIncidentArchive();
initializeFavoritesView();
initializeOriginMap();
window.renderIncidentCards = renderIncidentCards;

if (incidentSearchInput) {
    incidentSearchInput.addEventListener('input', (event) => {
        incidentFilterState.search = event.target.value;
        saveIncidentFilterState();
        renderIncidentCards();
    });
}

if (incidentCategoryFilter) {
    incidentCategoryFilter.addEventListener('change', (event) => {
        incidentFilterState.category = event.target.value;
        saveIncidentFilterState();
        renderIncidentCards();
    });
}

if (incidentDangerFilter) {
    incidentDangerFilter.addEventListener('change', (event) => {
        incidentFilterState.danger = event.target.value;
        saveIncidentFilterState();
        renderIncidentCards();
    });
}

if (incidentResetBtn) {
    incidentResetBtn.addEventListener('click', () => {
        Object.assign(incidentFilterState, getDefaultIncidentFilterState());
        saveIncidentFilterState();
        syncIncidentFilterControls();
        renderIncidentCards();
    });
}

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
    addMessage(getOriginFoundationGreeting(username), 'ai');
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
    
    addMessage(getAiResponse(message), 'ai');
    chatInput.focus();
}

function scrollChatToBottom(animated = true) {
    if (!chatMessagesWrapper) {
        return;
    }

    const lastMessage = chatMessagesWrapper.lastElementChild;
    if (!lastMessage) {
        return;
    }

    if (animated) {
        lastMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        return;
    }

    lastMessage.scrollIntoView({ block: 'end' });
}

function getAiResponse(message) {
    const text = message.trim().toLowerCase();

    if (/^(こんにちは|おはよう|こんばんは)[！!。.]?$/.test(text)) {
        return 'ORIGIN案内機能です。現在はProjectORIGIN内の基本的な探索方法を案内できます。';
    }
    if (text.includes('projectorigin') || text.includes('使い方') || text.includes('何ができ')) {
        return 'ProjectORIGINでは、事件ファイルの一覧、場所から探すORIGIN MAP、時間から探すTimeline、保存したCaseへ戻るFavoritesを利用できます。現在のORIGINは、これら既存機能の基本案内に限定されています。';
    }
    if (text.includes('archive') || text.includes('事件ファイル') || text.includes('一覧')) {
        return '事件ファイルでは、登録済みCaseの検索と、利用可能な正式項目による絞り込みができます。Case Cardを選択するとDossierが開きます。';
    }
    if (text.includes('map') || text.includes('地図') || text.includes('場所')) {
        return 'ORIGIN MAPは、場所から事件を探索する画面です。地点を選ぶとCase Cardが表示され、そこからDossierを開けます。';
    }
    if (text.includes('timeline') || text.includes('タイムライン') || text.includes('時間') || text.includes('年代')) {
        return 'Timelineは時間から未知を探索するためのFoundationです。正式な年代記録が未整備のため、現在は検証待ち状態を表示しています。';
    }
    if (text.includes('favorite') || text.includes('お気に入り') || text.includes('保存')) {
        return 'Favoritesには、星印で保存したCaseだけが表示されます。保存状態は現在のユーザーごとにこのブラウザへ保持されます。';
    }

    return '現在、この質問には対応していません。ORIGINは現段階ではArchive、ORIGIN MAP、Timeline、Favoritesの基本案内のみ提供します。Case固有の調査回答、Source検索、推薦、分類、Risk判断には対応していません。';
}

function getOriginFoundationGreeting(username) {
    const displayName = typeof username === 'string' && username.trim() ? username.trim() : 'ゲスト';
    return `${displayName}さん、ORIGIN案内機能です。現在はArchive、ORIGIN MAP、Timeline、Favoritesの役割を案内できます。Case固有の調査回答やSource検索には対応していません。`;
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
    return messageDiv;
}

function addMessage(text, type, options = {}) {
    const messageType = type === 'user' ? 'user' : 'ai';
    // 現在時刻を「HH:mm」形式で取得
    const now = new Date();
    const time = now.toLocaleTimeString('ja-JP', { hour12: false, hour: '2-digit', minute: '2-digit' });
    
    chatHistory.push({ sender: messageType, text, time });
    saveChatHistory();

    const messageElement = createMessageElement(text, messageType, time);
    
    const shouldAnimate = options.animate !== false;
    if (shouldAnimate) {
        messageElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
        messageElement.scrollIntoView({ block: 'end' });
    }
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
        addMessage(getOriginFoundationGreeting(username), 'ai', { animate: false });
    }

    loadFavoriteIncidentIds();
    initializeIncidentArchive();
    initializeFavoritesView();
    initializeOriginMap();

    const savedSection = getStoredSectionName();
    setActiveSection(savedSection, { persist: false });
    if (savedSection === 'chat') {
        requestAnimationFrame(() => {
            scrollChatToBottom(false);
        });
    }
    
    chatInput.focus();
}

// ============================================================
// HEADER SCROLL BEHAVIOR
// ============================================================

function updateHeaderMetrics() {
    if (!dashboardHeader) {
        return;
    }

    const headerHeight = dashboardHeader.offsetHeight;

    document.documentElement.style.setProperty('--header-height', `${headerHeight}px`);
}

function setHeaderVisibility(visible, options = {}) {
    if (!dashboardHeader) {
        return;
    }

    const shouldPersist = options.persist !== false;

    if (isHeaderVisible !== visible) {
        isHeaderVisible = visible;
        dashboardHeader.classList.toggle('header-hidden', !visible);
        lastHeaderToggleScrollY = window.scrollY;

        if (shouldPersist) {
            persistHeaderVisibility(visible);
        }
    }

    clearHeaderBootState();
    updateHeaderMetrics();
}

function handleHeaderScroll() {
    scrollTicking = false;

    if (!dashboardHeader || loginContainer.style.display !== 'none') {
        return;
    }

    const currentScrollY = window.scrollY;
    const delta = currentScrollY - lastKnownScrollY;

    if (currentScrollY <= HEADER_TOP_REVEAL_THRESHOLD) {
        setHeaderVisibility(true);
        lastKnownScrollY = currentScrollY;
        lastHeaderToggleScrollY = currentScrollY;
        return;
    }

    if (Math.abs(delta) < 1) {
        lastKnownScrollY = currentScrollY;
        return;
    }

    const scrolledDistanceFromToggle = currentScrollY - lastHeaderToggleScrollY;

    if (delta > 0 && isHeaderVisible && scrolledDistanceFromToggle >= HEADER_SCROLL_TOGGLE_THRESHOLD) {
        setHeaderVisibility(false);
    } else if (delta < 0 && !isHeaderVisible && Math.abs(scrolledDistanceFromToggle) >= HEADER_SCROLL_TOGGLE_THRESHOLD) {
        setHeaderVisibility(true);
    }

    lastKnownScrollY = currentScrollY;
}

function requestHeaderScrollUpdate() {
    if (headerVisibilityLocked || scrollTicking) {
        return;
    }

    scrollTicking = true;
    requestAnimationFrame(handleHeaderScroll);
}

function resetHeaderScrollState(options = {}) {
    lastKnownScrollY = window.scrollY;
    lastHeaderToggleScrollY = window.scrollY;
    setHeaderVisibility(true, options);
}

function lockHeaderVisibility(lockVisible) {
    headerVisibilityLocked = lockVisible;
    if (lockVisible) {
        resetHeaderScrollState({ persist: false });
        return;
    }

    requestHeaderScrollUpdate();
}

function refreshHeaderLayout() {
    if (!dashboardHeader) {
        return;
    }

    clearHeaderBootState();

    updateHeaderMetrics();
    lastKnownScrollY = window.scrollY;
    lastHeaderToggleScrollY = window.scrollY;

    if (window.scrollY <= HEADER_TOP_REVEAL_THRESHOLD) {
        setHeaderVisibility(true);
        return;
    }

    dashboardHeader.classList.toggle('header-hidden', !isHeaderVisible);
}

window.addEventListener('scroll', requestHeaderScrollUpdate, { passive: true });
window.addEventListener('resize', () => {
    requestAnimationFrame(refreshHeaderLayout);

    if (!isMobileNavigationViewport()) {
        closeMobileNavDrawer({ restoreFocus: false, immediate: true });
    }
});

if (desktopSidebarMediaQuery.addEventListener) {
    desktopSidebarMediaQuery.addEventListener('change', refreshHeaderLayout);
}

// Update system time
function updateSystemTime() {
    const statusElement = document.getElementById('systemStatus');
    if (statusElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ja-JP', { hour12: false });
        statusElement.textContent = timeString;
    }
}

setInterval(updateSystemTime, 1000);
updateSystemTime();

// ============================================================
// INITIALIZATION
// ============================================================

window.addEventListener('load', () => {
    console.log('ProjectORIGIN AI OS - Initialized successfully');
    applyAuthView(hasPersistedLogin());
});
