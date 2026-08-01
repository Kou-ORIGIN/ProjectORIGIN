# Chapter 1

# Mission

## Purpose

ProjectORIGINにおけるデータベースの設計および運用に関する基準を定義する。

本書は、未知の事件・現象・歴史・技術などを長期的に管理するための正式なデータベース設計書とする。

ProjectORIGINは、1000件以上の事件ファイルを継続的に管理・運用できる構造を目標とする。

UIおよびシステム操作は英語、事件ファイルなどのコンテンツは日本語を基本とする。

本書では、データベース設計、データ管理、および運用基準を対象とし、実装、GitHub Copilot、コード作成は対象外とする。

---

# Chapter 2

# Database Philosophy

## Basic Philosophy

ProjectORIGINは、未知の事件・現象を調査・整理・蓄積するためのデータベースとして設計する。

事件ファイルは単なる紹介記事ではなく、長期的に調査・更新・管理されるデータとして扱う。

Case Card Imageは、事件データを構成する正式なデータ管理対象として扱う。

ProjectORIGINでは、無料版および将来的なCLASSIFIED ACCESSを前提としたデータ管理を行う。

ただし、現時点では有料機能は実装しない。

Researchによって整理・検証された情報を基準とし、データベース全体で一貫した品質を維持する。

## Data Responsibility

事件そのものを表す正式な事実データと、画面表示のために使用する表示用データは分離して管理する。

事件データには、正式な事件情報を保持し、UI固有の表示値や、既存データから共通ルールで導出できる表示情報を重複して保存しない。

以下の情報は、正式な事件データとして管理する。

- 日本語の正式事件名
- `englishName`
- 正式な`country`
- 正式な`location`
- 正式な日付・年代情報
- `category`
- `class`
- `tags`
- `riskLevel`
- `caseCardImage`
- その他の正式な事件情報

以下の情報は、事件データへ保存しない。

- 代表タグの複製
- 短縮国名
- 表示用地域略称
- `displayEra`
- Risk Levelの英語表示名
- Risk Levelの表示色
- UI専用ラベル
- 既存データから共通ルールで導出できる表示文字列

代表タグは`tags`から、短縮地域名は正式な`country`および`location`と共通の地域表示定義から取得する。

`displayEra`は事件データへ保存せず、正式な日付・年代情報から共通ルールで導出する。

表示用情報は、正式な事件データおよびProjectORIGIN全体の共通定義から取得する。

これにより、UIや表示方針が変更された場合でも、事件データ全件へ表示専用の修正を行う必要がない構造を維持する。

# Chapter 3

# Database Scope

## Scope

本書は、ProjectORIGINにおけるデータベースの設計および運用に関する基準を定義する。

対象とする範囲は、以下のとおりとする。

- データベース設計
- 事件管理
- タグ設計
- カテゴリ設計
- データ運用

本書では、事件ファイルのデータ構造や管理基準を対象とし、実装、GitHub Copilot、コード作成は対象外とする。

データベースは、1000件以上の事件ファイルを長期的に管理できる構造を前提とし、ProjectORIGIN全体で統一された運用基準を維持する。

また、本書はAGENTS.md、Operating Manual、Research Bible、Research Template、Case File Template、Master Case File Template、Audit Rule、およびImage Ruleと連携し、それぞれの役割を尊重しながら運用する。

---

## Case Data Structure

事件データは、ProjectORIGIN全体で共通して利用できる正式な情報を保持する。

表示専用の情報は事件データへ重複保存せず、正式な事件データおよび共通定義から取得する。

### englishName

正式フィールド名は、`englishName`とする。

事件の正式英語名を保持する。

#### 値型

```text
string | null
```

#### 必須・任意

正式公開データでは必須とする。

調査中または移行中の事件データでは、一時的に`null`を許容する。

#### 未設定値

正式な未設定値は`null`とする。

空文字は正式な値として使用しない。

既存データでフィールドが未定義の場合は未設定として扱う。

正式な事件データでは、`englishName`フィールドを保持する。

---

### riskLevel

正式フィールド名は、`riskLevel`とする。

事件のRisk Level段階を保持する。

#### 値型

```text
integer | null
```

#### 許可値

```text
1
2
3
4
5
```

正式公開データでは必須とする。

調査中または移行中の事件データでは、一時的に`null`を許容する。

#### 未設定値

正式な未設定値は`null`とする。

以下は正式な値として使用しない。

- 空文字
- 文字列
- 小数
- 0
- 6以上の整数

事件データには、Risk Levelを整数値のみで保持する。

Risk Levelの英語表示名、表示色その他の表示情報は保持しない。

---

## Case Card Image Data Structure

Case Card Imageの正式フィールド名は、`caseCardImage`とする。

`caseCardImage`の値は、Case Card Imageが設定されている場合はオブジェクト、設定されていない場合は`null`とする。

Case Card Imageが設定されている場合、画像パスは`path`プロパティに保持する。

正式なデータ構造は、以下のとおりとする。

```text
caseCardImage
└── path: string
```

`path`には、Case Card Imageとして使用する画像リソースを参照する、空文字ではない文字列を保持する。

Case Card Imageが設定されていない場合は、以下の形式で管理する。

```text
caseCardImage: null
```

正式な事件データでは、Case Card Imageの設定有無を明確にするため、`caseCardImage`フィールドを保持する。

以下は、事件データ内での概念的な記述例である。

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

この記述例はデータ構造を示すものであり、特定の実装言語やファイル形式を指定するものではない。

---

# Chapter 4

# Case File Policy

## Basic Policy

事件ファイルは、無料版および将来のCLASSIFIED ACCESSを前提として設計する。

ただし、現時点では有料機能は実装しない。

Case Card Imageは、各Case Fileに属する事件データ内で直接管理する。

各事件データは、自身の`caseCardImage`フィールドを保持し、Case Card Imageが設定されている場合は画像参照情報を記録する。

Case Card ImageをCase Fileとは別の対応表のみで管理する構造は採用しない。

`englishName`は、事件を識別する正式な英語名称として管理する。

正式公開データでは、`englishName`および`riskLevel`を必須とする。

代表タグは、`tags`を順序付き一覧として管理し、先頭に登録された有効なタグを使用する。

代表タグを別フィールドとして重複保存しない。

`tags`が空の場合は、代表タグを未設定として扱う。

### Free Edition

無料版は、事件の全体像を理解できる品質を目標とする。

無料版には、以下の内容を含める。

- 概要
- 事実
- 有力な説
- 仮説
- 未解決点

無料版のみでも、事件の概要と主要な論点を理解できる内容とする。

### Future CLASSIFIED ACCESS

調査中に収集した情報は、公開の有無にかかわらず継続的に保管する。

将来的なCLASSIFIED ACCESSへの発展を想定し、以下の情報を管理対象とする。

- 詳細な証言
- 詳細時系列
- 参考資料
- 一次資料
- 軍資料
- 公文書
- 書籍
- 論文
- 写真
- 地図
- 関連事件
- AI分析用メモ

これらの情報は、将来的なコンテンツ拡張に対応できるよう管理する。

# Chapter 5

# Research Policy

## Information Classification

事件に関する情報は、以下の3つに分類して管理する。

1. Fact（事実）
2. Leading Theory（有力な説）
3. Hypothesis（仮説）

各分類は明確に区別し、相互に混同しない。

### Fact

公的機関の発表、一次資料、信頼性の高い記録などにより確認できる情報を対象とする。

### Leading Theory

一定の根拠や複数の資料・研究によって支持されている説を対象とする。

### Hypothesis

十分な証拠による裏付けがなく、現時点では推測や可能性の段階にある内容を対象とする。

## Research Principle

事件ファイルの制作およびデータ管理は、Research BibleおよびResearch Templateで定める調査基準に従って実施する。

ProjectORIGINでは、事実・有力な説・仮説を明確に区別し、客観性と中立性を維持した情報管理を行う。

---

# Chapter 6

# Source Priority

## Source Evaluation

事件の調査およびデータ管理では、資料の信頼性を考慮し、以下の優先順位に従って取り扱う。

| Priority | Source |
|----------|--------|
| ★★★★★ | 一次資料 |
| ★★★★★ | 公的機関 |
| ★★★★☆ | 書籍 |
| ★★★★☆ | 学術資料 |
| ★★★☆☆ | 信頼できるニュース |
| ★★☆☆☆ | 研究家・民間調査資料 |
| ★☆☆☆☆ | SNS・個人投稿 |

## Basic Policy

一次資料および公的機関が公開する資料を最優先とする。

書籍、学術資料、報道、研究家による資料は、それぞれの信頼性を考慮した上で参照する。

SNSや個人投稿は参考情報として扱うが、事実認定の根拠とはしない。

資料の評価はResearch BibleおよびResearch Templateで定める調査基準に従い、事件ファイルの制作およびデータ管理に反映する。

# Chapter 7

# Image Policy

## Basic Policy

事件ファイルで使用する画像は、著作権および利用条件を尊重して管理する。

利用許諾を満たさない画像は掲載しない。

画像の選定および管理は、ProjectORIGIN全体の画像運用基準に従って実施する。

## Background Images

事件ファイルの背景画像は、ProjectORIGINで制作・管理する背景画像を優先して使用する。

背景画像は、事件の世界観や調査資料としての雰囲気を補完する目的で使用し、本文の可読性や情報伝達を妨げないことを前提とする。

## Case Card Image Data Management

Case Card Imageが設定されていない場合は、`caseCardImage`の値をnullとする。

空文字は、Case Card Imageの正式な値として使用しない。

`caseCardImage`が空文字の場合、または`path`が空文字の場合は、Case Card Image未設定として扱い、正式データではnullへ統一する。

既存の事件データに`caseCardImage`フィールドが存在しない場合は、Case Card Image未設定として扱う。

ただし、正式な事件データでは`caseCardImage`フィールドを保持し、未設定の場合はnullを記録する。

Case Card Imageが未設定の場合、既定画像または代替画像のパスをデータ上で参照しない。

画像未設定時のカード表現はImage Ruleに従い、Database Ruleでは画像データが存在しない状態のみを定義する。

## Image Management

画像の管理および運用は、Image Ruleで定める基準に従う。

データベースでは、画像を事件データの構成要素として管理するが、画像制作や画像品質の詳細な基準は本書の対象外とする。

---

# Chapter 8

# AI Analysis Policy

## Basic Policy

ProjectORIGINでは、将来的にAIによる分析機能を導入することを想定し、分析に活用できる情報を継続的に蓄積する。

現時点では、AI分析機能の実装は行わず、分析に必要な情報の管理を対象とする。

## Analysis Data

将来のAI分析に備え、以下の情報を管理対象とする。

- 分析メモ
- 矛盾点
- 比較情報

これらの情報は、事件ファイルとは区別して管理し、将来的な分析機能の基礎データとして活用する。

## Operation Policy

AI分析に関するデータ管理は、Research BibleおよびResearch Templateで定める調査基準に従う。

本書では、AI分析機能の仕様や実装は対象とせず、分析に必要なデータの管理方針のみを定義する。

---

# Chapter 9

# Long-Term Operation

## Long-Term Policy

ProjectORIGINは、1000件以上の事件ファイルを長期的に管理・運用することを前提として設計する。

データベースは、一時的な情報の蓄積ではなく、継続的な調査・更新・管理を行うための基盤として運用する。

## Database Operation

事件ファイルは、ProjectORIGIN全体で統一された設計思想および品質基準に基づいて管理する。

新たな資料や信頼性の高い情報が確認された場合は、既存データを継続的に見直し、必要に応じて更新する。

すべての事件ファイルは、Research Bible、Research Template、Case File Template、およびMaster Case File Templateに基づいて制作・管理する。

既存データの正規化を継続的に実施し、同一の意味を持つ情報を複数の正式フィールドへ重複保存しない。

正式な事件情報は事件データとして保持し、表示専用の情報はProjectORIGIN全体の共通定義から取得する。

UIや表示方針が変更された場合でも、事件データ全件を修正することなく、共通定義のみを更新できる構造を維持する。

Risk Levelの英語表示名は、`riskLevel`の値からProjectORIGIN全体の共通表示定義を使用して取得する。

正式な対応は以下のとおりとする。

| riskLevel | English Display |
|-----------|-----------------|
| 1 | LOW |
| 2 | MEDIUM |
| 3 | HIGH |
| 4 | VERY HIGH |
| 5 | EXTREME |

Risk Levelの英語表示名は事件データへ保存しない。

Risk Levelの表示色、配置、サイズ、強調方法およびアニメーションはUIおよび視覚表現側の責務とし、Database Ruleでは定義しない。

Case Card、Case File、Favorites、ORIGIN MAPおよび将来のCLASSIFIED ACCESSは、同一の共通表示定義を使用する。

将来的に表示名称を変更する場合も、事件データは変更せず、共通表示定義のみを更新する。

## Project Philosophy

ProjectORIGINは、事件を紹介するサイトではなく、事件を調査・整理・蓄積するデータベースとして長期運営する。

すべての事件ファイルは、事実・有力な説・仮説を明確に区別し、統一された品質基準のもとで継続的に管理する。

長期運営においても、ProjectORIGIN全体の設計思想、世界観、およびデータ品質の一貫性を維持する。

# Version History

| Version | Date | Changes |
|----------|------------|---------|
| v2.2 | 2026-08-01 | Case Card Imageの正式フィールド名を`caseCardImage`、画像パスの正式プロパティ名を`path`として定義。`caseCardImage`の正式な未設定値を`null`とし、空文字、空の`path`、フィールド未定義を未設定として扱い、正式データでは未設定値を`null`へ統一する方針を確定。Case Card Imageを各事件データ内で直接管理し、未設定時に既定画像または代替画像をデータ上で参照しない方針、およびImage Ruleとの責務分離を明確化。`englishName`および`riskLevel`を正式フィールドとして定義し、`riskLevel`の値型を`integer \| null`、許可値を1〜5として定義。Risk Levelの英語表示名は共通表示定義から取得し、代表タグは`tags`の先頭の有効値から取得する方針を確定。短縮地域名は共通の地域表示定義から取得し、`displayEra`は保存せず正式な日付・年代情報から導出する方針を追加。事実データと表示データを分離する方針を正式化。 |
| v2.1 | 2026-07-30 | Case Card Imageを正式なデータ管理対象として追加。Database Philosophyへ管理対象を明記し、Case Fileとの関連付けおよび参照ルールを追加。画像未登録時は既定のカード画像を参照する運用を定義。既存のデータベース設計・データ管理・運用基準との整合性を維持。 |
| v2.0 | 2026-07-27 | ProjectORIGIN Database Ruleを正式設計書として再構成。Mission、Database Philosophy、Database Scope、Case File Policy、Research Policy、Source Priority、Image Policy、AI Analysis Policy、Long-Term Operationを整理し、ProjectORIGIN全体（AGENTS.md、Operating Manual、Research Bible、Research Template、Case File Template、Master Case File Template、Audit Rule、Image Rule）との整合性を維持した正式版として確定。 |
