# Chapter 1

# Mission

ProjectORIGINを長期的かつ継続的に運営するため、各チャットの役割、作業フロー、および運用ルールを統一する。

Operating Manualは、ProjectORIGIN全体の案内書として機能し、各作業を適切なチャットへ振り分けるための基準を提供する。

本マニュアルは、Database Rule、Research Bible、Case File Template、Image Ruleなど、各設計書の内容を変更するものではない。

目的は、それぞれの設計書が担う役割を明確化し、「どこで何を行うか」を統一することで、役割の重複や運用上の混乱を防ぐことである。

ProjectORIGINは、1000件以上の事件ファイルを想定した長期プロジェクトである。

そのため、設計・調査・画像制作・実装・運営を明確に分離し、それぞれが独立して管理・更新できる運用体制を維持する。

Operating Manualは、ProjectORIGIN全体の運営基準として、すべての専用チャットを横断する共通の指針となる。

---

# Chapter 2

# Chat Structure

ProjectORIGINでは、長期的な運営と保守性を確保するため、作業内容ごとに専用チャットを分離して管理する。

各チャットは明確な役割を持ち、担当外の内容を扱わないことを原則とする。

複数の分野にまたがる内容であっても、それぞれの担当チャットで管理し、一つのチャットに運用が集中しないよう統一する。

## Operating Manual

ProjectORIGIN全体の運用方法を管理する。

### 管理内容

- チャットの役割
- 作業フロー
- 運用ルール
- ドキュメント管理
- Version管理
- リリース手順
- 長期運営方針

---

## Development

Webサイトの設計および開発を管理する。

### 管理内容

- UI / UX設計
- システム設計
- 実装方針
- GitHub Copilot用プロンプト管理
- Git運用
- 実装レビュー

---

## Database

事件ファイルおよびデータベース構造を管理する。

### 管理内容

- Database Rule
- Case File制作
- カテゴリ管理
- タグ管理
- 分類ルール
- データ構造

---

## Research Bible

調査基準および情報品質を管理する。

### 管理内容

- 調査基準
- 出典管理
- Evidence Rule
- Source Rule
- AI Analysis Rule
- 品質管理

---

## Image Rule

画像運用に関する基準を管理する。

### 管理内容

- 画像分類
- ライセンス管理
- キャプションルール
- Asset Management
- 品質基準

---

## Art Bible

ProjectORIGINの世界観およびビジュアルデザインを管理する。

### 管理内容

- 背景画像制作
- 世界観の統一
- ビジュアルコンセプト
- アートディレクション

---

## Principle

各チャットは、それぞれの役割に従って運用する。

あるチャットで定めたルールを別のチャットで重複して管理しない。

必要に応じて関連する設計書を参照しながら作業を進めるが、内容の変更や管理は担当チャットで行う。

これにより、ProjectORIGIN全体の設計を一貫した状態で維持し、長期的な保守性・拡張性・運用効率を確保する。

# Chapter 3

# Workflow

ProjectORIGINでは、すべての作業を適切な順序で進めるため、各チャットの役割に従ってワークフローを統一する。

一つのチャットですべての作業を完結させることはせず、それぞれの専門分野ごとに管理・更新を行う。

## Standard Workflow

基本的な制作フローは、以下の順序で進める。

1. Operating Manual
   - 作業内容を確認し、担当チャットを決定する。

2. Database
   - 事件情報を整理し、Case Fileの基本情報やデータ構造を作成する。

3. Research Bible
   - 情報を調査・検証し、Evidence RuleおよびSource Ruleに基づいて内容を確認する。

4. Image Rule
   - 使用する画像の分類、ライセンス、キャプション、および品質基準を確認する。

5. Art Bible
   - ProjectORIGINの世界観に沿った背景画像やビジュアルを制作する。

6. Development
   - 設計内容をもとにWebサイトへ実装し、動作確認および品質確認を行う。

## Responsibility

各チャットは、自身の担当範囲のみを管理する。

他チャットの設計内容を直接変更せず、必要な修正は該当チャットで管理・更新する。

## Consistency

すべてのチャットは、ProjectORIGIN全体の設計思想および運用方針を共有する。

各チャットで独自のルールを定める場合でも、他の設計書との整合性を維持し、運用上の矛盾が生じないよう管理する。

## Continuous Operation

ProjectORIGINは長期的な運営を前提としたプロジェクトである。

新たなチャットや設計書を追加する場合は、本Operating Manualに従って役割を定義し、既存の運用フローとの整合性を確認したうえで運用を開始する。

---

# Chapter 4

# Operating Principles

ProjectORIGINでは、すべての作業を長期的かつ一貫した品質で運営するため、以下の運用原則を共通ルールとして採用する。

## Role Separation

各チャットは、それぞれ定められた役割に従って運用する。

担当外の内容を管理・変更せず、必要な場合は該当する専用チャットで作業を行う。

---

## Single Source of Truth

同じ内容を複数の設計書で重複管理しない。

各ルール・基準・テンプレートは、それぞれの担当ドキュメントを唯一の管理元とし、変更や更新も担当チャットで実施する。

---

## Consistency

ProjectORIGIN全体で、設計思想・品質基準・運用方針を統一する。

新しいルールや運用方法を追加する場合は、既存の設計書との整合性を確認し、矛盾が生じないよう管理する。

---

## Documentation

重要なルールや運用方法は、必ず対応する設計書へ記録する。

チャット内のみで運用ルールを決定せず、正式なドキュメントへ反映することを原則とする。

---

## Change Management

運用ルールや設計書を更新する場合は、変更内容を明確に記録する。

必要に応じてVersion Historyを更新し、互換性や影響範囲を確認したうえで適用する。

---

## Scalability

ProjectORIGINは、1000件以上の事件ファイルと継続的な機能追加を前提としたプロジェクトである。

短期的な利便性よりも、将来的な保守性・拡張性・再利用性を優先して運用する。

---

## Quality First

すべての成果物は、公開速度よりも品質を優先する。

内容・構成・設計・画像・実装を十分に確認し、ProjectORIGINの品質基準を満たしたもののみを正式版として採用する。
```

# Chapter 5

# Document Structure

ProjectORIGINでは、各分野を独立した公式ドキュメントとして管理する。

各ドキュメントは明確な役割を持ち、担当する内容のみを管理する。

複数のドキュメントで同じルールを重複して管理しないことを原則とする。

---

## Operating Manual

ProjectORIGIN全体の運用方法を管理する。

### 管理内容

- チャットの役割
- 作業フロー
- 運用ルール
- ドキュメント管理
- 長期運営方針

---

## Database Rule

事件ファイルおよびデータベース構造を管理する。

### 管理内容

- データ構造
- カテゴリ
- タグ
- Class
- Status
- データ管理ルール

---

## Research Bible

情報収集および品質基準を管理する。

### 管理内容

- 調査基準
- 出典管理
- Evidence Rule
- Source Rule
- AI Analysis Rule

---

## Case File Template

Case Fileの構成および執筆形式を管理する。

### 管理内容

- Chapter構成
- セクション構成
- 記述ルール
- 品質基準
- 更新ルール

---

## Image Rule

画像運用に関する基準を管理する。

### 管理内容

- 画像分類
- ライセンス管理
- キャプション
- Asset Management
- 品質基準

---

## Art Bible

ProjectORIGINのビジュアルデザインおよび世界観を管理する。

### 管理内容

- 背景画像
- 世界観
- ビジュアルコンセプト
- アートディレクション

---

## Development Documents

Webサイトの設計および実装に関するドキュメントを管理する。

### 管理内容

- システム設計
- UI / UX設計
- Git運用
- GitHub Copilotプロンプト
- 実装ガイドライン

---

## Principle

新しいルールや設計書を追加する場合は、既存のドキュメントとの役割を明確に区別する。

運用中に役割が重複した場合は、本Operating Manualを基準として担当範囲を整理し、一つの内容につき一つの公式ドキュメントのみを管理元とする。

---

# Chapter 6

# Version Management

ProjectORIGINでは、すべての公式ドキュメントを継続的に管理し、変更履歴を明確に記録する。

Version Managementの目的は、変更内容を追跡し、各ドキュメントの整合性と保守性を維持することである。

---

## Version Policy

すべての公式ドキュメントは、バージョン番号を付与して管理する。

バージョン番号は、変更規模に応じて更新する。

- **Major Version（例：v2.0）**
  - 構成や運用方針に大きな変更があった場合。

- **Minor Version（例：v1.1）**
  - 新しいルールや章を追加した場合。

- **Patch Version（例：v1.0.1）**
  - 誤字修正や表現の改善など、内容に影響しない軽微な修正を行った場合。

---

## Change Log

ドキュメントを更新した場合は、変更内容をVersion Historyへ記録する。

変更履歴には、少なくとも以下の内容を含める。

- Version
- 更新日
- 更新内容
- 変更理由（必要に応じて）

---

## Compatibility

既存の運用へ影響する変更を行う場合は、関連するドキュメントとの整合性を確認する。

運用上の矛盾や重複が生じる場合は、担当ドキュメントを更新し、内容を統一する。

---

## Document Status

各ドキュメントは、現在の管理状態を明確にする。

必要に応じて、以下の状態を使用する。

- Draft
- Review
- Official
- Archived

---

## Responsibility

各ドキュメントの更新は、担当チャットで管理する。

Operating Manualは、ProjectORIGIN全体のVersion Management方針を定義し、各ドキュメントは本方針に従って運用する。
```

# Chapter 7

# Maintenance

ProjectORIGINは、一度公開して完了するプロジェクトではなく、継続的に更新・改善・保守を行う長期運営型プロジェクトである。

本章では、ProjectORIGINを安定して維持するための保守運用方針を定める。

---

## Continuous Improvement

公開後も必要に応じて内容を見直し、品質・正確性・使いやすさの向上を継続する。

改善は既存の設計思想を尊重し、全体との整合性を確認したうえで実施する。

---

## Regular Review

公式ドキュメントおよび運用ルールは、定期的に見直す。

見直しでは、次の項目を確認する。

- 運用ルールの整合性
- ドキュメント間の重複や矛盾
- 品質基準への適合
- 長期運営への適応状況

---

## Scalability

新しい機能、カテゴリ、事件ファイル、または運用ルールを追加する場合は、既存の構成を維持しながら拡張する。

短期的な対応ではなく、将来的な保守性と再利用性を優先する。

---

## Issue Management

運用中に課題や改善点が見つかった場合は、担当チャットで内容を整理し、必要に応じて関連ドキュメントを更新する。

一時的な対応を正式なルールとして扱わず、運用へ反映する際は十分な確認を行う。

---

## Long-Term Operation

ProjectORIGINは、1000件以上の事件ファイルと継続的な機能拡張を前提として運営する。

そのため、日々の運用においても、現在だけでなく将来の保守・更新・拡張を考慮して判断する。

---

## Operating Principle

保守作業では、既存の品質を維持することを最優先とする。

改善や新機能の追加を行う場合でも、ProjectORIGIN全体の一貫性を損なわないことを基本方針とする。

---

# Chapter 8

# Quality Management

ProjectORIGINでは、すべての成果物において品質を最優先とする。

品質管理の目的は、各チャット・各ドキュメント・各成果物が統一された基準に従って作成・更新・公開されることを保証し、ProjectORIGIN全体の信頼性と一貫性を維持することである。

---

## Quality Policy

すべての成果物は、正確性・一貫性・保守性を満たした状態で管理する。

公開や実装の速度ではなく、品質を優先することを基本方針とする。

---

## Consistency Check

公開前および正式採用前には、ProjectORIGIN全体との整合性を確認する。

特に以下の点を確認する。

- 運用ルールとの整合性
- 関連ドキュメントとの矛盾の有無
- 命名規則の統一
- 用語の統一
- 構成の統一

---

## Documentation Quality

公式ドキュメントは、内容だけでなく構成や表現についても統一する。

各ドキュメントは、目的・役割・対象範囲が明確であり、担当範囲を逸脱しないことを原則とする。

---

## Review Process

重要な変更を行う場合は、内容を確認し、関連するドキュメントへの影響を検証したうえで反映する。

必要に応じてVersion Historyを更新し、変更内容を記録する。

---

## Continuous Quality Improvement

品質基準は固定されたものではなく、ProjectORIGINの成長に合わせて継続的に改善する。

新たな運用方法や制作手法を採用する場合は、既存の品質基準との整合性を確認し、正式なルールとして文書化する。

---

## Final Principle

ProjectORIGINにおける品質とは、単に誤りがないことではなく、長期的な運営・保守・拡張に耐えられる設計と運用が維持されている状態を指す。

すべての成果物は、この品質基準に基づいて管理・更新・公開する。
```

# Chapter 9

# Future Expansion

ProjectORIGINは、継続的な成長と長期運営を前提としたプロジェクトである。

新しい機能、コンテンツ、運用方法、または設計書を追加する場合は、本Operating Manualを基準として運用する。

---

## Expansion Policy

新たな要素を追加する場合は、既存の運用ルールや設計思想との整合性を確認する。

短期的な利便性ではなく、長期的な保守性・拡張性・一貫性を優先する。

---

## New Documents

新しい公式ドキュメントを作成する場合は、目的・役割・管理範囲を明確に定義する。

既存ドキュメントと内容が重複する場合は、新規作成ではなく既存ドキュメントの更新を優先する。

---

## New Chat

新しい専用チャットを追加する場合は、担当する分野を明確にし、他チャットとの責務が重複しないよう設計する。

必要に応じてOperating Manualの「Chat Structure」を更新し、ProjectORIGIN全体の運用体制を維持する。

---

## Future Features

新機能の導入や運営方法の変更を行う場合は、既存のワークフローや品質基準への影響を確認したうえで適用する。

実装だけでなく、必要な運用ルールや関連ドキュメントもあわせて更新する。

---

## Continuous Evolution

ProjectORIGINは完成を目的とするのではなく、継続的に進化するプロジェクトである。

運営を通じて得られた知見や改善点は、適切なドキュメントへ反映し、将来の制作・保守・運営に活用する。

---

## Final Principle

ProjectORIGINの拡張は、既存の設計を置き換えるためではなく、その価値を維持しながら発展させるために行う。

すべての追加・変更・改善は、本Operating Manualを基準として計画・管理し、ProjectORIGIN全体の一貫性と持続可能な運営を維持する。

---

# Version History

## v1.0

Initial Release

### Contents

- Established the official Operating Manual for ProjectORIGIN.
- Defined the mission and role of the Operating Manual.
- Standardized the responsibilities of each dedicated chat.
- Established the official workflow for project operations.
- Defined the core operating principles for long-term management.
- Organized the structure and responsibilities of official documents.
- Established version management and maintenance policies.
- Defined project-wide quality management standards.
- Established guidelines for future expansion and continuous operation.