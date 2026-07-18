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
const desktopLogoutBtn = document.getElementById('desktopLogoutBtn');
const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
const errorMessage = document.getElementById('errorMessage');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const dashboardHeader = document.querySelector('.dashboard-header');
const logoutConfirmOverlay = document.getElementById('logoutConfirmOverlay');
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

if (dashboardHeader && !isHeaderVisible) {
    dashboardHeader.classList.add('header-hidden');
}

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

function executeLogout() {
    closeMobileNavDrawer({ restoreFocus: false, immediate: true });
    dashboard.style.display = 'none';
    loginContainer.style.display = 'flex';
    loginForm.reset();
    errorMessage.style.display = 'none';
    localStorage.removeItem('username');
    favoriteIncidentIds = new Set();
    lockHeaderVisibility(true);
}

function openLogoutConfirmDialog() {
    if (!logoutConfirmOverlay || logoutConfirmOpen) {
        return;
    }

    logoutConfirmOpen = true;
    logoutConfirmOverlay.hidden = false;
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
    unlockBodyScroll('logout-confirm');

    if (shouldRestoreFocus) {
        if (!isMobileNavigationViewport() && desktopLogoutBtn) {
            desktopLogoutBtn.focus();
        }
        if (isMobileNavigationViewport() && mobileLogoutBtn) {
            mobileLogoutBtn.focus();
        }
    }
}

if (desktopLogoutBtn) {
    desktopLogoutBtn.addEventListener('click', () => {
        openLogoutConfirmDialog();
    });
}

if (mobileLogoutBtn) {
    mobileLogoutBtn.addEventListener('click', () => {
        openLogoutConfirmDialog();
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

let mobileNavItems = [];
let mobileNavHideTimerId = null;
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
    if (sectionName === 'timeline') {
        initializeTimelineSystemLog();
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
            mobileNavToggleBtn.focus();
        }
        return;
    }

    mobileNavHideTimerId = window.setTimeout(() => {
        mobileNavOverlay.hidden = true;
        mobileNavHideTimerId = null;
    }, MOBILE_NAV_TRANSITION_MS);

    if (shouldRestoreFocus) {
        mobileNavToggleBtn.focus();
    }
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

const incidentData = [
    {
        id: 'FILE-001',
        name: 'ロズウェル事件',
        region: 'アメリカ・ニューメキシコ州',
        era: '1947年',
        category: 'UFO・未確認飛行物体',
        danger: 3,
        status: '調査継続中',
        facts: [
            '1947年の夏、ニューメキシコ州で異常な金属片が回収された。',
            '目撃情報と地上の残留物が報告された。'
        ],
        theories: [
            '軍事機関が収集した物体の調査記録が存在する。',
            '高高度の航空機または試験機と見られる。'
        ],
        legends: [
            'UFOの墜落現場として都市伝説化した。',
            '政府が真相を秘匿していると語られる。'
        ]
    },
    {
        id: 'FILE-002',
        name: 'ディアトロフ峠事件',
        region: 'ロシア・ウラル山脈',
        era: '1959年',
        category: '未解決事件',
        danger: 4,
        status: '一部解明',
        facts: [
            'ソ連時代の山岳地帯で複数の目撃情報が残されている。',
            '地形と足跡の異常が記録された。'
        ],
        theories: [
            '地元の遭難者や軍事部隊の動きと関連がある。',
            '不明な生物または人為的な装置の存在が推定される。'
        ],
        legends: [
            '山中に「異常な生物」が潜むという噂がある。',
            '秘密の実験場との噂もある。'
        ]
    },
    {
        id: 'FILE-003',
        name: 'ナスカの地上絵',
        region: 'ペルー・ナスカ高原',
        era: '紀元前後〜西暦800年頃',
        category: '古代文明・遺跡',
        danger: 1,
        status: '研究継続中',
        facts: [
            '巨大な幾何学模様が高原に描かれている。',
            '空からしか全容が把握しにくい構造になっている。'
        ],
        theories: [
            '古代文明の祭祀・天文観測の記録と見なされる。',
            '地域共同体の儀式空間として利用された可能性がある。'
        ],
        legends: [
            '異星人のメッセージと解釈する説がある。',
            '神秘的な象徴として現代でも語り継がれている。'
        ]
    }
];

const incidentList = document.getElementById('incidentList');
const incidentModalOverlay = document.getElementById('incidentModalOverlay');
const incidentModalFile = document.getElementById('incidentModalFile');
const incidentModalTitle = document.getElementById('incidentModalTitle');
const incidentFactsList = document.getElementById('incidentFactsList');
const incidentTheoriesList = document.getElementById('incidentTheoriesList');
const incidentLegendsList = document.getElementById('incidentLegendsList');
const incidentCloseBtn = document.getElementById('incidentCloseBtn');
const incidentSearchInput = document.getElementById('incidentSearchInput');
const incidentCategoryFilter = document.getElementById('incidentCategoryFilter');
const incidentDangerFilter = document.getElementById('incidentDangerFilter');
const incidentResetBtn = document.getElementById('incidentResetBtn');
const incidentFilterSummary = document.getElementById('incidentFilterSummary');
const favoritesList = document.getElementById('favoritesList');
const favoritesSummary = document.getElementById('favoritesSummary');
const originWorldMap = document.getElementById('originWorldMap');
const originMapInfo = document.getElementById('originMapInfo');
const timelineLogList = document.getElementById('timelineLogList');
const INCIDENT_FILTER_STORAGE_KEY = 'ProjectORIGIN_incident_filters';
const FAVORITES_STORAGE_PREFIX = 'ProjectORIGIN_favorites_';

let favoriteIncidentIds = new Set();
let activeOriginMapIncidentId = null;

const originMapMarkerPositions = {
    'FILE-001': { left: 22, top: 40 },
    'FILE-002': { left: 62, top: 24 },
    'FILE-003': { left: 30, top: 67 }
};

const incidentFilterState = {
    search: '',
    category: 'all',
    danger: 'all'
};

const timelineLogData = [
    {
        code: 'SYS-BOOT',
        status: 'BOOT',
        title: 'ProjectORIGIN起動',
        message: 'グローバル監視ノード接続完了。未解明事件データベースの同期率100%。',
        source: 'Core Kernel',
        date: '2026.07.18',
        time: '00:01 UTC'
    },
    {
        code: 'CASE-ADD',
        status: 'INPUT',
        title: '事件追加',
        message: '新規ケースFILE-004を登録。北大西洋で観測された異常信号群をアーカイブ化。',
        source: 'Intake Gateway',
        date: '2026.07.18',
        time: '00:12 UTC'
    },
    {
        code: 'ANL-START',
        status: 'RUNNING',
        title: '解析開始',
        message: '衛星画像・音響記録・観測報告のマルチモーダル解析を開始。',
        source: 'Analysis Engine',
        date: '2026.07.18',
        time: '00:20 UTC'
    },
    {
        code: 'ANL-DONE',
        status: 'COMPLETED',
        title: '解析完了',
        message: '既存資料との照合を完了。複数の一致パターンを検出。',
        source: 'Analysis Engine',
        date: '2026.07.18',
        time: '00:46 UTC'
    },
    {
        code: 'SIG-DETECT',
        status: 'ALERT',
        title: '新しい情報検出',
        message: '類似波形を再検出。過去の未分類案件との相関を確認。',
        source: 'Signal Recon',
        date: '2026.07.18',
        time: '01:03 UTC'
    }
];

function createTimelineLogCard(log, index) {
    const item = document.createElement('article');
    item.className = index % 2 === 0 ? 'timeline-log-item is-left' : 'timeline-log-item is-right';

    const junction = document.createElement('div');
    junction.className = 'timeline-log-junction';

    const stamp = document.createElement('div');
    stamp.className = 'timeline-log-stamp';

    const date = document.createElement('p');
    date.className = 'timeline-log-date';
    date.textContent = log.date;

    const time = document.createElement('p');
    time.className = 'timeline-log-time';
    time.textContent = log.time;

    const node = document.createElement('span');
    node.className = 'timeline-log-node';
    node.setAttribute('aria-hidden', 'true');

    stamp.appendChild(date);
    stamp.appendChild(time);
    junction.appendChild(stamp);
    junction.appendChild(node);

    const card = document.createElement('article');
    card.className = 'incident-card timeline-log-card';

    const header = document.createElement('div');
    header.className = 'incident-card-header';

    const code = document.createElement('span');
    code.className = 'timeline-log-code';
    code.textContent = log.code;

    const status = document.createElement('span');
    status.className = 'timeline-log-status';
    status.textContent = log.status;

    const title = document.createElement('h4');
    title.className = 'timeline-log-title';
    title.textContent = log.title;

    header.appendChild(code);
    header.appendChild(status);
    header.appendChild(title);

    const message = document.createElement('p');
    message.className = 'timeline-log-message';
    message.textContent = log.message;

    const meta = document.createElement('div');
    meta.className = 'timeline-log-meta';

    const source = document.createElement('span');
    source.textContent = `SOURCE: ${log.source}`;

    const label = document.createElement('span');
    label.textContent = 'SYSTEM LOG';

    meta.appendChild(source);
    meta.appendChild(label);

    card.appendChild(header);
    card.appendChild(message);
    card.appendChild(meta);

    item.appendChild(junction);
    item.appendChild(card);

    return item;
}

function initializeTimelineSystemLog() {
    if (!timelineLogList) {
        return;
    }

    timelineLogList.innerHTML = '';
    const fragment = document.createDocumentFragment();

    timelineLogData.forEach((log, index) => {
        fragment.appendChild(createTimelineLogCard(log, index));
    });

    timelineLogList.appendChild(fragment);
}

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

    const categories = [...new Set(incidentData.map((incident) => incident.category))];
    const currentValue = incidentCategoryFilter.value || 'all';

    incidentCategoryFilter.innerHTML = '<option value="all">すべて</option>';

    categories.forEach((category) => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        incidentCategoryFilter.appendChild(option);
    });

    const nextValue = categories.includes(incidentFilterState.category) ? incidentFilterState.category : 'all';
    incidentFilterState.category = nextValue === 'all' && currentValue !== 'all' && categories.includes(currentValue) ? currentValue : nextValue;
    incidentCategoryFilter.value = incidentFilterState.category;
}

function getFilteredIncidents() {
    const searchText = incidentFilterState.search.trim().toLowerCase();
    const selectedCategory = incidentFilterState.category;
    const selectedDanger = incidentFilterState.danger;
    const minimumDanger = selectedDanger === 'all' ? null : Number(selectedDanger);

    return incidentData.filter((incident) => {
        const matchesCategory = selectedCategory === 'all' || incident.category === selectedCategory;
        const matchesDanger = minimumDanger === null || incident.danger >= minimumDanger;

        if (!matchesCategory || !matchesDanger) {
            return false;
        }

        if (!searchText) {
            return true;
        }

        const searchableText = [
            incident.id,
            incident.name,
            incident.region,
            incident.era,
            incident.category,
            incident.status,
            ...incident.facts,
            ...incident.theories,
            ...incident.legends
        ].join(' ').toLowerCase();

        return searchableText.includes(searchText);
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

    const baseSummary = `${filteredIncidents.length}件 / 全${incidentData.length}件を表示`;
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
    const validIncidentIds = new Set(incidentData.map((incident) => incident.id));
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
    return incidentData.find((incident) => incident.id === incidentId) || null;
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
        const position = originMapMarkerPositions[incident.id];
        if (!position) {
            return;
        }

        const marker = document.createElement('button');
        marker.type = 'button';
        marker.className = 'origin-map-marker';
        marker.setAttribute('data-id', incident.id);
        marker.setAttribute('aria-label', `${incident.name}の地点`);
        marker.setAttribute('draggable', 'false');
        marker.style.left = `${position.left}%`;
        marker.style.top = `${position.top}%`;

        marker.addEventListener('click', () => {
            handleOriginMapMarkerSelect(incident.id);
        });

        marker.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                handleOriginMapMarkerSelect(incident.id);
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
        activeOriginMapIncidentId = incidentData[0]?.id || null;
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

    const card = document.createElement('article');
    card.className = settings.cardClassName
        ? `incident-card ${settings.cardClassName}`
        : 'incident-card';
    card.setAttribute('data-id', incident.id);

    if (settings.enableCardModalOpen) {
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.setAttribute('aria-label', `${incident.name}の詳細を表示`);
    }

    const favoriteButton = document.createElement('button');
    favoriteButton.type = 'button';
    favoriteButton.className = 'incident-favorite-btn';
    updateFavoriteButtonState(favoriteButton, incident.name, isIncidentFavorite(incident.id));

    favoriteButton.addEventListener('click', (event) => {
        event.stopPropagation();
        toggleIncidentFavorite(incident.id);
    });

    card.appendChild(favoriteButton);

    const header = document.createElement('div');
    header.className = 'incident-card-header';

    const idElement = document.createElement('span');
    idElement.className = 'incident-id';
    idElement.textContent = incident.id;

    const statusElement = document.createElement('span');
    statusElement.className = 'incident-status';
    statusElement.textContent = incident.status;

    header.appendChild(idElement);
    header.appendChild(statusElement);
    card.appendChild(header);

    const title = document.createElement('h4');
    title.className = 'incident-name';
    title.textContent = incident.name;
    card.appendChild(title);

    const metaFields = [
        { label: '地域', value: incident.region },
        { label: '年代', value: incident.era },
        { label: '分類', value: incident.category }
    ];

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
        card.appendChild(meta);
    });

    const danger = document.createElement('div');
    danger.className = 'incident-danger';

    const dangerLabel = document.createElement('span');
    dangerLabel.className = 'incident-danger-label';
    dangerLabel.textContent = `危険度: ${incident.danger} / 5`;

    const gauge = document.createElement('div');
    gauge.className = 'danger-gauge';

    for (let index = 0; index < 5; index += 1) {
        const segment = document.createElement('span');
        segment.className = 'danger-gauge-segment';
        if (index < incident.danger) {
            segment.classList.add('active');
        }
        gauge.appendChild(segment);
    }

    danger.appendChild(dangerLabel);
    danger.appendChild(gauge);
    card.appendChild(danger);

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
        fragment.appendChild(createIncidentCard(incident));
    });

    incidentList.appendChild(fragment);
}

function renderFavoriteCards() {
    if (!favoritesList) {
        return;
    }

    favoritesList.innerHTML = '';

    const favoriteIncidents = incidentData.filter((incident) => favoriteIncidentIds.has(incident.id));
    if (favoritesSummary) {
        favoritesSummary.textContent = `${favoriteIncidents.length}件 / 全${incidentData.length}件の事件をお気に入り登録`;
    }

    if (favoriteIncidents.length === 0) {
        const emptyState = document.createElement('div');
        emptyState.className = 'incident-empty-state';
        emptyState.textContent = 'まだお気に入りは登録されていません';
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

function fillList(container, items) {
    container.innerHTML = '';
    const fragment = document.createDocumentFragment();

    items.forEach((item) => {
        const listItem = document.createElement('li');
        listItem.textContent = item;
        fragment.appendChild(listItem);
    });

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

    incidentModalFile.textContent = incident.id;
    incidentModalTitle.textContent = incident.name;
    fillList(incidentFactsList, incident.facts);
    fillList(incidentTheoriesList, incident.theories);
    fillList(incidentLegendsList, incident.legends);
    incidentModalOverlay.hidden = false;
    lockBackgroundScrollForModal();
    lockHeaderVisibility(true);
}

function closeIncidentModal() {
    if (!incidentModalOverlay) {
        return;
    }

    incidentModalOverlay.hidden = true;
    unlockBackgroundScrollForModal();
    lockHeaderVisibility(false);
}

if (incidentCloseBtn) {
    incidentCloseBtn.addEventListener('click', closeIncidentModal);
}

if (incidentModalOverlay) {
    incidentModalOverlay.addEventListener('click', (event) => {
        if (event.target === incidentModalOverlay) {
            closeIncidentModal();
        }
    });
}

document.addEventListener('keydown', (event) => {
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
    syncIncidentFilterControls();
    renderIncidentCards();
}

initializeIncidentArchive();
initializeFavoritesView();
initializeOriginMap();
initializeTimelineSystemLog();
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

function refreshIncidentArchiveIfNeeded() {
    const incidentSection = document.querySelector('.chat-section[data-section="incident-file"]');
    if (!incidentSection) {
        return;
    }

    if (incidentSection.classList.contains('active')) {
        initializeIncidentArchive();
    }
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
    
    // Smooth scroll to bottom
    typingDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    return typingDiv;
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
        addMessage(`こんにちは、${username}さん！ProjectORIGINへようこそ。本日はどのようなことでお役に立てますか？`, 'ai', { animate: false });
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
        refreshHeaderLayout();
    } else {
        loginContainer.style.display = 'flex';
        dashboard.style.display = 'none';
        resetHeaderScrollState();
    }
});
