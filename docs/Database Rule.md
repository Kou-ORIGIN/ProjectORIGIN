# ProjectORIGIN Database Rule v2.0

# Chapter 1

# Mission

## Purpose

ProjectORIGINは、「未知を探索する機密データベース」として、未確認現象、未解決事件、歴史的事象、都市伝説などに関する情報を体系的に整理・管理することを目的とする。

本書は、ProjectORIGINにおけるデータベース設計、事件管理、およびデータ運用の基準を定義する正式設計書である。

本ルールは、1000件以上の事件ファイルを長期的に管理・運用できるデータベースを前提とし、ProjectORIGIN全体で統一された品質と運用基準を維持することを目的とする。

データベースの設計および運用は、ProjectORIGIN全体の設計思想に従い、UIは英語、コンテンツは日本語の方針を維持する。

また、本書はデータベース設計、事件管理、タグ設計、カテゴリ設計、およびデータ運用を対象とし、実装、GitHub Copilot、コード作成は対象外とする。

---

# Chapter 2

# Database Philosophy

## Basic Policy

ProjectORIGINは、事件を紹介するサイトではなく、事件を調査・整理・蓄積するデータベースとして設計する。

事件ファイルは、無料版および将来のCLASSIFIED ACCESSを前提とした構成とする。ただし、現時点では有料機能は実装しない。

無料版は、事件の全体像を理解できる品質を目標とし、読者が事件の概要や主要な論点を把握できる内容を提供する。

調査過程で収集した詳細な資料や分析情報は、公開の有無にかかわらず継続的に保管し、将来的なCLASSIFIED ACCESSへの発展を想定したデータとして管理する。

すべての事件ファイルは、ProjectORIGIN全体で統一された設計思想および品質基準に基づいて制作・管理し、長期運営においても一貫性を維持する。

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

# Chapter 4

# Case File Policy

## Basic Policy

事件ファイルは、無料版および将来のCLASSIFIED ACCESSを前提として設計する。

ただし、現時点では有料機能は実装しない。

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
```

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
```

# Chapter 7

# Image Policy

## Basic Policy

事件ファイルで使用する画像は、著作権および利用条件を尊重して管理する。

利用許諾を満たさない画像は掲載しない。

画像の選定および管理は、ProjectORIGIN全体の画像運用基準に従って実施する。

## Background Images

事件ファイルの背景画像は、ProjectORIGINで制作・管理する背景画像を優先して使用する。

背景画像は、事件の世界観や調査資料としての雰囲気を補完する目的で使用し、本文の可読性や情報伝達を妨げないことを前提とする。

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

## Project Philosophy

ProjectORIGINは、事件を紹介するサイトではなく、事件を調査・整理・蓄積するデータベースとして長期運営する。

すべての事件ファイルは、事実・有力な説・仮説を明確に区別し、統一された品質基準のもとで継続的に管理する。

長期運営においても、ProjectORIGIN全体の設計思想、世界観、およびデータ品質の一貫性を維持する。

# Version History

| Version | Date | Changes |
|----------|------------|---------|
| v2.0 | 2026-07-27 | ProjectORIGIN Database Ruleを正式設計書として再構成。Mission、Database Philosophy、Database Scope、Case File Policy、Research Policy、Source Priority、Image Policy、AI Analysis Policy、Long-Term Operationを整理し、ProjectORIGIN全体（AGENTS.md、Operating Manual、Research Bible、Research Template、Case File Template、Master Case File Template、Audit Rule、Image Rule）との整合性を維持した正式版として確定。 |
```