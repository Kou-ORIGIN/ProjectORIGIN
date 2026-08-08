# Chapter 1

# Mission and Authority

## Purpose

本章は、ProjectORIGINにおけるDatabase Ruleの目的、適用範囲および権限に関する基本原則を定義する。

Database Ruleは、ProjectORIGIN全体で共通して適用するデータ管理およびデータベース設計の最上位原則とする。

---

## Mission

Database Ruleは、ProjectORIGINにおけるデータ管理およびデータベース設計の基本原則を定義する。

ProjectORIGINは、未知の事件・現象・歴史・技術などを長期的に管理・運用することを目的とする。

Database Ruleは、個別のデータ仕様や実装方法ではなく、ProjectORIGIN全体で共通して維持する設計原則を定義する。

---

## Authority

Database Ruleは、ProjectORIGINにおけるデータ管理およびデータベース設計に関する最上位の設計原則とする。

Database Schemaおよび関連する正式文書は、本書で定義する設計原則に従って管理する。

---

## Scope

Database Ruleは、以下を対象とする。

- データベース設計原則
- データ管理原則
- データ責務
- データ分類
- 長期運用原則

Database Ruleは、以下を対象外とする。

- 個別データ仕様
- データ構造
- Validation
- Migration
- 実装
- UI
- システム運用

これらは、それぞれの正式文書または正式な責務領域で定義する。

---

## Long-Term Objective

ProjectORIGINは、1000件以上の管理対象を長期的かつ継続的に管理できる構造を前提として設計する。

Database Ruleは、一時的な要件ではなく、ProjectORIGIN全体で長期的に維持できる設計原則を定義する。

# Chapter 2

# Core Data Principles

## Purpose

本章は、ProjectORIGIN全体で共通して適用するデータ管理の基本原則を定義する。

本章で定義する原則は、Database Rule全体および関連する正式文書に共通して適用する。

---

## Single Source of Truth

正式な情報は、一つの正式な情報源のみで管理する。

同一の意味を持つ情報を複数の正式な管理対象へ重複保存しない。

表示専用の情報は、正式なデータまたは共通定義から取得する。

---

## Separation of Responsibilities

各正式文書および各データは、それぞれ定義された責務のみを持つ。

責務の異なる情報を同一の管理対象へ混在させない。

---

## Data Integrity

正式データは、一貫性および整合性を維持しなければならない。

正式データの変更は、ProjectORIGIN全体の整合性を維持することを前提とする。

---

## Technology Independence

Database Ruleは、特定の実装言語、データベース製品または開発環境へ依存しない。

設計原則は、技術の変更後も継続して適用できることを前提とする。

---

## Long-Term Maintainability

Database Ruleは、長期運用に耐えられる構造を維持する。

一時的な要件ではなく、継続的な保守性を優先する。

---

## Change Impact Isolation

変更による影響は、可能な限り局所化する。

一つの変更がProjectORIGIN全体へ不要な影響を与えない構造を維持する。

---

## Common Definitions

表示名、分類、その他の共通情報は、ProjectORIGIN全体で共通定義として管理する。

正式データへ同一内容を重複保存しない。

# Chapter 3

# Data Classification and Ownership

## Purpose

本章は、ProjectORIGINにおける正式データの分類および管理責任に関する基本原則を定義する。

データ分類および管理責任は、ProjectORIGIN全体で一貫して適用する。

---

## Data Classification

正式データは、その役割および責務に応じて分類する。

各データ分類は、明確な目的および責務を持たなければならない。

責務の異なる情報を同一のデータ分類へ混在させない。

---

## Data Ownership

すべての正式データは、明確な管理責任を持たなければならない。

各データは、一つの正式な管理主体によって維持および管理する。

管理責任が不明確な正式データを作成しない。

---

## Responsibility Separation

データ分類と管理責任は、それぞれ独立した責務として管理する。

データ分類は情報の役割を定義し、管理責任は維持および更新の責任を定義する。

---

## Ownership Consistency

正式データの管理責任は、ProjectORIGIN全体で一貫性を維持する。

データ分類の変更または拡張を行う場合も、管理責任を明確に定義しなければならない。

---

## Long-Term Maintainability

データ分類および管理責任は、将来のデータ追加および拡張に対応できる構造を維持する。

一時的な要件ではなく、長期的な保守性および継続的な運用を前提として設計する。

# Chapter 4

# Document and Layer Responsibilities

## Purpose

本章は、ProjectORIGINを構成する正式文書および各レイヤーの責務に関する基本原則を定義する。

各正式文書は、明確に定義された責務のみを持つ。

---

## Responsibility Principle

各正式文書は、それぞれ定義された責務のみを管理する。

責務の異なる内容を同一の正式文書へ混在させない。

---

## Layer Independence

各レイヤーは、それぞれ独立した責務を持つ。

一つのレイヤーの変更が、他のレイヤーへ不要な影響を与えない構造を維持する。

---

## Single Responsibility

一つの正式文書は、一つの主要な責務を持つ。

複数の異なる責務を一つの正式文書へ集約しない。

---

## Document Relationship

正式文書は、それぞれ独立した責務を維持しながら相互に連携する。

各正式文書は、他の正式文書の責務を代替しない。

---

## Responsibility Consistency

正式文書間の責務境界は、ProjectORIGIN全体で一貫性を維持する。

新しい正式文書を追加する場合も、既存の責務境界を維持しなければならない。

---

## Long-Term Maintainability

正式文書および各レイヤーは、将来の機能追加および文書追加に対応できる構造を維持する。

ProjectORIGIN全体のルールが増えても、責務を整理し続けられる構造を維持する。

# Chapter 5

# Change and Evolution Principles

## Purpose

本章は、ProjectORIGINにおける変更および継続的な進化に関する基本原則を定義する。

変更は、一貫性、責務分離および長期運用性を維持することを前提とする。

---

## Controlled Change

正式な変更は、明確な目的および責務に基づいて実施する。

一時的な要件によって設計原則を変更しない。

---

## Change Impact Isolation

変更による影響は、可能な限り局所化する。

一つの変更が他の責務領域へ不要な影響を与えない構造を維持する。

---

## Backward Consistency

変更を実施する場合は、ProjectORIGIN全体の整合性および一貫性を維持しなければならない。

既存の設計原則と矛盾する変更を行わない。

---

## Sustainable Growth

ProjectORIGINは、継続的な拡張および改善を前提として設計する。

将来の機能追加およびデータ拡張に対応できる構造を維持する。

---

## Evolution Responsibility

変更および進化は、各正式文書の責務を維持した上で実施する。

一つの変更を理由として責務境界を曖昧にしない。

---

## Long-Term Maintainability

ProjectORIGINは、変更を繰り返しても長期的な保守性を維持できる構造を目指す。

設計原則は、一時的な最適化ではなく継続的な成長を支えることを目的とする。

# Chapter 6

# Data Integrity and Relationships

## Purpose

本章は、ProjectORIGINにおける正式データ間の関係性および整合性に関する基本原則を定義する。

データ間の関係は、一貫性、独立性および長期的な保守性を維持することを前提とする。

---

## Data Integrity

正式データは、常に一貫性および整合性を維持しなければならない。

データの追加、変更または削除を行う場合も、ProjectORIGIN全体の整合性を維持する。

---

## Relationships

正式データ間の関係は、明確な目的および責務に基づいて定義する。

不要または曖昧な関係を作成しない。

---

## Referential Consistency

正式データ間の参照関係は、一貫性を維持しなければならない。

参照関係の変更は、関連する正式データ全体への影響を考慮した上で実施する。

---

## Data Independence

各正式データは、それぞれ独立した責務を持つ。

一つの正式データが他の正式データの責務を代替しない。

---

## Common Definitions

複数の正式データで共通して利用する情報は、共通定義として管理する。

同一内容を複数の正式データへ重複保存しない。

---

## Integrity Responsibility

データ間の関係性および整合性は、ProjectORIGIN全体で継続的に維持しなければならない。

データ構造を変更する場合も、本章で定義する原則を維持する。

# Chapter 7

# Lifecycle Principles

## Purpose

本章は、ProjectORIGINにおける正式データのライフサイクルに関する基本原則を定義する。

正式データは、継続的な品質向上および長期的な維持管理を前提として管理する。

---

## Continuous Improvement

正式データは、継続的な改善を前提として維持する。

新たな情報または知見が得られた場合は、一貫性および整合性を維持した上で改善する。

---

## Lifecycle Principle

正式データは、作成から更新、維持および将来の発展までを含めたライフサイクル全体を考慮して管理する。

一時的な利用のみを前提とした設計を行わない。

---

## Quality Progression

正式データの品質は、継続的な改善を通じて向上させる。

品質向上は、既存データとの整合性および責務分離を維持した上で実施する。

---

## Stable Publication

正式データは、安定した品質を維持した状態で公開および利用する。

継続的な改善を行う場合も、正式データとしての信頼性を損なわない。

---

## Long-Term Evolution

正式データは、将来の拡張および改善に対応できる構造を維持する。

継続的な成長を前提とし、一時的な最適化を目的とした設計を行わない。

---

## Lifecycle Responsibility

正式データのライフサイクルは、ProjectORIGIN全体で一貫した責務のもとに管理する。

ライフサイクル全体を通じて、品質、一貫性および長期的な保守性を維持する。

# Chapter 8

# Long-Term Operation

## Purpose

本章は、ProjectORIGIN全体の長期的かつ持続的な運営に関する基本原則を定義する。

ProjectORIGINは、継続的な成長および将来の拡張を前提として設計する。

---

## Long-Term Operation Principle

ProjectORIGINは、短期的な要件ではなく、長期的な運営を前提として管理する。

設計原則は、継続的な保守性および安定性を維持しなければならない。

---

## Scalability

ProjectORIGINは、管理対象、データ量および機能の拡張に対応できる構造を維持する。

将来の拡張を妨げる設計を行わない。

---

## Maintainability

ProjectORIGINは、長期的な保守性を維持できる構造を維持する。

設計原則は、一時的な最適化ではなく、継続的な保守を優先する。

---

## Adaptability

ProjectORIGINは、技術の変化および新しい要件へ柔軟に対応できる構造を維持する。

技術の変更を理由として設計原則を変更しない。

---

## Sustainable Operation

ProjectORIGINは、継続的な運営および改善を前提として管理する。

長期運営に必要な一貫性、責務分離および保守性を維持する。

---

## Future Readiness

ProjectORIGINは、将来の機能追加および運営環境の変化に対応できる構造を維持する。

長期的な成長を支える設計原則を継続的に維持する。

# Chapter 9

# Governance and Document Authority

## Purpose

本章は、ProjectORIGINにおける正式文書のガバナンスおよび文書間の責務に関する基本原則を定義する。

すべての正式文書は、明確な責務および権限のもとで管理する。

---

## Governance Principle

正式文書は、それぞれ定義された責務および権限に基づいて管理する。

責務の異なる内容を同一の正式文書へ混在させない。

---

## Document Authority

各正式文書は、それぞれ定義された責務範囲において正式な情報源とする。

一つの正式文書が、他の正式文書の責務を代替しない。

---

## Responsibility Consistency

正式文書間の責務境界は、ProjectORIGIN全体で一貫して維持する。

正式文書の追加または変更を行う場合も、既存の責務境界を維持しなければならない。

---

## Governance Consistency

正式文書間で内容の不整合が確認された場合は、各文書の責務範囲を確認した上で整合性を回復する。

データ管理およびデータベース設計の基本原則については、Database Ruleを正式基準とする。

個別のデータ仕様については、Database Ruleに反しない範囲でDatabase Schemaを正式基準とする。

---

## Long-Term Governance

ProjectORIGINは、長期的な運営および継続的な成長に対応できるガバナンスを維持する。

新しい正式文書を追加する場合も、本章で定義する責務および権限の原則を維持する。

# Version History

| Version | Date | Changes |
|----------|------------|---------|
| v3.0 | 2026-08-08 | Database RuleをProjectORIGIN V3 Architectureの正式な設計原則として全面再設計。Mission and Authorityを再構成し、Database RuleをProjectORIGIN全体で共通して適用するデータ管理およびデータベース設計の最上位原則として明確化。Core Data Principles、Data Classification and Ownership、Document and Layer Responsibilities、Change and Evolution Principles、Data Integrity and Relationships、Lifecycle Principles、Long-Term Operation、Governance and Document Authorityを再構成し、責務分離、Single Source of Truth、Change Impact Isolation、長期運用性および変更に強い設計を正式原則として確立。Database RuleとDatabase Schemaの責務境界を明確化し、正式文書間で不整合が発生した場合のガバナンス原則を追加。ProjectORIGIN全体で共通して適用するデータ管理およびデータベース設計の基盤として正式版を確立。 |
| v2.2 | 2026-08-01 | Case Card Imageの正式フィールド名を`caseCardImage`、画像パスの正式プロパティ名を`path`として定義。`caseCardImage`の正式な未設定値を`null`とし、空文字、空の`path`、フィールド未定義を未設定として扱い、正式データでは未設定値を`null`へ統一する方針を確定。Case Card Imageを各事件データ内で直接管理し、未設定時に既定画像または代替画像をデータ上で参照しない方針、およびImage Ruleとの責務分離を明確化。`englishName`および`riskLevel`を正式フィールドとして定義し、`riskLevel`の値型を`integer \| null`、許可値を1〜5として定義。Risk Levelの英語表示名は共通表示定義から取得し、代表タグは`tags`の先頭の有効値から取得する方針を確定。短縮地域名は共通の地域表示定義から取得し、`displayEra`は保存せず正式な日付・年代情報から導出する方針を追加。事実データと表示データを分離する方針を正式化。 |
| v2.1 | 2026-07-30 | Case Card Imageを正式なデータ管理対象として追加。Database Philosophyへ管理対象を明記し、Case Fileとの関連付けおよび参照ルールを追加。画像未登録時は既定のカード画像を参照する運用を定義。既存のデータベース設計・データ管理・運用基準との整合性を維持。 |
| v2.0 | 2026-07-27 | ProjectORIGIN Database Ruleを正式設計書として再構成。Mission、Database Philosophy、Database Scope、Case File Policy、Research Policy、Source Priority、Image Policy、AI Analysis Policy、Long-Term Operationを整理し、ProjectORIGIN全体との整合性を維持した正式版として確定。 |