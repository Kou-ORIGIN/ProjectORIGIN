
# Chapter 1

## Schema Overview

### Purpose

Database Schema v1.0は、ProjectORIGINで管理する事件データの正式な構造を定義する文書である。

本Schemaは、すべての事件データを一貫した形式で作成、保存、検証、移行および更新できる状態を維持することを目的とする。

事件ファイルが1000件以上へ増加した場合も、データごとの差異、構造の分岐、情報の重複および未設定値の不統一が発生しない構造を基準とする。

### Highest Standard

Database Schema v1.0の最上位基準は、Database Rule v2.2とする。

本Schemaに定義するすべての構造、フィールド、型、制約および未設定値は、Database Rule v2.2に従わなければならない。

Database Rule v2.2と本Schemaの内容に矛盾が生じた場合は、Database Rule v2.2を優先する。

### Scope

本Schemaは、ProjectORIGINで管理する事件データに適用する。

本Schemaが定義する対象は、以下のとおりとする。

- 事件データのRoot構造
- 正式フィールド
- ネスト構造
- 値型
- 必須・任意
- 許可値
- 未設定値
- データ間の関連付け
- データ品質
- 検証基準
- 移行基準
- Version管理
- 長期運用基準

### Responsibilities

本Schemaは、以下を保証するための正式な構造定義を提供する。

- 正式フィールドの統一
- 一貫したRoot構造
- 責務分離
- Single Source of Truth
- 一括検証可能な構造
- 一括移行可能な構造
- 長期運用可能な構造

### Out of Scope

本Schemaでは以下を定義しない。

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

これらは、それぞれの正式文書または実装側の責務とする。

---

# Chapter 2

## Schema Design Principles

### Purpose

本Chapterは、Database Schema全体へ適用する設計原則を定義する。

### Principles

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

### Chapter Boundary

本Chapterでは設計原則のみを定義する。

正式フィールド、値型、制約および構造の詳細は後続Chapterで定義する。

---

# Chapter 3

## Incident Data Root Structure

### Purpose

本Chapterは、ProjectORIGINで管理する事件データの正式なRoot構造を定義する。

### Root Structure

ProjectORIGINの事件データは、`incidentData`をRootとする。

`incidentData`は複数の事件データを保持する。

各事件データは、一つの事件を表す独立したオブジェクトとする。

正式なRoot構造は以下のとおりとする。

```text
incidentData
└── incident object
```

各incident objectは、本Schemaで定義する正式フィールドのみを保持する。

### Formal Nested Structure

Database Rule v2.2で正式化されたネスト構造は以下とする。

```text
incidentData
└── incident object
    ├── englishName
    ├── riskLevel
    └── caseCardImage
        └── path
```

- `englishName`はincident object直下に配置する。
- `riskLevel`はincident object直下に配置する。
- `caseCardImage`はincident object直下に配置する。
- `path`は`caseCardImage`配下のみで管理する。

### Root Structure Example

以下はRoot構造を示す概念例である。

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

この概念例はRoot構造および正式なネスト関係を示すものであり、特定の実装言語または保存形式を指定するものではない。

### Root Rules

- Root構造は全事件データで共通とする。
- 独自のRoot構造を追加してはならない。
- 独自のネスト構造を追加してはならない。
- 正式フィールドを複数階層へ重複保存してはならない。
- 表示専用データを事件データへ保存してはならない。
- 正式な未設定値は各フィールド定義に従う。
- Root構造は1000件以上の長期運用、一括検証、一括更新および一括移行に対応できる構造を維持する。

# Chapter 4

## Core Identification Fields

### Purpose

本Chapterは、事件データを識別するための正式フィールドを定義する。

識別情報は事件そのものを識別することのみを目的とし、分類、表示または実装方法を表してはならない。

---

## Official Identification Fields

事件データの識別情報として使用する正式フィールドは、以下とする。

- Internal Identifier
- File Number
- Case Name
- `englishName`

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

既存データでフィールドが未定義の場合は未設定として扱う。

### Constraints

- 正式英語名のみを保持する。
- 値を設定する場合は文字列とする。
- 空文字を使用しない。
- 正式公開データでは`null`を使用しない。
- 調査中または移行中のみ一時的に`null`を許容する。
- 正式な事件データではフィールドを省略しない。
- 英語名以外の表示情報を保持しない。

---

# Chapter 5

## Core Incident Facts

### Purpose

本Chapterは、事件そのものを説明する基礎情報の正式構造を定義する。

---

## Official Fact Fields

Core Incident Factsとして管理する正式フィールドは、以下とする。

- Date
- Location
- Country
- Coordinates
- Short Summary

各フィールドは事件の基本情報のみを保持する。

事件識別情報、分類情報および表示情報は本Chapterの責務に含めない。

---

## Responsibility

各正式フィールドは一つの責務のみを持つ。

同一情報を複数の正式フィールドへ重複保存してはならない。

表示情報は保持しない。

---

## Validation

Core Incident Factsは以下を満たさなければならない。

- 正式フィールドへ保存されていること
- 各フィールドの責務が重複していないこと
- 同一情報が重複保存されていないこと
- Schema構造へ適合していること

---

## Chapter Boundary

本Chapterでは事件の基本情報のみを定義する。

値型、必須・任意、許可値、未設定値および制約の詳細は各正式フィールド定義またはField Definition Standardで管理する。

---

# Chapter 6

## Classification and Controlled Values

### Purpose

本Chapterは、事件データを分類する正式フィールドおよび管理値を定義する。

分類情報は事件そのものの事実とは独立した管理情報として扱う。

---

## Official Classification Fields

正式分類フィールドは以下とする。

- Category
- Class
- Status
- `riskLevel`
- Tags

本Chapterでは、`riskLevel`の正式Schema定義を定義する。

---

## riskLevel

事件のRisk Level段階を保持する正式フィールドとする。

### Field Name

```text
riskLevel
```

### Purpose

事件のRisk Level段階を保持する。

### Data Type

```text
integer | null
```

### Required / Optional

正式公開データでは必須とする。

調査中または移行中の事件データでは、一時的に`null`を許容する。

正式な事件データでは、`riskLevel`フィールド自体を保持する。

### Allowed Value

```text
1
2
3
4
5
```

### Default Value

なし。

### Unset Value

```text
null
```

既存データでフィールドが未定義の場合は未設定として扱う。

### Constraints

- 整数値のみ保持する。
- 1〜5のみ使用する。
- 空文字を使用しない。
- 文字列を使用しない。
- 小数を使用しない。
- 0を使用しない。
- 6以上を使用しない。
- 正式公開データでは`null`を使用しない。
- 調査中または移行中のみ一時的に`null`を許容する。
- 正式な事件データではフィールドを省略しない。
- Risk Levelの英語表示名を保存しない。
- 表示色その他の表示専用情報を保存しない。

---

## Risk Level Display Separation

Risk Levelの英語表示名は、ProjectORIGIN全体の共通表示定義から取得する。

| riskLevel | English Display |
|-----------|-----------------|
| 1 | LOW |
| 2 | MEDIUM |
| 3 | HIGH |
| 4 | VERY HIGH |
| 5 | EXTREME |

英語表示名は事件データへ保存しない。

---

## Tags

Tagsは順序付き一覧として管理する。

代表タグは先頭に登録された有効なタグから取得する。

代表タグを別フィールドとして重複保存してはならない。

Tagsが空の場合は代表タグを未設定として扱う。

---

## Chapter Boundary

本Chapterでは分類情報および`riskLevel`の正式Schema定義のみを扱う。

UI、表示色、配置、サイズ、強調方法およびアニメーションは本Chapterの責務に含めない。

# Chapter 7

## Content and Media References

### Purpose

本Chapterは、事件データと関連コンテンツおよびメディアデータとの正式な参照構造を定義する。

事件データは、コンテンツやメディアそのものを保持するのではなく、正式な参照情報のみを管理する。

本Chapterでは、PASS済みの参照責務を維持したまま、`caseCardImage`および`caseCardImage.path`の正式Schema定義を追加する。

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

Case Card Imageの設定状態および画像参照情報を保持する正式フィールドとする。

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

設定済みの場合は以下の構造とする。

```text
caseCardImage
└── path: string
```

未設定の場合は以下とする。

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

Case Card Imageとして使用する画像リソースへの参照を保持する正式プロパティとする。

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

Case Card Imageとして使用する画像リソースを参照する空文字ではない文字列。

### Default Value

なし。

### Unset Value

単独のUnset Valueは定義しない。

Case Card Imageが未設定の場合は、親フィールドである`caseCardImage`全体を`null`とする。

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

UI、CSS、JavaScript、API、画像品質、表示方法および実装方法は本Chapterの責務に含めない。

---

# Chapter 8

## Relationships Between Data

### Purpose

本Chapterは、事件データと他の正式データとの関連付け方法を定義する。

関連付けは正式データ間の対応関係のみを管理し、同一情報を重複保存することを目的としない。

---

## Official Relationship Targets

正式な関連付け対象は以下とする。

- Related Cases
- Research Data
- Master Case File
- Content References
- Media References

---

## Responsibility

関連付けは正式データ同士の関係のみを管理する。

関連先の本文または画像データ本体を事件データへ保持してはならない。

---

## Referential Integrity

すべての関連付けは正式データを対象としなければならない。

存在しない対象または正式管理されていない対象を参照してはならない。

---

## Validation

関連付けは以下を満たさなければならない。

- 正式な関連対象を参照していること
- 正式構造へ適合していること
- 関連付けの責務が重複していないこと
- 整合性が維持されていること

---

## Chapter Boundary

本Chapterでは正式データ間の関連付けのみを定義する。

個別フィールド、値型、許可値、実装方法は本Chapterの責務に含めない。

---

# Chapter 9

## Field Definition Standard

### Purpose

本Chapterは、すべての正式フィールドで共通して使用する定義フォーマットを定義する。

---

## Standard Definition Format

正式フィールドは、以下の定義項目を使用する。

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

各正式フィールドは、

- 一つの責務のみを持つこと
- 一つの正式名称のみを持つこと
- 正式な値型を持つこと
- 必須・任意を明確にすること
- 許可値を定義すること
- Default Valueの有無を明確にすること
- Unset Valueを一意に定義すること
- 制約を明確にすること

を満たさなければならない。

---

## Validation

正式フィールド定義は以下を満たさなければならない。

- 必要な定義項目がすべて存在すること
- 責務が重複していないこと
- 共通フォーマットが維持されていること

---

## Chapter Boundary

本Chapterでは正式フィールドの定義方法のみを定義する。

個別フィールドの内容、許可値および未設定値の具体的な値は、それぞれの正式フィールド定義で管理する。

# Chapter 10

## Nullability and Unset Values

### Purpose

本Chapterは、正式フィールドにおける未設定値およびNullabilityの共通基準を定義する。

未設定値の表現を統一することにより、事件データの一貫性、検証性および長期運用性を維持することを目的とする。

本Chapterは、未設定状態の表現方法を定義するものであり、個別フィールドの採用値を決定するものではない。

---

## Scope

本Chapterは、本Schemaで定義されるすべての正式フィールドへ適用する。

ルートフィールド、ネストフィールドおよび参照フィールドを区別せず、共通の基準として適用する。

---

## Nullability

各正式フィールドは、値を必須とするか、未設定を許可するかを明確に定義しなければならない。

Nullabilityは、各正式フィールドの責務に基づいて決定する。

同一の正式フィールドについて、状況によってNullabilityを変更してはならない。

---

## Unset Value

未設定状態を許可する正式フィールドは、正式なUnset Valueを一つ定義しなければならない。

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

Unset Valueは、正式フィールドの責務および保持する情報の性質に基づいて決定する。

運用上の都合のみを理由として未設定値を選択してはならない。

---

## Consistency

同一の正式フィールドは、すべての事件データで同一のUnset Valueを使用しなければならない。

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

個別フィールドが採用するUnset ValueおよびDefault Valueは、それぞれの正式フィールド定義で管理する。

---

# Chapter 11

## Data Validation

### Purpose

本Chapterは、事件データがDatabase Schema v1.0へ適合していることを確認するための共通検証基準を定義する。

Data Validationは、Schemaで定義された構造、制約および整合性への適合を確認することを目的とする。

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

値型、許可値、Default ValueおよびUnset Valueは、それぞれの正式定義に従う。

---

## Relationship Validation

正式な関連付けは、有効な正式データとの間でのみ成立しなければならない。

存在しない対象への関連付けを認めない。

---

## Validation Result

検証結果は以下の状態で管理する。

- PASS
- ERROR
- WARNING

判定基準はSchema全体で統一しなければならない。

---

## Long-Term Operation

Data Validationは1000件以上の事件データに対しても適用できる構造でなければならない。

個別事件だけではなく、一括検証を前提とする。

---

## Chapter Boundary

本ChapterではSchema適合性を確認するための共通検証基準のみを定義する。

実装方法、ライブラリおよび検証コードは本Chapterの責務に含めない。

---

# Chapter 12

## Data Quality Requirements

### Purpose

本Chapterは、Database Schema v1.0へ適合した事件データについて、正式データとして維持すべき品質基準を定義する。

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

品質は少なくとも以下の観点から評価する。

- 完全性
- 一貫性
- 正確性
- 重複の有無
- 関連付けの整合性
- Schema適合性

---

## Long-Term Operation

品質基準は1000件以上の事件データに対しても同一条件で適用しなければならない。

---

## Chapter Boundary

本Chapterでは正式データとして維持すべき品質基準のみを定義する。

Schema構造、正式フィールド、実装方法、調査内容の信頼性評価および情報源の評価は本Chapterの責務に含めない。

# Chapter 13

## Existing Data Migration

### Purpose

本Chapterは、既存の事件データをDatabase Schema v1.0へ移行するための共通基準を定義する。

Data Migrationは、既存データを正式なSchemaへ適合させることを目的とし、事件内容を変更することを目的としない。

すべての移行は、データの整合性、一貫性および追跡可能性を維持した状態で実施しなければならない。

---

## Scope

本Chapterは、Database Schema v1.0へ移行するすべての既存事件データへ適用する。

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

移行後の事件データは、本Schemaで定義するData ValidationおよびData Quality Requirementsを満たさなければならない。

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

---

# Chapter 14

## Schema Versioning and Change Management

### Purpose

本Chapterは、Database SchemaのVersion管理および変更管理に関する共通基準を定義する。

Schemaの変更は、一貫性、互換性および長期運用性を維持した状態で管理しなければならない。

---

## Scope

本Chapterは、Database Schema全体に適用する。

正式フィールド、構造、制約、許可値、未設定値および関連付けを含む、Schema全体の変更を対象とする。

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

Schema変更後は、本Schemaで定義するData ValidationおよびData Quality Requirementsによって変更結果を確認しなければならない。

Schema変更によって一貫性または整合性を損なってはならない。

---

## Long-Term Operation

Schemaは、長期運用において継続的な拡張および改善が可能な状態を維持しなければならない。

事件件数の増加によってVersion管理方法を変更することを前提としてはならない。

1000件以上の事件データを管理する場合でも、同一のVersion管理基準を適用しなければならない。

---

## Chapter Boundary

本Chapterでは、Schema Version管理および変更管理の共通基準のみを定義する。

以下の内容は、本Chapterでは定義しない。

- Version番号の付与方法
- Version History
- データ移行手順
- 実装方法
- Git運用
- リリース管理
- デプロイ手順

これらは、それぞれを所管する他Chapterまたは関連文書で定義する。

---

# Chapter 15

## Long-Term Schema Operation

### Purpose

本Chapterは、Database Schemaを長期的かつ継続的に運用するための共通基準を定義する。

事件データ数の増加、Schemaの拡張および運用期間の長期化によっても、Schema全体の一貫性、保守性および検証性を維持することを目的とする。

---

## Scope

本Chapterは、Database Schema全体に適用する。

正式フィールド、構造、関連付け、Version管理および移行を含むSchema全体の長期運用を対象とする。

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

正式フィールド、構造および責務は、Schema全体を通じて統一しなければならない。

---

## Validation Continuity

長期運用においても、本Schemaで定義するData Validationを継続して適用できなければならない。

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

確認の結果、正式な変更が必要と判断された場合は、Schema Version管理および変更管理の基準に従う。

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
|----------|------------|---------|
| v1.0 | 2026-08-01 | Database Schema v1.0正式版を確定。Database Rule v2.2をSingle Source of Truthとして採用し、事件データの正式なSchemaを再構成。`incidentData`をRootとする正式なRoot構造およびincident objectの配置基準を定義。`englishName`、`riskLevel`、`caseCardImage`、`caseCardImage.path`について、Field Name、Purpose、Data Type、Required / Optional、Allowed Value、Default Value、Unset Value、Constraintsを正式Schemaとして定義し、Field Definition Standardとの整合性を確立。`caseCardImage`の正式なネスト構造を明確化し、PASS済みのContent and Media Referencesの責務を維持したままSchema定義を追加。概念例と正式フィールド命名の整合性を整理し、Chapter間の責務を統一。Data Validation、Data Quality、Existing Data Migration、Schema Version管理およびLong-Term Schema Operationを含む正式なSchema構成を完成。Gitリポジトリ保存用正式版として確定。 |