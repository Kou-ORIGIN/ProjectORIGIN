# Chapter 1
# Schema Overview
## Purpose
Database
Schemaは、ProjectORIGINで管理する事件データの正式な構造および個別データ仕様を定義する文書である。
本Schemaは、すべての事件データを一貫した形式で作成、保存、検証、移行および更新できる状態を維持することを目的とする。
事件ファイルが1000件以上へ増加した場合も、データごとの差異、構造の分岐、情報の重複および未設定値の不統一が発生しない構造を基準とする。
---
## Highest Standard
Database Rule
v3.0を、ProjectORIGINにおけるデータ管理およびデータベース設計の最上位原則として参照する。
Database Rule
v3.0は、ProjectORIGIN全体で共通して適用するデータ管理およびデータベース設計の基本原則を定義する。
個別データ仕様、データ構造、Validation、Migrationその他の具体的なSchema仕様は、Database
Rule v3.0の責務範囲ではない。
本Schemaは、Database Rule
v3.0に反しない範囲で、ProjectORIGINにおける個別データ仕様の正式基準として扱う。
本Schemaに定義する正式フィールド、ネスト構造、値型、必須・任意、許可値、Default
Value、Unset
Value、Constraints、ValidationおよびMigrationは、本Schemaの責務として管理する。
Database Rule
v3.0と本Schemaの間に不整合が確認された場合は、両文書の責務範囲を確認する。
データ管理およびデータベース設計の基本原則に関する不整合では、Database
Rule v3.0を正式基準とする。
個別データ仕様については、Database Rule
v3.0に反しない範囲で、本Schemaを正式基準とする。
---
## Scope
本Schemaは、ProjectORIGINで管理する事件データに適用する。
本Schemaが定義する対象は、以下のとおりとする。
- 正式フィールド
- ネスト構造
- 値型
- 必須・任意
- 許可値
- Default Value
- Unset Value
- Constraints
- データ間の関連付け
- データ品質
- Validation
- Migration
- Schema Version管理
- 長期運用基準
---
## Responsibilities
本Schemaは、以下を保証するための正式な個別データ仕様および構造定義を提供する。
- 正式フィールドの統一
- 一貫したネスト構造
- 責務分離
- 個別データ仕様のSingle Source of Truth
- 一括検証可能な構造
- 一括移行可能な構造
- 長期運用可能な構造
Database
Ruleが管理するデータ管理およびデータベース設計の基本原則を、本Schemaで重複定義または置換してはならない。
---
## Out of Scope
本Schemaでは以下を定義しない。
- ProjectORIGIN全体のデータ管理原則
- ProjectORIGIN全体のデータベース設計原則
- UI仕様
- CSS
- JavaScript
- API
- 実装方法
- データベース製品
- Git運用
- 画像制作
- 世界観
- アートディレクション
ProjectORIGIN全体のデータ管理およびデータベース設計の基本原則はDatabase
Ruleで管理する。
その他の対象外事項は、それぞれの正式文書または実装側の責務とする。
# Chapter 2
# Schema Design Principles
## Purpose
本Chapterは、Database Schema全体へ適用する設計原則を定義する。
---
## Principles
Schemaは以下の原則を維持しなければならない。
- Single Source of Truth
- 責務分離
- 表示データと事実データの分離
- 一貫した構造
- 明確な正式定義
- 長期運用性
- 拡張性
- 後方互換性
- 予測可能性
- Validation First
- Technology Independence
---
## Chapter Boundary
本Chapterでは、Database Schema全体へ適用する設計原則のみを定義する。
正式フィールド、値型、制約、未設定値および正式なネスト構造の詳細は、後続Chapterで定義する。
# Chapter 3

# Incident Data Root Structure

## Purpose

本Chapterは、事件データ内で正式化されているフィールドおよびネスト関係を定義する。

本Chapterは、事件データ全体の正式なRoot構造を定義するものではない。

---

## Field Nesting Structure

本Schemaで正式化されている事件データ内のフィールドおよびネスト関係は、以下のとおりとする。

```text
事件データ
├── englishName
├── riskLevel
└── caseCardImage
    └── path
```

- `englishName`は事件データ内の正式フィールドとする。
- `riskLevel`は事件データ内の正式フィールドとする。
- `caseCardImage`は事件データ内の正式フィールドとする。
- `path`は`caseCardImage`配下のみで管理する。

---

## Structure Example

以下は、事件データ内の正式フィールドおよびネスト関係を説明するための概念例である。

```yaml
incidentData:
  - fileNumber: "0001"
    caseName: "ロズウェル事件"
    englishName: "Roswell Incident"
    riskLevel: 4
    caseCardImage:
      path: "images/case-cards/file-0001.webp"

  - fileNumber: "0002"
    caseName: "Example Case"
    englishName: null
    riskLevel: null
    caseCardImage: null
```

`incidentData`は概念例における説明用の記述であり、正式なRoot構造または正式なRoot名称を定義するものではない。

また、本概念例は事件データ内の正式フィールドおよびネスト関係を説明することのみを目的とし、特定の実装言語、保存形式またはデータベース製品を指定するものではない。

---

## Structure Rules

- 本Chapterに記載する正式フィールドおよびネスト関係は、本Schemaの責務として管理する。
- `englishName`は事件データ内の正式フィールドとして管理する。
- `riskLevel`は事件データ内の正式フィールドとして管理する。
- `caseCardImage`は事件データ内の正式フィールドとして管理する。
- `path`は`caseCardImage`配下のみで管理する。
- `path`を事件データ直下へ重複して保持してはならない。
- `incidentData`を、本Chapterの概念例のみを根拠として正式なRoot構造または正式なRoot名称として扱ってはならない。
- 本Chapterに定義されていないRoot構造を推測によって追加してはならない。
- 新しい正式フィールドまたは新しい正式なネスト関係を推測によって追加してはならない。

---

## Chapter Boundary

本Chapterでは、事件データ内で正式化されているフィールドおよびネスト関係のみを定義する。

事件データ全体の正式なRoot構造または正式なRoot名称は、本Chapterでは定義しない。

各フィールドのData Type、Required / Optional、Allowed Value、Default Value、Unset ValueおよびConstraintsの詳細は、それぞれを所管するField Definitionで定義する。

# Chapter 4
# Core Identification Fields
## Purpose
本Chapterは、事件データを識別するための正式フィールドを定義する。
識別情報は、事件そのものを識別することのみを目的とし、分類、表示または実装方法を表してはならない。
---
## Official Identification Fields
事件データの識別情報として使用する正式フィールドは、以下とする。
- Internal Identifier
- File Number
- Case Name
- englishName
本Chapterでは、`englishName`の正式Schema定義を定義する。
---
## englishName
事件の正式英語名を保持する正式フィールドとする。
### Field Name
```text
englishName
```
### Purpose
事件の正式英語名を保持する。
### Data Type
```text
string | null
```
### Required / Optional
正式公開データでは必須とする。
調査中または移行中の事件データでは、一時的に`null`を許容する。
正式な事件データでは、`englishName`フィールド自体を保持する。
### Allowed Value
事件の正式英語名を表す文字列。
空文字は許可しない。
### Default Value
なし。
### Unset Value
```text
null
```
既存データでフィールドが未定義の場合は、未設定として扱う。
### Constraints
- 正式英語名のみを保持する。
- 値を設定する場合は文字列とする。
- 空文字を使用しない。
- 正式公開データでは`null`を使用しない。
- 調査中または移行中のみ一時的に`null`を許容する。
- 正式な事件データではフィールドを省略しない。
- 英語名以外の表示情報を保持しない。
# Chapter 5
# Core Incident Facts
## Purpose
本Chapterは、事件そのものを説明する基礎情報の正式構造を定義する。
---
## Official Fact Fields
Core Incident Factsとして管理する正式フィールドは、以下とする。
- Date
- Location
- Country
- Coordinates
- Short Summary
各正式フィールドは、事件の基本情報のみを保持する。
事件識別情報、分類情報および表示情報は、本Chapterの責務に含めない。
---
## Responsibility
各正式フィールドは、一つの責務のみを持つ。
同一情報を複数の正式フィールドへ重複保存してはならない。
表示情報を保持してはならない。
---
## Validation
Core Incident Factsは、以下を満たさなければならない。
- 正式フィールドへ保存されていること
- 各正式フィールドの責務が重複していないこと
- 同一情報が重複保存されていないこと
- Schema構造へ適合していること
---
## Chapter Boundary
本Chapterでは、事件の基本情報のみを定義する。
値型、必須・任意、許可値、未設定値および制約の詳細は、各正式フィールド定義またはField
Definition Standardで管理する。
# Chapter 6

# Classification and Controlled Values

## Purpose

本Chapterは、事件データを分類する正式フィールドおよび管理値を定義する。

分類情報は、事件そのものの事実とは独立した管理情報として扱う。

---

## Official Classification Fields

正式分類フィールドは、以下とする。

- Category
- Class
- Status
- Risk Level
- Tags

各正式Classification Fieldは、Field Definition Standardに従って定義する。

未確定の仕様は推測によって補完せず、対応するHOLDの解消条件に従って確定する。

---

## Category

### Field Name

`category`

### Purpose

事件または事例が属する最上位の主題・領域を表す正式な大分類値を保持する。

Categoryは、事件または事例が「何の領域に属するか」を分類するために使用する。

CategoryはClassとは独立したClassification Fieldとして扱う。

Categoryを、事件の中心となる現象タイプを表すために使用してはならない。

事件の中心となる現象タイプはClassの責務とする。

CategoryとClassを階層関係として扱ってはならない。

CategoryからClassを自動導出してはならない。

ClassからCategoryを自動導出してはならない。

Tagsその他のClassification Fieldの責務をCategoryで代替してはならない。

### Data Type

`string | null`

Category値が正式に設定されている場合は、`string`として保持する。

`null`はCategory Controlled Valueではなく、Category分類がまだ正式に設定されていない状態を表すUnset Valueとしてのみ使用する。

### Required / Optional

`category`フィールド自体は、正式な事件データでは必須とする。

各事件または事例は、同時に最大1つの正式Category値を保持する。

複数のCategory値を同時に保持してはならない。

調査中または移行中でCategory分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。

正式公開データでは`null`を許容しない。

正式公開データでは、正式なCategory Controlled Valueのいずれか1つを必ず保持する。

### Allowed Value

正式なCategory Controlled Valuesは以下の6値とする。

- `Extraterrestrial & UAP`
- `Spirit Phenomena`
- `Cryptid Phenomena`
- `Psi Phenomena`
- `Ancient & Archaeological`
- `Occult`

上記6値を初期Category Controlled Valuesとする。

Category Controlled Valuesは、正式なHuman Decisionを経ることによって将来拡張可能とする。

未承認のCategory値を正式Categoryとして使用してはならない。

AI、Database層、Application層その他の処理が、新しいCategory値を自動的に正式Controlled Valueへ追加してはならない。

`Other`、`Unknown`、`Miscellaneous`、`Unexplained`その他のFallback値を、未定義Categoryの代替として使用してはならない。

既存の正式Categoryに該当しない新しい主題領域が必要となった場合は、既存Categoryへ強制的に分類せず、新しいCategory候補として正式な判断を行う。

#### `Extraterrestrial & UAP`

UFO / UAP、未知の飛行・空中現象、地球外知的存在その他、それらに直接関連する事件または事例を包含する主題領域。

UFO / UAPであることのみを理由として、対象または現象が地球外起源であると解釈してはならない。

地球外起源その他の未確定の原因・起源・仮説を、Category値のみを根拠として事実として扱ってはならない。

#### `Spirit Phenomena`

幽霊、霊的存在、心霊現象、Hauntingその他、霊的存在または霊的現象そのものを中心主題とする事件または事例を包含する主題領域。

宗教、信仰、神話、伝承、オカルトまたは儀式一般を意味するCategoryとして使用してはならない。

#### `Cryptid Phenomena`

未確認生物、未知生物、およびProjectORIGINでCryptidとして正式に扱う伝説的・伝承的生物に直接関連する事件または事例を包含する主題領域。

Category値のみを根拠として、対象となる生物の実在を断定してはならない。

神話、宗教または伝承に登場する存在であることのみを理由として、自動的に`Cryptid Phenomena`へ分類してはならない。

#### `Psi Phenomena`

超感覚的知覚、テレパシー、透視、予知、念力その他、ProjectORIGINでPsi現象またはPsi能力として正式に扱う事件または事例を包含する主題領域。

Psi現象またはPsi能力を主題とすることと、事件の中心となる現象タイプを分類するClassの責務を混同してはならない。

#### `Ancient & Archaeological`

古代文明、失われた文明、考古学的対象、不可解な遺物・遺構その他、それらに直接関連する事件または事例を包含する主題領域。

単なる歴史上の未解決事件一般を、このCategoryへ含めてはならない。

地球外文明、超自然的作用その他の未確定の起源・原因・仮説を理由として、別のCategoryを自動導出してはならない。

#### `Occult`

オカルト、魔術、呪術、儀式その他、それらの実践または作用そのものが事件または事例の中心主題となるものを包含する主題領域。

宗教、信仰、神話、伝承または文化そのものをCategory対象としてはならない。

霊的存在または心霊現象そのものが中心主題である場合と、魔術、呪術または儀式そのものが中心主題である場合を区別する。

未確定の原因または因果関係を推測して`Occult`へ分類してはならない。

### Category Selection

各事件または事例について、正式Categoryは1つだけ選択する。

複数のCategory領域に関連する情報を含む場合でも、事件または事例の中心主題に基づいて最も適切な正式Categoryを1つ選択する。

複数領域に関連することのみを理由として、複数Categoryを保持してはならない。

Categoryは、確認された事件または事例の主題に基づいて決定する。

未確定の原因、起源、仮説、解釈または推測からCategoryを自動導出してはならない。

正式Categoryを一意に決定できない調査中または移行中のデータでは、推測によって既存Categoryへ強制分類せず、`null`を使用する。

正式公開前にCategory分類を確定し、正式なCategory Controlled Valueのいずれか1つを設定する。

### Default Value

なし。

`category`へDefault Valueを設定してはならない。

新規データ作成時その他の処理において、特定のCategory値または`null`を暗黙のDefault Valueとして自動設定してはならない。

Default Valueが存在しないことと、正式なUnset Valueが`null`であることを混同してはならない。

### Unset Value

`null`

`null`は、Category分類がまだ正式に設定されていない状態を表す。

`null`はCategory Controlled Valueではない。

調査中または移行中の事件データでは、Category分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。

正式公開データでは`null`を許容しない。

空文字をCategoryのUnset Valueとして使用してはならない。

`category`フィールド自体の欠落を、正式な未設定状態として使用してはならない。

### Constraints

- `category`はProjectORIGINの正式なClassification Fieldとして扱う。
- Categoryは、事件または事例が属する最上位の主題・領域を表す大分類として使用する。
- CategoryはClassとは独立したClassification Fieldとして扱う。
- CategoryとClassを階層関係として扱ってはならない。
- CategoryからClassを自動導出してはならない。
- ClassからCategoryを自動導出してはならない。
- Categoryを事件の中心となる現象タイプの分類に使用してはならない。
- Class、Status、Risk Level、Tagsその他の正式Classification Fieldの責務をCategoryで代替してはならない。
- Date、Location、Countryその他の専用Fieldの責務をCategoryで代替してはならない。
- `category`のData Typeは`string | null`とする。
- `category`フィールド自体は正式な事件データで保持する。
- Category値が設定されている場合は`string`として保持する。
- 各事件または事例は、同時に最大1つのCategory値のみを保持する。
- Categoryを配列として保持してはならない。
- 複数Categoryを同時に設定してはならない。
- 正式なCategory値として使用できるのは、本Field DefinitionのAllowed Valueに登録された値のみとする。
- 未登録Category値を正式Categoryとして使用してはならない。
- AI、Database層、Application層その他の処理が、未登録Category値を独自生成、補完または正式Controlled Valueへ自動追加してはならない。
- `Other`、`Unknown`、`Miscellaneous`、`Unexplained`その他のFallback値を、未定義Categoryの代替として使用してはならない。
- 既存Categoryに該当しない新しい主題領域を、意味の近い既存Categoryへ強制的に分類してはならない。
- 新しいCategory Controlled Valueは、正式なHuman Decisionを経た後にのみAllowed Valueへ追加できる。
- Categoryは事件または事例の中心主題に基づいて決定する。
- 未確定の原因、起源、因果関係、仮説または解釈からCategoryを自動導出してはならない。
- UFO / UAPであることのみを理由として地球外起源を断定してはならない。
- 神話、宗教または伝承に登場する存在であることのみを理由として`Cryptid Phenomena`へ自動分類してはならない。
- 宗教、信仰、神話、伝承または文化そのものを`Occult`へ分類してはならない。
- 古代または歴史的対象であることのみを理由として`Ancient & Archaeological`へ分類してはならない。
- 単なる歴史上の未解決事件一般を`Ancient & Archaeological`へ分類してはならない。
- 複数Category領域に関連する場合でも、正式Categoryは1つだけ選択する。
- 補助的な特徴を追加Categoryとして保持してはならない。
- Category分類が正式に設定されていない調査中または移行中のデータでは、推測によってCategoryを補完してはならない。
- 調査中または移行中でCategory分類がまだ正式に設定されていない場合に限り、`null`を一時的に許容する。
- 正式公開データでは`null`を許容してはならない。
- 正式公開データでは、正式なCategory Controlled Valueのいずれか1つを必ず保持する。
- `null`をCategory Controlled Valueとして扱ってはならない。
- 空文字をCategory値またはUnset Valueとして使用してはならない。
- `category`フィールド自体の欠落を正式なUnset状態として使用してはならない。
- `category`へDefault Valueを設定してはならない。
- `null`をDefault Valueとして扱ってはならない。

### Audit Status

`Field Name` ― PASS  
`Purpose` ― PASS  
`Data Type` ― PASS  
`Required / Optional` ― PASS  
`Allowed Value` ― PASS  
`Default Value` ― PASS  
`Unset Value` ― PASS  
`Constraints` ― PASS

**Field Definition Structure: PASS**

### Current Audit Result

Category Field Definitionについて、Human Decisionによる正式仕様の確定、Database Schema Chapter 6への反映、および最終再監査を完了した。

Category Repository Working Draftおよび旧Category HOLD Recordは回収されていない。

ただし、旧RecordのRecoveryとは独立して、現存する正式Source of Truth、Human Decision、現行Field Definitionへの正式反映、および最終再監査によって現行Category仕様を確定した。

旧Category Repository Working Draftまたは旧Category HOLD Recordの未回収状態を、現行Category Field Definitionの未解決依存関係として扱わない。

新規REVISION：0  
新規HOLD：0  
BLOCKER：0

**Overall Status: PASS**
---

## Class

### Field Name

`class`

### Purpose

事件を、その事件または現象の性質および中心となる現象タイプに基づいて分類するための正式な分類値を保持する。

ClassはCategoryとは独立したClassification Fieldとして扱う。

### Data Type

`string | null`

### Required / Optional

`class`フィールド自体は、正式な事件データでは必須とする。

Class値が設定されている場合は、単一の`string`として保持する。

調査中または移行中の事件データでは、Class分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。

正式公開データでは`null`を許容しない。

正式公開データでは、正式なClass Controlled Valuesのいずれかを必ず保持する。

### Allowed Value

`class`の正式なControlled Valuesは、以下の7値とする。

- `Encounter`
- `Disappearance`
- `Anomaly`
- `Discovery`
- `Transmission`
- `Transformation`
- `Disturbance`

各値の正式な意味は、以下とする。

#### `Encounter`

主体が対象、存在または現象と直接的に遭遇した事件を表す。

#### `Disappearance`

人、物または対象が所在不明または消失した事件を表す。

#### `Anomaly`

通常の状態、法則または既知パターンから外れる異常そのものが中心となる事件を表す。

#### `Discovery`

未知または未確認だった対象、痕跡、構造、事実その他の発見が中心となる事件を表す。

#### `Transmission`

信号、通信、メッセージ、放送、受信その他の伝送または通信現象が事件の中心となるものを表す。

#### `Transformation`

対象、状態または性質の変化そのものが事件の中心となるものを表す。

#### `Disturbance`

環境、機器、身体、空間その他への異常な干渉または攪乱が事件の中心となるものを表す。

Class Controlled ValuesのSingle Source of Truthは、本Field DefinitionのAllowed Valueとする。

Class Controlled Valuesを別の正式管理元へ重複定義してはならない。

CategoryとClassは独立したClassification Fieldとして扱う。

CategoryをClassの上位分類として扱ってはならない。

Categoryの値によって使用可能なClass Controlled Valueを制限してはならない。

Categoryの値からClass値を自動導出してはならない。

### Default Value

なし。

Class値を暗黙に補完してはならない。

### Unset Value

`null`

`null`は、Class分類自体がまだ正式に設定されていない状態を表す。

`null`をClassのControlled Valueとして扱ってはならない。

空文字、`"Unknown"`、`"Unclassified"`、`"N/A"`その他の疑似Class値を、正式なUnset Valueとして使用してはならない。

`Unknown`を正式なClass Controlled Valueとして使用してはならない。

`class`フィールド自体の欠落と、`class: null`は異なる状態として扱う。

調査中または移行中の事件データでは、Class分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。

正式公開データでは`null`を許容しない。

### Constraints

- `class`はProjectORIGINの正式なClassification Fieldとして扱う。
- `class`は、事件または現象の性質および中心となる現象タイプを表す。
- `class`フィールド自体は、正式な事件データで保持する。
- `class`は単一のClass値を保持する。
- `class`のData Typeは`string | null`とする。
- 非`null`値は`string`とする。
- 非`null`値は、正式な7つのControlled Valueのいずれかとする。
- `Encounter`、`Disappearance`、`Anomaly`、`Discovery`、`Transmission`、`Transformation`、`Disturbance`以外の値を正式なClass値として使用してはならない。
- Class Controlled ValuesのSingle Source of Truthは、本Field DefinitionのAllowed Valueとする。
- Class Controlled Valuesを複数の正式管理元へ重複定義してはならない。
- 複数のClass候補に該当し得る場合は、事件の中心となる現象タイプを1つだけ採用する。
- 複数のClass値を同時に保持してはならない。
- CategoryとClassは独立したClassification Fieldとして扱う。
- CategoryをClassの上位分類として扱ってはならない。
- ClassをCategoryの下位分類として扱ってはならない。
- Categoryの値によって使用可能なClass値を制限してはならない。
- CategoryからClass値を自動導出してはならない。
- ClassからCategory値を自動導出してはならない。
- Categoryとの組み合わせを理由として、新しいClass値を生成してはならない。
- `null`はClassのControlled Valueではなく、正式なUnset Valueとして扱う。
- `class`フィールド自体の欠落と`class: null`を同一の状態として扱ってはならない。
- `Unknown`を正式なClass Controlled Valueとして使用してはならない。
- 空文字、`"Unknown"`、`"Unclassified"`、`"N/A"`その他の疑似Class値を、正式なUnset Valueとして使用してはならない。
- 調査中または移行中の事件データでは、Class分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。
- 正式公開データでは`null`を使用してはならない。
- 正式公開データでは、正式な7つのControlled Valueのいずれかを必ず保持する。
- 正式に定義・承認されていないClass値を、新しい正式Class値として独自に生成してはならない。
- 正式に定義されていない自由入力値を、新しい正式Class値として使用してはならない。
- AI、Database層、Application層その他の処理が、正式に定義されていないClass値を正式値として生成または補完してはならない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名その他の表示上の差異を理由として、新しいClass値を独自に作成してはならない。
- `Category`、`Status`、`Risk Level`、`Tags`その他のClassification Fieldを、`class`の代替として使用してはならない。
- 他のClassification Fieldの値から、正式な分類判断を経ずにClass値を推測または自動補完してはならない。
- 事件本文その他の情報から、正式な分類判断を経ずにClass値を推測または自動補完してはならない。
- `riskLevel`その他のFieldに存在するControlled Valuesまたは分類規則を、正式な根拠なく`class`へ転用してはならない。
- `class`にDefault Valueを設定してはならない。

### Audit Status

`Field Name` ― PASS  
`Purpose` ― PASS  
`Data Type` ― PASS  
`Required / Optional` ― PASS  
`Allowed Value` ― PASS  
`Default Value` ― PASS  
`Unset Value` ― PASS  
`Constraints` ― PASS

**Field Definition Structure: PASS**

**HOLD-CLASS-01: RESOLVED**

`HOLD-CLASS-01`が担当していたClass Controlled Values、Controlled ValuesのSingle Source of Truth、およびCategoryとの依存関係について、Human Decisionによる正式確定、Class Field Definitionへの反映、および最終再監査を完了した。

Category自体に残る未解決事項は、`HOLD-CLASS-01`とは分離して継続管理する。

**Overall Status: PASS**

---

## Status

### Field Name

`status`

### Purpose

事件そのものの解決状態を表す正式な分類値を保持する。

`status`は、ProjectORIGINにおける制作工程のWorkflow Statusまたは公開状態を表すPublication Statusとして使用しない。

### Data Type

`string | null`

### Required / Optional

`status`フィールド自体は、正式な事件データでは必須とする。

調査中または移行中の事件データでは、Status分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。

正式公開データでは`null`を許容しない。

正式公開データでは、以下のいずれかのControlled Valueを必ず保持する。

- `Unresolved`
- `Partially Resolved`
- `Resolved`
- `Undetermined`

### Allowed Value

`status`の正式なControlled Valuesは、以下とする。

- `Unresolved`
- `Partially Resolved`
- `Resolved`
- `Undetermined`

各値は、事件そのものの解決状態のみを表す。

`Unresolved`は、事件の主要な問題が未解決である状態を表す。

`Partially Resolved`は、事件の一部が解決している一方で、主要な未解決事項が残っている状態を表す。

`Resolved`は、事件の主要な問題が解決している状態を表す。

`Undetermined`は、Status分類を実施した結果、現時点で確認できる正式情報から事件の解決状態を一意に確定できない状態を表す。

Workflow Status、Publication Statusその他の運用状態を表す値を、`status`のControlled Valueとして使用してはならない。

### Default Value

なし。

Status値を暗黙に補完してはならない。

### Unset Value

`null`

`null`は、Status分類自体がまだ正式に設定されていない状態を表す。

`null`をStatusのControlled Valueとして扱ってはならない。

`Undetermined`と`null`は異なる状態として扱う。

`Undetermined`は、Status分類を実施した結果、現時点で確認できる正式情報から事件の解決状態を一意に確定できない場合に使用する。

`null`は、Status分類自体がまだ正式に設定されていない場合に使用する。

### Constraints

- `status`はProjectORIGINの正式なClassification Fieldとして扱う。
- `status`フィールド自体は、正式な事件データで保持する。
- `status`は、事件そのものの解決状態のみを表す。
- `status`をWorkflow Statusとして使用してはならない。
- `status`をPublication Statusとして使用してはならない。
- `status`のData Typeは`string | null`とする。
- 非`null`値は`string`とする。
- 非`null`値は、正式なControlled Valuesのいずれかとする。
- `Unresolved`、`Partially Resolved`、`Resolved`、`Undetermined`以外の値を正式なStatus値として使用してはならない。
- Workflow Status、Publication Statusその他のStatus体系の値を`status`へ流用してはならない。
- 数値コードまたはbooleanを正式なStatus値として使用してはならない。
- `null`はStatusのControlled Valueではなく、正式なUnset Valueとして扱う。
- `null`と`Undetermined`を同一の状態として扱ってはならない。
- 調査中または移行中の事件データでは、Status分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。
- 正式公開データでは`null`を使用してはならない。
- 正式公開データでは、4つのControlled Valueのいずれかを必ず保持する。
- 正式な事件データでは`status`フィールド自体を省略してはならない。
- 正式に定義されていない自由入力値を、新しい正式Status値として使用してはならない。
- AI、Database層、Application層その他の処理が、正式に定義されていないStatus値を正式値として生成または補完してはならない。
- `Category`、`Class`、`Risk Level`、`Tags`その他のClassification Fieldを、`status`の代替として使用してはならない。
- 他のClassification Fieldの値または事件本文その他の情報から、正式な分類判断を経ずにStatus値を推測または自動補完してはならない。
- `status`にDefault Valueを設定してはならない。
- Status値を推測によって補完してはならない。

### Audit Status

`Field Name` ― PASS  
`Purpose` ― PASS  
`Data Type` ― PASS  
`Required / Optional` ― PASS  
`Allowed Value` ― PASS  
`Default Value` ― PASS  
`Unset Value` ― PASS  
`Constraints` ― PASS

**Field Definition Structure: PASS**

**HOLD-STATUS-01: RESOLVED**

`HOLD-STATUS-01`が担当していたStatusの分類責務、Data Type、Controlled Values、Unset Value、NullabilityおよびLifecycle条件は、正式確定、Field Definitionへの反映、および再監査を完了した。

**Overall Status: PASS**

---

## Risk Level

### Field Name

`riskLevel`

### Purpose

事件のRisk Level段階を保持する。

### Data Type

`integer | null`

### Required / Optional

正式公開データでは必須とする。

調査中または移行中の事件データでは、一時的に`null`を許容する。

正式な事件データでは、`riskLevel`フィールド自体を保持する。

### Allowed Value

以下の整数値のみを正式なRisk Level値として使用する。

- `1`
- `2`
- `3`
- `4`
- `5`

### Default Value

なし。

### Unset Value

`null`

`null`は、Risk Levelが設定されていない状態を表す正式なUnset Valueとする。

`null`をRisk LevelのControlled Valueとして扱ってはならない。

調査中または移行中の事件データでは、一時的に`null`を許容する。

正式公開データでは`null`を許容しない。

既存データで`riskLevel`フィールドが未定義の場合は、未設定として扱う。

### Constraints

- `riskLevel`は`integer | null`とする。
- Risk Levelの正式な値として整数値のみを保持する。
- Risk Levelの正式な値には`1`～`5`のみを使用する。
- `0`をRisk Level値として使用してはならない。
- `6`以上の整数をRisk Level値として使用してはならない。
- 小数をRisk Level値として使用してはならない。
- 文字列をRisk Level値として使用してはならない。
- 空文字をRisk Level値またはUnset Valueとして使用してはならない。
- `null`はRisk LevelのControlled Valueではなく、正式なUnset Valueとして扱う。
- 調査中または移行中の事件データでは、一時的に`null`を許容する。
- 正式公開データでは`null`を使用してはならない。
- 正式な事件データでは`riskLevel`フィールド自体を省略してはならない。
- Risk Levelの英語表示名を事件データへ保存してはならない。
- 表示色その他の表示専用情報を事件データへ保存してはならない。
- Risk Levelの英語表示名およびその他の共通表示情報は、ProjectORIGIN全体の共通表示定義から取得する。

### Audit Status

`Field Name` ― PASS  
`Purpose` ― PASS  
`Data Type` ― PASS  
`Required / Optional` ― PASS  
`Allowed Value` ― PASS  
`Default Value` ― PASS  
`Unset Value` ― PASS  
`Constraints` ― PASS

**Overall Status: PASS**

---

## Risk Level Display Separation

Risk Levelの英語表示名は、ProjectORIGIN全体の共通表示定義から取得する。

| `riskLevel` | English Display |
| ---: | --- |
| `1` | `LOW` |
| `2` | `MEDIUM` |
| `3` | `HIGH` |
| `4` | `VERY HIGH` |
| `5` | `EXTREME` |

事件データには`riskLevel`の整数値のみを保存する。

Risk Levelの英語表示名を、事件データへ重複保存してはならない。

表示色その他の表示専用情報についても、事件データへ重複保存してはならない。

---

## Tags

### Field Name

`tags`

### Purpose

事件または事例について、Category、Classその他の正式Classification Fieldだけでは表現しきれない特徴を補助的に分類するための正式なTag値を保持する。

Tagsは、検索、絞り込み、および事件横断の関連付けを補助するために使用する。

TagsをCategory、Class、Status、Risk Levelその他の正式Classification Fieldの代替として使用してはならない。

Date、Location、Countryその他の専用Fieldで管理する情報を、同じ意味のTagとして重複管理してはならない。

Tagsは自由入力Fieldとして扱わない。

### Data Type

`array<string>`

`tags`は、0個以上の正式なTag Controlled Valueを保持する配列とする。

各Tag値は`string`として保持する。

`null`を`tags`の正式な値として使用してはならない。

### Required / Optional

`tags`フィールド自体は、正式な事件データでは必須とする。

適用可能な正式Tagが存在する場合は、該当するTag Controlled Valueを配列として保持する。

適用可能な正式Tagが存在しない場合、または正式なTagを設定できない場合は、空配列`[]`を保持する。

`tags`フィールド自体の欠落を正式な未設定状態として使用してはならない。

### Allowed Value

正式な初期Tag Controlled Valuesは、以下の11値とする。

- `Photographic Record`
- `Video Record`
- `Audio Record`
- `Physical Trace`
- `Radar Detection`
- `Multiple Witnesses`
- `Military Involvement`
- `Government Involvement`
- `Scientific Investigation`
- `Missing Time`
- `Electronic Interference`

Tag Controlled ValuesのSingle Source of Truthは、本Field DefinitionのAllowed Valueとする。

上記11値を初期Tag Controlled Valuesとする。

Tag Controlled Valuesは、正式なHuman Decisionを経ることによって将来拡張可能とする。

未承認のTag値を正式Tagとして使用してはならない。

AI、Database層、Application層その他の処理が、新しいTag値を独自に生成、補完または正式Controlled Valueへ自動追加してはならない。

既存の正式Tagに該当しない特徴が必要となった場合は、意味の近い既存Tagへ強制的に分類せず、新しいTag候補として正式な判断を行う。

1事件だけにしか意味を持たない固有表現は、原則として正式Tag Controlled Valueへ追加しない。

新しいTag候補は、複数事件への適用可能性、検索・絞り込み・事件横断の関連付け上の必要性、既存Fieldおよび既存Tagとの責務重複の有無を確認した上で判断する。

#### `Photographic Record`

事件または事例に直接関連する写真記録が存在することを表す。

写真記録の存在について確認できない場合は適用しない。

本Tagの付与のみを根拠として、写真の真正性、信頼性、証拠能力、撮影対象の正体または事件に関する主張の真実性を認定してはならない。

#### `Video Record`

事件または事例に直接関連する映像記録が存在することを表す。

静止画記録のみが存在する場合は、本Tagを適用しない。

映像から静止画が生成または切り出されていることのみを理由として、`Photographic Record`を自動的に追加してはならない。

本Tagの付与のみを根拠として、映像の真正性、信頼性、証拠能力、撮影対象の正体または事件に関する主張の真実性を認定してはならない。

#### `Audio Record`

事件または事例に直接関連する音声記録が存在することを表す。

映像に音声トラックが存在することのみを理由として、独立した`Audio Record`を自動的に付与してはならない。

本Tagの付与のみを根拠として、音声の真正性、信頼性、証拠能力、記録対象の正体または事件に関する主張の真実性を認定してはならない。

#### `Physical Trace`

事件または事例に関連して、物理的な痕跡、変化、残留物その他の物理的対象が記録されていることを表す。

本Tagは、物理的特徴が記録されていることを分類するものであり、その原因または起源を認定するものではない。

本Tagの付与のみを根拠として、物理的痕跡の真正性、原因、因果関係または事件に関する主張の真実性を認定してはならない。

#### `Radar Detection`

事件または事例に関連する対象または現象について、レーダーによる検出記録が存在することを表す。

本Tagは、レーダー検出対象の正体、原因または起源を認定するものではない。

本Tagの付与のみを根拠として、検出記録の真正性、信頼性、証拠能力または事件に関する主張の真実性を認定してはならない。

#### `Multiple Witnesses`

同一の事件または事例について、複数のWitnessによる観察または経験の記録が存在することを表す。

本Tagは、複数のWitnessによる記録が存在することのみを表す。

複数のWitnessの証言または記録が相互に一致していること、互いに独立していること、信頼できること、または真実であることを意味しない。

#### `Military Involvement`

軍または軍事組織による、事件または事例への調査、対応、記録その他の実質的な組織的関与が確認されていることを表す。

軍人がWitnessまたは事件関係者として登場することのみを理由として、本Tagを適用してはならない。

本Tagの付与のみを根拠として、軍または軍事組織による事件原因、責任、秘密作戦、隠蔽その他の未確認事項を認定してはならない。

`Military Involvement`から`Government Involvement`を自動導出してはならない。

#### `Government Involvement`

政府機関または行政機関による、事件または事例への調査、対応、記録その他の実質的な組織的関与が確認されていることを表す。

政府または行政に属する人物がWitnessまたは事件関係者として登場することのみを理由として、本Tagを適用してはならない。

本Tagの付与のみを根拠として、政府機関または行政機関による事件原因、責任、隠蔽その他の未確認事項を認定してはならない。

`Government Involvement`から`Military Involvement`を自動導出してはならない。

`Military Involvement`と`Government Involvement`の両方を設定する場合は、それぞれの適用条件を独立して満たさなければならない。

#### `Scientific Investigation`

事件、対象または関連資料を対象として、科学的な調査、研究または分析が実施されたことを表す。

科学者、研究者その他の専門家が事件についてコメントしたことのみを理由として、本Tagを適用してはならない。

本Tagの付与は、科学的な調査、研究または分析が実施されたことを表すものであり、その結果が事件に関する主張を支持、証明または否定したことを意味しない。

#### `Missing Time`

事件当事者について、時間経過または記憶に関する欠落が、事件または事例の記録された特徴として報告されていることを表す。

本Tagは、時間そのものが物理的に消失したことを意味しない。

本Tagの付与のみを根拠として、時間または記憶の欠落の原因、起源または因果関係を認定してはならない。

`Missing Time`をClass `Disappearance`と同一の意味として扱ってはならない。

#### `Electronic Interference`

事件または事例に関連して、電気機器または電子機器への干渉、異常動作または機能障害が記録された特徴として存在することを表す。

本Tagは、電子的または電気的な干渉が事件の特徴として存在することを表す。

本TagをClass `Disturbance`と同一の意味として扱ってはならない。

本Tagの付与のみを根拠として、干渉、異常動作または機能障害の原因、起源または因果関係を認定してはならない。

### Default Value

なし。

`tags`へDefault Valueを設定してはならない。

新規データ作成時その他の処理において、特定のTag Controlled Valueまたは特定のTag集合を暗黙のDefault Valueとして自動設定してはならない。

Default Valueが存在しないことと、正式なUnset Valueが空配列`[]`であることを混同してはならない。

### Unset Value

`[]`

空配列`[]`は、適用可能な正式Tagが存在しない場合、または正式なTagを設定できない状態を表す。

`[]`はTag Controlled Valueではない。

`null`をTagsのUnset Valueとして使用してはならない。

空文字をTag値またはUnset Valueとして使用してはならない。

`tags`フィールド自体の欠落を正式なUnset状態として使用してはならない。

### Constraints

- `tags`はProjectORIGINの正式なClassification Fieldとして扱う。
- TagsはCategory、Classその他の正式Classification Fieldだけでは表現しきれない特徴を補助的に分類するために使用する。
- Tagsは検索、絞り込み、および事件横断の関連付けを補助するために使用する。
- Tagsを自由入力Fieldとして扱ってはならない。
- `tags`のData Typeは`array<string>`とする。
- `tags`フィールド自体は正式な事件データで保持する。
- `tags`の各要素は`string`とする。
- `tags`へ`null`を設定してはならない。
- 適用可能な正式Tagが存在しない場合、または正式なTagを設定できない場合は`[]`を使用する。
- `tags`フィールド自体の欠落を正式なUnset状態として使用してはならない。
- 正式Tagとして使用できるのは、本Field DefinitionのAllowed Valueに登録されたControlled Valueのみとする。
- Tag Controlled ValuesのSingle Source of Truthは、本Field DefinitionのAllowed Valueとする。
- 未承認のTag値を正式Tagとして使用してはならない。
- AI、Database層、Application層その他の処理が、未承認Tagを独自に生成、補完または正式Controlled Valueへ自動追加してはならない。
- 新しいTag Controlled Valueは、正式なHuman Decisionを経た後にのみAllowed Valueへ追加できる。
- 新しいTag候補は、既存Fieldおよび既存Tagとの責務重複を確認してから正式化する。
- 新しいTag候補は、原則として複数事件への適用可能性を持たなければならない。
- 1事件だけにしか意味を持たない固有表現を、原則として正式Tag Controlled Valueへ追加してはならない。
- Category、Class、Status、Risk Levelその他の正式Classification Fieldと同じ意味をTagとして重複管理してはならない。
- Date、Location、Countryその他の専用Fieldと同じ意味をTagとして重複管理してはならない。
- Category値からTagを自動導出してはならない。
- Class値からTagを自動導出してはならない。
- Status値からTagを自動導出してはならない。
- Risk Level値からTagを自動導出してはならない。
- Tag同士を階層関係として扱ってはならない。
- あるTagの存在のみを理由として別のTagを自動導出してはならない。
- 複数Tagを設定する場合は、それぞれのTagが独立して適用条件を満たさなければならない。
- `Military Involvement`から`Government Involvement`を自動導出してはならない。
- `Government Involvement`から`Military Involvement`を自動導出してはならない。
- `Video Record`から`Photographic Record`を自動導出してはならない。
- 同一のTag値を同一`tags`配列内へ重複して保持してはならない。
- Tagsは順序付き配列として保持する。
- 複数Tagを保持する場合は、事件または事例を最も代表するTagを先頭に配置する。
- 代表Tagは、事件または事例の中心的特徴との関連性に基づいて判断する。
- 代表Tagの判断をCategory、Class、Status、Risk Levelその他のFieldから機械的に自動導出してはならない。
- Tagが付与されていることのみを根拠として、記録、痕跡、検出情報その他の真正性、信頼性または証拠能力を認定してはならない。
- Tagが付与されていることのみを根拠として、事件または事例の原因、起源、因果関係または主張の真実性を認定してはならない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名その他の表示上の差異を理由として、新しい正式Tag値を独自に作成してはならない。
- 正式Allowed Valueに存在しない類義語または別表記を、正式Tagとして使用してはならない。
- `tags`へDefault Valueを設定してはならない。
- `[]`をDefault Valueとして扱ってはならない。
- `[]`は正式なUnset Valueとしてのみ扱う。

### Audit Status

`Field Name` ― PASS  
`Purpose` ― PASS  
`Data Type` ― PASS  
`Required / Optional` ― PASS  
`Allowed Value` ― PASS  
`Default Value` ― PASS  
`Unset Value` ― PASS  
`Constraints` ― PASS

**Field Definition Structure: PASS**

### Current Audit Result

Tags Field Definitionについて、Human Decisionによる具体的な初期Tag Controlled Valuesの正式確定、Database Schema Chapter 6への反映、および最終再監査を完了した。

正式な初期Tag Controlled Valuesは、以下の11値とする。

- `Photographic Record`
- `Video Record`
- `Audio Record`
- `Physical Trace`
- `Radar Detection`
- `Multiple Witnesses`
- `Military Involvement`
- `Government Involvement`
- `Scientific Investigation`
- `Missing Time`
- `Electronic Interference`

Tag Controlled ValuesのSingle Source of Truthは、本Field DefinitionのAllowed Valueとする。

初期Tag Controlled Valuesについて、Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldとの責務重複がないことを確認した。

「有効なTag」の判定条件、代表タグ判定、重複Tag禁止、Default Value、Unset Value、および既存Constraintsとの整合性を確認した。

未承認Tagの使用、自動生成、自動補完および正式Controlled Valueへの自動追加は禁止を維持する。

将来、新しいTag Controlled Valueが必要となった場合は、既存Fieldおよび既存Tagとの責務重複、複数事件への適用可能性、および検索・絞り込み・事件横断の関連付け上の必要性を確認し、正式なHuman Decisionを経た後にAllowed Valueへ追加する。

`HOLD-TAGS-01`が対象としていた具体的な正式Tag Controlled Values一覧について、未確認事項は残っていない。

新規REVISION：0  
新規HOLD：0  
BLOCKER：0

**Overall Status: PASS**

---

## Chapter Audit Status

`Purpose` ― PASS  
`Official Classification Fields` ― PASS  
`Category` ― PASS  
`Class` ― PASS  
`Status` ― PASS  
`Risk Level` ― PASS  
`Risk Level Display Separation` ― PASS  
`Tags` ― PASS  
`Chapter Boundary` ― PASS

**Chapter Structure: PASS**

**Chapter Overall Status: PASS**

### Open HOLD

なし。

### RESOLVED HOLD

- `HOLD-TAGS-01`
- `HOLD-STATUS-01`
- `HOLD-CLASS-02`
- `HOLD-CLASS-01`

### Historical Recovery

Category Repository Working Draftおよび旧Category HOLD Recordは回収されていない。

Category関連のHistorical Record Recoveryは、旧Recordを推測復元せず未回収状態を保持した上でCLOSEDとして扱う。

旧Category Repository Working Draftまたは旧Category HOLD Recordの未回収状態は、現行Category Field Definitionの未解決依存関係として扱わない。

現行Category Field Definitionは、現存する正式Source of Truthの確認、Human Decision、Database Schema Chapter 6への正式反映、および最終再監査によってPASSしている。

### Current Audit Result

Category ― PASS  
Class ― PASS  
Status ― PASS  
Risk Level ― PASS  
Tags ― PASS

Tags Field Definitionについて、具体的な初期Tag Controlled ValuesのHuman Decision、Database Schema Chapter 6への正式反映、および最終再監査を完了した。

正式な初期Tag Controlled Valuesは、以下の11値とする。

- `Photographic Record`
- `Video Record`
- `Audio Record`
- `Physical Trace`
- `Radar Detection`
- `Multiple Witnesses`
- `Military Involvement`
- `Government Involvement`
- `Scientific Investigation`
- `Missing Time`
- `Electronic Interference`

`HOLD-TAGS-01`が対象としていた具体的な正式Tag Controlled Values一覧について、未解決事項は残っていない。

新規REVISION：0  
新規HOLD：0  
BLOCKER：0

Chapter 6全体について、現時点で未解決HOLDは存在しない。

**Chapter 6 Overall Status: PASS**

# Chapter 7
# Content and Media References
## Purpose
本Chapterは、事件データと関連コンテンツおよびメディアデータとの正式な参照構造を定義する。
事件データは、コンテンツやメディアそのものを保持するのではなく、正式な参照情報のみを管理する。
本Chapterでは、既存の参照責務を維持したまま、`caseCardImage`および`caseCardImage.path`の正式Schema定義を追加する。
---
## Official Reference Fields
Content and Media Referencesとして管理する正式な参照対象は、以下とする。
- FREE Content Reference
- CLASSIFIED Content Reference
- Research Reference
- Master Case File Reference
- Case Card Image Reference
各参照は、それぞれ独立した責務を持つ。
事件データへ本文や画像データ本体を重複保存してはならない。
---
## FREE Content Reference
FREE版Case Fileとの正式な参照関係を管理する。
FREE版本文そのものを事件データへ保持してはならない。
---
## CLASSIFIED Content Reference
将来のCLASSIFIED ACCESSとの正式な参照関係を管理する。
CLASSIFIED本文そのものを事件データへ保持してはならない。
---
## Research Reference
Researchデータとの正式な参照関係を管理する。
Research本文そのものを事件データへ保持してはならない。
---
## Master Case File Reference
Master Case Fileとの正式な参照関係を管理する。
Master Case File本文そのものを事件データへ保持してはならない。
---
## Case Card Image Reference
Case Card Imageは各事件データ内で直接管理する。
Case Card ImageをCase Fileとは別の対応表のみで管理する構造は採用しない。
---
## caseCardImage
Case Card
Imageの設定状態および画像参照情報を保持する正式フィールドとする。
### Field Name
```text
caseCardImage
```
### Purpose
Case Card Imageの参照情報を保持する。
### Data Type
```text
object | null
```
### Required / Optional
正式な事件データでは必須とする。
設定済み・未設定を問わず、`caseCardImage`フィールド自体は保持する。
### Allowed Value
設定済みの場合は、以下の構造とする。
```text
caseCardImage
└── path: string
```
未設定の場合は、以下とする。
```text
caseCardImage: null
```
### Default Value
なし。
### Unset Value
```text
null
```
### Constraints
- 設定済みの場合はオブジェクトとする。
- 未設定の場合は`null`とする。
- 空文字を使用しない。
- 空オブジェクトを使用しない。
- `path`を持たないオブジェクトを使用しない。
- 画像データ本体を保持しない。
- 各事件データ内で直接管理する。
---
## caseCardImage.path
Case Card
Imageとして使用する画像リソースへの参照を保持する正式プロパティとする。
### Field Name
```text
caseCardImage.path
```
### Purpose
Case Card Imageとして使用する画像リソースへの参照を保持する。
### Data Type
```text
string
```
### Required / Optional
`caseCardImage`がオブジェクトの場合は必須とする。
`caseCardImage`が`null`の場合は保持しない。
### Allowed Value
Case Card
Imageとして使用する画像リソースを参照する空文字ではない文字列。
### Default Value
なし。
### Unset Value
単独のUnset Valueは定義しない。
Case Card
Imageが未設定の場合は、親フィールドである`caseCardImage`全体を`null`とする。
### Constraints
- 文字列のみ保持する。
- 空文字を使用しない。
- `caseCardImage`配下でのみ管理する。
- `path`が存在しないオブジェクトを正式データとして使用しない。
- 画像品質や表示情報を保持しない。
---
## Formal Nested Structure
```text
incident object
└── caseCardImage
└── path: string
```
---
## Chapter Boundary
本Chapterでは、正式な参照構造および`caseCardImage`のSchema定義のみを扱う。
UI、CSS、JavaScript、API、画像品質、表示方法および実装方法は、本Chapterの責務に含めない。
# Chapter 8
# Relationships Between Data
## Purpose
本Chapterは、事件データと他の正式データとの関連付け方法を定義する。
関連付けは、正式データ間の対応関係のみを管理し、同一情報を重複保存することを目的としない。
---
## Official Relationship Targets
正式な関連付け対象は、以下とする。
- Related Cases
- Research Data
- Master Case File
- Content References
- Media References
---
## Responsibility
関連付けは、正式データ同士の関係のみを管理する。
関連先の本文または画像データ本体を事件データへ保持してはならない。
---
## Referential Integrity
すべての関連付けは、正式データを対象としなければならない。
存在しない対象または正式管理されていない対象を参照してはならない。
---
## Validation
関連付けは、以下を満たさなければならない。
- 正式な関連対象を参照していること
- 正式構造へ適合していること
- 関連付けの責務が重複していないこと
- 整合性が維持されていること
---
## Chapter Boundary
本Chapterでは、正式データ間の関連付けのみを定義する。
個別フィールド、値型、許可値および実装方法は、本Chapterの責務に含めない。
# Chapter 9
# Field Definition Standard
## Purpose
本Chapterは、すべての正式フィールドで共通して使用する定義フォーマットを定義する。
---
## Standard Definition Format
すべての正式フィールドは、以下の定義項目を使用する。
- Field Name
- Purpose
- Data Type
- Required / Optional
- Allowed Value
- Default Value
- Unset Value
- Constraints
すべての正式フィールドは、この共通フォーマットに従って定義しなければならない。
---
## Common Rules
各正式フィールドは、以下を満たさなければならない。
- 一つの責務のみを持つこと
- 一つの正式名称のみを持つこと
- 正式な値型を持つこと
- 必須・任意を明確にすること
- 許可値を定義すること
- Default Valueの有無を明確にすること
- Unset Valueを一意に定義すること
- 制約を明確にすること
---
## Validation
正式フィールド定義は、以下を満たさなければならない。
- 必要な定義項目がすべて存在すること
- 責務が重複していないこと
- 共通フォーマットが維持されていること
- 各正式フィールド定義と本Chapterの定義フォーマットが一致していること
---
## Chapter Boundary
本Chapterでは、正式フィールドの定義方法のみを定義する。
個別フィールドの内容、許可値、Default Value、Unset
Valueおよび制約の具体的な値は、それぞれの正式フィールド定義で管理する。
# Chapter 10
# Nullability and Unset Values
## Purpose
本Chapterは、正式フィールドにおける未設定値およびNullabilityの共通基準を定義する。
未設定値の表現を統一することにより、事件データの一貫性、検証性および長期運用性を維持することを目的とする。
本Chapterは、未設定状態の表現方法を定義するものであり、個別フィールドの採用値を決定するものではない。
---
## Scope
本Chapterは、本Schemaで定義されるすべての正式フィールドへ適用する。
正式フィールド、ネストフィールドおよび参照フィールドを区別せず、共通基準として適用する。
---
## Nullability
各正式フィールドは、値を必須とするか、未設定を許可するかを明確に定義しなければならない。
Nullabilityは、各正式フィールドの責務に基づいて決定する。
同一の正式フィールドについて、状況によってNullabilityを変更してはならない。
---
## Unset Value
未設定状態を許可する正式フィールドは、正式なUnset
Valueを一つ定義しなければならない。
同一フィールドに対して複数の未設定表現を認めない。
Unset Valueは、各正式フィールドごとに一意でなければならない。
---
## Default Value and Unset Value
Default ValueとUnset Valueは異なる責務を持つ。
Default Valueは初期値として設定される値である。
Unset Valueは正式な値が存在しない状態を表現する値である。
両者を同一の意味として扱ってはならない。
---
## Selection Principle
Unset
Valueは、正式フィールドの責務および保持する情報の性質に基づいて決定する。
運用上の都合のみを理由として未設定値を選択してはならない。
---
## Consistency
同一の正式フィールドは、すべての事件データで同一のUnset
Valueを使用しなければならない。
事件ごとに異なる未設定表現を採用してはならない。
Schema全体で未設定状態の表現を統一しなければならない。
---
## Validation
未設定値は以下を満たさなければならない。
- 正式なUnset Valueが定義されていること
- 一意であること
- Default Valueと区別されていること
- Schema全体で一貫していること
---
## Long-Term Operation
未設定値の定義は、事件件数の増加によって変更を前提としてはならない。
Schema更新時に変更する場合は、正式な移行基準に従う。
---
## Chapter Boundary
本Chapterでは、NullabilityおよびUnset Valueの共通基準のみを定義する。
個別フィールドが採用するUnset ValueおよびDefault
Valueは、それぞれの正式フィールド定義で管理する。
# Chapter 11
# Data Validation
## Purpose
本Chapterは、事件データが本Database Schemaへ適合していることを確認するための共通検証基準を定義する。
Data
Validationは、Schemaで定義された構造、正式フィールド、制約および整合性への適合を確認することを目的とする。
---
## Scope
本Chapterは、本Schemaで定義されるすべての正式フィールドおよび正式構造へ適用する。
---
## Validation Principles
Data Validationは、Schemaで定義された基準のみを対象とする。
検証基準は、すべての事件データへ同一条件で適用しなければならない。
---
## Validation Targets
検証対象は少なくとも以下とする。
- 正式フィールド
- データ構造
- 値型
- 必須・任意
- 許可値
- 未設定値
- 制約
- 関連付け
- 一意性
- 構造の一貫性
---
## Structural Validation
事件データは、本Schemaで定義された正式構造へ適合しなければならない。
正式に定義されていない構造を採用してはならない。
---
## Field Validation
正式フィールドは、それぞれの正式定義へ適合しなければならない。
正式に定義されていないフィールドを追加してはならない。
---
## Value Validation
各正式フィールドの値は、Schemaで定義された基準へ適合しなければならない。
値型、許可値、Default ValueおよびUnset
Valueは、それぞれの正式定義に従う。
---
## Relationship Validation
正式な関連付けは、有効な正式データとの間でのみ成立しなければならない。
存在しない対象への関連付けを認めない。
---
## Validation Result
検証結果は、以下の状態で管理する。
- PASS
- ERROR
- WARNING
判定基準は、Schema全体で統一しなければならない。
---
## Long-Term Operation
Data
Validationは、1000件以上の事件データに対しても適用できる構造でなければならない。
個別事件だけではなく、一括検証を前提とする。
---
## Chapter Boundary
本Chapterでは、Schema適合性を確認するための共通検証基準のみを定義する。
実装方法、ライブラリ、検証コードおよび運用手順は、本Chapterの責務に含めない。
# Chapter 12
# Data Quality Requirements
## Purpose
本Chapterは、本Database Schemaへ適合した事件データについて、正式データとして維持すべき品質基準を定義する。
---
## Scope
本Chapterは、本Schemaで管理するすべての事件データへ適用する。
---
## Quality Principles
正式データは、Schemaへの適合に加え、本Chapterで定義する品質基準を満たさなければならない。
---
## Completeness
正式データは、Schemaで必要とされる情報を適切に保持しなければならない。
---
## Consistency
正式データは、事件データ全体を通じて一貫性を維持しなければならない。
---
## Accuracy
正式データは、本Schemaで定義された正式フィールドへ適切に保存しなければならない。
---
## Uniqueness
同一情報を不必要に重複保持してはならない。
---
## Referential Integrity
正式な関連付けは、有効な正式データとの整合性を維持しなければならない。
---
## Placeholder Data
仮データ、一時データ、テストデータまたはプレースホルダーを正式データとして採用してはならない。
---
## Quality Evaluation
品質は、少なくとも以下の観点から評価する。
- 完全性
- 一貫性
- 正確性
- 重複の有無
- 関連付けの整合性
- Schema適合性
---
## Long-Term Operation
品質基準は、1000件以上の事件データに対しても同一条件で適用しなければならない。
---
## Chapter Boundary
本Chapterでは、正式データとして維持すべき品質基準のみを定義する。
Schema構造、正式フィールド、実装方法、調査内容の信頼性評価および情報源の評価は、本Chapterの責務に含めない。
# Chapter 13
# Existing Data Migration
## Purpose
本Chapterは、既存の事件データを本Database Schemaへ移行するための共通基準を定義する。
Data
Migrationは、既存データを正式なSchemaへ適合させることを目的とし、事件内容を変更することを目的としない。
すべての移行は、データの整合性、一貫性および追跡可能性を維持した状態で実施しなければならない。
---
## Scope
本Chapterは、本Database Schemaへ移行するすべての既存事件データへ適用する。
対象には、過去のSchemaで管理されていた正式データおよび正式採用予定のデータを含む。
---
## Migration Principles
データ移行は、正式なSchemaへの適合を目的として実施する。
一時的な運用上の都合を理由として、正式構造を変更してはならない。
移行基準は、すべての事件データへ同一条件で適用しなければならない。
---
## Migration Planning
移行を開始する前に、対象データおよび影響範囲を明確にしなければならない。
移行対象となる正式フィールド、構造および関連付けを確認した上で移行を実施する。
事前確認を行わずに正式データを変更してはならない。
---
## Field Mapping
既存データと新Schemaの正式フィールドとの対応関係を明確に定義しなければならない。
対応関係が定義されていない正式フィールドへデータを移行してはならない。
一つの既存情報を複数の正式フィールドへ重複移行してはならない。
---
## Structure Migration
既存データの構造は、新Schemaで定義された正式構造へ移行しなければならない。
事件ごとに異なる移行構造を採用してはならない。
正式に定義されていない構造を移行先として使用してはならない。
---
## Data Integrity
移行後も、事件データの意味および責務を維持しなければならない。
移行によって正式データの意味が変更されてはならない。
情報の欠落、重複または不正な変換を認めない。
---
## Relationship Migration
正式な関連付けは、移行後も維持しなければならない。
関連付け先が変更される場合は、正式な対応関係に基づいて移行する。
存在しない対象への関連付けを生成してはならない。
---
## Migration Validation
移行後の事件データは、本Schemaで定義するData ValidationおよびData
Quality Requirementsを満たさなければならない。
Schemaへ適合しないデータを正式データとして採用してはならない。
---
## Rollback
移行は、必要に応じて移行前の状態へ戻せるよう管理しなければならない。
移行履歴を追跡できない状態で正式データを更新してはならない。
ロールバック可能性は、移行計画の一部として考慮しなければならない。
---
## Long-Term Operation
Schema更新に伴う移行は、1000件以上の事件データを対象としても実施できることを前提とする。
個別対応を前提とした移行を正式な運用として採用してはならない。
長期運用においても、一括移行、一括検証および一括確認が可能な状態を維持しなければならない。
---
## Chapter Boundary
本Chapterでは、既存データを正式Schemaへ移行するための共通基準のみを定義する。
以下の内容は、本Chapterでは定義しない。
- Schema構造
- 正式フィールド
- 値型
- 許可値
- 未設定値
- Version管理
- 実装方法
- 移行ツール
- データベース製品
- Git運用
これらは、それぞれを所管する他Chapterまたは実装側で定義する。
# Chapter 14
# Schema Versioning and Change Management
## Purpose
本Chapterは、Database
SchemaのVersion管理および変更管理に関する共通基準を定義する。
Schemaの変更は、一貫性、互換性および長期運用性を維持した状態で管理しなければならない。
---
## Scope
本Chapterは、Database Schema全体に適用する。
正式フィールド、構造、制約、許可値、未設定値および関連付けを含むSchema全体の変更を対象とする。
---
## Version Management
Database Schemaは、正式なVersionを持たなければならない。
すべての変更は、対応するSchema Versionの管理対象とする。
Versionを持たないSchema変更を正式変更として採用してはならない。
---
## Change Principles
Schema変更は、必要性、責務および長期運用への影響を確認した上で実施しなければならない。
一時的な運用上の都合または実装上の都合のみを理由としてSchemaを変更してはならない。
---
## Compatibility
Schema変更は、既存事件データとの互換性を考慮しなければならない。
互換性を維持できる変更を優先する。
互換性を維持できない変更を行う場合は、正式な移行を前提とする。
---
## Addition
正式フィールドまたは正式構造を追加する場合は、既存Schemaとの責務重複がないことを確認しなければならない。
既存の正式構造で責務を満たせる場合は、新たな正式構造を追加してはならない。
---
## Modification
正式フィールドまたは正式構造を変更する場合は、変更前後の責務を明確にしなければならない。
変更によって他の正式構造との整合性を失ってはならない。
---
## Deprecation
正式フィールドまたは正式構造を廃止する場合は、廃止状態を明確に管理しなければならない。
廃止予定および廃止済みを区別して管理する。
廃止に伴う既存データへの対応は、Existing Data Migrationに従う。
---
## Validation After Change
Schema変更後は、本Schemaで定義するData ValidationおよびData Quality
Requirementsによって変更結果を確認しなければならない。
Schema変更によって一貫性または整合性を損なってはならない。
---
## Long-Term Operation
Schemaは、長期運用において継続的な拡張および改善が可能な状態を維持しなければならない。
事件件数の増加によってVersion管理方法を変更することを前提としてはならない。
1000件以上の事件データを管理する場合でも、同一のVersion管理基準を適用しなければならない。
---
## Chapter Boundary
本Chapterでは、Schema
Version管理および変更管理の共通基準のみを定義する。
以下の内容は、本Chapterでは定義しない。
- Version番号の付与方法
- Version History
- データ移行手順
- 実装方法
- Git運用
- リリース管理
- デプロイ手順
これらは、それぞれを所管する他Chapterまたは関連文書で定義する。
# Chapter 15
# Long-Term Schema Operation
## Purpose
本Chapterは、Database
Schemaを長期的かつ継続的に運用するための共通基準を定義する。
事件データ数の増加、Schemaの拡張および運用期間の長期化によっても、Schema全体の一貫性、保守性および検証性を維持することを目的とする。
---
## Scope
本Chapterは、Database Schema全体に適用する。
正式フィールド、正式構造、関連付け、Version管理およびデータ移行を含むSchema全体の長期運用を対象とする。
---
## Long-Term Principles
Schemaは、短期的な要件ではなく、長期的な運用を前提として設計および維持しなければならない。
一時的な運用上の都合または個別事件への対応のみを理由として、Schema全体の整合性を損なってはならない。
---
## Scalability
Schemaは、事件件数の増加によって構造の一貫性を失ってはならない。
1000件以上の事件データを管理する場合でも、同一のSchemaを適用できなければならない。
---
## Maintainability
Schemaは、継続的に保守できる状態を維持しなければならない。
正式フィールド、正式構造および責務は、継続的に理解および管理できる状態で維持する。
---
## Consistency
Schemaは、Version更新後も一貫性を維持しなければならない。
正式フィールド、正式構造および責務は、Schema全体を通じて統一しなければならない。
---
## Validation Continuity
長期運用においても、本Schemaで定義するData
Validationを継続して適用できなければならない。
Schema更新後も、全件一括検証を実施できる状態を維持する。
---
## Migration Continuity
Schema更新に伴う既存データの移行は、長期運用においても継続して実施できなければならない。
移行不能となるSchema構造を正式構造として採用してはならない。
---
## Controlled Evolution
Schemaの拡張は、既存Schemaとの整合性を維持した状態で実施しなければならない。
新しい正式フィールドまたは正式構造を追加する場合は、責務の重複、構造の重複および長期運用への影響を確認しなければならない。
---
## Technology Independence
Schemaは、特定の実装環境、保存方式または技術要素へ依存しない状態を維持しなければならない。
技術環境が変更された場合でも、Schemaで定義する責務、構造および制約は維持されなければならない。
---
## Periodic Review
Schemaは、長期運用において定期的に適合性を確認しなければならない。
確認の結果、正式な変更が必要と判断された場合は、Schema
Version管理および変更管理の基準に従う。
---
## Chapter Boundary
本Chapterでは、Database Schemaの長期運用に関する共通基準のみを定義する。
以下の内容は、本Chapterでは定義しない。
- システム構成
- データベース製品
- 実装方法
- API設計
- ファイル配置
- コードアーキテクチャ
- 運用手順
- Git運用
- デプロイ方法
これらは、それぞれを所管する関連文書または実装側で定義する。
# Version History

| Version | Date | Changes |
|---|---|---|
| v1.3 | 2026-08-22 | Database Rule v3.0とのAuthorityおよびResponsibility Boundaryを整合。Chapter 1でDatabase Rule v3.0をデータ管理・データベース設計の最上位原則、本Schemaを個別データ仕様の正式基準として明確化。Chapter 3の正式フィールドおよびネスト関係の責務帰属を本Schemaへ修正。PASS済みChapter 6 Working Draftを正式統合し、Category / Class / Status / Risk Level / TagsのField Definitionおよび解消済みHOLD状態を反映。Chapter 11〜13の旧Version固定参照を本Database Schemaへの参照へ修正。新しいRoot構造は追加していない。 |
| v1.2 | 2026-08-03 | Codex最終監査のBLOCKERを反映。Database Rule v2.2との整合性を修正し、`incidentData`を正式なRoot構造として扱う記述を削除。`incidentData`は概念例における説明用の記述であることを明確化した。正式化される対象を事件データ内の正式フィールドおよびネスト関係に限定し、新しいSchema、Root構造、正式フィールドおよび運用ルールは追加していない。 |
| v1.1 | 2026-08-01 | Database Rule v2.2をSingle Source of Truthとして採用し、事件データの正式なSchemaを再構成。`incidentData`をRootとする構造、`englishName`、`riskLevel`、`caseCardImage`および`caseCardImage.path`の正式Schema定義を追加。Field Name、Purpose、Data Type、Required / Optional、Allowed Value、Default Value、Unset Value、Constraintsを正式定義として整理し、Field Definition Standardとの整合性を確立。Content and Media Referencesの責務を維持したままCase Card ImageのSchema定義を追加し、Data Validation、Data Quality、Existing Data Migration、Schema Version管理およびLong-Term Schema Operationを含む正式版として確定。 |
| v1.0 | 2026-08-01 | Database Schema v1.0を初版として策定。Database Rule v2.2を基準とし、正式フィールド、ネスト構造、値型、必須・任意、許可値、未設定値、データ間の関連付け、データ品質、検証基準、既存データ移行、Schema Version管理および長期運用基準を定義する正式設計書として確定。 |
