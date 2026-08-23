const incidentData = [
    {
        id: 'FILE-001',
        name: 'ロズウェル事件',
        region: 'アメリカ・ニューメキシコ州',
        era: '1947年',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: {
            path: "images/case-cards/file-0001.webp"
        },
        modalBackground: {
            imagePath: './images/backgrounds/roswell.png',
            desktopPosition: 'center 18%',
            mobilePosition: '62% 16%',
            fallbackLabel: 'ROSWELL INCIDENT',
            fallbackColors: ['#08111e', '#1b3043', '#060a14']
        },
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
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
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
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
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
    },
    {
        id: 'FILE-004',
        name: 'Area 51',
        englishName: 'Area 51',
        region: 'アメリカ・ネバダ州',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-005',
        name: 'Phoenix Lights',
        englishName: 'Phoenix Lights',
        region: 'アメリカ・アリゾナ州',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-006',
        name: 'Rendlesham Forest Incident',
        englishName: 'Rendlesham Forest Incident',
        region: 'イギリス・サフォーク',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-007',
        name: 'Belgian UFO Wave',
        englishName: 'Belgian UFO Wave',
        region: 'ベルギー',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-008',
        name: 'Tunguska Event',
        englishName: 'Tunguska Event',
        region: 'ロシア・シベリア',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-009',
        name: 'Great Pyramid of Giza',
        englishName: 'Great Pyramid of Giza',
        region: 'エジプト・ギザ',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-010',
        name: 'Göbekli Tepe',
        englishName: 'Göbekli Tepe',
        region: 'トルコ・シャンルウルファ',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-011',
        name: 'Mary Celeste',
        englishName: 'Mary Celeste',
        region: '北大西洋',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    },
    {
        id: 'FILE-012',
        name: 'Bermuda Triangle',
        englishName: 'Bermuda Triangle',
        region: '北大西洋・バミューダ海域',
        era: 'TBD',
        category: null,
        class: null,
        riskLevel: null,
        status: null,
        tags: [],
        caseCardImage: null,
        facts: [],
        theories: [],
        legends: []
    }
];
