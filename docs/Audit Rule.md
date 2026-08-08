# Chapter 1
# Mission

## Purpose

本Audit Ruleは、ProjectORIGIN全体で適用する品質監査および品質保証の基準を定義する正式文書である。

ProjectORIGINでは、1000件以上の事件ファイルを長期的に運用することを前提とし、Research・Master Case File・FREE・CLASSIFIED・画像・データベース・各種設計文書について、一貫した品質を維持することを目的とする。

本書は、成果物の制作方法を定義するものではなく、それらが定められた品質基準を満たしているかを評価するための監査基準を定義する。

---

## Mission

ProjectORIGIN Audit Ruleの使命は、ProjectORIGIN全体の品質を客観的かつ継続的に保証することである。

監査では、成果物の内容だけではなく、情報管理、品質、一貫性、制作フロー、Version管理、AI運用を含めた品質管理全体を評価対象とする。

また、監査を通じてProjectORIGIN全体の品質向上を支援し、長期運営に適した品質管理体制を維持する。

---

## Scope

本Audit Ruleは、以下を監査対象とする。

- Research
- Master Case File
- FREE Case File
- CLASSIFIED Case File
- Database
- Image Assets
- Rule Documents
- Template Documents
- AI生成コンテンツ
- Version管理
- 制作フロー

各成果物の詳細な制作方法は、それぞれの専用文書で定義し、本Audit Ruleでは品質監査基準のみを定義する。

---

## Responsibilities

Audit Ruleは、以下の責任を担う。

- 品質監査基準の策定
- 品質評価基準の統一
- 品質チェックリストの管理
- AI監査基準の整備
- 品質改善提案の基準策定
- Version管理に関する監査基準の整備

一方で、本Audit Ruleは成果物の制作・編集・修正を行わない。

成果物の制作は各専用チャットで実施し、本Audit Ruleは品質保証および品質監査に専念する。

---

## Fundamental Principles

ProjectORIGIN Auditでは、以下の基本原則を維持する。

1. 品質評価は客観的な監査基準に基づいて実施する。
2. 制作と監査の役割を明確に分離する。
3. 監査結果は再現可能な基準に基づいて記録する。
4. すべての成果物を共通の品質基準で評価する。
5. 品質管理は長期運営と拡張性を考慮して継続的に改善する。
6. AIによる監査を基本とし、人間は最終承認者として品質を確認する。
7. 監査は品質保証を目的とし、成果物の内容を制作・修正することを目的としない。

---

## Operational Model

ProjectORIGINでは、以下の役割分担を品質管理の基本モデルとする。

| 担当 | 役割 |
|------|------|
| 制作担当AI | Research・Case File・画像などの成果物を制作する。 |
| 監査担当AI（Codexを想定） | Audit Ruleに基づき品質を監査し、問題点および改善提案を提示する。 |
| 人間 | 監査結果を確認し、公開・差し戻し・更新の最終判断を行う。 |

各担当は、それぞれの責任範囲を越えて作業を行わず、制作・監査・承認を明確に分離する。

---

## Expected Outcome

本Audit Ruleを適用することにより、ProjectORIGIN全体で統一された品質監査基準を維持し、成果物の品質・一貫性・保守性・拡張性を継続的に保証する。

また、AIによる品質監査と人間による最終承認を組み合わせることで、制作効率と品質保証を両立し、1000件以上の事件ファイルを長期的かつ安定して運用できる品質管理基盤を構築する。

# Chapter 2
# Audit Principles

## Purpose

本章では、ProjectORIGINにおける品質監査の基本原則を定義する。

すべての監査は、本章で定める共通原則に基づいて実施する。監査対象や監査担当が異なる場合でも、評価基準と判断方法の一貫性を維持し、監査結果の再現性を確保することを目的とする。

---

## Objectivity

監査は、個人の意見、好み、印象に基づかず、承認済みのルール、テンプレート、チェックリストおよび基準文書に基づいて実施する。

監査担当は、事件の知名度、話題性、面白さ、独自性ではなく、監査対象が定められた品質基準を満たしているかを評価する。

客観的な判断が困難な場合は、推測によって結論を補完せず、確認不能または追加確認が必要な項目として記録する。

---

## Independence

制作と監査は、明確に分離する。

制作担当AIは成果物を制作し、監査担当AIは成果物が監査基準へ適合しているかを評価する。監査担当AIは、監査中に成果物を直接修正、追記または再構成してはならない。

監査で問題が確認された場合は、問題箇所、判定理由および必要な改善内容を監査結果として記録し、修正作業は該当する制作工程へ差し戻す。

この役割分離により、自己評価による判断の偏りを抑え、品質保証の独立性を維持する。

---

## Evidence-Based Audit

監査は、確認可能な情報および記録に基づいて実施する。

情報の正確性を監査する場合は、Research、出典、References、Source Management、Reliability Assessmentその他の関連記録を確認する。

監査担当AIは、監査対象に不足している情報を独自に追加せず、未記録の情報や推測を根拠として評価してはならない。

情報の根拠が確認できない場合は、根拠未確認または追加確認が必要な問題として報告する。

---

## Consistency

監査では、単一の成果物だけでなく、関連する成果物および基準文書との整合性を確認する。

主な確認関係は、以下のとおりとする。

- ResearchとMaster Case File
- Master Case FileとFREE Case File
- Master Case FileとCLASSIFIED Case File
- Databaseと各Case File
- 本文と画像およびキャプション
- 成果物と適用テンプレート
- 各ルール文書と関連設計書

不整合を確認した場合、監査担当AIは一方を独自に正しいと判断して修正せず、不整合の内容と影響範囲を記録する。

---

## Standardization

ProjectORIGINのすべての監査は、共通の品質基準に基づいて実施する。

事件の分類、知名度、資料量、公開範囲または制作時期によって、基本的な監査基準を任意に変更してはならない。

ただし、Research、Master Case File、FREE、CLASSIFIED、画像、Databaseなど、成果物ごとに定められた専用の監査項目は、その役割に応じて適用する。

共通基準と成果物別基準を組み合わせることで、全体の統一性と個別成果物の適切な評価を両立する。

---

## Traceability

すべての監査結果は、後から確認できる状態で記録する。

監査記録には、少なくとも以下を含める。

- 監査対象
- 対象Version
- 監査実施日
- 監査担当
- 適用したAudit RuleのVersion
- 判定結果
- 指摘事項
- 判定理由
- 改善提案
- 再監査の要否

監査結果を追跡可能にすることで、公開判断、修正履歴、Version更新および品質改善の根拠を確認できる状態を維持する。

---

## Reproducibility

同一の監査対象に同一の基準を適用した場合、監査担当が異なっても同等の結果を得られる状態を目標とする。

そのため、監査結果では、単に問題の有無を示すだけでなく、該当する基準、問題箇所および判定理由を明確に記録する。

曖昧な表現や監査担当の感覚に依存した判定は避け、可能な限り確認可能な条件に基づいて評価する。

---

## Role Compliance

監査では、各成果物および各専用チャットが定められた役割を逸脱していないかを確認する。

Research、Master Case File、FREE、CLASSIFIED、画像、Database、ルール文書およびテンプレートは、それぞれ異なる目的と責任範囲を持つ。

一つの成果物が他の成果物の役割を不必要に包含している場合や、専用文書で定義されていない処理を行っている場合は、役割逸脱として記録する。

Audit Rule自体も監査基準の策定と管理に専念し、成果物の制作または修正を行わない。

---

## AI-First Audit

ProjectORIGINでは、AIによる監査を品質管理の基本とする。

監査担当AIは、Audit Rule、Quality Checklistおよび関連基準文書を参照し、定められた項目を一定の順序と形式で確認する。

AI監査は、以下を目的とする。

- 品質評価の均一化
- 人間による確認作業の削減
- 監査漏れの防止
- 重複作業の削減
- 監査結果の記録と比較
- 長期運営における監査効率の維持

AIは監査結果と改善提案を提示するが、最終承認および公開判断は人間が行う。

---

## Human Approval

AIによる監査結果は、公開およびVersion承認のための判断資料として扱う。

人間は、監査結果、重大な指摘事項、改善提案および関連するVersion情報を確認し、承認、差し戻し、保留または公開不可の最終判断を行う。

人間による承認は、監査基準を省略または置き換えるものではない。承認判断も、可能な限り監査結果と定められた品質基準に基づいて実施する。

---

## Continuous Improvement

監査は、個別の成果物を評価するだけでなく、ProjectORIGIN全体の品質管理を改善するために活用する。

監査で同種の問題が継続的に確認された場合は、個別の修正だけで対応せず、ルール、テンプレート、チェックリスト、制作フローまたはAI運用に共通の原因がないかを確認する。

改善が必要と判断された場合は、所定のVersion管理および承認手順を経て関連文書へ反映する。

監査担当AIは改善を提案できるが、承認を受けずにルールや基準を変更してはならない。

---

## Long-Term Operation

すべての監査原則は、ProjectORIGINで1000件以上の事件ファイルを継続的に管理することを前提として適用する。

監査基準は、一時的な運用や特定の事件だけに依存せず、再利用可能であり、成果物の増加後も同じ方法で適用できる状態を維持する。

品質を維持するために必要な監査と、運用負担を過度に増加させる監査を区別し、自動化、差分確認および再監査範囲の限定によって、品質と制作効率の両立を図る。

# Chapter 3
# Audit Scope

## Purpose

本章では、ProjectORIGINにおける品質監査の対象範囲を定義する。

ProjectORIGINでは、事件ファイルだけではなく、調査資料、画像、データベース、テンプレート、ルール文書および制作フローを含めたプロジェクト全体を品質監査の対象とする。

監査対象を明確に定義することで、監査範囲の重複や漏れを防止し、長期運営において一貫した品質保証を実現する。

---

## Audit Scope

本Audit Ruleでは、ProjectORIGINで管理する以下の成果物および関連資産を監査対象とする。

- Research
- Master Case File
- FREE Case File
- CLASSIFIED Case File
- Database
- Image Assets
- Rule Documents
- Template Documents
- AI生成コンテンツ
- 制作フロー
- Version管理

各監査対象には、それぞれの役割に応じた監査基準を適用する。

---

## Research Audit

Researchは、ProjectORIGINにおけるすべての事件ファイルの基礎資料である。

監査では、Research BibleおよびResearch Templateに基づき、以下を確認する。

- テンプレートへの準拠
- 出典管理
- Reliability Assessment
- Source Management
- 情報分類
- 未確認情報の管理
- 更新履歴
- AI Notesの適切性

Researchは、後続するすべての成果物の基準資料として監査する。

---

## Master Case File Audit

Master Case Fileは、Researchを基に構成される正式な事件資料である。

監査では、以下を確認する。

- Researchとの整合性
- 情報分類の適切性
- 中立性
- 構成
- References
- テンプレート準拠
- 品質基準への適合

Master Case Fileは、FREEおよびCLASSIFIEDの基準資料として監査する。

---

## FREE Case File Audit

FREE Case Fileは、事件の概要を読者へ提供する公開版である。

監査では、Case File Templateに基づき、以下を確認する。

- OVERVIEW
- FACTS
- THEORIES
- 情報量
- 客観性
- Masterとの整合性
- FREE版としての役割

詳細情報が過度に含まれていないことも監査対象とする。

---

## CLASSIFIED Case File Audit

CLASSIFIED Case Fileは、詳細資料を提供する拡張版である。

監査では、以下を確認する。

- Masterとの整合性
- 詳細情報
- 証言
- 一次資料
- AI Analysis
- References
- テンプレート準拠

CLASSIFIED独自の構成であっても、ResearchおよびMasterとの整合性を維持する。

---

## Database Audit

Databaseは、ProjectORIGIN全体の基盤情報を管理する。

監査では、以下を確認する。

- File Number
- 基本情報
- Category
- Class
- Status
- Risk Level
- Tags
- Coordinates
- Related Cases
- Metadata

重複、欠落、表記ゆれおよび整合性を確認する。

---

## Image Audit

画像は、ProjectORIGINにおける情報資産として監査する。

監査対象には、以下を含む。

- 背景画像
- 写真
- 地図
- 資料画像
- AI Visualization
- ロゴ
- アイコン

監査では、Image Ruleに基づき、ライセンス、出典、品質、キャプション、配置および本文との整合性を確認する。

---

## Rule Document Audit

ProjectORIGIN全体で使用するルール文書を監査対象とする。

対象文書は、以下を含む。

- Audit Rule
- Research Bible
- Image Rule
- Database Rule
- Operating Manual
- AGENTS.md

監査では、役割分離、内容の整合性、Version管理および相互参照の適切性を確認する。

---

## Template Audit

テンプレート文書を監査対象とする。

対象文書は、以下を含む。

- Research Template
- Master Case File Template
- Case File Template

監査では、テンプレート構成、品質基準との整合性、Version管理および他文書との互換性を確認する。

---

## Flow Audit

制作フロー全体を監査対象とする。

標準的な制作フローは以下のとおりとする。

1. Research
2. Master Case File
3. FREE Case File
4. CLASSIFIED Case File
5. Image制作
6. Database更新
7. AI監査
8. 人間による承認
9. 公開

監査では、各工程が所定の順序で実施され、必要な監査および承認が完了していることを確認する。

---

## AI Operation Audit

AI運用も監査対象とする。

監査では、以下を確認する。

- AIの役割分離
- Template準拠
- Audit Rule準拠
- 制作工程との整合性
- 品質評価の一貫性
- 改善提案の妥当性

AIが定義されていない役割を実施していないことも確認対象とする。

---

## Exclusions

本Audit Ruleでは、以下を監査対象外とする。

- 新規事件の調査
- Research本文の制作
- Master Case File本文の制作
- FREE・CLASSIFIED本文の制作
- デザイン制作
- 実装・プログラム開発
- 公開可否の最終決定

これらは各専用チャットおよび最終承認者の責任範囲とする。

---

## Long-Term Scope

ProjectORIGINでは、監査対象が今後も継続的に増加することを前提とする。

そのため、本Audit Scopeは特定の事件や文書だけを対象とするものではなく、新たに追加される事件ファイル、テンプレート、ルール文書および関連資産にも適用できる共通基準として運用する。

監査対象の追加または変更を行う場合は、Version管理および承認手順に従い、本Audit Ruleへ反映する。

# Chapter 4
# Quality Checklist

## Purpose

本章では、ProjectORIGIN全体で共通して使用する品質チェックリストを定義する。

Quality Checklistは、成果物が定められた品質基準を満たしているかを確認するための監査基準であり、Research・Master Case File・FREE・CLASSIFIED・Database・画像・ルール文書・テンプレートに適用する。

本チェックリストは、公開可否を判断するための共通基準であり、監査担当や対象が異なっても一貫した品質評価を実現することを目的とする。

---

## Checklist Structure

Quality Checklistは、以下の三段階で構成する。

### Critical

公開可否に直接影響する必須項目。

Critical項目を満たしていない成果物は、公開対象としない。

---

### Standard

品質を維持するために確認する標準項目。

重大な問題ではないが、必要に応じて修正および再監査を行う。

---

### Recommended

品質向上を目的とした推奨項目。

未達成であっても公開は可能とするが、改善提案として記録する。

---

## Critical Checklist

すべての成果物について、以下を必須確認項目とする。

- 承認済みテンプレートに準拠している。
- 必須セクションに欠落がない。
- 役割を逸脱していない。
- Researchを基準とした整合性が維持されている。
- 情報分類が適切である。
- 必要な出典およびReferencesが整理されている。
- 適用Versionが最新である。
- Rule Documentsとの矛盾がない。

いずれか一項目でも満たしていない場合は、Critical Issueとして記録する。

---

## Standard Checklist

品質維持のため、以下を確認する。

- 表記が統一されている。
- 用語が統一されている。
- 時系列に矛盾がない。
- Database情報と一致している。
- Related Casesが適切である。
- Category、TagsおよびMetadataが統一されている。
- Image Ruleに準拠している。
- Version Historyが更新されている。
- 更新履歴が適切に記録されている。

問題が確認された場合は、修正対象として記録する。

---

## Recommended Checklist

品質向上のため、以下を確認する。

- 読みやすい構成である。
- 情報の重複がない。
- 将来の更新が容易である。
- 長期運営を考慮した構造となっている。
- AIによる監査および制作が容易である。
- 関連事件との接続性が適切である。

必要に応じて改善提案として記録する。

---

## Document-Specific Checklist

共通チェックリストに加え、成果物ごとの監査項目を適用する。

### Research

- Research Templateへの準拠
- 出典管理
- Reliability Assessment
- Source Management
- Unverified Information
- Research Tasks
- AI Notes

---

### Master Case File

- Researchとの整合性
- 情報分類
- 中立性
- References
- Master Templateへの準拠

---

### FREE Case File

- OVERVIEWが概要として適切である。
- FACTSがResearchおよびMasterと一致している。
- THEORIESが客観的に整理されている。
- FREE版として適切な情報量である。

---

### CLASSIFIED Case File

- Masterとの整合性
- 詳細資料
- 一次資料
- 証言
- AI Analysis
- References

---

### Database

- 基本情報
- Category
- Tags
- Coordinates
- Related Cases
- Metadata
- 重複の有無

---

### Image Assets

- ライセンス
- 出典
- キャプション
- 解像度
- Image Rule準拠
- 本文との整合性

---

### Rule Documents

- 役割分離
- 相互参照
- Version整合性
- 他文書との矛盾がない。

---

### Template Documents

- 構成の統一
- 品質基準との整合性
- Rule Documentsとの互換性
- Version管理

---

## Audit Evaluation

Quality Checklistに基づく監査結果は、以下の区分で評価する。

| 判定 | 内容 |
|------|------|
| PASS | すべてのCritical項目を満たしており、公開可能である。 |
| PASS WITH MINOR REVISION | 公開可能であるが、軽微な改善を推奨する。 |
| REVISION REQUIRED | 修正後に再監査を実施する。 |
| FAIL | Critical項目を満たしておらず、公開不可とする。 |

監査結果には、判定理由を記録する。

---

## Audit Record

監査結果には、少なくとも以下を記録する。

- Audit ID
- Audit Date
- Audit Target
- Target Version
- Auditor
- Audit Result
- Critical Issues
- Standard Issues
- Recommended Improvements
- Overall Comment

監査記録は、Version管理および品質改善の基礎資料として保存する。

---

## Checklist Maintenance

Quality Checklistは固定されたものではなく、ProjectORIGIN全体の運用状況に応じて継続的に見直す。

新しいテンプレート、ルール文書または制作工程が追加・更新された場合は、本チェックリストも必要に応じて改訂する。

変更を行う場合は、所定のVersion管理および承認手順に従い、Version Historyへ記録する。

---

## Long-Term Operation

Quality Checklistは、一時的な案件や特定の事件に依存しない共通品質基準として運用する。

ProjectORIGINで1000件以上の事件ファイルを管理する場合でも、同一の品質基準で監査を実施できるよう、再利用性、拡張性および保守性を維持する。

# Chapter 5
# Evidence Verification

## Purpose

本章では、ProjectORIGINにおける証拠および出典情報の監査基準を定義する。

Evidence Verificationは、成果物に記載された情報が適切な根拠に基づいて管理されていることを確認し、事実・証言・仮説・AI分析の区分が一貫して維持されていることを保証することを目的とする。

本章は、Research Bibleで定義された調査基準および出典管理方針を前提とし、それらが成果物へ適切に反映されているかを監査するための基準を定める。

---

## Verification Principles

Evidence Verificationは、以下の原則に基づいて実施する。

- 情報は確認可能な根拠に基づいていること。
- 出典と本文の対応関係が明確であること。
- 推測を根拠として扱わないこと。
- Researchに記録されていない情報を新たに追加しないこと。
- 証拠の有無と記述内容が一致していること。
- 情報分類が適切に維持されていること。

監査担当AIは、新たな証拠を補完したり、独自の判断で内容を修正したりしてはならない。

---

## Evidence Classification

Evidenceは、以下の区分に基づいて監査する。

| 区分 | 内容 |
|------|------|
| Primary Evidence | 一次資料（公文書、公式記録、当時の資料など） |
| Secondary Evidence | 二次資料（書籍、論文、調査記事など） |
| Witness Testimony | 証言 |
| Physical Evidence | 写真、映像、物的資料 |
| Historical Record | 歴史資料、新聞記事、年代記録 |
| AI Analysis | AIによる分析・整理 |

AI Analysisは、既存のEvidenceを整理・分析した結果として扱い、Evidenceそのものとして扱わない。

---

## Source Verification

監査では、Evidenceに対応する出典情報を確認する。

確認項目は、以下のとおりとする。

- 出典が明記されている。
- 出典がResearchに記録されている。
- 出典情報に欠落がない。
- Referencesと一致している。
- 引用と要約が適切に区別されている。
- 出典情報が重複または矛盾していない。

出典を確認できない情報は、Evidenceとして確定しない。

---

## Information Classification Verification

成果物に含まれる情報分類を監査する。

確認対象は、以下の区分とする。

- FACT
- TESTIMONY
- THEORY
- HYPOTHESIS
- AI ANALYSIS

各情報が適切な区分で扱われていることを確認し、分類が混在または誤用されている場合は監査結果へ記録する。

---

## Consistency Verification

Evidenceは、関連する成果物間で整合性を維持していなければならない。

監査では、以下の対応関係を確認する。

- ResearchとMaster Case File
- Master Case FileとFREE Case File
- Master Case FileとCLASSIFIED Case File
- Referencesと本文
- Databaseと本文

不整合が確認された場合は、監査担当AIが修正を行わず、問題内容および影響範囲を記録する。

---

## Unsupported Information

以下に該当する情報は、根拠未確認情報として扱う。

- 出典が存在しない。
- 出典を確認できない。
- Researchに記録されていない。
- 情報源が特定できない。
- 推測のみを根拠としている。
- AIが独自に補完した内容である。

根拠未確認情報は、事実として評価せず、監査結果へ記録する。

---

## Image Evidence Verification

画像は、Evidenceを補助する情報資産として監査する。

確認項目は、以下のとおりとする。

- 出典
- ライセンス
- キャプション
- 本文との整合性
- Image Ruleへの準拠
- AI生成画像である場合の明示

画像のみを根拠として本文の事実を確定してはならず、関連するEvidenceおよび出典とあわせて評価する。

---

## AI Analysis Verification

AI Analysisは、Evidenceに基づく分析として監査する。

確認項目は、以下のとおりとする。

- 根拠となるEvidenceが明確である。
- 新しい事実を追加していない。
- 推測を事実として扱っていない。
- 分析とEvidenceが明確に区別されている。
- 客観的な記述である。

Evidenceを伴わないAI Analysisは、品質上の問題として記録する。

---

## Audit Result

Evidence Verificationの監査結果は、以下の区分で記録する。

| 判定 | 内容 |
|------|------|
| Verified | 根拠が確認され、適切に管理されている。 |
| Verified with Notes | 根拠は確認できるが、補足または改善を推奨する。 |
| Needs Verification | 根拠の確認が不十分であり、追加確認が必要である。 |
| Unsupported | 根拠を確認できず、Evidenceとして採用できない。 |

判定結果には、対象項目および判定理由を記録する。

---

## Responsibilities

Evidence Verificationにおける役割を以下のとおり定義する。

| 担当 | 役割 |
|------|------|
| 制作担当AI | ResearchにEvidenceおよび出典を整理し、成果物へ反映する。 |
| 監査担当AI（Codexを想定） | Evidence、出典、情報分類および整合性を監査し、問題点および改善提案を提示する。 |
| 人間 | 監査結果を確認し、Evidenceの採用、差し戻しおよび公開可否を最終判断する。 |

監査担当AIは、Evidenceの内容を変更せず、Evidenceが適切に管理されているかを評価する。

---

## Long-Term Operation

Evidence Verificationは、ProjectORIGINに蓄積されるすべての事件ファイルに対して共通に適用する。

事件数や出典数が増加した場合でも、一貫した基準でEvidenceを監査できるよう、Evidenceの分類、出典管理、情報分類および監査記録を標準化し、長期的な品質保証を維持する。

# Chapter 6
# Consistency Audit

## Purpose

本章では、ProjectORIGIN全体における成果物の整合性を監査するための基準を定義する。

ProjectORIGINでは、一つの事件に対してResearch、Master Case File、FREE、CLASSIFIED、Database、画像など複数の成果物が作成される。

Consistency Auditは、それぞれの成果物が共通の基準に基づいて一貫性を維持し、情報、構成、Versionおよび役割に矛盾が生じていないことを確認することを目的とする。

監査担当AIは整合性を評価し、不整合を検出・記録することを責務とし、成果物を直接修正してはならない。

---

## Audit Principles

Consistency Auditは、以下の原則に基づいて実施する。

- Researchを基準資料として監査する。
- 成果物間の情報を一貫して管理する。
- 各成果物の役割を維持する。
- Version間の整合性を確認する。
- 不整合を検出した場合は修正せず記録する。

監査では、どの成果物が正しいかを独自に判断せず、不整合の有無および影響範囲を客観的に評価する。

---

## Research Consistency

Researchは、ProjectORIGINにおけるすべての成果物の基準資料である。

監査では、以下を確認する。

- Researchに存在しない情報が後続成果物へ追加されていない。
- 出典およびEvidenceが一致している。
- Reliability Assessmentとの整合性が維持されている。
- 情報分類が適切である。
- Unverified Informationが事実として扱われていない。

Researchとの不整合は、後続成果物全体へ影響する重要事項として記録する。

---

## Master Case File Consistency

Master Case Fileは、Researchを基に構成される正式資料である。

監査では、以下を確認する。

- Researchとの整合性
- 情報の追加または欠落の有無
- 情報分類
- References
- 中立的な記述
- テンプレートへの準拠

Master Case Fileは、FREEおよびCLASSIFIEDの基準資料として一貫性を維持する。

---

## FREE Case File Consistency

FREE Case Fileは、Master Case Fileを基準とした公開版である。

監査では、以下を確認する。

- Masterに存在する情報のみを使用している。
- OVERVIEWが事件概要として適切である。
- FACTSがResearchおよびMasterと一致している。
- THEORIESが客観的に整理されている。
- FREE版として適切な情報量である。

FREE版独自の情報追加や解釈を行っていないことを確認する。

---

## CLASSIFIED Case File Consistency

CLASSIFIED Case Fileは、Master Case Fileを基準とした詳細資料である。

監査では、以下を確認する。

- Masterとの整合性
- 詳細情報の妥当性
- Evidenceとの対応
- 証言の整理
- AI Analysis
- References

詳細情報を追加する場合も、ResearchおよびMasterとの一貫性を維持する。

---

## Database Consistency

Databaseは、ProjectORIGIN全体の共通情報を管理する。

監査では、以下を確認する。

- File Number
- Case Name
- English Name
- Date
- Location
- Country
- Category
- Class
- Status
- Risk Level
- Tags
- Coordinates
- Related Cases

Databaseと各成果物の基本情報に不一致がないことを確認する。

---

## Image Consistency

画像は、本文を補助する情報資産として監査する。

監査では、以下を確認する。

- 本文との整合性
- キャプションとの一致
- Image Ruleへの準拠
- 出典
- ライセンス
- AI生成画像の明示

画像が本文と矛盾する情報を示していないことを確認する。

---

## Rule and Template Consistency

ProjectORIGIN全体で使用するルール文書およびテンプレート間の整合性を監査する。

対象は、以下を含む。

- Audit Rule
- Research Bible
- Image Rule
- Database Rule
- Operating Manual
- AGENTS.md
- Research Template
- Master Case File Template
- Case File Template

監査では、以下を確認する。

- 役割の重複
- 相互参照
- 用語の統一
- Version整合性
- 内容の矛盾

---

## Version Consistency

Version更新時には、関連成果物との整合性を確認する。

監査では、以下を確認する。

- 最新Versionを使用している。
- Rule更新が反映されている。
- 古いテンプレートを使用していない。
- Version Historyが一致している。
- 関連文書との互換性が維持されている。

Version番号だけでなく、変更内容の反映状況も監査対象とする。

---

## Audit Result

Consistency Auditの監査結果は、以下の区分で記録する。

| 判定 | 内容 |
|------|------|
| Consistent | 不整合は確認されなかった。 |
| Minor Inconsistency | 軽微な不整合が確認された。 |
| Major Inconsistency | 重要な不整合が確認され、修正が必要である。 |
| Critical Inconsistency | 基準資料との重大な矛盾があり、公開できない。 |

監査結果には、対象範囲、影響範囲および判定理由を記録する。

---

## Responsibilities

Consistency Auditにおける役割を以下のとおり定義する。

| 担当 | 役割 |
|------|------|
| 制作担当AI | Researchを基準として成果物を制作し、一貫性を維持する。 |
| 監査担当AI（Codexを想定） | 成果物間の整合性、役割およびVersionを監査し、不整合および改善提案を提示する。 |
| 人間 | 監査結果を確認し、修正、差し戻しおよび公開可否を最終判断する。 |

監査担当AIは、不整合を検出・報告することを責務とし、成果物の内容を直接修正しない。

---

## Long-Term Operation

Consistency Auditは、ProjectORIGIN全体を単一の知識基盤として維持するための品質保証基準である。

事件数、成果物および関連文書が増加した場合でも、Researchを基準とした一貫した監査を継続できるよう、成果物間の関係性、Version管理および役割分離を標準化し、長期的な品質維持を実現する。

# Chapter 7
# Version Audit

## Purpose

本章では、ProjectORIGINにおけるVersion管理の監査基準を定義する。

Version Auditは、ルール文書、テンプレート、成果物および関連資産が適切なVersionで管理され、変更内容が正しく反映されていることを保証するための品質監査である。

ProjectORIGINでは1000件以上の事件ファイルを長期的に運用することを前提とするため、Version管理は品質保証、保守性および継続的改善を支える重要な要素として位置付ける。

---

## Audit Principles

Version Auditは、以下の原則に基づいて実施する。

- 承認済みの最新Versionを基準として監査する。
- Version情報は追跡可能な状態で管理する。
- 更新内容と適用状況を確認する。
- 関連文書との整合性を維持する。
- Version番号だけでなく、変更内容も監査対象とする。

監査担当AIは、Versionの適用状況を評価するが、Version番号や履歴を独自に変更してはならない。

---

## Audit Targets

Version Auditの対象は、以下とする。

### Rule Documents

- Audit Rule
- Research Bible
- Image Rule
- Database Rule
- Operating Manual
- AGENTS.md

### Template Documents

- Research Template
- Master Case File Template
- Case File Template

### Case Files

- Research
- Master Case File
- FREE Case File
- CLASSIFIED Case File

### Database

- Database構造
- Metadata
- Category
- Tags

### Assets

- 画像
- 地図
- AI Visualization
- その他の関連資産

すべての対象について、適用Versionおよび関連Versionとの整合性を確認する。

---

## Version Verification

Version Auditでは、少なくとも以下を確認する。

- Version番号
- 更新日
- 更新内容
- 適用Version
- 承認状況
- 更新履歴
- 関連文書との対応状況

Version番号のみ一致していても、変更内容が反映されていない場合は適合と判断しない。

---

## Change Verification

更新内容について、以下を確認する。

- 更新理由が記録されている。
- 変更内容が明確である。
- 関連文書へ必要な更新が反映されている。
- 他の成果物への影響を確認している。
- Version Historyが更新されている。

更新の影響範囲が不明な場合は、追加確認が必要な項目として記録する。

---

## Cross-Version Consistency

Version更新時には、関連する成果物および文書との整合性を確認する。

対象例

- Research BibleとResearch Template
- ResearchとMaster Case File
- Master Case FileとFREE Case File
- Master Case FileとCLASSIFIED Case File
- Rule DocumentsとTemplate Documents
- DatabaseとCase File

Version更新によって関連文書との整合性が失われていないことを確認する。

---

## Deprecated Version Management

旧Versionの管理について監査する。

確認項目は、以下のとおりとする。

- 廃止Versionが新規成果物に使用されていない。
- 廃止Versionが明確に区別されている。
- 必要な互換性情報が記録されている。
- 更新対象が明確である。

旧Versionは履歴として保持するが、承認済みの最新Versionを標準として運用する。

---

## Version History Verification

Version Historyについて、以下を確認する。

- Version番号
- 更新日
- 更新内容
- 変更理由
- 影響範囲
- 承認状況

Version Historyは削除または上書きせず、継続的に記録する。

---

## AI Version Audit

監査担当AI（Codexを想定）は、以下を確認する。

- 最新Versionを参照している。
- 承認済みVersionを使用している。
- Rule更新が成果物へ反映されている。
- Version間の矛盾がない。
- Version Historyが適切に更新されている。

監査担当AIは、Version管理上の問題点を報告するが、Version情報を直接変更しない。

---

## Audit Result

Version Auditの監査結果は、以下の区分で記録する。

| 判定 | 内容 |
|------|------|
| Up-to-Date | 最新Versionが適用され、更新内容も反映されている。 |
| Update Recommended | 現在の運用に問題はないが、最新Versionへの更新を推奨する。 |
| Outdated | 旧Versionを使用しており、更新が必要である。 |
| Version Conflict | Version間に不整合があり、公開前に解決が必要である。 |

判定結果には、対象Versionおよび判定理由を記録する。

---

## Responsibilities

Version Auditにおける役割を以下のとおり定義する。

| 担当 | 役割 |
|------|------|
| 制作担当AI | 承認済みの最新Versionに基づいて成果物を制作・更新する。 |
| 監査担当AI（Codexを想定） | Versionの適用状況、更新履歴および整合性を監査し、問題点と改善提案を提示する。 |
| 人間 | Version更新を承認し、重大な変更および互換性への影響を最終判断する。 |

監査担当AIは、Version管理の品質を保証することを責務とし、Versionを独自に変更しない。

---

## Long-Term Operation

Version Auditは、ProjectORIGIN全体の品質保証を長期的に維持するための基盤である。

事件ファイル、テンプレートおよびルール文書が継続的に増加・更新される環境においても、Version情報を一貫して管理し、変更履歴、互換性および適用状況を追跡可能な状態で維持する。

これにより、ProjectORIGIN全体で安定した品質管理と継続的な運用を実現する。

# Chapter 8
# Publication Approval

## Purpose

本章では、ProjectORIGINにおける公開承認（Publication Approval）の基準を定義する。

Publication Approvalは、品質監査が完了した成果物について、公開可否を判断するための最終工程である。

ProjectORIGINでは、「制作」「監査」「承認」を明確に分離し、制作担当AI、監査担当AI（Codexを想定）および人間がそれぞれの責任範囲に従って品質管理を行う。

公開承認は、監査結果に基づいて実施し、成果物の品質、一貫性および運用基準への適合を最終確認することを目的とする。

---

## Approval Principles

公開承認は、以下の原則に基づいて実施する。

- 品質監査完了後に実施する。
- Audit Ruleに基づく監査結果を判断基準とする。
- 監査を省略して公開しない。
- 制作担当AI、監査担当AIおよび承認者の役割を分離する。
- 最終的な公開判断は人間が行う。

公開承認では、個人的な評価や主観ではなく、監査結果および品質基準に基づいて判断する。

---

## Publication Flow

ProjectORIGINにおける標準的な公開フローは、以下のとおりとする。

1. 制作担当AIによる成果物の制作
2. 監査担当AIによる品質監査
3. Audit Reportの作成
4. 人間による監査結果の確認
5. 公開承認
6. 公開

監査で修正が必要と判断された場合は、制作工程へ差し戻し、再監査を実施する。

---

## Approval Requirements

公開承認を行うためには、以下の条件を満たしている必要がある。

### 品質監査

- 品質監査が完了している。
- Audit Resultが記録されている。
- Critical Issueが解消されている。

### Version管理

- 承認済みの最新Versionを使用している。
- Version Historyが更新されている。

### Evidence

- Evidence Verificationが完了している。
- Referencesおよび出典管理が適切である。

### 整合性

- Researchとの整合性
- Masterとの整合性
- Databaseとの整合性
- Imageとの整合性

### ルール準拠

- テンプレートに準拠している。
- Rule Documentsと矛盾していない。
- Image Ruleなど関連ルールへ準拠している。

いずれかの条件を満たさない場合は、公開承認を行わない。

---

## Publication Status

公開状態は、以下の区分で管理する。

| Status | 内容 |
|--------|------|
| Draft | 制作中 |
| Under Audit | 品質監査中 |
| Awaiting Approval | 承認待ち |
| Approved | 公開承認済み |
| Published | 公開済み |
| Revision Required | 修正および再監査が必要 |
| Rejected | 公開不可 |

公開状態は、成果物およびDatabaseで一貫して管理する。

---

## Approval Decision

承認者は、監査結果を確認し、以下のいずれかを決定する。

### Approve

品質基準を満たしており、公開を承認する。

### Approve with Minor Revision

軽微な改善事項は存在するが、公開を承認する。

改善内容は、次回Versionで反映する。

### Return for Revision

修正が必要であり、制作工程へ差し戻す。

修正後は再監査を実施する。

### Reject

品質基準を満たしておらず、公開を承認しない。

重大な問題を解消した後、再度監査および承認を実施する。

---

## Audit Report Review

公開承認では、Audit Reportを確認する。

少なくとも以下を確認対象とする。

- Audit Result
- Critical Issues
- Standard Issues
- 改善提案
- Version
- Audit Date
- Auditor

Audit Reportは公開判断の基礎資料として扱い、監査担当AIの提案をそのまま採用するものではない。

---

## Responsibilities

Publication Approvalにおける役割を以下のとおり定義する。

| 担当 | 役割 |
|------|------|
| 制作担当AI | 成果物を制作し、監査対象として提出する。 |
| 監査担当AI（Codexを想定） | Audit Ruleに基づき品質監査を実施し、Audit Reportを作成する。 |
| 人間 | Audit Reportを確認し、公開、差し戻しまたは却下を最終判断する。 |

監査担当AIは公開可否を決定せず、人間は成果物を制作しない。

---

## Re-Audit Policy

以下の場合は、再監査を実施する。

- Researchが更新された場合
- Master Case Fileが更新された場合
- Rule Documentsが更新された場合
- Template Documentsが更新された場合
- Evidenceが追加または変更された場合
- Database情報が変更された場合
- Versionが更新された場合
- 画像または関連資料が変更された場合

再監査では、変更内容および影響範囲に応じて必要な監査を実施する。

---

## Publication Record

公開承認後は、公開履歴として以下を記録する。

- Publish Date
- Published Version
- Approval Date
- Approver
- Audit Version
- Audit ID
- Related Case
- Notes

公開履歴は、品質保証およびVersion管理の記録として継続的に保存する。

---

## Long-Term Operation

ProjectORIGINでは、1000件以上の事件ファイルを継続的に運用することを前提とする。

そのため、公開承認は単なる公開手続きではなく、品質保証の最終工程として位置付ける。

制作担当AI、監査担当AI（Codexを想定）および人間が、それぞれの責任範囲を維持しながら品質管理を実施することで、成果物の品質、一貫性および信頼性を長期的に維持する。

# Chapter 9
# Continuous Improvement

## Purpose

本章では、ProjectORIGINにおける品質管理の継続的改善（Continuous Improvement）の基準を定義する。

Continuous Improvementは、個々の成果物を改善することを目的とするものではなく、監査を通じて得られた知見を品質管理基盤へ反映し、ProjectORIGIN全体の品質、制作効率、保守性および長期運営性を継続的に向上させることを目的とする。

ProjectORIGINでは、品質管理を固定的な仕組みではなく、継続的に改善される運用基盤として管理する。

---

## Improvement Principles

継続的改善は、以下の原則に基づいて実施する。

- 同一の問題を繰り返さない。
- 個別対応ではなく仕組みの改善を優先する。
- 客観的な監査結果に基づいて改善する。
- 品質、一貫性および保守性を向上させる。
- AIによる制作および監査を支援する。
- 長期運営を前提として改善する。

改善は、承認済みの監査結果を基礎資料として実施する。

---

## Improvement Sources

改善の検討には、以下の情報を活用する。

- Audit Report
- Quality Checklist
- Evidence Verification
- Consistency Audit
- Version Audit
- Publication Approvalの結果
- 人間によるレビュー
- AIによる改善提案
- 運営上の課題

単一の事例だけではなく、継続的に発生する傾向や共通する課題を分析対象とする。

---

## Improvement Targets

改善対象は、ProjectORIGIN全体の品質管理基盤とする。

対象には、以下を含む。

### Rule Documents

- Audit Rule
- Research Bible
- Image Rule
- Database Rule
- Operating Manual
- AGENTS.md

### Template Documents

- Research Template
- Master Case File Template
- Case File Template

### 制作フロー

- 制作工程
- 品質監査工程
- 公開承認工程
- Version管理

### Database

- Metadata
- Category
- Tags
- Related Cases

### AI運用

- AI制作フロー
- AI監査フロー
- AI運用基準
- AIプロンプト管理

改善は、関連する文書および運用全体への影響を考慮して実施する。

---

## Improvement Process

継続的改善は、以下の手順で実施する。

1. 問題の検出
2. 原因分析
3. 改善提案
4. 関連文書の更新
5. Version更新
6. 承認
7. 運用開始
8. 効果確認

改善内容は、承認後に関連文書へ反映し、Version Historyへ記録する。

---

## Preventive Improvement

継続的改善では、問題が発生した後の対応だけではなく、将来発生する可能性がある問題を未然に防ぐ改善も実施する。

対象例

- テンプレートの標準化
- 用語の統一
- 品質チェック項目の追加
- AI運用の最適化
- Database構造の改善
- 重複防止の仕組み

予防的改善は、長期的な品質維持および運用負荷の低減を目的とする。

---

## AI Improvement Policy

監査担当AI（Codexを想定）は、監査結果を基に改善提案を行うことができる。

ただし、AIはルール、テンプレートまたは運用基準を自動的に変更してはならない。

改善は、人間による承認を経て、Version管理手順に従って正式に反映する。

これにより、品質管理基準の一貫性および再現性を維持する。

---

## Performance Evaluation

継続的改善では、品質だけでなく運用効率も評価対象とする。

評価対象例

- 品質向上
- 修正件数の推移
- 再監査率
- Rule違反件数
- 重複作業の削減
- AI監査時間
- 人間による確認時間
- Version更新の安定性

評価結果は、品質改善の参考資料として活用する。

---

## Responsibilities

Continuous Improvementにおける役割を以下のとおり定義する。

| 担当 | 役割 |
|------|------|
| 制作担当AI | 改善後のルールおよびテンプレートに基づいて成果物を制作する。 |
| 監査担当AI（Codexを想定） | 改善が必要な傾向を分析し、改善提案を行う。 |
| 人間 | 改善提案を評価・承認し、ルール、テンプレートおよび運用へ反映するかを最終判断する。 |

監査担当AIは改善提案を行うが、品質基準を独自に変更しない。

---

## Continuous Monitoring

品質改善は、一度実施して終了するものではない。

ProjectORIGINでは、監査結果、Version更新および運用状況を継続的に確認し、改善の効果を評価する。

改善によって新たな課題が発生した場合は、再度分析を行い、必要に応じて改善プロセスを繰り返す。

---

## Long-Term Operation

ProjectORIGINでは、1000件以上の事件ファイルおよび関連資産を長期的に運用することを前提とする。

そのため、Continuous Improvementは、個別の成果物ではなく、ProjectORIGIN全体の品質管理システムを継続的に改善するための運用基盤として位置付ける。

監査を通じて得られた知見をルール、テンプレート、制作フローおよびAI運用へ適切に反映することで、品質、一貫性、制作効率および保守性を継続的に向上させ、長期的に安定した品質保証体制を維持する。

# Version History

---

# Audit Rule v1.1

**Release Date**  
2026-08-03

## Overview

Audit Rule v1.0を基準として、Compatibility情報を最新の正式文書構成へ更新した。

本Versionでは、ProjectORIGIN全体の監査基準および運用ルールは変更せず、Database RuleとのVersion整合性のみを修正した。

---

## Changes

### Compatibility Update

Compatibilityに記載するDatabase Ruleの対応Versionを、正式なSingle Source of Truthに合わせて更新した。

- Database Rule **v2.0 → v2.2**

監査基準、運用方針および各Chapterの本文には変更を加えていない。

---

# Audit Rule v1.0

**Release Date**  
2026-07-26

## Overview

ProjectORIGINにおける品質監査および品質保証の正式基準として、Audit Rule v1.0を初版リリースした。

本Versionでは、ProjectORIGIN全体を対象とした品質監査の目的、原則、監査範囲、品質評価、証拠確認、整合性確認、Version管理、公開承認および継続的改善の基準を定義した。

また、ProjectORIGINが1000件以上の事件ファイルを長期的に運用することを前提とし、**「AIが制作し、AIが監査し、人間が最終承認する」**品質管理モデルを正式な運用方針として採用した。

---

## Chapters

- Chapter 1 — Mission
- Chapter 2 — Audit Principles
- Chapter 3 — Audit Scope
- Chapter 4 — Quality Checklist
- Chapter 5 — Evidence Verification
- Chapter 6 — Consistency Audit
- Chapter 7 — Version Audit
- Chapter 8 — Publication Approval
- Chapter 9 — Continuous Improvement

---

## Major Changes

### Initial Audit Framework

ProjectORIGIN全体で共通して使用する品質監査基準を新規策定した。

品質監査の目的、責任範囲および監査対象を明確化し、制作工程から独立した品質保証体制を定義した。

---

### AI-First Quality Assurance

制作担当AI、監査担当AI（Codexを想定）および人間の責任範囲を明確に分離し、AIを中心とした品質監査モデルを正式に採用した。

監査担当AIは品質評価および改善提案を担当し、成果物の制作・修正は行わないことを明文化した。

---

### Standardized Audit Criteria

Research、Master Case File、FREE Case File、CLASSIFIED Case File、Database、画像、テンプレートおよびルール文書を共通基準で監査する品質評価体系を策定した。

---

### Quality Checklist

Critical、StandardおよびRecommendedの三段階による品質チェックリストを導入し、公開判定および再監査の共通基準を定義した。

---

### Evidence Verification

Evidence、出典、情報分類およびAI Analysisを対象とした監査基準を整備し、Research Bibleに基づく証拠管理との整合性を確立した。

---

### Consistency Audit

Researchを基準資料とし、成果物間、Database、画像、テンプレートおよびルール文書との整合性を監査する基準を定義した。

---

### Version Audit

Version管理、更新履歴、互換性および関連文書への反映状況を監査する基準を整備し、長期運用における保守性を強化した。

---

### Publication Approval

品質監査完了後に人間が最終承認を行う公開承認フローを正式に定義した。

公開判断は監査結果に基づいて実施し、制作・監査・承認の責任範囲を明確に分離した。

---

### Continuous Improvement

監査結果を品質管理基盤へ継続的に反映する改善サイクルを定義し、ルール、テンプレート、制作フローおよびAI運用を継続的に改善する運用方針を策定した。

---

## Compatibility

| Document | Compatible Version |
|----------|--------------------|
| AGENTS.md | v1.0 |
| Research Bible | v1.0 |
| Research Template | v1.0 |
| Master Case File Template | v1.0 |
| Case File Template | v1.0 |
| Database Rule | **v2.2** |
| Image Rule | v1.0 |
| Operating Manual | v1.0 |

---

## Operational Notes

- Audit Ruleは、ProjectORIGIN全体の品質監査および品質保証基準のみを管理する。
- 成果物（Research、Master Case File、FREE、CLASSIFIED）の制作・編集・修正は行わない。
- 監査担当AIは品質評価、問題点の抽出および改善提案を担当し、成果物を直接変更しない。
- 人間は監査結果を基に公開可否およびVersion更新を最終承認する。
- 監査基準の変更は、承認済みのVersion管理手順に従って実施する。

---

## Status

**Audit Rule v1.1** を、ProjectORIGINにおける品質監査および品質保証の正式設計書として採用する。