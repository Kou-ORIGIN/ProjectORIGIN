**ProjectORIGIN Repository Rule**
Version: v1.0
**Status:** Official
**Project:** ProjectORIGIN

---

# Chapter 1

# Mission, Authority and Scope

## 1.1 Purpose

ProjectORIGIN Repository Ruleは、ProjectORIGINにおける正式なProduction Artifactおよび関連成果物のRepository上での配置、識別、管理および統合に関する基準を定義する正式文書である。

ProjectORIGINは、1000件以上のCaseを長期的かつ継続的に制作、監査、更新および公開することを前提とする。

本書は、Case数および成果物数が増加した場合でも、各Caseおよび各Production Artifactを一貫した構造で管理し、成果物の責務、Version、状態および関係性を追跡できるRepository環境を維持することを目的とする。

---

## 1.2 Mission

Repository Ruleの使命は、ProjectORIGINの正式なProduction ArtifactがRepository上で一貫して管理され、異なるCase、Production Layer、Versionおよび成果物が混同されない状態を維持することである。

Repository Ruleは、以下を実現するためのRepository管理基準を提供する。

- Case単位での成果物管理
- Production Artifact間の責務分離
- Artifactの識別
- Artifact Versionの識別
- Repository上の配置の一貫性
- Production WorkflowとRepository状態の整合
- Approved ArtifactのRepository Integration
- Artifact間のTraceability
- Repository変更時の互換性維持
- 長期的なRepository保守性および拡張性

Repository Ruleは、個々の成果物の内容または制作方法を定義するものではない。

---

## 1.3 Authority

Repository Ruleは、ProjectORIGINにおけるProduction ArtifactのRepository上の配置、識別、管理およびRepository Integrationについて、本書のScopeに属する事項の正式なSource of Truthとして使用する。

本書は、他の正式なSource of Truthが保持する専門仕様を変更、無効化または置換しない。

Database、Research、Case File、Image、Art、Audit、AI Production、Developmentその他の専門領域に正式なSource of Truthが存在する場合、その専門仕様はそれぞれの正式文書に従う。

Repository Ruleと他の正式文書との間に不一致が確認された場合は、対象事項のResponsibility Scopeを確認し、その事項を正式に管理するSource of Truthを優先する。

責務の所在を確認できない場合は、推測によって仕様を補完せず、未確認または未確定として扱う。

---

## 1.4 Scope

Repository Ruleは、以下を対象とする。

- Case単位のRepository Structure
- Production ArtifactのRepository Layer
- Production Artifactの配置
- Artifact Filename
- Artifact VersionのRepository上の識別
- Case Workflow Statusの正式な名称およびRepository上の状態管理原則
- Publication StatusのRepository上の管理原則
- Repository Integration
- Production Artifact間のTraceability
- Repository Integrity
- Repository Structure変更時のCompatibility Principle
- 長期的なRepository運用原則
- Repository Rule自身のVersion Management

本書は、Repository上で正式成果物をどのように整理、識別および管理するかを定義する。

---

## 1.5 Out of Scope

Repository Ruleは、以下を直接管理しない。

### Project-wide Operation

Chat Structure、Project全体のWorkflow、Document Management、長期運営方針その他のProject-wide OperationはOperating Manualの責務とする。

### AI Agent Operation

AI Agentの行動、Production Workflow上の役割、責任境界、Audit Gate、Automation BoundaryおよびHuman Approvalへの移行条件はAGENTS.mdの責務とする。

Production Workflowの工程順序、Agent制御、Audit Gateおよび自動進行条件はAGENTS.mdの責務とし、Repository Ruleはそれらを変更または置換しない。

### Database Specification

Database Field、Data Type、Controlled Values、Nullability、Validation、Relationship、Metadataその他のDatabase仕様はDatabase RuleおよびDatabase Schemaの責務とする。

Repository Ruleは、Case Workflow StatusのRepository上の正式定義および状態管理原則を管理する。

Databaseへ保存するField、Data Type、Nullability、Validationその他のDatabase Schema仕様は、Database RuleおよびDatabase Schemaの責務とする。

Repository RuleとDatabase RuleまたはDatabase Schemaの間で整合が必要となる場合、一方の正式仕様を独自に変更せず、Applicable Source of Truth間の整合性を確認し、必要な正式変更工程を経て整合性を維持する。

### Research Specification

Researchの調査方法、Source、Evidence、Fact、Claim、Theory、Hypothesis、ReliabilityおよびResearch Artifact内部の構造はResearch BibleおよびResearch Templateの責務とする。

### Case File Specification

Master Case File、FREE、CLASSIFIEDその他のCase File内部構造、SectionおよびWriting Ruleは、それらを管理する正式Templateの責務とする。

### Image and Art Specification

画像分類、Source、License、Caption、画像制作、Art DirectionおよびVisual Designは、それぞれImage RuleおよびArt Bibleの責務とする。

### Audit Specification

監査方法、Audit Criteria、PASS、REVISION、BLOCKERその他の品質監査基準はAudit Ruleの責務とする。

Repository RuleはAudit ArtifactのRepository上の管理を扱うことができるが、Audit Ruleが保持する監査方法および判定基準を変更しない。

### Implementation

UI、UX、Application Architecture、Code、Runtime、具体的な実装技術およびGit Commandそのものは、本書の直接の責務としない。

---

## 1.6 Logical Layer and Physical Repository Structure

ProjectORIGINにおけるProduction Layerの論理的な責務分離と、Repository上の物理的なDirectory Structureは区別して管理する。

AGENTS.mdその他の正式文書が定義するResearch Layer、Master Layer、Publication Layer、Asset Layer、Audit Layerその他の論理的責務は、それだけを根拠として特定の物理Directory Structureを意味するものではない。

物理的なRepository Structureについて、本書のScopeに属する事項はRepository Ruleで正式に定義する。

論理的な責務と物理的な配置を混同しない。

---

## 1.7 No-Assumption Principle

Repository上に新しいDirectory、Artifact Category、Filename Convention、Version Conventionまたは管理構造が必要になった場合、既存の正式仕様から確認できない内容を推測によって追加してはならない。

一般的なRepository設計、開発慣行、類似Projectまたは過去の不完全な記憶だけを根拠として、ProjectORIGINの正式なRepository仕様を作成しない。

必要な仕様が本書または他の正式なSource of Truthに存在しない場合は、未定義として扱い、必要なReview、Human Decisionおよび正式なVersion更新を経て追加する。

---

## 1.8 Single Source of Truth Principle

Repository管理に関する同一の正式仕様を、複数の正式文書へ重複して定義しない。

Repository RuleのScopeに属する正式仕様は本書で管理し、他の正式文書から必要な場合は本書を参照する。

一方、他の正式文書が正式に管理する専門仕様をRepository Ruleへ複製し、新たな管理元として扱ってはならない。

これにより、同一仕様に複数の異なる正式定義が発生することを防止する。

---

## 1.9 Long-Term Objective

Repository Ruleは、ProjectORIGINが1000件以上のCaseを管理する状態を前提として設計する。

Case、Research、Master Case File、Publication Artifact、Asset、Audit Artifactその他の正式成果物が増加した場合でも、特定のCaseまたは一時的なProduction工程だけに依存しないRepository Structureを維持する。

Repository Structureは、長期的な保守性、追跡性、拡張性および変更影響の局所化を優先する。

---

## 1.10 Core Principle

Repository Ruleの基本原則は、

\*\*「何を制作するか」ではなく、「正式に制作されたものをRepository上でどのように配置、識別、追跡および統合するか」を管理すること\*\*

である。

Repository RuleはResearch、Case File、Image、Auditその他の専門仕様を決定しない。

各専門Source of Truthが定義する成果物を、ProjectORIGINのRepository上で長期的かつ一貫して管理できる状態を維持する。

# Chapter 2

# Repository Principles

## 2.1 Purpose

本章は、ProjectORIGIN Repository全体に共通して適用するRepository管理の基本原則を定義する。

本章で定義する原則は、Case数、Production Artifact数、Version数および関連Asset数が増加した場合でも、Repository上の成果物を一貫して識別、配置、追跡および管理できる状態を維持することを目的とする。

Repository Structure、Artifact配置、Filename、Version、Workflow State、Repository Integrationその他の本書のScopeに属する仕様は、本章の基本原則に従って設計および管理する。

---

## 2.2 Case-Centered Management

ProjectORIGINのProduction Artifactは、原則として対象となるCaseとの関係を明確にした状態で管理する。

Caseに属するResearch、Master Case File、Publication Artifact、Asset、Audit Artifactその他の関連成果物は、どのCaseに属する成果物であるかをRepository上で識別可能な状態にする。

異なるCaseの成果物を、所属Caseを判別できない状態で混在させてはならない。

Case単位の管理は、特定のCaseだけを対象とした一時的な運用ではなく、ProjectORIGIN全体に共通するRepository管理原則として適用する。

具体的なCase Directory Structureは、本書のCase Repository Structureに関するChapterで定義する。

---

## 2.3 Responsibility Separation

Repository上の各Production ArtifactおよびRepository Layerは、それぞれ定義された責務に従って管理する。

Research、Master、Publication、Asset、Auditその他の責務が異なる成果物を、責務を区別できない状態で管理してはならない。

物理的に同一Caseの配下で管理される場合でも、各Artifactの責務は独立して維持する。

一つのArtifactまたはRepository Layerを、異なる責務を持つ複数の正式成果物の代替として扱ってはならない。

具体的なArtifact Layerおよび物理配置は、本書のProduction Artifact and Repository Layersに関するChapterで定義する。

---

## 2.4 Repository Source of Truth

Repository RuleのScopeに属する正式なProduction ArtifactのRepository上の管理では、同一のCase、Artifact TypeおよびVersionについて、正式な管理対象を一意に識別できる状態を維持する。

同一のCase、同一のArtifact Typeおよび同一のVersionについて、どれが正式な管理対象であるか判断できない複数のArtifactを並立させてはならない。

Backup、Working Copy、Exportその他の補助的なCopyが必要となる場合でも、それらを正式なRepository上の管理対象と混同してはならない。

正式Artifactと補助的Artifactの区別方法について正式仕様が必要となる場合は、推測によって追加せず、本書またはApplicable Source of Truthの正式な変更工程を経て定義する。

本原則は、Artifact内部の情報内容、Database Data、Research Factその他の専門領域におけるSingle Source of TruthをRepository Ruleへ移管するものではない。

---

## 2.5 Explicit Identification

正式なProduction Artifactは、Repository上でその対象および役割を識別可能な状態で管理する。

必要に応じて、以下の関係を判別できる状態を維持する。

- 対象Case
- Artifact Type
- Artifact Version
- Production Layer
- Publication区分
- WorkflowまたはApproval上の状態
- 関連する正式Artifact

識別に使用する具体的なFilename、Directory、Version表記またはMetadata仕様は、それぞれの責務を持つ正式仕様に従う。

本章は、識別可能性の原則を定義するものであり、Database FieldまたはMetadata Schemaを独自に定義しない。

---

## 2.6 Traceability

Production Artifactは、Applicable Source of Truthで定義されたProduction Flowに従い、その生成元、承認済み上流成果物、関連Audit Artifactおよび後続成果物との関係を必要な範囲で追跡できる状態で管理する。

ResearchからMaster Case File、Master Case FileからPublication Artifactへ情報が継承される場合、その間に必要とされるAuditおよびApproval状態を含め、正式なProduction Flowを逆転または省略したものとしてRepository上の関係を記録してはならない。

Audit Artifact、Assetその他の関連成果物についても、対象となるCaseまたはArtifactとの関係を識別可能な状態にする。

Traceabilityは、同一内容を複数のArtifactへ不必要に複製することによって実現してはならない。

Repository RuleはProduction Flowそのもの、Audit GateまたはApproval条件を本Sectionによって新たに定義しない。

具体的なTraceabilityの管理方法は、本書のIntegrity and Traceabilityに関するChapterおよびApplicable Source of Truthに従う。

---

## 2.7 Version Distinction

異なるVersionの正式Artifactは、Repository上で区別できる状態を維持する。

Version更新によって、どの成果物がどのVersionであるか確認できなくなる状態を作ってはならない。

新しいVersionの作成を理由として、過去Versionとの関係、更新対象または正式状態が不明確になる管理を行わない。

具体的なArtifact VersionおよびFilename Conventionは、本書のArtifact Naming and Versioningに関するChapterで定義する。

Versionの意味、更新条件または専門文書側のVersion Ruleが別の正式Source of Truthによって定義されている場合は、その責務を尊重する。

---

## 2.8 Repository Integrity

Repositoryは、正式成果物の所属、責務、Versionおよび関係性を一貫して確認できる状態を維持する。

以下の状態を避ける。

- Case所属を確認できない正式Artifact
- Artifact Typeを判別できない正式Artifact
- Versionを判別できないVersion管理対象Artifact
- 同一の正式Artifactが複数存在し、どれが正式管理対象か判断できない状態
- Production Layer間の責務が混在した状態
- 関連Artifactとの関係を必要な範囲で追跡できない状態
- Repository Ruleで定義されていない構造が正式仕様として無断で追加された状態

Repository Integrityに問題が確認された場合、推測によって正式状態を補完せず、確認可能な情報およびApplicable Source of Truthに基づいて状態を確認する。

---

## 2.9 Change Impact Isolation

Repository StructureまたはArtifact管理仕様の変更による影響は、可能な限り局所化する。

一つのCase、Artifact Type、LayerまたはVersionに対する変更が、関係のないCaseまたは成果物へ不要な変更を要求する構造を避ける。

新しいCase、Artifact Typeまたは将来のProduction要件を追加する場合も、既存Repository全体を不必要に再構成しなければならない設計を原則として採用しない。

ただし、正式な構造変更がProjectORIGIN全体のIntegrity維持に必要な場合は、変更影響を確認した上で、本書のChange and Compatibility Principlesに従って管理する。

---

## 2.10 Long-Term Maintainability

Repository Structureは、現在の少数Caseだけではなく、ProjectORIGINが1000件以上のCaseを継続的に管理する状態を前提として維持する。

CaseおよびProduction Artifactが増加しても、

- 特定のCaseを識別できること
- 必要なArtifactへ到達できること
- Artifactの責務を判別できること
- Versionを区別できること
- 関連成果物を追跡できること
- 新規Caseを既存Caseと同じ基本原則で追加できること

を維持する。

短期的な作業効率だけを理由として、長期的なRepository Integrity、TraceabilityまたはMaintainabilityを損なう構造を正式仕様として採用しない。

---

## 2.11 Technology Independence

Repository Ruleは、特定のOperating System、Development Environment、Editor、Application、Programming LanguageまたはRepository Hosting Serviceだけに依存する設計原則を定義しない。

具体的な実装環境またはToolが将来変更された場合でも、Case、Artifact、Version、ResponsibilityおよびTraceabilityを一貫して管理できるRepository原則を維持する。

特定のToolまたはTechnologyに依存する実装が必要となる場合、その実装詳細はApplicable Technical SpecificationまたはDevelopment領域で管理する。

---

## 2.12 Controlled Expansion

新しいDirectory、Repository Layer、Artifact Type、Publication区分その他のRepository構造を追加する場合は、明確な責務および必要性を確認する。

既存構造で管理可能な内容について、重複する新しい管理領域を不必要に作成しない。

新しい構造が必要な場合は、

- 追加する目的
- 責務
- 既存構造との関係
- Source of Truth
- 既存Artifactへの影響
- Traceabilityへの影響
- 長期運用への影響

を確認する。

正式仕様として未定義のRepository構造を、一般的な慣行または推測だけを根拠として追加してはならない。

---

## 2.13 Core Principle

ProjectORIGIN Repositoryは、

\*\*Caseを中心として成果物を整理し、各Artifactの責務を分離し、正式な成果物、Versionおよび関係性を継続して識別・追跡できる状態\*\*

を維持する。

Repositoryの成長は、成果物を単に蓄積することではない。

CaseおよびArtifactが増加しても、どの成果物が何であり、どのCaseに属し、どのVersionであり、他の成果物とどのような関係を持つかを確認できる状態を維持することを、Repository管理の基本原則とする。

# Chapter 3

# Case Repository Structure

## 3.1 Purpose

本章は、ProjectORIGINにおけるCase単位の正式なRepository Structureを定義する。

Caseに属するProduction Artifactおよび関連成果物を一貫した物理構造の下で管理し、Case間の混在を防止するとともに、各Caseを独立して識別、制作、監査、更新および追跡できるRepository環境を維持することを目的とする。

本章はCase Repositoryの物理構造を定義するものであり、各Production Artifact内部の内容、Production Workflowそのもの、Database SchemaまたはAudit Methodを定義しない。

---

## 3.2 Case Root

ProjectORIGINにおけるCase Production Artifactは、Repository上の`cases/`をCase管理のRoot Directoryとする。

各Caseは、`cases/`直下に独立したCase Directoryを持つ。

基本構造は以下とする。

 cases/
 └── FILE-XXX/

`FILE-XXX`は、Repository上で対象Caseを識別する正式なCase Directory Identifierを表す。

Case Directory IdentifierとDatabase上のCase ID、File Numberその他の正式な識別情報との対応関係は、Applicable Database Source of Truthとの整合を維持する。

Repository Ruleは、Case Directory Identifierの存在を根拠として、Database上のCase IDとFile Numberが同一の概念であると独自に定義しない。

各CaseのProduction Artifactは、Applicable Source of Truthによって別の正式配置が定義されている場合を除き、対象CaseのCase Directoryとの関係を識別可能な状態で管理する。

---

## 3.3 Case Directory Identification

Case Directoryは、対象CaseをRepository上で識別する正式なCase Directory Identifierによって識別する。

例：

 cases/
 ├── FILE-001/
 ├── FILE-002/
 ├── FILE-003/
 └── ...

Case Directory名を、Case Title、略称、表示名その他の可変的な名称だけで管理してはならない。

Case Titleまたは表示名が将来変更された場合でも、同一CaseのRepository上のIdentityを維持できる構造とする。

Case Directory IdentifierとDatabase上のCase ID、File Numberその他の識別情報との正式な対応関係は、Applicable Database Source of Truthとの整合を維持する。

Case ID、File Numberその他のDatabase上の識別情報について、その生成規則、Data Type、ValidationまたはRelationshipを本章によって独自に再定義しない。

---

## 3.4 Formal Basic Case Structure

各Case Directoryの正式な基本構造は、以下とする。

 cases/
 └── FILE-XXX/
 ├── research/
 ├── master/
 ├── publication/
 │ ├── free/
 │ └── classified/
 ├── assets/
 ├── audit/
 └── publication-tracking.json

この構造は、ProjectORIGINのCase Production Artifact、関連成果物および
Repository-managed Operational Metadata ArtifactをCase単位で管理するための
正式な基本Repository Structureとする。

各Directoryは、異なるProduction責務または関連成果物の管理責務を
物理的に分離するために使用する。

`publication-tracking.json`はDirectoryまたは新しいProduction Layerではない。

`publication-tracking.json`は、対象Caseに属するFREE Publication Artifactおよび
CLASSIFIED Publication ArtifactのArtifact-level Trackingを保持する
Case-level Repository-managed Operational Metadata Artifactとする。

本構造に対する正式な例外または追加が必要となる場合は、
Chapter 2のControlled Expansionおよび本書の正式な変更工程に従う。

具体的な各Directoryの責務、格納対象およびArtifact間の境界は
Chapter 4「Production Artifact and Repository Layers」で定義する。

`publication-tracking.json`の管理責務、Controlled Values、
Workflow Statusとの関係、TraceabilityおよびValidationは、
本書のApplicableな後続Sectionで定義する。
---
## 3.5 Research Directory

Caseに属する正式なResearch Artifactは、対象Caseの`research/` Directoryとの関係を維持する。

基本配置は以下とする。

 cases/FILE-XXX/research/

Research Artifact内部の構造、Research Method、Source、Evidence、Fact、Claim、Theory、Hypothesisその他のResearch仕様は、本章では定義しない。

それらはResearch Bible、Research Templateその他のApplicable Source of Truthに従う。

Research Artifactの具体的なFilenameおよびVersion ConventionはChapter 5で定義する。

---

## 3.6 Master Directory

Caseに属するMaster Case File Artifactは、対象Caseの`master/` Directoryとの関係を維持する。

基本配置は以下とする。

 cases/FILE-XXX/master/

Master Case File内部のSection、Writing Rule、Content Structureその他のMaster Case File仕様は、本章では定義しない。

それらはApplicable Case File Templateその他の正式なSource of Truthに従う。

Master Artifactの具体的なFilenameおよびVersion ConventionはChapter 5で定義する。

---

## 3.7 Publication Directory

Caseに属するPublication Artifactは、対象Caseの`publication/` Directoryとの関係を維持する。

Publication Artifactは、Repository上でFREEとCLASSIFIEDを物理的に区別する。

基本配置は以下とする。

 cases/FILE-XXX/publication/
 ├── free/
 └── classified/

FREE Artifactは`free/`、CLASSIFIED Artifactは`classified/`との関係を維持する。

本SectionはFREEおよびCLASSIFIEDのContent、Disclosure Boundary、Writing Rule、Access ControlまたはPublication Workflowを定義しない。

それらはApplicable Source of Truthに従う。

具体的なFilenameおよびVersion ConventionはChapter 5で定義する。

---

## 3.8 Assets Directory

対象Caseに属する正式なAssetは、Case Directory内の`assets/`との関係を維持する。

基本配置は以下とする。

 cases/FILE-XXX/assets/

`assets/`は、対象Caseに関連し、Applicable Source of Truthによって正式なAssetとして認められた成果物をCase単位で管理するための物理領域とする。

Assetの分類、Source、License、Caption、Visual Role、Art Direction、生成方法その他の専門仕様は、本章では定義しない。

それらはImage Rule、Art Bibleその他のApplicable Source of Truthに従う。

`assets/`の存在だけを根拠として、新しいAsset Type、Metadata Structure、Metadata File Format、Registration Procedureその他の未定義仕様を独自に定義してはならない。

`assets/`内部に追加のSubdirectoryが必要となる場合、その構造を一般的慣行または推測だけを根拠として正式仕様に追加してはならない。

---

## 3.9 Case Isolation

異なるCaseのProduction Artifactを、所属Caseを識別できない状態で同一Case Directory内に混在させてはならない。

`FILE-001`に属するArtifactを`FILE-002`のCase Directoryへ正式Artifactとして配置するなど、Case Identityと物理配置が矛盾する状態を作ってはならない。

Case間で共通利用される情報またはAssetが将来必要となった場合も、既存Case Directoryへ便宜的に所属させて正式管理してはならない。

そのような共有構造が必要となる場合は、責務、Source of Truth、Traceabilityおよび既存構造への影響を確認し、正式な変更工程によって定義する。

---

## 3.10 No Uncontrolled Case-Level Expansion

各Case Directory直下に、本書で正式定義されていないDirectoryを独自に追加し、正式なRepository Structureとして扱ってはならない。

例えば、必要性および責務が正式に確認されていない状態で、

 notes/
 temp/
 draft/
 misc/
 archive/

その他のDirectoryを正式なCase Layerとして追加しない。

作業上の一時ファイルまたは補助的なCopyが必要な場合も、それらを正式なProduction Artifactまたは正式なRepository Layerと混同してはならない。

新しいCase-level Directoryが正式に必要となった場合は、Chapter 2のControlled Expansionおよび本書の正式な変更工程に従う。

---

## 3.11 Audit Artifact Placement

Audit ArtifactはProjectORIGINにおける正式な関連成果物として識別し、対象ArtifactとのTraceabilityを維持する。

Case単位のAudit Artifactの正式な物理Repository Placementは、Human Decisionにより、

 cases/FILE-XXX/audit/

とする。

このPlacementはCase Identityを維持するための物理配置を定義するものであり、Audit Artifact Filename Convention、Audit Artifact Versioning、`audit/`配下のSubdirectory、Retention / Archive Placement、Database / Metadata Fieldまたは具体的Automation実装を自動的に確定しない。

Audit Artifactは少なくとも、

- 所属Case
- 対象Artifact
- Applicable Version
- Audit Result

とのTraceabilityを維持しなければならない。

具体的なNaming、Versioning、MetadataまたはAutomation仕様はApplicable Source of Truthおよび正式HOLD Ledger上のApplicableな未解決事項に従う。

Audit Method、Audit Criteria、PASS、REVISION、BLOCKERその他の監査仕様はAudit Ruleの責務とする。

---

## 3.12 HOLD-AUDIT-PLACEMENT-01 Resolution State

`HOLD-AUDIT-PLACEMENT-01`は、Audit Artifactの正式な物理Repository Placementを決定するために登録されたHOLDである。

Human Decisionにより、Case単位の正式Placementとして、

 cases/FILE-XXX/audit/

がAPPROVEDとなり、Repository Ruleへ反映された。

その後、Applicable Source of TruthとのCompatibility確認、必要な影響確認および最終再監査が完了し、正式HOLD Ledgerにおいて、

 HOLD-AUDIT-PLACEMENT-01 — RESOLVED

として記録されている。

したがって、本HOLDをActive HOLD、OPENまたは未確定事項として扱ってはならない。

ただし、本HOLDのResolutionは、

- Audit Artifact Filename Convention
- Audit Artifact Versioning
- `audit/`配下のSubdirectory
- Retention / Archive Placement
- Database / Metadata Field
- 具体的Automation実装

を新たに確定または承認したことを意味しない。

これらについて正式仕様が必要となる場合は、それぞれのApplicable Source of Truth、既存HOLDおよび正式な変更工程に従う。

解消済み`HOLD-AUDIT-PLACEMENT-01`を、本章または他のRepository Rule Chapterから推測によってActive HOLDへ再Openしてはならない。

Historical Recordおよび正式Resolutionの詳細は正式HOLD Ledgerに従う。

---

## 3.13 Operational Metadata

Operational Metadataについて、本章は独立した物理Directoryを定義しない。

Workflow Status、Publication Status、Version、Approvalその他の
Operational Metadataは、それぞれのApplicable Source of Truthおよび
本書の後続Chapterで定義される責務に従って管理する。

FREE Publication ArtifactおよびCLASSIFIED Publication Artifactの
Artifact-level Trackingについては、

 cases/FILE-XXX/publication-tracking.json

を正式なCase-level Repository-managed Operational Metadata Artifactとして使用する。

`publication-tracking.json`は、FREEおよびCLASSIFIEDについて、
それぞれ独立して、

- Applicability
- Production State
- Applicable Audit Reference

を管理する。

本ArtifactはProduction Artifact、Audit ArtifactまたはDatabase Recordではなく、
新しいProduction Layerを構成しない。

`publication-tracking.json`の存在から、
Case-level Workflow Status、Publication Status、Audit Result、
Human Approval Decisionまたはその他の専門状態を独自に導出してはならない。

同様に、Case-level Workflow Status、Publication Status、
Audit Result、Human Approval DecisionまたはRepository上の
ファイル存在状態だけを根拠として、
`publication-tracking.json`に保持すべき値を推測してはならない。

論理的なOperational Metadata Layerまたは
`publication-tracking.json`の存在だけを根拠として、

 metadata/

その他の物理Directoryを独自に追加してはならない。

Database Field、Data Type、Nullability、Validationその他の
Database Schema仕様はDatabase RuleおよびDatabase Schemaの責務とし、
`publication-tracking.json`の正式化だけを理由として
Database Fieldを新設してはならない。

---

## 3.14 Case Creation Principle

新しいCaseをRepositoryへ追加する場合は、正式なCase Directory Identifierと対象Caseとの対応を確認し、既存Caseと同一の正式な基本構造に従ってCase Directoryを管理する。

例えば`FILE-001`、`FILE-002`に続いて新しいCaseを追加する場合も、Caseごとに異なる独自構造を便宜的に採用しない。

Case固有の要件によって正式な基本構造だけでは管理できない成果物が必要となった場合は、Case単独の例外構造を即座に作成するのではなく、その要件がProjectORIGIN全体のRepository Structureへ与える影響を確認する。

例外または拡張が必要な場合は、正式なReviewおよび変更工程を経る。

---

## 3.15 Core Structure

ProjectORIGINの正式な基本Case Repository Structureは、以下とする。

 cases/
 └── FILE-XXX/
 ├── research/
 ├── master/
 ├── publication/
 │ ├── free/
 │ └── classified/
 ├── assets/
 ├── audit/
 └── publication-tracking.json

`FILE-XXX`は、Repository上で対象Caseを識別する正式な
Case Directory Identifierを表す。

本構造は、CaseをRepository管理の基本単位とし、
Research、Master、Publication、AssetおよびAudit関連成果物の
物理的責務を分離するとともに、
FREEおよびCLASSIFIED Publication ArtifactのArtifact-level Trackingを
Case-level Repository-managed Operational Metadataとして管理する。

`publication-tracking.json`は新しいProduction Layerではなく、
専用`metadata/` Directoryの新設を意味しない。

Audit Artifactの正式な物理Repository Placementは、

 cases/FILE-XXX/audit/

とする。

このPlacementはHuman Decisionによって承認され、
Applicable Source of Truthへの必要な反映および最終再監査を経て、
`HOLD-AUDIT-PLACEMENT-01`は正式HOLD Ledger上でRESOLVEDとなっている。

したがって、Audit Artifact Placementを未確定、OPENまたは
Active HOLDとして扱ってはならない。

一方、このResolutionからAudit Artifact Filename Convention、
Audit Artifact Versioning、`audit/`配下のSubdirectory、
Retention / Archive Placement、Database / Metadata Fieldまたは
具体的Automation実装を推測によって確定してはならない。

`publication-tracking.json`に保持するApplicable Audit Referenceは、
Audit ArtifactのAudit上のApplicabilityまたはAudit Resultそのものを
Repository Ruleが独自に決定することを意味しない。

Audit上のApplicabilityおよびAudit Resultの意味判断は、
Applicable Audit Source of Truthに従う。

本章で正式定義されていない追加構造は、
確認および承認なしに推測して追加しない。
---
# Chapter 4

# Production Artifact and Repository Layers

## 4.1 Purpose

本章は、ProjectORIGIN Repositoryにおける各Production ArtifactおよびRepository Layerの責務、格納対象および境界を定義する。

Chapter 3で定義された正式な基本Case Repository Structureに対し、それぞれのDirectoryがRepository上でどの種類の成果物または関連成果物を管理するかを明確にし、異なる責務を持つArtifactの混在を防止することを目的とする。

本章はProduction Artifactおよび関連成果物のRepository上の責務を定義するものであり、Artifact内部のContent Structure、Research Method、Writing Rule、Audit Criteria、Database Schemaその他の専門仕様を再定義しない。

---

## 4.2 Repository Layer Principle

ProjectORIGINでは、Production Artifactおよび関連成果物を、その責務に応じたRepository Layerまたは正式な物理配置で管理する。

Case Repositoryの正式な基本構造は、Chapter 3で定義された以下の構造を前提とする。

cases/
└── FILE-XXX/
├── research/
├── master/
├── publication/
│ ├── free/
│ └── classified/
├── assets/
├── audit/
└── publication-tracking.json

各Directoryは、それぞれ異なるProduction責務または関連成果物の管理責務を持つ。

\`publication-tracking.json\`はDirectoryまたはProduction Layerではない。

\`publication-tracking.json\`は、FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Trackingを保持するCase-level Repository-managed Operational Metadata Artifactである。

物理的に同一Case Directory内へ配置されていても、Research、Master、Publication、Asset、AuditおよびOperational Metadataの責務を混同してはならない。

論理的なProduction LayerとRepository上の物理配置は区別して管理する。

本章で定義されていない新しいRepository Layer、DirectoryまたはArtifact Categoryを、一般的慣行または推測だけを根拠として追加してはならない。

---

## 4.3 Research Layer

Research Layerは、対象Caseに関する正式なResearch ArtifactをRepository上で管理する責務を持つ。

物理的な基本配置は以下とする。

cases/FILE-XXX/research/

Research Layerでは、Applicable Source of Truthに基づいて正式に作成されたResearch Artifactを、対象Caseとの関係が識別可能な状態で管理する。

Research Layerは、Research Artifactの調査方法、Source評価、Evidence評価、Fact、Claim、Theory、Hypothesis、Reliabilityその他のResearch内部仕様を独自に定義しない。

これらの専門仕様はResearch Bible、Research Templateその他のApplicable Source of Truthに従う。

Research Layerに配置されていることだけを理由として、ArtifactをAudit済み、Approvedまたは後続工程への使用許可済みとみなしてはならない。

ApprovalおよびAudit条件は、それらを管理するApplicable Source of Truthに従う。

---

## 4.4 Master Layer

Master Layerは、対象Caseの正式なMaster Case File ArtifactをRepository上で管理する責務を持つ。

物理的な基本配置は以下とする。

cases/FILE-XXX/master/

Master Layerは、正式な上流成果物およびApplicable Production Flowに基づいて作成されたMaster Case Fileを、対象Caseとの関係が識別可能な状態で管理する。

Master Case File内部のSection、Writing Rule、Narrative Structure、Evidence Presentationその他の専門仕様は、本章では定義しない。

それらはApplicable Case File Templateその他の正式なSource of Truthに従う。

Master Layerに配置されていることだけを理由として、ArtifactをAudit済み、ApprovedまたはPublication Productionへの使用許可済みとみなしてはならない。

Applicable AuditおよびApproval条件を満たしていることは、別途Applicable Source of Truthに基づいて確認する。

---

## 4.5 Publication Layer

Publication Layerは、対象CaseのPublication ArtifactをRepository上で管理する責務を持つ。

物理的な基本配置は以下とする。

cases/FILE-XXX/publication/

Publication Layerでは、FREE Publication ArtifactとCLASSIFIED Publication Artifactを異なるArtifact Identityとして管理する。

基本構造は以下とする。

publication/
├── free/
└── classified/

Publication Layerは、Publication ArtifactのRepository上の管理責務を定義するものであり、公開条件、Disclosure Boundary、Access Control、Membership、Writing RuleまたはPublication Contentそのものを定義しない。

それらはApplicable Source of Truthに従う。

---

## 4.6 FREE Publication Layer

FREE Publication Artifactは、以下との関係を維持する。

cases/FILE-XXX/publication/free/

FREE Publication Artifactは、CLASSIFIED Publication Artifactとは異なる正式なArtifact Identityとして扱う。

FREEとCLASSIFIEDが同一Caseに属することだけを理由として、同一Artifactまたは同一Audit対象として扱ってはならない。

FREE Artifact内部のContent Structure、Writing Ruleおよび公開内容はApplicable Source of Truthに従う。

Repository上の配置だけを理由としてPublication Statusを\`PUBLISHED\`とみなしてはならない。

---

## 4.7 CLASSIFIED Publication Layer

CLASSIFIED Publication Artifactは、以下との関係を維持する。

cases/FILE-XXX/publication/classified/

CLASSIFIED Publication Artifactは、FREE Publication Artifactとは異なる正式なArtifact Identityとして扱う。

CLASSIFIED Artifact内部のContent Structure、Writing Rule、Disclosure Boundary、Access条件その他の専門仕様はApplicable Source of Truthに従う。

Repository上の配置だけを理由としてPublication Statusを\`PUBLISHED\`とみなしてはならない。

---

## 4.8 FREE and CLASSIFIED Independence

FREE Publication ArtifactとCLASSIFIED Publication Artifactは、同一Caseに属する場合でも、それぞれ独立したPublication Artifact Identityを持つ。

一方のArtifactのProduction、Audit、Approval、Repository IntegrationまたはPublication状態だけを根拠として、他方も同一状態であると推測してはならない。

FREEおよびCLASSIFIEDのArtifact-level Trackingは、

cases/FILE-XXX/publication-tracking.json

をRepository管理領域におけるPrimary Source of Truthとして管理する。

Artifact-level Trackingでは、FREEおよびCLASSIFIEDについて、それぞれ独立して、

- Applicability
- Production State
- Applicable Audit Reference

を管理する。

ApplicabilityのControlled Valuesは、

APPLICABLE
NOT_APPLICABLE

とする。

Production StateのControlled Valuesは、

NOT_STARTED
IN_PROGRESS
COMPLETE

とする。

\`NOT_APPLICABLE\`であるPublication Artifactについては、Production Stateを要求しない。

本Sectionから、これら以外のApplicabilityまたはProduction StateのControlled Valueを独自に追加してはならない。

Artifact-level Trackingは、Case-level Workflow Status、Publication Status、Audit ResultまたはHuman Approval Decisionとは異なる責務を持つ。

Case-level Workflow Status
≠
Artifact-level Production State
≠
Publication Status
≠
Audit Result

とする。

Artifact-level Trackingだけを根拠として、新しいCase-level Workflow Status、Publication Status、Audit ResultまたはHuman Approval Decisionを生成してはならない。

同様に、Case-level Workflow Status、Publication Status、Audit Result、Human Approval Decisionまたは他方のPublication Artifactの状態だけを根拠として、対象ArtifactのApplicabilityまたはProduction Stateを推測してはならない。

Applicable Audit Referenceの具体的なTraceabilityおよびValidationは、本書のApplicableな後続SectionおよびApplicable Audit Source of Truthとの責務境界に従う。

---

## 4.9 Asset Layer

Asset Layerは、対象Caseに関連する正式なAssetをRepository上で管理する責務を持つ。

物理的な基本配置は以下とする。

cases/FILE-XXX/assets/

Asset Layerでは、Applicable Source of Truthによって正式なAssetとして認められた成果物を、対象Caseとの関係が識別可能な状態で管理する。

Assetの分類、Source、License、Caption、Visual Role、Art Direction、生成方法その他の専門仕様はImage Rule、Art Bibleその他のApplicable Source of Truthに従う。

\`assets/\`の存在だけを根拠として、Asset Type、Subdirectory、Filename Convention、Metadata Structure、Registration Procedureその他の未定義仕様を独自に追加してはならない。

---

## 4.10 Audit Artifact Layer

Audit Artifactは、対象Caseおよび対象ArtifactとのTraceabilityを維持する正式な関連成果物として管理する。

Case単位のAudit Artifactの正式な物理Repository Placementは、Chapter 3で定義されたとおり、

cases/FILE-XXX/audit/

とする。

Audit Artifactは少なくとも、

- 所属Case
- 対象Artifact
- Applicable Version
- Audit Result

とのTraceabilityを維持しなければならない。

\`audit/\`への配置は、Audit Method、Audit Criteria、Audit Resultの意味または監査工程そのものを定義しない。

それらはAudit RuleおよびApplicable Source of Truthに従う。

また、このPlacementから、

- Audit Artifact Filename Convention
- Audit Artifact Versioning
- \`audit/\`配下のSubdirectory
- Retention / Archive Placement
- Database / Metadata Field
- 具体的Automation実装

を推測によって確定してはならない。

---

## 4.11 Audit Artifact Placement Resolution Boundary

\`HOLD-AUDIT-PLACEMENT-01\`について、Case単位のAudit Artifact正式物理Repository Placementとして、

cases/FILE-XXX/audit/

を採用するHuman Decision、Applicable Source of Truthへの必要な反映、Compatibility確認および最終再監査は完了している。

正式HOLD Ledgerにおいて、本HOLDはRESOLVEDとして管理される。

したがって、本章から\`HOLD-AUDIT-PLACEMENT-01\`をActive HOLD、OPENまたは未確定事項として再定義してはならない。

一方、本HOLDのResolutionはAudit ArtifactのNaming、Versioning、Subdirectory、Retention / Archive、Database / MetadataまたはAutomation仕様を承認したことを意味しない。

Historical Recordおよび正式Resolutionの詳細は正式HOLD Ledgerに従う。

---

## 4.12 Artifact Responsibility Separation

Research、Master、FREE、CLASSIFIED、AssetおよびAudit関連成果物は、それぞれ異なる責務を持つ。

一つのArtifactを、別のArtifact TypeまたはRepository Layerの正式成果物の代替として扱ってはならない。

例えば、Research Artifactが存在することだけを理由としてMaster Case Fileが成立したものと扱わない。

同様に、Master Case Fileが存在することだけを理由としてFREEまたはCLASSIFIED Publication Artifactが成立したものと扱わない。

Audit Artifactが存在することだけを理由として、対象ArtifactがApproved、Repository IntegratedまたはPublishedであると推測してはならない。

Artifact間の進行条件はApplicable Production FlowおよびApplicable Source of Truthに従う。

---

## 4.13 Artifact Identity

Production Artifactは、対象Case、Artifact TypeおよびApplicable Versionとの関係を識別可能な状態で管理する。

FREEとCLASSIFIEDは異なるArtifact Identityとして扱う。

Audit Artifactは対象Production Artifactそのものではなく、対象Artifactに対する監査結果とのTraceabilityを持つ関連成果物として扱う。

Assetも、それが関連するProduction Artifactそのものと自動的に同一Identityを持つものとして扱わない。

Filename、Directory PlacementまたはMetadataだけを根拠として、Applicable Source of Truthに存在しない新しいArtifact Identityを独自に生成してはならない。

---

## 4.14 Version Boundary

Production ArtifactのVersionはChapter 5「Artifact Naming and Versioning」で定義された正式Criteriaに従う。

本章はMajor Version Increment、Minor Version Increment、No Version Increment、Current Version SelectionまたはHistorical Version Retentionを独自に再定義しない。

Repository Layer間の移動、Repository Integration、Re-Integration、Placement変更またはFilename変更だけを理由として、Automatic Version Incrementを成立させてはならない。

Production ArtifactのVersion表記にはChapter 5で定義された\`vX.Y\`を使用し、Production Artifact用のPatch Componentを本章から追加してはならない。

Version判断がChapter 5のCriteriaから一意に確定できない場合は、推測またはAutomationによって決定せず、Human Decisionを要求する。

Audit Artifact固有のVersioningは、本Sectionによって新たに確定しない。

---

## 4.15 Repository Placement Does Not Establish State

Repository上にArtifact、DirectoryまたはOperational Metadata Artifactが存在することだけを根拠として、Workflow Status、Artifact-level Production State、Publication Status、Audit Result、Human Approval DecisionまたはRepository Integration状態を確定してはならない。

例えば、

publication/free/

にFREE Publication Artifactが存在することだけでは、そのArtifactがProduction State \`COMPLETE\`、Audit \`PASS\`、APPROVED、Repository IntegratedまたはPUBLISHEDであることを意味しない。

同様に、

publication/classified/

にCLASSIFIED Publication Artifactが存在することだけでは、そのArtifactのApplicabilityまたはProduction Stateを確定できない。

publication-tracking.json

が存在することだけでも、FREEまたはCLASSIFIEDが\`APPLICABLE\`、\`NOT_APPLICABLE\`、\`NOT_STARTED\`、\`IN_PROGRESS\`または\`COMPLETE\`のいずれであるかを推測してはならない。

audit/

にAudit Artifactが存在することだけでは、対象ArtifactがPASS、APPROVED、Repository IntegratedまたはPUBLISHEDであることを意味しない。

各StateおよびApplicable Audit Referenceは、それぞれの正式なSource of Truth、明示的に管理された値および必要なTraceabilityに基づいて判断する。

Applicable Audit Referenceが存在することだけを根拠として、Audit Resultを推測してはならない。

---

## 4.16 No Uncontrolled Layer Expansion

本章で定義されたRepository Layerまたは物理配置に対して、新しいLayer、DirectoryまたはSubdirectoryを一般的慣行、便宜または推測だけを根拠として追加してはならない。

新しいRepository構造が必要となる場合は、Chapter 2のControlled Expansion、Chapter 3のCase Repository StructureおよびApplicable Source of TruthとのCompatibilityを確認する。

新しい構造の必要性が確認された場合も、責務、既存Artifactへの影響、Traceability、Naming、Versioning、Database、AutomationおよびCompatibilityへの影響を確認した上で正式な変更工程を行う。

---

## 4.17 HOLD and Compatibility Boundary

本章に関連するHOLDおよびCompatibility事項は、それぞれの正式状態を維持する。

\`HOLD-AUDIT-PLACEMENT-01\`はRESOLVEDであり、Case単位のAudit Artifact正式物理Repository Placementは、

cases/FILE-XXX/audit/

とする。

本ResolutionからAudit Artifact Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、Subdirectory、追加Database / Metadata Fieldまたは具体的Automation実装を派生させてはならない。

\`HOLD-PUBLICATION-TRACKING-01\`については、FREE / CLASSIFIED Artifact-level Trackingに必要なHuman Decisionが完了し、以下の仕様が本書へ正式反映されている。

- FREE / CLASSIFIEDごとの独立したApplicability
- FREE / CLASSIFIEDごとの独立したProduction State
- Applicable Audit Reference
- \`cases/FILE-XXX/publication-tracking.json\`を使用するRepository-managed Operational Metadata
- Case-level Workflow Statusとの責務分離
- Publication Statusとの責務分離
- Audit Resultとの責務分離
- Database Schemaとの責務分離
- Reference Validation Boundary
- Automation Boundary
- Existing Case Compatibility Boundary

Resolution前は、本章への反映だけでは\`HOLD-PUBLICATION-TRACKING-01\`をRESOLVEDとせず、Applicable Source of Truthへの必要な反映、関連文書とのCompatibility確認、Repository Integrationへの影響確認および最終横断再監査のPASSが要求されていた。

これらのResolution条件は完了し、\`HOLD-PUBLICATION-TRACKING-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

一方、Human Decisionによって確定済みのArtifact-level Tracking仕様を、未確定であることを理由として独自に変更、縮小、拡張または別体系へ置換してはならない。

\`HOLD-ARTIFACT-VERSION-01\`は正式HOLD Ledger上でRESOLVEDである。

Production Artifact Version Increment CriteriaはChapter 5に従い、本章から独自に再定義しない。

解消済みHOLDを、本章から推測によってActive HOLDへ再Openしてはならない。

---

## 4.18 Core Layer Principle

ProjectORIGINのCase Repositoryでは、

research/
master/
publication/free/
publication/classified/
assets/
audit/

を、それぞれの正式な責務に従って管理する。

各Repository Layerまたは物理配置は、Artifactの所属および管理責務を明確にするために使用する。

Repository上の配置だけを理由として、Production Workflow上の進行、Audit Result、Human Approval、Repository IntegrationまたはPublication Statusを成立させてはならない。

各Artifactおよび関連成果物は、その責務、Identity、Applicable Versionおよび必要なTraceabilityを維持し、Applicable Source of Truthに従って管理する。

# Chapter 5

# Artifact Naming and Versioning

## 5.1 Purpose

本章は、ProjectORIGIN RepositoryにおけるProduction Artifactの正式なNamingおよびVersion Identificationの基本原則を定義する。

各Caseに属するProduction Artifactについて、対象Case、Artifact TypeおよびArtifact VersionをRepository上で一貫して識別可能な状態にし、異なるCase、異なるArtifact Typeおよび異なるVersionの混同を防止することを目的とする。

本章はRepository上のArtifact NamingおよびVersion Identificationを定義するものであり、各Artifact内部のContent Structure、Production Method、Audit Criteria、Database SchemaまたはPublication Ruleを再定義しない。

---

## 5.2 Core Naming Convention

ProjectORIGINのCase Production Artifactは、以下をFilename IdentityのCoreとする。

- Case Directory Identifier
- Artifact Type
- Artifact Version

基本Naming Conventionは以下とする。

FILE-XXX\_\[ARTIFACT-TYPE\]\_vX.Y.ext

例：

FILE-001_RESEARCH_v1.0.md
FILE-001_MASTER_v1.0.md
FILE-001_FREE_v1.0.md
FILE-001_CLASSIFIED_v1.0.md

本Naming Conventionは、ProjectORIGIN RepositoryにおけるProduction Artifactの基本命名方式として使用する。

\`FILE-XXX\`、\`\[ARTIFACT-TYPE\]\`、\`vX.Y\`および\`.ext\`は、それぞれ異なる識別責務を持つ。

Filenameの各構成要素は、単なる表示上の文字列としてではなく、対象ArtifactをRepository上で識別するための情報として扱う。

---

## 5.3 Case Identifier Component

Filenameの\`FILE-XXX\`部分は、対象Artifactが属するCaseのCase Directory Identifierと整合しなければならない。

例えば、以下のArtifactは、

FILE-001_RESEARCH_v1.0.md

原則として\`FILE-001\`として識別されるCaseとの関係を維持する。

Case Directory IdentifierとFilename内のCase Identifierが矛盾する状態を正式なRepository管理として許容しない。

例えば、

cases/FILE-001/research/FILE-002_RESEARCH_v1.0.md

のように、Directory上のCase IdentityとFilename上のCase Identityが一致しない状態を正式Artifactとして扱ってはならない。

Case Directory IdentifierとDatabase上のCase ID、File Numberその他の識別情報との関係についてはChapter 3およびApplicable Database Source of Truthに従い、本章から独自に再定義しない。

---

## 5.4 Artifact Type Component

Filenameの\`\[ARTIFACT-TYPE\]\`部分は、対象Artifactの正式なProduction Artifact Typeを識別する。

本Versionで基本対象とするProduction Artifact Typeは以下とする。

- \`RESEARCH\`
- \`MASTER\`
- \`FREE\`
- \`CLASSIFIED\`

基本例：

FILE-001_RESEARCH_v1.0.md
FILE-001_MASTER_v1.0.md
FILE-001_FREE_v1.0.md
FILE-001_CLASSIFIED_v1.0.md

Artifact Typeは、Chapter 4で定義されたRepository Layer上の責務と整合しなければならない。

例えば、\`RESEARCH\`として識別されるArtifactを、Filename変更だけによって\`MASTER\`として成立させてはならない。

新しいArtifact Typeが必要となる場合は、一般的慣行または便宜的判断だけを根拠として新しいType Tokenを追加してはならない。

新しいArtifact Typeの追加は、Chapter 4のLayer Expansion Principleおよび本書の正式な変更工程に従う。

---

## 5.5 Version Component

Filenameの\`vX.Y\`部分は、対象Production ArtifactのArtifact VersionをRepository上で識別するために使用する。

基本表現は以下とする。

vX.Y

\`X\`はMajor Version、\`Y\`はMinor Versionを表す。

Production Artifact Versionは、単純な変更量、Filename変更、Timestamp、Workflow Status、Publication Statusその他の単独状態によって決定しない。

Version Incrementは、対象Artifactに成立している正式な承認境界への影響を基準として判定する。

公式Documentに適用されるVersion Management Rule、Semantic Versioningその他の一般的慣行を、Production Artifactへ自動的に転用してはならない。

Production ArtifactのVersion表記は\`vX.Y\`を正式な基本表現とする。

本Ruleを根拠としてPatch Componentを追加してはならない。

したがって、

vX.Y.Z

をProduction Artifactの正式なVersion表現として、本Ruleから生成してはならない。

Version表記が存在することだけを根拠として、そのArtifactがApproved、Audit済み、Publication Ready、PublishedまたはCurrent Versionであるとみなしてはならない。

---

## 5.6 Version Identity and Artifact State

Artifact VersionとWorkflow Status、Audit Result、Human Approval Decision、Repository IntegrationおよびPublication Statusは、それぞれ異なる概念として管理する。

したがって、

Artifact Version
≠
Workflow Status
≠
Audit Result
≠
Human Approval Decision
≠
Repository Integration
≠
Publication Status

とする。

例えば、

FILE-001_RESEARCH_v1.0.md

というFilenameを持つことだけを理由として、当該Research ArtifactがAudit PASS済みまたはApproved Researchであると判断してはならない。

Version Numberが大きいこと、Timestampが新しいこと、Filenameが最新版に見えることその他の単独条件だけを根拠として、そのArtifactを正式なCurrent Version、Approved ArtifactまたはPublished Artifactと判断してはならない。

Version Incrementの成立と、Required Production / Publication Audit、Applicable Final Flow Audit、Human Review、Human Approval、Repository IntegrationまたはPublicationの成立を混同してはならない。

新しいVersionに対して、旧Versionに成立していたAudit ResultまたはHuman Approval Decisionを自動的に継承してはならない。

Re-Audit、Final Flow Auditの再実施、再Human Reviewまたは再Human Approvalの必要性は、Applicable Production Flow、Audit Rule、AGENTS.md、Human Decisionその他のApplicable Source of Truthに従って判断する。

本章は、Workflow Status、Publication Status、Audit Result、Human Approval DecisionまたはDatabase FieldのControlled Valueを独自に再定義しない。

---

## 5.7 Filename and Repository Placement Consistency

FilenameとRepository Placementは相互に矛盾しない状態を維持する。

例えば、以下のような対応を基本とする。

cases/FILE-001/research/
└── FILE-001_RESEARCH_v1.0.md

cases/FILE-001/master/
└── FILE-001_MASTER_v1.0.md

cases/FILE-001/publication/free/
└── FILE-001_FREE_v1.0.md

cases/FILE-001/publication/classified/
└── FILE-001_CLASSIFIED_v1.0.md

Filenameが正しい場合でも、誤ったCase DirectoryまたはRepository Layerへ配置されたArtifactを正式な配置として扱ってはならない。

同様に、正しいDirectoryへ配置されていることだけを根拠として、Filename上のCase Identity、Artifact TypeまたはVersionの矛盾を許容してはならない。

Filename IdentityとRepository Placementの双方がApplicable Source of Truthと整合する必要がある。

---

## 5.8 Filename Does Not Create Artifact Identity

Filename変更だけによってProduction Artifactの正式なArtifact Type、Version State、Approval StateまたはPublication Stateを変更してはならない。

例えば、

FILE-001_RESEARCH_v1.0.md

を単純に、

FILE-001_MASTER_v1.0.md

へRenameしただけでは、正式なMaster Case Fileは成立しない。

同様に、

FILE-001_MASTER_v1.0.md

を、

FILE-001_MASTER_v2.0.md

へRenameしただけでは、正式なVersion Updateが成立したものとみなしてはならない。

Artifact TypeおよびArtifact Versionの正式な変更は、Applicable Production Flow、Source of Truth、必要なAudit、Approval、Traceabilityその他の条件と整合しなければならない。

---

## 5.9 File Extension

基本Naming Conventionにおける\`.ext\`は、対象Artifactの正式なFile Formatに対応するExtensionを表す。

例として、

FILE-001_RESEARCH_v1.0.md

の\`.md\`はMarkdown Fileを示す。

ただし、本章に示す\`.md\`の例だけを根拠として、すべてのProduction Artifactの正式File FormatをMarkdownへ固定してはならない。

各Artifact Typeに許容されるFile Formatは、Applicable Source of Truth、Production Requirementまたは正式なHuman Decisionに従う。

File Extensionを変更するだけで、Artifactの正式なFormat Conversionが完了したものとみなしてはならない。

---

## 5.10 Date and Timestamp

Production Artifactの基本Filename Identityには、DateまたはTimestampを必須構成要素として含めない。

したがって、基本Naming Conventionは、

FILE-XXX\_\[ARTIFACT-TYPE\]\_vX.Y.ext

を維持する。

Date、Created At、Updated Atその他の時間情報が必要となる場合、それらはApplicable Source of Truthに従って管理する。

DateまたはTimestampをFilenameへ追加する必要が将来正式に確認された場合は、Versionとの責務重複、Sorting、Traceability、AutomationおよびCompatibilityへの影響を確認した上で正式な変更工程を経る。

---

## 5.11 Draft, Approved and Status Tokens

基本Filename Identityには、\`DRAFT\`、\`APPROVED\`、\`PASS\`、\`PUBLISHED\`その他のWorkflow、Audit、ApprovalまたはPublication Stateを示すTokenを必須構成要素として含めない。

例えば、

FILE-001_RESEARCH_APPROVED_v1.0.md

のようなNamingを、本章を根拠として正式Conventionへ追加してはならない。

Artifact StateはFilenameだけに依存して管理せず、Applicable Source of Truthおよび正式なOperational Metadataとの整合を維持する。

将来、特定のStatus TokenをFilenameへ含める必要性が正式に確認された場合は、既存のStatus Managementとの責務重複およびCompatibilityへの影響を確認した上で正式に定義する。

---

## 5.12 Working Copies and Temporary Files

Working Copy、一時File、Backup、Exportその他の非正式Copyを、正式なProduction Artifactと混同してはならない。

正式Filename Conventionに類似した名称を持つFileであっても、それだけを根拠として正式Artifactとみなしてはならない。

Working CopyまたはTemporary Fileの具体的なNaming Conventionが正式に必要となる場合は、その目的、保存場所、Lifecycle、正式Artifactとの識別方法および削除条件を確認した上で定義する。

本章は、未確定のWorking Copy、Temporary File、BackupまたはExport Naming Conventionを推測によって新設しない。

---

## 5.13 Multiple Versions and Historical Preservation

同一Caseおよび同一Artifact Typeについて複数Versionが存在する場合、各VersionをFilename上で識別可能な状態にする。

例：

FILE-001_RESEARCH_v1.0.md
FILE-001_RESEARCH_v1.1.md

Version更新によって必要なVersion HistoryまたはTraceabilityを失う管理を行ってはならない。

新しいVersionがCurrent Versionとなった場合でも、旧Versionをその事実だけを理由として上書きまたは削除してはならない。

旧Versionは、Applicableな範囲でArtifact Identity、Version Relation、Applicable Audit Result、Applicable Final Flow Audit、Human Approval Decision、Repository Integration、Publication、Correction、Replacement、Supersessionその他Applicable Source of Truthが要求するHistorical Traceabilityを維持できる状態で保持する。

旧Versionを保持することは、そのVersionが現在もApplicableまたはCurrentであることを意味しない。

したがって、

Historical Preservation
≠
Current Applicability

とする。

旧Versionの削除をDefault Operationとしてはならない。

旧Versionを削除する場合は、Applicable Source of Truthまたは明示的なHuman Decisionによって削除可能であること、および必要なHistorical Traceabilityを破壊しないことを確認しなければならない。

Historical Version Retentionを理由として、本章から新しい物理\`archive/\` Directoryを自動的に追加してはならない。

本Version Ruleだけを根拠として、Retention Period、Automatic Deletion Schedule、Archive Filename Convention、Archive専用Metadata Field、Archive専用Database FieldまたはAutomatic Archive Migrationを独自に確定してはならない。

物理的なArchive Placementまたは追加のRetention Ruleが必要となる場合は、Chapter 2、Chapter 3およびApplicable Source of Truthに従い、必要なReviewおよびHuman Decisionを経て正式に決定する。

Current Versionへの変更だけを理由として、旧Versionを自動移動、自動Renameまたは自動削除してはならない。

---

## 5.14 Asset Naming Boundary

Asset Filenameについて、本章はProduction Artifactと同一のNaming Conventionを自動適用しない。

AssetはChapter 4で定義されたAsset Layerの責務に従い、そのNaming、Source、License、Caption、Visual Role、Metadataその他の専門仕様はImage Rule、Art Bibleその他のApplicable Source of Truthとの整合を維持する。

FILE-XXX\_\[ARTIFACT-TYPE\]\_vX.Y.ext

というProduction Artifact Naming Conventionの存在だけを根拠として、Asset Filename Conventionを推測してはならない。

Asset Filename Conventionが正式に必要となる場合は、Asset Managementに関する未確定事項および関連Source of Truthとの整合を確認した上で定義する。

---

## 5.15 Audit Artifact Naming Boundary

Audit ArtifactのFilenameについて、本章は具体的なNaming Conventionを確定しない。

Audit Artifactは対象ArtifactとのTraceabilityを維持し、Case単位の正式な物理Repository PlacementについてはChapter 3で定義された\`cases/FILE-XXX/audit/\`に従う。

物理Placementが正式決定されていることだけを理由として、Audit ArtifactのFilename ConventionまたはVersioningを推測してはならない。

したがって、Audit Artifactについて、

FILE-XXX_AUDIT_vX.Y.ext

その他のNaming Conventionを、本章を根拠として正式仕様へ追加してはならない。

Audit ArtifactのNamingを正式化する場合は、Audit ArtifactのIdentity、対象ArtifactとのRelationship、Version、Repository Placement、Audit Ruleとの責務境界およびTraceabilityを確認する。

Audit Artifactの物理Placementに関するDecisionから、Audit Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、SubdirectoryまたはAutomation実装を派生させてはならない。

---

## 5.16 Naming Convention Expansion

新しいArtifact Type、Filename ComponentまたはNaming Conventionが必要となった場合、既存Conventionへ便宜的に追加してはならない。

追加を正式化する場合は、少なくとも以下を確認する。

- Naming Componentの目的
- 対象Artifact Type
- Case Identityとの関係
- Version Identityとの関係
- Repository Placementとの関係
- Operational Metadataとの責務境界
- Databaseへの影響
- Auditへの影響
- Automationへの影響
- Compatibilityへの影響
- Existing ArtifactへのMigration Impact

必要なReview、Human Decisionおよび正式なVersion更新を経た後にのみRepository Ruleへ反映する。

---

## 5.17 Production Artifact Version Increment Principle

Production ArtifactのVersion Incrementは、変更量の大小だけではなく、対象Artifactに成立している正式な承認境界への影響を基準として判定する。

本RuleにおけるVersion Increment Modelは、Approval Boundary Modelを採用する。

本章における「承認境界」とは、Human Approval Decision単独を意味しない。

承認境界とは、対象Artifactの正式な成立範囲を判断するためにApplicableとなる、Artifact Identity、目的、責務、主要構成、主要内容、Required Audit、Applicable Final Flow Audit、Human Approval Decisionその他Applicable Source of Truthとの関係を含む判断境界をいう。

したがって、

Approval Boundary
≠
Human Approval Decision単独

とする。

Production Artifactに実質的変更が発生した場合、変更後Artifactが既存の承認境界を維持できるかを確認し、MajorまたはMinor Version Incrementを判定する。

Audit Correction、Content Revision、Publication Revision、Human Approval後のRevision、Repository Integration後のRevisionその他のRevision発生原因だけを根拠として、MajorまたはMinorを自動決定してはならない。

---

## 5.18 Major Version Increment

既存Artifactの承認境界を維持できず、新しい正式Artifactとして再評価する必要がある実質的変更を行う場合、Major VersionをIncrementする。

基本遷移は以下とする。

vX.Y
↓
v(X+1).0

Major Version Incrementの対象には、Artifactの目的、責務、主要構成、主要内容その他、既存の正式成立範囲を実質的に作り直し、既存の承認境界をそのまま維持できない変更を含む。

単に変更行数が多いこと、File Sizeが大きく変化したこと、作業量が多いことその他の定量的理由だけを根拠としてMajor Versionを決定してはならない。

---

## 5.19 Minor Version Increment

同一Artifact Identityおよび基本的な承認境界を維持したまま、Artifactの正式内容に実質的変更を行う場合、Minor VersionをIncrementする。

基本遷移は以下とする。

vX.Y
↓
vX.(Y+1)

Minor Version Incrementには、承認境界を維持できる範囲での新情報追加、限定的なContent Revision、Audit Correction、Publication Revisionその他の実質的内容変更を含むことができる。

ただし、Audit Correction、Content RevisionまたはPublication Revisionであるという理由だけで、自動的にMinor Versionとしてはならない。

変更によって既存の承認境界を維持できない場合は、Major Version Increment Criteriaに従う。

---

## 5.20 No Version Increment

Artifactの意味、情報、論旨、構造または承認対象を変更しない非実質的修正については、Version Incrementを要求しない。

誤字、脱字、空白、改行、Markdown、表示整形その他のCorrectionは、Artifactの意味、情報、論旨、構造および承認対象を変更しないことが確認できる場合に限り、No Version Incrementとして扱うことができる。

「軽微な変更である」という理由だけを根拠としてNo Version Incrementとしてはならない。

Artifactの意味、情報、論旨、構造または承認対象のいずれかに実質的変更が生じる場合は、MajorまたはMinor Version Increment Criteriaに従って判定する。

以下の状態または工程それ自体は、Automatic Version Incrementの根拠としない。

- Workflow Statusの変更
- Publication Statusの変更
- Human Approval記録の更新
- Repository Integration
- Re-Integration
- Repository上のPlacement変更
- Filename Rename
- Timestamp更新
- Metadata変更
- Migration

ただし、これらと同時にProduction Artifactの正式内容が変更された場合は、その内容変更を本章のVersion Increment Criteriaによって判定する。

---

## 5.21 Revision Type and Version Boundary

Audit Correction、Content Revision、Publication Revision、Human Approval後のRevisionおよびRepository Integration後のRevisionは、Version Incrementの発生原因を示すことができるが、それ自体をMajorまたはMinor Versionの固定的な分類として扱わない。

Version Incrementは、実際の変更内容と既存の承認境界への影響によって判定する。

したがって、

Audit Correction
≠
Automatic Minor Increment

Publication Revision
≠
Automatic Minor Increment

Human Approval後のRevision
≠
Automatic Major Increment

Repository Integration
≠
Automatic Version Increment

とする。

Revisionによって新Versionが成立した場合でも、旧Versionに成立していたAudit Result、Final Flow AuditまたはHuman Approval Decisionを新Versionへ自動継承してはならない。

---

## 5.22 Current Version Selection

Production ArtifactのCurrent Versionとは、Version番号、Timestamp、Filename、Repository Placementまたは更新日時が単に最新であるVersionではなく、当該Artifactについて現在正式にApplicableであることが確認されたVersionをいう。

MajorまたはMinor Versionが新たに生成されたことだけを理由として、そのVersionを自動的にCurrent Versionとしてはならない。

Current Versionの判定では、Applicableな範囲で以下とのTraceabilityおよび整合を確認する。

- Artifact Identity
- Artifact Version
- Version Relation
- Required Production / Publication Audit
- Applicable Final Flow Audit
- Human Approval Decision
- Repository Integration
- Publication
- Applicable Source of Truth

新VersionがProductionまたはRevision工程中であり、Currentとして正式にApplicableであることが確認されていない場合、Version番号が大きいことだけを理由として既存Current Versionを置換してはならない。

複数Versionが存在し、Applicable Source of Truthおよび確認可能なTraceabilityからCurrent Versionを一意に判定できない場合、AI AgentまたはAutomationは推測によってCurrent Versionを決定してはならない。

その場合はHuman Reviewへ送る。

---

## 5.23 Version Decision and Automation Boundary

AI AgentまたはAutomationは、本章のVersion Criteriaおよび確認可能なEvidenceから一意に判定できる範囲を超えて、Major、Minor、No Version IncrementまたはCurrent Versionを推測によって決定してはならない。

変更量、File Size、Timestamp、Filename、Directory Placement、Workflow Statusその他の単独条件からVersion Decisionを推測してはならない。

Major、Minor、No Version IncrementまたはCurrent Versionのいずれに該当するか一意に判断できない場合は、Conflictまたは未確認状態を不可視化せず、Human Reviewへ送る。

AutomationによるVersion処理が成功したという事実だけを、Version Decisionの正式な根拠として扱ってはならない。

---

## 5.24 HOLD-ARTIFACT-VERSION-01 Reflection State

\`HOLD-ARTIFACT-VERSION-01\`について、Production Artifact Version Increment Criteria、Patch Component、Revision Typeとの関係、Current Version SelectionおよびHistorical Version Retention / Archive Boundaryに関する必要なHuman Decisionは完了している。

決定内容は本章へ反映されている。

Resolution前は、本章への反映だけでは\`HOLD-ARTIFACT-VERSION-01\`をRESOLVEDとせず、Audit Rule、AGENTS.md、Repository Integration、Compatibility、Automationその他Applicable Source of Truthとの最終Compatibility確認、必要な反映および最終横断再監査のPASSが要求されていた。

これらのResolution条件は完了し、\`HOLD-ARTIFACT-VERSION-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

本HOLDのResolutionから、Audit Artifact固有のVersioning、専用\`archive/\` Directory、Retention Period、Automatic Deletion Scheduleまたは追加Database / Metadata Fieldを推測してはならない。

\`HOLD-PUBLICATION-TRACKING-01\`は本HOLDとは別個のResolution工程を経ており、現在は正式HOLD Ledger上でRESOLVEDとして管理されている。

---

## 5.25 Core Naming and Versioning Principle

ProjectORIGINのProduction Artifactは、

\*\*Case Identity、Artifact TypeおよびArtifact VersionをRepository上で明示的に識別し、Filename、Repository Placement、Version DecisionおよびArtifact Stateを混同しない。\*\*

Production Artifactの基本Naming Conventionは、

FILE-XXX\_\[ARTIFACT-TYPE\]\_vX.Y.ext

とする。

Production Artifactの基本Version表記は、

vX.Y

とする。

Version IncrementはApproval Boundary Modelに従い、Major、MinorまたはNo Version Incrementとして判定する。

Filename、Version、Workflow Status、Audit Result、Human Approval Decision、Repository IntegrationおよびPublication Statusは、それぞれの正式な責務を維持する。

NamingまたはVersioningだけを根拠として、ArtifactのContent、Audit Result、Approval State、Current ApplicabilityまたはPublication Stateを推測してはならない。
---
---

## 5.26 Publication Tracking Metadata Naming and Version Boundary

\`publication-tracking.json\`は、Chapter 3およびChapter 4で定義された
Case-level Repository-managed Operational Metadata Artifactであり、
Production Artifactではない。

したがって、\`publication-tracking.json\`には、本章でProduction Artifactに対して
定義する以下のNaming and Versioning Ruleを適用しない。

- \`FILE-XXX\_\[ARTIFACT-TYPE\]\_vX.Y.ext\`
- Production Artifact Version \`vX.Y\`
- Major Version Increment Criteria
- Minor Version Increment Criteria
- No Version Increment Criteria
- Approval Boundary ModelによるProduction Artifact Version Decision

\`publication-tracking.json\`の正式なRepository上のFilenameは、

publication-tracking.json

とする。

本Sectionから、

publication-tracking_vX.Y.json

その他のVersion Suffixを持つFilename Conventionを派生させてはならない。

また、本Sectionは\`publication-tracking.json\`について、

- 独立したMetadata Version
- Patch Version
- Historical Metadata Version Convention
- Archive Filename Convention
- 専用\`archive/\` Directory
- Retention Period
- Automatic Deletion Schedule

を新たに定義しない。

FREE Publication ArtifactまたはCLASSIFIED Publication Artifactの
Production Artifact Versionが変更されたことだけを理由として、
\`publication-tracking.json\`自体へProduction Artifact Versionを付与してはならない。

\`publication-tracking.json\`に保持されるApplicable Audit Referenceについて、
対象Publication ArtifactのApplicable Versionとの整合を確認する必要がある場合、
その確認はReference、TraceabilityおよびValidationの責務として扱う。

対象Production ArtifactのVersionを参照または検証することは、
\`publication-tracking.json\`自体がProduction Artifact Versionを持つことを意味しない。

したがって、

Referenced Artifact Version
≠
publication-tracking.json Version

とする。

Applicable Audit Referenceが参照するAudit Artifactについても、
本SectionからAudit Artifact固有のFilename Conventionまたは
Audit Artifact Versioningを新たに定義してはならない。

Production Artifact Version Criteriaは本章のApplicable Sectionに従い、
Publication Tracking Metadataの責務、Controlled Values、
Applicable Audit Reference、Workflow Statusとの関係およびValidationは、
Chapter 3、Chapter 4および本書のApplicableな後続Sectionに従う。

---

# Chapter 6

# Workflow Status and Publication Status

## 6.1 Purpose

本章は、ProjectORIGINにおけるCase Workflow StatusおよびPublication StatusのRepository上の正式な管理原則を定義する。
Workflow Statusは、CaseがProduction Workflow上のどの段階にあるかを表す。
Publication Statusは、Caseが正式なPublication済み状態にあるかを表す。
Case Resolution Status、Workflow Status、Audit Result、Human Approval DecisionおよびPublication Statusは、それぞれ異なる責務を持つ独立した状態概念として管理する。
本章は、AGENTS.mdが管理するProduction Workflowの工程順序、Audit Ruleが管理するAudit Resultおよび品質監査基準、Database RuleおよびDatabase Schemaが管理するDatabase仕様を変更または置換しない。

## 6.2 Status Responsibility Separation

ProjectORIGINでは、状態に関する異なる責務を一つのStatus体系へ統合しない。

少なくとも以下を独立した状態または判断概念として管理する。

 Case Resolution Status
 ≠
 Case-level Workflow Status
 ≠
 Artifact-level Production State
 ≠
 Audit Result
 ≠
 Human Approval Decision
 ≠
 Publication Status

Case Resolution Statusは、Caseそのものの解決状態に関する責務を持つ。

Case-level Workflow Statusは、対象CaseがProduction Workflow上のどの段階にあるかをRepository上で識別する責務を持つ。

Artifact-level Production Stateは、ApplicableなFREE Publication ArtifactおよびCLASSIFIED Publication ArtifactそれぞれのProduction進行状態を識別する責務を持つ。

Artifact-level Production StateはCase-level Workflow Statusではない。

Audit Resultは、Applicable Audit Source of Truthに従って監査結果を表す。

Human Approval Decisionは、人間による正式判断を表す。

Publication Statusは、対象CaseまたはApplicableな公開対象がPublication済みであるかをRepository上で識別するための独立した状態概念とする。

これらの一つの値だけを根拠として、他の状態または判断を自動的に確定してはならない。

FREEおよびCLASSIFIEDのArtifact-level Trackingは、

 cases/FILE-XXX/publication-tracking.json

をRepository管理領域におけるPrimary Source of Truthとして管理する。

Artifact-level TrackingのControlled Valuesおよび具体的責務はChapter 3およびChapter 4に従う。

本Sectionから新しいCase-level Workflow Status、Artifact-level Production State、Audit Result、Human Approval DecisionまたはPublication StatusのControlled Valueを追加してはならない。

## 6.3 Workflow Status Principle

Workflow Statusは、CaseがProduction Workflow上のどの段階にあるかを表す。
Workflow Statusは、Publication済みかどうかを直接表すものではない。
また、Workflow Statusだけを根拠として、必要なProduction、Audit、Final Flow Audit、Human Approval、Repository IntegrationまたはPublicationが実際に完了した証拠として扱ってはならない。
各工程の完了は、Applicable Source of Truthおよび必要なEvidenceによって確認する。

## 6.4 Workflow Status Primary States

ProjectORIGINにおけるCase-level Workflow Statusの正式なPrimary Statesは、以下とする。
 `REGISTERED`
 `RESEARCHING`
 `RESEARCH_AUDIT`
 `APPROVED_RESEARCH`
 `MASTER_PRODUCTION`
 `MASTER_AUDIT`
 `APPROVED_MASTER`
 `PUBLICATION_PRODUCTION`
 `PUBLICATION_AUDIT`
 `HUMAN_REVIEW`
 `APPROVED`
これらのPrimary Statesは、CaseがProduction Workflow上のどの主要段階にあるかを表す。
Workflow Statusの名称を、一般的な開発慣行または過去のStatus表現だけを根拠として追加、変更または置換してはならない。

## 6.5 Workflow Exception States

ProjectORIGINにおけるWorkflow Exception Statesは、以下とする。
 `REVISION_REQUIRED`
 `BLOCKED`
**REVISION_REQUIRED**
Applicableな問題が確認され、Responsible StageでRevisionおよび必要なRe-Auditが必要な状態を表す。
`REVISION_REQUIRED`はWorkflow Exception Stateであり、Human Approval Decisionの`REVISION REQUESTED`と同一の管理値として扱ってはならない。
**BLOCKED**
未解決のBlocking Issue、Rule Conflict、Source Conflict、Dependencyその他の理由により、Workflowを安全に進行できない状態を表す。
`BLOCKED`はPublication Statusではない。
また、Human Approval Decisionの代替として使用してはならない。

## 6.6 Workflow Progression Principle

Workflow Statusは、Applicable Source of Truthで定義されたProduction Flowに従って管理する。
Status値を変更しただけで、対象工程が正式に完了したものとして扱ってはならない。
例えば、
 `APPROVED_RESEARCH`は、必要なResearch ProductionおよびResearch Auditの成立確認なしに設定しない。
 `APPROVED_MASTER`は、必要なMaster ProductionおよびMaster Auditの成立確認なしに設定しない。
 `HUMAN_REVIEW`は、ApplicableなRequired Publication AuditsおよびFinal Flow Auditへの必要条件を無視して設定しない。
 `APPROVED`は、正式なHuman Approval Decisionの根拠なしに設定しない。
Workflow Statusは工程の状態を表すものであり、工程完了Evidenceそのものではない。

## 6.7 PUBLICATION_PRODUCTION

`PUBLICATION_PRODUCTION`は、対象CaseにおけるApplicableなPublication ArtifactのProductionを行うCase-level Workflow Statusとする。

FREE Publication ArtifactおよびCLASSIFIED Publication Artifactは、それぞれ独立したArtifact IdentityおよびArtifact-level Trackingを持つ。

Case-level Workflow StatusとArtifact-level Production Stateを同一概念として扱ってはならない。

 Case-level Workflow Status
 ≠
 Artifact-level Production State

FREEおよびCLASSIFIEDそれぞれのApplicabilityおよびProduction Stateは、

 cases/FILE-XXX/publication-tracking.json

によって管理する。

Applicabilityが`APPLICABLE`であるPublication Artifactについて、少なくとも一つのProduction Stateが`COMPLETE`ではない場合、Case-level Workflow Statusは`PUBLICATION_PRODUCTION`に留まる、またはApplicableな後続工程から`PUBLICATION_PRODUCTION`へ戻す。

すべての`APPLICABLE`なPublication ArtifactのProduction Stateが`COMPLETE`である場合に限り、Publication Production Gateを満たしたものとして`PUBLICATION_AUDIT`への進行を許可できる。

`NOT_APPLICABLE`であるPublication ArtifactについてProduction Stateを要求してはならず、Publication Production GateのProduction Completion判定対象にも含めない。

一方のPublication Artifactが`COMPLETE`であることだけを根拠として、他方のPublication ArtifactのProduction Stateを`COMPLETE`と推測してはならない。

Repository上にFREEまたはCLASSIFIED Artifactが存在することだけを根拠として、そのProduction Stateを`COMPLETE`と判断してはならない。

本Sectionは、FREE用またはCLASSIFIED用の新しいCase-level Workflow Statusを定義しない。

例えば、

 FREE_PUBLICATION_PRODUCTION
 CLASSIFIED_PUBLICATION_PRODUCTION
 FREE_COMPLETE
 CLASSIFIED_COMPLETE

その他の未定義TokenをCase-level Workflow Statusとして追加してはならない。。

## 6.8 PUBLICATION_AUDIT

`PUBLICATION_AUDIT`は、Publication Production Gateを満たした対象Caseについて、ApplicableなPublication Artifactの必要なAuditを行うCase-level Workflow Statusとする。

`PUBLICATION_AUDIT`へ進行するためには、すべての`APPLICABLE`なPublication Artifactについて、Artifact-level Production Stateが`COMPLETE`でなければならない。

`NOT_APPLICABLE`であるPublication ArtifactについてProduction StateまたはAuditの存在を、本Sectionだけを根拠として要求してはならない。

FREE Publication ArtifactおよびCLASSIFIED Publication Artifactは独立したArtifact Identityを持つため、一方のAudit ResultまたはApplicable Audit Referenceを他方へ流用してはならない。

Applicable Audit Referenceは、

 cases/FILE-XXX/publication-tracking.json

において対象Publication Artifactごとに管理する。

Applicable Audit Referenceは、Applicable Audit ArtifactへのRepository-relative Referenceとして扱い、Audit Resultそのものを複製するFieldとして扱ってはならない。

Applicable Audit Referenceの存在だけを根拠としてAudit Resultを推測してはならない。

Publication Audit後のRevisionによって、`APPLICABLE`なPublication ArtifactがProductionへ差し戻される場合、その対象ArtifactのProduction Stateを`IN_PROGRESS`として管理し、Case-level Workflow Statusを`PUBLICATION_PRODUCTION`へ戻す。

このReturn Gateによって、

 PUBLICATION_AUDIT
 ↓
 Applicable Artifact Revision
 ↓
 Artifact-level Production State = IN_PROGRESS
 ↓
 PUBLICATION_PRODUCTION

の関係を維持する。

修正後、再びすべての`APPLICABLE`なPublication Artifactが`COMPLETE`となった場合にのみ、`PUBLICATION_AUDIT`への再進行を許可できる。

Audit Result、Audit Method、PASS、REVISION、BLOCKERその他の監査仕様はAudit Ruleの責務とし、本Sectionから新しいAudit Resultを定義してはならない。

## 6.9 Publication Status Principle

Publication Statusは、対象Caseが正式なPublication済み状態にあるかを表す。
Publication StatusはProduction Workflowの進行段階、Audit ResultまたはHuman Approval Decisionを表すために使用しない。
ProjectORIGINにおけるPublication Statusの正式なControlled Valuesは、以下の2値とする。
 `NOT_PUBLISHED`
 `PUBLISHED`
この2値モデルは、Production、Audit、Human ApprovalおよびPublicationの責務を分離するための正式なPublication Statusモデルとして使用する。
Audit Ruleにおいても、Publication StatusはWorkflow Status、Audit ResultおよびHuman Approval Decisionから独立した状態概念として扱い、正式なControlled Valuesとして`NOT_PUBLISHED`および`PUBLISHED`を使用する。
旧Audit RuleでPublication Statusとして使用されていた状態表現は、現在のPublication Status Controlled Valuesとして使用しない。

## 6.10 NOT_PUBLISHED

`NOT_PUBLISHED`は、対象Caseについて正式なPublication済み状態が成立していないことを表す。
`NOT_PUBLISHED`には、以下の状態が含まれ得る。
 Production開始前
 Research進行中
 Audit進行中
 Master Production進行中
 Publication Production進行中
 Publication Audit進行中
 Human Review中
 Human Approval完了後かつRepository IntegrationまたはPublication完了前
 その他、正式なPublication完了Evidenceが確認されていない状態
したがって、`NOT_PUBLISHED`だけを根拠としてCaseのProduction進行段階を判断してはならない。
Production進行状態はWorkflow Statusによって独立して確認する。
Human Approval Decisionが`APPROVED`であっても、正式なPublicationが完了していない場合、Publication Statusは`NOT_PUBLISHED`であり得る。

## 6.11 PUBLISHED

`PUBLISHED`は、対象CaseについてApplicableなPublication Processが正式に完了し、Publication済み状態が成立していることを表す。
`PUBLISHED`は、Workflow Statusとして使用しない。
また、以下だけを根拠として`PUBLISHED`を設定してはならない。
 Production完了
 Audit PASS
 Final Flow Audit PASS
 Human Review開始
 Human Approval Decision `APPROVED`
 Workflow Status `APPROVED`
 Repository Integrationのみの完了
 Filename変更
 Version更新
 Status値の手動変更
`PUBLISHED`は、Applicable Source of Truthに従った正式なPublication完了を確認できる場合にのみ使用する。
したがって、
`Audit PASS`
`    ``≠`
`Human Approval`

`Human Approval`
`    ``≠`
`Repository Integration`

`Repository Integration`
`    ``≠`
`Publication`

`APPROVED`
`    ``≠`
`PUBLISHED`
とする。

## 6.12 Publication Status Independence

Publication Statusは、Case-level Workflow Status、Artifact-level Production State、Audit ResultおよびHuman Approval Decisionとは独立して管理する。

正式なPublication Statusは、

 NOT_PUBLISHED
 PUBLISHED

とする。

Artifact-level Production Stateが`COMPLETE`であることだけを根拠として、Publication Statusを`PUBLISHED`へ変更してはならない。

同様に、すべてのApplicableなPublication Artifactが`COMPLETE`であること、Applicable Audit Referenceが存在すること、Auditが完了していること、またはCase-level Workflow Statusが`APPROVED`であることだけを根拠として、Publication Statusを`PUBLISHED`と判断してはならない。

 Artifact-level Production State
 ≠
 Publication Status

 Audit Result
 ≠
 Publication Status

 Human Approval Decision
 ≠
 Publication Status

Publication Statusの変更には、Applicable Source of Truthおよび正式なPublication Evidenceに基づく独立した確認を必要とする。

`publication-tracking.json`はFREEおよびCLASSIFIEDのArtifact-level Trackingを管理するが、Publication Statusを自動的に導出するためのSource of Truthとして扱ってはならない。

本Sectionから新しいPublication Status Controlled Valueを追加してはならない。

## 6.13 Audit Result Boundary

Audit ResultはPublication Statusではない。
Audit PASSは、対象Artifactまたは対象工程がApplicable Audit Criteriaを満たしたことを表す。
Audit PASSだけを理由として、
 Workflow Status `APPROVED`
 Human Approval Decision `APPROVED`
 Publication Status `PUBLISHED`
を成立させてはならない。
Audit Resultの正式な判定基準および監査方法はAudit Ruleの責務とする。
Repository RuleはAudit ResultのControlled Valuesを本章によって新たに定義しない。

## 6.14 Human Approval Decision Boundary

Human Approval DecisionはPublication Statusではない。
正式なHuman Approval DecisionはAGENTS.mdの責務とする。
Human Approval Decision `APPROVED`は、Publicationへ進むために必要な正式判断であるが、それ自体はPublication完了を意味しない。
同様に、Human Approval Decision `REVISION REQUESTED`をWorkflow Exception State `REVISION_REQUIRED`と同一のControlled Valueとして扱ってはならない。
Human Approval Decision `HOLD`をWorkflow Status `BLOCKED`と自動的に同一視してはならない。
異なる責務を持つ状態値は、それぞれ独立して管理する。

## 6.15 Repository Integration Boundary

Repository Integrationは、Human Approval後の正式成果物をApplicable Repository Structureへ統合する工程である。
Repository Integrationの完了だけを理由としてPublication Statusを`PUBLISHED`へ変更してはならない。
Repository IntegrationとPublicationは独立した工程として扱う。
`Human Approval`
`    ``≠`
`Repository Integration`

`Repository Integration`
`    ``≠`
`Publication`
Repository Integrationに必要なArtifact、Version、Metadata、Asset Referenceその他の更新は、Applicable Source of Truthに従う。
Database FieldまたはOperational Metadataの具体的なSchemaを、本章だけを根拠として新設してはならない。

## 6.16 Database and Metadata Boundary

Workflow StatusおよびPublication Statusは、Repository上の状態管理概念として本章で定義する。

Artifact-level Trackingについては、

 cases/FILE-XXX/publication-tracking.json

をCase-level Repository-managed Operational Metadata Artifactとして使用する。

`publication-tracking.json`はDatabase Fieldではなく、新しいProduction Layerでもない。

その正式なRepository Placement、管理対象、Controlled Valuesおよび責務境界はApplicable Repository Rule Sectionに従う。

本章の定義だけを根拠として、新しいDatabase Field、Data Type、Nullability、Metadata Directory、Production LayerまたはStorage Structureを追加してはならない。

Databaseに保存する正式FieldおよびSchema仕様はDatabase RuleおよびDatabase Schemaの責務とする。

Database Schemaで定義されるCase Resolution status Fieldを、Case-level Workflow Status、Artifact-level Production StateまたはPublication Statusの保存先として使用してはならない。

`publication-tracking.json`の存在を理由として、Database SchemaへFREE / CLASSIFIED Artifact-level Tracking用Fieldを自動的に追加してはならない。

Workflow StatusまたはPublication Statusについて別途永続的保存仕様が必要となる場合、その具体的仕様はApplicable Source of Truthまたは必要なHuman Decisionによって正式決定する。

本Sectionから未定義のMetadata Field、Metadata Versioning SchemeまたはDatabase Mappingを推測してはならない。

## 6.17 Evidence and Traceability

Status値またはArtifact-level Tracking値そのものを、工程完了またはPublication完了のEvidenceとして扱ってはならない。

必要に応じて、以下を独立して確認可能な状態を維持する。

 Production対象Artifact
 Artifact Identity
 Artifact Version
 Artifact Applicability
 Artifact-level Production State
 Applicable Production Stage
 Applicable Audit Reference
 Required Audit
 Audit Result
 Final Flow Audit
 Human Approval Decision
 Repository Integration
 Publication
 Publication Status

FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Trackingは、

 cases/FILE-XXX/publication-tracking.json

によってTrace可能な状態を維持する。

Applicable Audit Referenceは、対象ArtifactにApplicableなAudit ArtifactへのRepository-relative Referenceとして扱う。

Applicable Audit ReferenceはAudit Resultそのものではなく、Audit Resultを複製するFieldとして使用してはならない。

Applicable Audit Referenceを検証する場合、少なくとも対象Case、対象Artifact、Applicable Versionおよび実際にApplicableなAuditとの対応を確認する。

Referenceが存在しない、別Caseを参照している、対象Artifactが一致しない、Applicable Versionが一致しない、またはApplicable Auditを一意に確認できない場合は、Reference Validationを成功として扱ってはならない。

Reference Validationの失敗それ自体をAudit Result `BLOCKER`と同一視してはならない。

曖昧なApplicable Audit ReferenceをAutomationによって推測、補完または自動修復してはならない。

例えば、Case-level Workflow Statusが`APPROVED`であっても、Publication Evidenceが確認できない場合は`PUBLISHED`と判断してはならない。

同様に、Publication Statusが`PUBLISHED`であるという値だけを根拠として、必要な上流工程のEvidenceを推測してはならない。

TraceabilityはApplicable Source of Truthおよび正式な記録によって維持する。

本SectionからAudit Artifact Filename ConventionまたはAudit Artifact固有のVersioning Schemeを新設してはならない。

## 6.18 Core Status Principle

ProjectORIGINでは、

 Case Resolution Status
 Case-level Workflow Status
 Artifact-level Production State
 Audit Result
 Human Approval Decision
 Publication Status

を、それぞれ独立した責務を持つ状態または判断概念として管理する。

Case-level Workflow Statusの正式なPrimary Statesは、

 REGISTERED
 RESEARCHING
 RESEARCH_AUDIT
 APPROVED_RESEARCH
 MASTER_PRODUCTION
 MASTER_AUDIT
 APPROVED_MASTER
 PUBLICATION_PRODUCTION
 PUBLICATION_AUDIT
 HUMAN_REVIEW
 APPROVED

とする。

Exception Statesは、Applicable Repository Rule Sectionで定義された正式値のみを使用する。

FREEおよびCLASSIFIEDのArtifact-level Production StateはCase-level Workflow Statusではない。

Artifact-level Production Stateの正式なControlled Valuesは、

 NOT_STARTED
 IN_PROGRESS
 COMPLETE

とする。

Artifact Applicabilityの正式なControlled Valuesは、

 APPLICABLE
 NOT_APPLICABLE

とする。

`NOT_APPLICABLE`をArtifact-level Production Stateとして扱ってはならない。

FREEおよびCLASSIFIEDについて、新しいCase-level Workflow Statusを追加してはならない。

ApplicableなPublication ArtifactがProduction未完了である場合、Case-level Workflow Statusは`PUBLICATION_PRODUCTION`に留まる、または必要に応じて`PUBLICATION_PRODUCTION`へ戻す。

すべてのApplicableなPublication Artifactが`COMPLETE`である場合にのみ、Publication Production Gateを満たし、`PUBLICATION_AUDIT`への進行を許可できる。

Publication Audit後のRevisionによってApplicableなPublication ArtifactがProductionへ戻る場合、そのArtifact-level Production Stateを`IN_PROGRESS`として管理し、Case-level Workflow Statusを`PUBLICATION_PRODUCTION`へ戻す。

Publication Statusは、

 NOT_PUBLISHED
 PUBLISHED

の独立した状態として管理し、Case-level Workflow Status、Artifact-level Production State、Audit ResultまたはHuman Approval Decisionから自動導出してはならない。

Artifact-level TrackingのPrimary Source of Truthは、

 cases/FILE-XXX/publication-tracking.json

とする。

ただし、Artifact-level Trackingの存在によってDatabase Schema Field、Audit Result、Human Approval Decision、Publication Statusまたは未定義のWorkflow Statusを新設または自動生成してはならない。

Automationは、正式に定義されたControlled Values、Reference、Workflow GateおよびResponsibility Boundaryを検証できる。

Automationは、未確定のApplicability、Production State、Applicable Audit Reference、Audit Result、Publication Statusまたはその他の状態を推測してはならない。

既存Caseについて、既存Fileの存在だけを根拠としてApplicabilityまたはProduction Stateを一括推定してはならない。

曖昧な既存CaseのApplicabilityまたはProduction StateにはHuman Decisionを必要とする。

本章のStatus Modelは、Case-level WorkflowとArtifact-level Publication Trackingを分離しながら、正式なWorkflow Gateによって両者を接続することをCore Principleとする。


# Chapter 7

# Repository Integration

## 7.1 Purpose

本章は、ProjectORIGIN Production Flowにおいて正式なHuman Approvalを経たProduction Artifactおよび関連管理情報を、Repository上の正式な管理状態へ統合するためのRepository Integration原則を定義する。

Repository Integrationは、単なるFile Copy、Directory Placement、Filename変更、Status変更またはDatabase Updateではない。

Repository Integrationでは、対象Caseおよび対象Artifactについて、少なくとも以下の整合性を維持する。

- Stable Identity
- Approved Artifact Identity
- Repository Placement
- Applicable Version
- Workflow Status
- Publication Status
- Metadata
- Asset Reference
- Dependency
- Traceability
- Existing Artifact Protection
- Applicable Source of Truthとの整合

本章はRepository IntegrationのRepository上の責務およびIntegrity要件を定義する。

Production Workflowそのもの、Agentの行動、Audit Criteria、Human Approval Criteria、Database Field、Data Type、Validation、Application ImplementationまたはGit Commandそのものを再定義しない。

それらはAGENTS.md、Audit Rule、Database Rule、Database Schemaその他のApplicable Source of Truthに従う。

---

## 7.2 Repository Integration Principle

ProjectORIGINにおけるRepository Integrationは、

\*\*正式なProduction Flowを通過した対象を、Identity、Version、Status、Metadata、DependencyおよびTraceabilityを維持した状態でRepositoryへ正式統合する工程\*\*

として扱う。

Repository Integrationは、Production ArtifactをRepository上に存在させることだけを目的としない。

以下のいずれかだけでは、正式なRepository Integrationが完了したものとみなしてはならない。

- FileがRepository内に存在する
- 正しいDirectoryにFileが存在する
- Filenameが正式形式に見える
- Version Tokenが付与されている
- Workflow Statusが\`APPROVED\`である
- Publication Statusが\`PUBLISHED\`である
- Database Recordが存在する
- Metadataが存在する
- Asset Referenceが存在する
- Git上で変更履歴が存在する

Repository Integrationの成立には、対象ArtifactおよびCaseについてApplicable Source of Truthが要求する正式な上流条件が満たされ、Repository上の管理状態と実際の正式状態が整合していなければならない。

Repository Integrationによって、未承認ArtifactをApproved Artifactへ昇格させてはならない。

Repository Integrationによって、未公開ArtifactをPublished Artifactへ昇格させてはならない。

Repository Integrationによって、Audit Result、Human Decision、Artifact ContentまたはCase Factを変更してはならない。

Repository Integrationは、既に成立した正式状態をRepository上へ正確に反映し、追跡可能に維持する工程とする。

---

## 7.3 Integration Entry Conditions

Repository Integrationへ進むためのProduction Workflow上の具体的なGateはAGENTS.mdその他のApplicable Source of Truthに従う。

本章は、それらのGateを独自に追加、削除または置換しない。

ProjectORIGINの標準Production Flowにおいて、Repository Integrationへ進むためには、Applicableな範囲で以下の上流工程が正式に完了していなければならない。

Required Production / Publication Audits PASS
↓
Applicable Final Flow Audit PASS
↓
Applicable Human Approval Decision = APPROVED
↓
Repository Integration

このSequenceは、Applicable Source of Truthによって要求される正式な上流GateをRepository Integrationから省略してはならないことを示す。

対象ArtifactまたはProduction Flowについて追加のAudit、Review、Approvalその他のGateがApplicable Source of Truthによって要求される場合、それらも満たさなければならない。

Repository Integrationを実施する時点では、少なくとも対象Integrationに必要な以下の情報または根拠が確認可能でなければならない。

- 対象CaseのStable Identity
- 対象Production ArtifactのIdentity
- Applicable Artifact Type
- Applicable Repository Layer
- Applicable Version
- 必要な上流ArtifactとのDependency
- Required Production / Publication Audit Result
- Applicable Final Flow Audit Result
- Applicable Human Approval Decision
- Repository Placement
- 必要なWorkflow Status
- 必要なPublication Status
- 必要なMetadata
- 必要なAsset Reference
- Blocking Issueの有無
- Source of Truth Conflictの有無

ただし、本Listに含まれるすべての項目が、すべてのArtifact Typeについて同一形式で必須であることを本章だけから推測してはならない。

対象Artifact、Case、Production StageまたはApplicable Source of Truthに応じて必要条件を確認する。

以下の状態を検出した場合、Repository Integrationを正常完了したものとして扱ってはならない。

- 対象Caseを一意に識別できない
- 対象Artifactを一意に識別できない
- Required Inputが不足している
- Applicable Versionを確認できない
- Required Production / Publication Auditが未完了または非PASSである
- Applicable Final Flow Auditが未完了または非PASSである
- Applicable Human Approval Decisionが\`APPROVED\`ではない
- 必要なHuman Approvalを確認できない
- Blocking Issueが存在する
- Source of Truth Conflictが存在する
- Repository Placementを正式仕様から確認できない
- 既存ArtifactとのIdentity Conflictが存在する
- 必要なDependencyを追跡できない
- Integrationによって既存の正式情報を破壊する可能性がある

Required Production / Publication AuditがPASSしていることだけを理由として、Final Flow Auditが完了したものとみなしてはならない。

Final Flow AuditがPASSしていることだけを理由として、Human Approval Decisionが\`APPROVED\`であるとみなしてはならない。

Human Approval Decisionが\`APPROVED\`であることだけを理由として、Repository Integrationが完了したものとみなしてはならない。

問題の内容に応じたWorkflow処理、Revision、Block、Human ReviewまたはEscalationは、AGENTS.mdその他のApplicable Source of Truthに従う。

Repository Ruleは、それらのProduction Workflow上の処理を独自に再定義しない。

---

## 7.4 Human Approval Boundary

ProjectORIGINの標準Production Flowでは、Repository IntegrationはApplicable Final Flow Audit後のHuman Approvalにおいて、Applicable Human Approval Decisionとして\`APPROVED\`が成立した後に位置する。

したがって、Human Approvalが必要な対象について、AIまたはAutomationがHuman Approvalを代替してRepository Integrationを正式完了させてはならない。

Human Approval工程が実施されたことだけでは、Repository Integration Entry Conditionは成立しない。

Repository Integrationへ進むためには、Applicable Source of Truthに基づくHuman Approval Decisionが\`APPROVED\`であることを確認しなければならない。

Human Approval DecisionとRepository Integrationは異なる責務を持つ。

Human Approvalは、Applicable Production Flowにおいて人間が成果物または公開候補について正式な判断を行う工程である。

Repository Integrationは、その正式な判断その他の必要条件を満たした対象をRepository上の正式管理状態へ反映する工程である。

したがって、

Human Approval Decision = APPROVED
↓
Repository Integration

という順序を維持する。

ただし、

Human Approval ≠ Repository Integration

とする。

Human Approval Decisionが\`APPROVED\`であることだけを理由として、Repository Integrationが完了しているとみなしてはならない。

同様に、Repository上に対象Artifactが存在することだけを理由として、Human Approval Decisionが\`APPROVED\`であるとみなしてはならない。

Human Approval Decisionとして\`REVISION REQUESTED\`が成立している場合、Repository Integrationへ正常進行してはならない。

Applicable Production Flowに従って必要なRevision、Re-Audit、Final Flow Audit、Human Reviewまたはその他の正式工程を確認する。

Human Approval Decisionとして\`HOLD\`が成立している場合、そのHOLDが正式に解消され、Applicable Production Flow上の必要条件が再確認されるまでRepository Integrationへ正常進行してはならない。

\`REVISION REQUESTED\`、\`HOLD\`その他の非承認状態を、Repository Integrationによって上書き、無視または\`APPROVED\`として扱ってはならない。

Human Approval Decisionの正式なControlled ValuesおよびDecision ProcedureはAGENTS.mdその他のApplicable Source of Truthに従う。

Repository RuleはHuman Approval Decision体系を独自に再定義しない。

---

## 7.5 Approved Artifact Identification

Repository Integrationでは、対象となるProduction Artifactが何であるかを明確に識別できなければならない。

対象Artifactの識別では、Applicableな範囲で以下を確認する。

- Case ID
- File Number
- Artifact Type
- Artifact Filename
- Artifact Version
- Repository Layer
- Upstream Artifact
- Dependency
- Applicable Audit
- Applicable Final Flow Audit
- Applicable Human Decision

Case ID、File Numberその他のStable Identifierを、Repository Integrationの都合だけを理由として独自変更してはならない。

Artifact FilenameまたはVersion Tokenだけを根拠として、そのArtifactがApproved Artifactであると判断してはならない。

同様に、Approved Artifactであることだけを理由として、そのArtifactがPublished Artifactであると判断してはならない。

Production Artifactの正式性は、単なるFilename、Directory PlacementまたはVersion表記ではなく、Applicable Source of Truth、Production Flow、Audit、Final Flow Audit、Human Approval、VersionおよびTraceabilityとの整合によって確認する。

複数Versionまたは複数Candidateが存在する場合、最新版に見えることだけを理由としてIntegration対象を決定してはならない。

Applicable Versionおよび正式に承認された対象を確認する。

Production Artifact VersionのIncrement CriteriaおよびCurrent Version SelectionはChapter 5の正式Criteriaに従う。

Version番号が最大であること、Timestampが新しいことまたはFilenameが最新版に見えることだけを理由として、Approved Artifactの優先順位、Revision SeverityまたはCurrent Versionを決定してはならない。

Chapter 5および確認可能なTraceabilityからApplicable VersionまたはCurrent Versionを一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

---

## 7.6 Integration Target

Repository Integrationでは、統合対象となるRepository上の正式なTargetを確認しなければならない。

Integration Targetは、対象Artifactの種類、Case Identity、Repository LayerおよびApplicable Repository Structureに基づいて決定する。

対象Artifactを、便宜上の判断、一般的なDirectory慣行または一時的な作業場所だけを根拠として正式なIntegration Targetへ配置してはならない。

Integration Targetの決定では、Applicableな範囲で少なくとも以下を確認する。

- Case Identity
- Artifact Type
- Repository Layer
- Applicable Directory Structure
- Filename
- Version
- Existing Artifact
- Upstream / Downstream Dependency
- Asset Reference
- Traceability Requirement
- Applicable HOLD

Production Artifactについて正式なRepository Placementが定義されている場合、そのPlacementに従う。

一方、正式な物理Placementが未確定であるArtifactについて、既存の論理Layer、類似Artifactまたは一般的なRepository構造から物理Directoryを推測してはならない。

Audit Artifactの正式な物理Repository Placementは、

cases/FILE-XXX/audit/

とする。

Repository Integrationはこの正式Placementを使用し、対象Case、対象Artifact、Applicable VersionおよびAudit ResultとのTraceabilityを維持しなければならない。

Audit ArtifactのPlacementが正式決定されていることだけを理由として、本章から以下を新たに確定してはならない。

- Audit Artifact Filename Convention
- Audit Artifact Versioning
- \`audit/\`配下のSubdirectory
- Audit Artifact Retention / Archive Placement
- 追加Database / Metadata Field
- Automationが使用する具体的なAudit Artifact Path Conventionまたは実装

\`HOLD-AUDIT-PLACEMENT-01\`のHuman DecisionおよびApplicable Source of Truthへの反映は完了している。

その正式ResolutionおよびHistorical RecordはHOLD Ledgerに従う。

Audit PlacementのResolutionを、Audit Filename Convention、Audit Artifact Versioning、Retention / Archive PlacementまたはAutomation実装の承認として拡張してはならない。

---

## 7.7 Workflow Status Integration

Repository Integrationでは、Repository上で管理されるCase Workflow Statusが、実際の正式なProduction状態と矛盾しないように維持する。

Workflow Statusの正式な名称および責務はChapter 6に従う。

Repository Integrationそのものを、独立したWorkflow Statusとして本章から新設しない。

Applicable Production FlowにおいてRepository Integration前後でWorkflow Statusの変更が必要となる場合、その変更はChapter 6、AGENTS.mdその他のApplicable Source of Truthと整合しなければならない。

以下を行ってはならない。

- FileをRepositoryへ配置しただけでWorkflow Statusを\`APPROVED\`へ変更する
- Workflow Statusが\`APPROVED\`であることだけを根拠としてRepository Integration完了とみなす
- Repository IntegrationによってRequired Production / Publication AuditをPASSしたものとみなす
- Repository IntegrationによってApplicable Final Flow AuditをPASSしたものとみなす
- Repository IntegrationによってHuman Approval Decisionを\`APPROVED\`として成立させる
- Repository Integrationによって\`REVISION_REQUIRED\`または\`BLOCKED\`の原因が解消されたものとみなす
- Status変更だけで必要なRepository Integrationが完了したものとみなす

\`REVISION_REQUIRED\`または\`BLOCKED\`が成立している場合、そのException Stateの原因およびRecovery条件を確認せずに通常のIntegrationを継続してはならない。

Exception StateからのRecoveryはChapter 6およびApplicable Source of Truthに従う。

Repository Integration後も、Workflow StatusはCaseの実際の正式なProduction状態を表さなければならない。

---

## 7.8 Publication Status Integration

Publication StatusはWorkflow StatusおよびRepository Integrationから独立した状態概念として管理する。

Repository Integrationが完了したことだけを理由として、Publication Statusを\`PUBLISHED\`へ変更してはならない。

同様に、Publication Statusが\`PUBLISHED\`であることだけを理由として、必要なRepository Integrationが完了していると推測してはならない。

本VersionのRepository RuleにおけるPublication Statusの基本モデルはChapter 6に従う。

- \`NOT_PUBLISHED\`
- \`PUBLISHED\`

Publication Statusの責務およびControlled Valuesは、Chapter 6およびApplicable Source of Truthの正式なCompatibility整理に従う。

Repository Integrationでは、Compatibilityを理由として以下を行ってはならない。

- Repository Rule側のPublication Status定義によって他の責務領域の状態を自動置換する
- Historical Statusを現在のPublication Statusへ自動Mappingする
- 異なる責務を持つControlled Valueを一つの管理項目へ無整理で混在させる
- 同名または類似Statusの意味をContextだけから推測する
- Repository Integrationだけを理由としてPublication Statusを決定する

Publication Statusの変更が必要な場合は、Applicable Source of Truthによって正式なPublication状態が成立していることを確認する。

Human Approval、Repository IntegrationおよびPublicationは、それぞれ異なる責務として維持する。

Human Approval
≠
Repository Integration
≠
Publication

一つの工程の完了を、他の工程の完了証拠として自動的に扱ってはならない。

Applicable Human Approval Decisionが\`APPROVED\`であることはRepository Integrationへの必要な上流条件となり得るが、それ自体をPublication完了の証拠として扱ってはならない。

同様に、Repository Integrationの完了をPublication完了の証拠として扱ってはならない。

Publication Status Compatibilityに関する過去のHOLDの正式ResolutionおよびHistorical RecordはHOLD Ledgerに従う。

解消済みCompatibility HOLDを、本章からActive HOLDとして再登録または再Openしてはならない。

---

## 7.9 Version Integration

Repository Integrationでは、対象Production ArtifactのApplicable Versionを識別可能な状態で維持する。

Artifact VersionはWorkflow Status、Publication Status、Human Approval DecisionまたはRepository Integration Statusの代替として使用してはならない。

同様に、Repository Integrationを実施したことだけを理由としてArtifact Versionを増加させてはならない。

Production ArtifactのVersion Increment CriteriaはChapter 5の正式Criteriaに従う。

Chapter 5ではProduction Artifactの基本Version表記を、

vX.Y

とし、\`X\`をMajor Version、\`Y\`をMinor Versionとして管理する。

Production ArtifactにPatch Componentを自動追加してはならない。

Version IncrementはApproval Boundary Modelに従い、実際の変更内容および既存の承認境界への影響によって、

- Major Version Increment
- Minor Version Increment
- No Version Increment

のいずれに該当するかを判定する。

Repository IntegrationまたはRe-Integrationが発生したことだけを理由として、MajorまたはMinor Version Incrementを決定してはならない。

したがって、

Repository Integration
≠
Automatic Version Increment

Re-Integration
≠
Automatic Version Increment

とする。

Audit Correction、Content Revision、Publication Revision、Human Approval後のRevisionまたはRepository Integration後のRevisionであるという原因だけを根拠としてMajorまたはMinorを固定的に決定してはならない。

Repository Integration時に複数Versionが存在する場合、単に数値が最大であること、更新日時が新しいことまたはFilenameが最新版に見えることだけを理由として正式なIntegration対象を決定してはならない。

Applicable Production Flow、Required Production / Publication Audit、Applicable Final Flow Audit、Human Approval Decision、Artifact Identity、Chapter 5およびTraceabilityから正式なApplicable Versionを確認する。

Applicable Final Flow AuditまたはHuman Approval Decisionが特定Versionを対象として成立している場合、その結果を別Versionへ自動的に適用したものとして扱ってはならない。

Repository Integration後に修正が必要となった場合も、Existing Versionを無条件に上書きしてはならない。

変更がMajor、MinorまたはNo Version Incrementのいずれに該当するかはChapter 5に従って判定する。

Chapter 5および確認可能なTraceabilityから一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

Current Versionについても、Version番号が最大であること、Timestampが新しいこと、Filenameが最新版に見えることまたはRepository Integrationが最後に実行されたことだけを根拠として決定してはならない。

Historical Versionを保持することは、そのVersionがCurrentまたは現在Applicableであることを意味しない。

したがって、

Historical Preservation
≠
Current Applicability

とする。

---

## 7.10 Metadata and Asset Reference Boundary

Repository Integrationでは、対象CaseおよびProduction Artifactについて必要なMetadataおよびAsset Referenceが、Repository上の正式状態と整合していることを確認する。

MetadataおよびAsset Referenceは、Production Artifactそのものとは異なる管理責務を持つ。

したがって、

Artifact Content
≠
Metadata
≠
Asset Reference

として扱う。

Repository IntegrationによってMetadataまたはAsset Referenceを更新する必要がある場合、その値、形式、Controlled Value、Data Type、ValidationおよびPersistence方法はApplicable Source of Truthに従う。

Repository Ruleは、Database RuleまたはDatabase Schemaに属するField Definitionを本章から再定義しない。

FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Trackingについては、

cases/FILE-XXX/publication-tracking.json

をCase-level Repository-managed Operational Metadata Artifactとして使用する。

\`publication-tracking.json\`はProduction Artifact、Audit ArtifactまたはDatabase Recordではなく、新しいProduction Layerを構成しない。

\`publication-tracking.json\`では、FREEおよびCLASSIFIEDそれぞれについて、Applicable Repository Rule Sectionで正式に定義された範囲で、

- Applicability
- Production State
- Applicable Audit Reference

を管理する。

Repository Integrationでは、ApplicableなPublication Artifactについて、\`publication-tracking.json\`に保持されるArtifact Identityとの対応、Applicability、Production StateおよびApplicable Audit Referenceの整合を確認する。

ただし、Repository Integrationの実施だけを理由として、Applicability、Production StateまたはApplicable Audit Referenceを新たに推測して設定してはならない。

Fileの存在、Directoryの存在、Workflow Status、Publication Status、Audit Result、Human Approval DecisionまたはRepository Integration結果だけを根拠として、\`publication-tracking.json\`の値を自動導出してはならない。

Applicable Audit Referenceは、対象Publication ArtifactにApplicableなAudit ArtifactへのRepository-relative Referenceとして扱う。

Applicable Audit ReferenceをAudit Resultそのものとして扱ってはならず、Audit Resultを\`publication-tracking.json\`へ複製してはならない。

Applicable Audit ReferenceのReference Validationでは、対象Case、対象Artifact、Applicable Versionおよび実際にApplicableなAuditとの対応を確認する。

Referenceが存在しない、別Caseを参照している、対象Artifactが一致しない、Applicable Versionが一致しない、またはApplicable Auditを一意に確認できない場合はReference Validationを成功として扱ってはならない。

Reference Validation FAILそれ自体をAudit Result \`BLOCKER\`として扱ってはならない。

曖昧なApplicable Audit ReferenceをAutomationまたはRepository Integration処理によって推測、補完または自動修復してはならない。

\`publication-tracking.json\`の存在を理由として、新しいDatabase Field、Metadata DirectoryまたはProduction Layerを追加してはならない。

Metadataとして管理され得るその他の情報についても、具体的なDatabase FieldおよびRequired / Optional条件はApplicable Database Source of Truthに従う。

Asset Referenceについて、Repository Integrationを理由として新しいAsset Identity、Path Convention、URL ConventionまたはStorage Ruleを推測によって作成してはならない。

既存Assetを参照する場合は、対象Caseおよび対象ArtifactとのTraceabilityを維持する。

Assetを差し替える場合は、既存の正式なReferenceを無関係なAssetへ付け替えてはならない。

Assetの物理Fileが存在することだけを理由として、正式なAsset Referenceが成立しているとみなしてはならない。

同様に、MetadataにAsset Referenceが存在することだけを理由として、対象Assetの存在、正当性またはApprovalを推測してはならない。

---

## 7.11 Database Integration Boundary

Repository Integrationでは、対象Caseおよび対象Artifactに関してDatabase上の管理情報を更新する必要が生じ得る。

ただし、Repository IntegrationとDatabase Integrationは同一の責務として扱ってはならない。

Repository Integration
≠
Database Schema Definition
≠
Database Validation
≠
Database Migration

Repository Ruleは、Repository Integrationに必要な整合性および責務境界を定義する。

Database Field、Data Type、Nullability、Controlled Values、Validation、Constraint、Migrationその他のDatabase実装仕様は、Database Rule、Database Schemaその他のApplicable Database Source of Truthに従う。

Repository Integrationを理由として、Repository Ruleから新しいDatabase Field、Enum、ConstraintまたはValidation Ruleを独自に追加してはならない。

Database上の管理情報を更新する場合は、Applicableな範囲で以下との整合を確認する。

- Case Identity
- File Number
- Workflow Status
- Publication Status
- Artifact Identity
- Artifact Version
- Metadata
- Asset Reference
- Existing Record
- Applicable Constraint
- Traceability

ただし、本Listを新しいDatabase SchemaまたはRequired Field一覧として扱ってはならない。

Repository上の状態とDatabase上の状態に差異を検出した場合、一方を自動的に正しいものとして他方へ上書きしてはならない。

まずApplicable Source of Truth、Production Flow、Required Production / Publication Audit、Applicable Final Flow Audit、Human Approval Decisionおよび既存Recordを確認し、どの状態が正式であるかを判断する。

正式な状態を判断できない場合は、Source of Truth ConflictまたはBlocking Issueとして扱い、推測による同期を行ってはならない。

Repository Integrationが成功したことだけを理由としてDatabase Updateが成功したものとみなしてはならない。

同様に、Database Updateが成功したことだけを理由としてRepository Integrationが完了したものとみなしてはならない。

RepositoryとDatabaseの両方への反映がApplicable Production Flowによって要求される場合、それぞれの正式な反映状態を確認する。

Publication Statusについては、Repository RuleとApplicable Source of Truth間の責務およびControlled Valueを確認し、異なる状態体系をDatabase上へ無整理で統合してはならない。

FREE / CLASSIFIEDのArtifact-level Trackingは、

cases/FILE-XXX/publication-tracking.json

によるRepository-managed Operational Metadataとして管理する。

この正式化はDatabase Schemaへの新しいField追加を意味しない。

Repository IntegrationまたはArtifact-level Trackingの必要性だけを理由として、FREE / CLASSIFIEDのApplicability、Production StateまたはApplicable Audit Referenceを保持する新しいDatabase Field、Enum、ConstraintまたはValidation Ruleを追加してはならない。

Database Fieldが将来必要となる場合は、Database Rule、Database Schemaその他のApplicable Database Source of Truthにおける正式な変更工程を必要とする。

---

## 7.12 Traceability Requirements

Repository Integrationでは、対象Case、対象Artifact、上流成果物、Required Production / Publication Audit、Applicable Final Flow Audit、Human Approval Decision、Versionおよび必要な関連情報のTraceabilityを維持する。

Traceabilityは、単にFileが存在することまたは同一Directoryに関連Fileが存在することだけでは成立しない。

Applicableな範囲で、少なくとも以下の関係を後から確認可能な状態に維持する。

- Case IdentityとProduction Artifactの関係
- Production ArtifactとArtifact Typeの関係
- Production ArtifactとApplicable Versionの関係
- Downstream ArtifactとUpstream Artifactの関係
- ArtifactとRequired Production / Publication Auditの関係
- ArtifactとApplicable Final Flow Auditの関係
- ArtifactとApplicable Human Approval Decisionの関係
- ArtifactとRepository Placementの関係
- Artifactと必要なMetadataの関係
- Artifactと必要なAsset Referenceの関係
- Revision前後のArtifactの関係
- Repository上の状態とApplicable Source of Truthの関係
- Publication ArtifactとArtifact-level Applicabilityの関係
- Publication ArtifactとArtifact-level Production Stateの関係
- Publication ArtifactとApplicable Audit Referenceの関係
- Applicable Audit Referenceと対象Caseの関係
- Applicable Audit Referenceと対象Artifactの関係
- Applicable Audit ReferenceとApplicable Versionの関係
FREEおよびCLASSIFIEDのArtifact-level Trackingに関するTraceabilityは、

cases/FILE-XXX/publication-tracking.json

をPrimary Source of Truthとして維持する。

Applicable Audit ReferenceはRepository-relative Referenceとして保持し、Audit Resultを複製してTraceabilityを成立させてはならない。

Applicable Audit Referenceの一意性またはApplicabilityを確認できない場合、推測によって対象Auditを選択してはならない。

Traceabilityを維持するために必要な具体的Field、Identifier、Manifest、Metadata FormatまたはDatabase Structureは、それぞれのApplicable Source of Truthに従う。

本章はTraceabilityを理由として未定義のDatabase FieldまたはFile Formatを新設しない。

Repository Integrationによって、既存のStable Identifierを失ってはならない。

Repository Integrationによって、上流ArtifactとのDependencyを不明にしてはならない。

Repository Integrationによって、どのVersionがどのRequired Production / Publication Audit、Applicable Final Flow AuditまたはHuman Approval Decisionの対象であったか判別不能な状態を作ってはならない。

複数Versionが存在する場合、Audit、Final Flow AuditまたはHuman Approval Decisionが別Versionへ誤って継承されたように見える状態を避ける。

新しいVersionまたはRevisionが作成された場合、旧VersionのAudit Result、Final Flow Audit ResultまたはHuman Approval Decisionを、新しいVersionへ自動的に適用したものとして扱ってはならない。

適用可能性はApplicable Production Flow、Audit Rule、Human Decisionその他の正式根拠から確認する。

Audit Artifactの正式な物理Placementは、

cases/FILE-XXX/audit/

とする。

Placement決定後もTraceability要件は独立して維持し、Audit ArtifactのFilename Convention、Versioning、Retention / Archive Placementまたは具体的Automation実装をPlacementから自動推測してはならない。

Audit Artifactは、少なくとも所属Case、対象Artifact、Applicable VersionおよびAudit ResultとのTraceabilityを維持しなければならない。

---

## 7.13 Existing Artifact Protection

Repository Integrationでは、既存の正式Artifact、Metadata、Asset Reference、Stable Identifierおよび履歴を不必要に破壊してはならない。

新しいArtifactまたはRevisionをIntegrationする際は、Applicableな範囲で既存Artifactとの関係を確認する。

少なくとも以下のような操作を、正式な根拠なしに行ってはならない。

- 既存Approved Artifactの無条件上書き
- 既存Published Artifactの無条件上書き
- Stable Identifierの再発行
- Case IDまたはFile Numberの変更
- Artifact Typeの暗黙変更
- Existing Versionの削除
- Existing Versionの内容差し替え
- Audit Resultの別Versionへの無条件継承
- Final Flow Audit Resultの別Versionへの無条件継承
- Human Approval Decisionの別Versionへの無条件継承
- Metadata Historyの破壊
- Asset Referenceの無関係なAssetへの付け替え
- Existing Dependencyの削除
- Repository Placement変更によるTraceability喪失

既存Artifactを更新、置換またはSupersedeする必要がある場合、その操作がChapter 5、Applicable Versioning Rule、Production Flow、Required Audit、Applicable Final Flow Audit、Human DecisionおよびRepository Structureと整合していることを確認する。

既存Artifactを置換すべきか、新Versionとして保持すべきか、No Version IncrementのCorrectionとして扱うべきかはChapter 5のCriteriaに従って判定する。

Chapter 5および確認可能なTraceabilityから一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

Existing Versionを、新Versionが存在するという理由だけで上書きまたは削除してはならない。

Historical Versionは必要なTraceabilityを維持できる状態で保持する。

ただし、Historical Versionを保持することは、そのVersionがCurrentまたは現在Applicableであることを意味しない。

既存Artifactと新しいArtifactのIdentity Conflictを検出した場合、更新日時、FilenameまたはVersion番号だけを根拠として一方を削除または上書きしてはならない。

正式な関係を確認できない場合は、Conflictを保持し、必要なReviewまたはHuman Decisionへ送る。

Repository Integrationの目的はRepositoryを見た目上単純化することではない。

必要なHistory、TraceabilityおよびCompatibilityを維持することを優先する。

Historical Version Retentionを理由として、本章から専用\`archive/\` Directory、Retention Period、Automatic Deletion Schedule、Archive Filename Convention、追加Metadata FieldまたはDatabase Fieldを新設してはならない。

---

## 7.14 Failure and Conflict Handling

Repository Integration中にFailure、Conflict、Missing RequirementまたはSource of Truth Conflictを検出した場合、問題を隠したままIntegration成功として扱ってはならない。

以下は、Integrationを停止または正式確認対象とすべき代表的な状態である。

- Case Identity Conflict
- Artifact Identity Conflict
- Version Conflict
- Repository Placement Conflict
- Missing Required Artifact
- Missing Required Production / Publication Audit
- Non-PASS Required Production / Publication Audit Result
- Missing Applicable Final Flow Audit
- Non-PASS Applicable Final Flow Audit Result
- Missing Applicable Human Approval Decision
- Applicable Human Approval Decisionが\`APPROVED\`ではない状態
- Blocking Issue
- Workflow Status Conflict
- Publication Status Conflict
- Metadata Conflict
- Asset Reference Conflict
- Database / Repository State Conflict
- Dependency Conflict
- Traceability Loss Risk
- Existing Artifact Overwrite Risk
- Applicable Source of Truth Conflict
- Active HOLDによって未確定の仕様を必要とする状態

ただし、本Listだけを根拠としてすべての問題を同一のWorkflow Stateへ変更してはならない。

問題の性質に応じて、Applicable Source of Truthが定義する、

- Revision
- Re-Audit
- Final Flow Audit
- Human Review
- Human Decision
- HOLD
- BLOCKED
- Escalation
- Source of Truth Correction

その他の正式処理を確認する。

Repository Ruleは、それらのProduction Workflow上の処理を本章から独自に再定義しない。

Conflictが存在する場合、AIまたはAutomationは以下を行ってはならない。

- より新しいTimestampを自動的に正とする
- より大きいVersion番号を自動的に正とする
- Repository側を常に正とする
- Database側を常に正とする
- Published側を常に正とする
- Approved側を常に正とする
- Fileが存在する側を常に正とする
- Missing Dataを推測で補完する
- Active HOLDの未確定事項を便宜的に決定する
- Conflictを削除または上書きによって不可視化する

正式なSource of Truthおよび必要なHuman Decisionから解消できないConflictは、未解決状態として保持する。

Conflict解消後にRepository Integrationを再開する場合、解消内容だけでなく、対象Artifact、Version、Status、Metadata、Dependency、Required Audit、Applicable Final Flow Audit、Human Approval DecisionおよびTraceabilityへの影響を再確認する。

Repository IntegrationのFailureを、Publicationまたは後続工程へ進むことで回避してはならない。

必要なRepository Integrationが正式に完了していない場合、その未完了状態を後続工程から隠してはならない。

---

## 7.15 Re-Integration After Revision

Repository Integration後にRevision、Correction、Re-Audit、Human Reviewその他の正式な再処理が必要となった場合、既存Integrationが存在することだけを理由として修正版を自動的にRe-Integrationしてはならない。

Re-Integrationでは、対象ArtifactおよびCaseについて、Applicableな範囲で少なくとも以下を再確認する。

- Case Identity
- Artifact Identity
- Revision対象
- Applicable Version
- Upstream Artifact
- Dependency
- Required Production / Publication Audit
- Re-Auditの必要性
- Applicable Final Flow Audit
- Final Flow Auditの再実施必要性
- Applicable Human Approval Decision
- Human Approvalの再実施必要性
- Workflow Status
- Publication Status
- Existing Integrated Artifact
- Existing Published Artifact
- Metadata
- Asset Reference
- Traceability
- Compatibility
- Active HOLDの影響
- Artifact Applicability
- Artifact-level Production State
- Applicable Audit Reference
- publication-tracking.jsonとの整合
Publication Audit後のRevisionによってApplicableなFREEまたはCLASSIFIED Publication ArtifactがProductionへ戻る場合は、Chapter 6に従い、対象ArtifactのProduction Stateを\`IN_PROGRESS\`として管理し、Case-level Workflow Statusを\`PUBLICATION_PRODUCTION\`へ戻す。

この状態変更をRepository IntegrationまたはRe-Integrationの成功だけを理由として\`COMPLETE\`へ戻してはならない。

修正後の対象Artifactが再び正式に\`COMPLETE\`となり、ApplicableなWorkflow Gateを満たしたことを確認した場合にのみ、後続のPublication AuditまたはRe-Integrationへ進める。

Revision前のApplicable Audit ReferenceをRevision後のArtifact Versionへ自動継承してはならない。

Revision後のArtifactにApplicableなAuditを確認し、そのReference Validationが成立した場合にのみApplicable Audit Referenceとして使用する。

Revision前のArtifactとRevision後のArtifactを、同一内容または同一正式状態であると自動的にみなしてはならない。

RevisionによってContent、Evidence、Metadata、Asset、Dependencyその他の正式情報が変更された場合、既存のRequired Production / Publication Audit Result、Final Flow Audit ResultまたはHuman Approval Decisionを修正版へ自動継承してはならない。

Re-Audit、Final Flow Auditの再実施、再Human Reviewまたは再Human Approvalが必要かどうかは、Applicable Production Flow、Audit Rule、Human Decisionその他の正式なSource of Truthに従う。

Re-Integrationへ進むためにApplicable Human Approval Decisionとして\`APPROVED\`が必要な場合、Revision前のArtifactに対して成立した\`APPROVED\`をRevision後のArtifactへ自動的に適用したものとして扱ってはならない。

既にPublication Statusが\`PUBLISHED\`であるArtifactにRevisionが必要となった場合、既存Published Artifactを無条件に上書きしてはならない。

既存Publicationの扱い、Revision後の再Publication、Publication Status Transition、公開履歴その他の具体的なPublication処理はApplicable Source of Truthに従う。

Repository Ruleは、Published ArtifactのRevisionだけを理由として新しいPublication WorkflowまたはPublication Statusを独自に定義しない。

Re-Integrationに伴うProduction Artifact Version DecisionはChapter 5の正式Criteriaに従う。

Re-Integrationが必要であることだけを理由として、

- Major Versionを増加させる
- Minor Versionを増加させる
- Patch Componentを追加する
- Existing Versionを上書きする
- 新しいVersionを必ず作成する

といったVersioning Decisionを自動的に行ってはならない。

Production ArtifactではPatch Componentを本章から追加してはならない。

Revisionの実際の変更内容および既存のApproval Boundaryへの影響を確認し、Chapter 5に従ってMajor、MinorまたはNo Version Incrementを判定する。

Chapter 5および確認可能なTraceabilityからVersion Decisionを一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

Re-Integration後も、Revision前後のArtifact、Required Production / Publication Audit、Final Flow Audit、Human Approval Decision、Version、Publication状態およびRepository上の履歴を必要に応じて追跡可能な状態に維持する。

Re-Integrationは、過去の正式状態を不可視化する工程ではない。

---

## 7.16 Automation Boundary

Repository Integrationの一部は、Applicable Source of Truthによって許可された範囲でAutomationによって支援され得る。

ただし、AutomationはRepository Integrationに必要なHuman Judgment、Human Approval、Source of Truth Conflict Resolutionまたは未確定仕様のDecisionを代替してはならない。

Automationが実行可能な処理と、Human Decisionを必要とする処理を区別する。

Automationは、正式仕様によって処理条件が確定している範囲で、例えば以下のような補助処理を行い得る。

- Required Fileの存在確認
- Filename Patternの確認
- Stable Identifierの照合
- Defined Repository Placementの確認
- Defined Metadataの存在確認
- Defined Referenceの整合確認
- Existing Artifactとの機械的比較
- Required Dependencyの存在確認
- Applicable Statusの読み取り
- Required Production / Publication Audit Resultの確認
- Applicable Final Flow Audit Resultの確認
- Applicable Human Approval Decisionの確認
- Integration後の整合性確認

ただし、本ListはAutomation Capabilityまたは実装要件を新たに定義するものではない。

具体的なAutomationの実装、Trigger、Permission、Failure HandlingおよびAgent BehaviorはAGENTS.mdその他のApplicable Source of Truthに従う。

Automationは以下を行ってはならない。

- Human Approvalを自動生成する
- Human Approval Decisionとして\`APPROVED\`を自動生成する
- Required Production / Publication Audit PASSを根拠なく生成する
- Final Flow Audit PASSを根拠なく生成する
- Source of Truth Conflictを推測によって解消する
- Missing Dataを推測によって補完する
- Stable Identifierを根拠なく変更する
- Existing Approved Artifactを無条件に上書きする
- Existing Published Artifactを無条件に上書きする
- Chapter 5に反するVersion Increment Decisionを生成する
- Major、Minor、No Version IncrementまたはCurrent Versionを一意に判定できない状態で推測によって決定する
- Patch ComponentをProduction Artifactへ追加する
- FREE / CLASSIFIED個別Tracking体系を新設する
- Audit Artifact Placement Decisionから未定義のNaming、Versioning、ArchiveまたはAutomation実装を生成する
- Active HOLDを自動的にRESOLVEDへ変更する

AutomationがActive HOLDの対象となる仕様を必要とする場合、その未確定事項を便宜的なDefault Value、Directory、Status、FieldまたはRuleによって埋めてはならない。

Version Decisionについて、Chapter 5および確認可能なEvidenceから一意に判定できない場合、Automationは推測によって処理を続行せず、Human Decisionを要求する。

AutomationによってRepository Integrationを実施した場合でも、その結果がApplicable Source of Truth、対象Artifact、Required Production / Publication Audit、Applicable Final Flow Audit、Human Approval Decision、Status、Version、Metadata、DependencyおよびTraceabilityと整合していることを確認可能でなければならない。

Automationの成功応答だけを、Repository Integrationの正式完了証拠として扱ってはならない。

---

## 7.17 HOLD Dependencies and Resolution Reflection

本章のRepository Integrationは、正式HOLD Ledgerに登録されたActive HOLDおよびRESOLVED Archiveとの境界を維持する。

HOLDの正式な状態はHOLD LedgerをSource of Truthとして確認する。

本章だけを根拠として、HOLDのStatus、解消条件、Human Decision Requirementまたは正式なDispositionを変更してはならない。

### HOLD-ARTIFACT-VERSION-01

\`HOLD-ARTIFACT-VERSION-01\`について、Production Artifact Version Increment Criteriaに必要なHuman Decisionは完了し、Major、Minor、No Version Increment、Patch Component不採用、Current Version Selection、Historical Version Retentionその他の正式CriteriaがChapter 5へ反映されている。

Repository IntegrationおよびRe-Integrationは、Chapter 5のVersion Criteriaに従う。

Repository IntegrationまたはRe-Integrationが発生したことだけを理由として、Version Incrementを自動決定してはならない。

Resolution前は、本章への反映だけでは\`HOLD-ARTIFACT-VERSION-01\`をRESOLVEDとせず、Applicable Source of Truthへの必要な反映、Compatibility確認および最終横断再監査のPASSが要求されていた。

これらのResolution条件は完了し、\`HOLD-ARTIFACT-VERSION-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

### HOLD-PUBLICATION-TRACKING-01

\`HOLD-PUBLICATION-TRACKING-01\`は、FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Production / Audit State Trackingに関する未確定事項を管理するため、Resolution前はActive HOLDとして管理されていた。

Resolution前は、本章からFREE / CLASSIFIED個別State用の新しいWorkflow Status、Metadata Field、Database FieldまたはTracking Systemを独自に確定せず、Repository Integration上で個別状態の識別が必要な場合も、正式な解消工程を経ずに新しい管理体系を作成しないことが要求されていた。

Human Decision、Applicable Source of Truthへの必要な反映、Compatibility確認および最終横断再監査は完了し、\`HOLD-PUBLICATION-TRACKING-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

解消済みの本HOLDを本章からActive HOLDとして再Openしてはならない。

### HOLD-AUDIT-PLACEMENT-01

\`HOLD-AUDIT-PLACEMENT-01\`について、Case単位のAudit Artifact正式物理Repository Placementとして、

cases/FILE-XXX/audit/

を採用するHuman DecisionおよびRepository Ruleへの反映は完了している。

本章はこの正式Placementを使用する。

ただし、Audit Placement Decisionから、Audit Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、追加Database / Metadata Fieldまたは具体的Automation実装を派生させてはならない。

本HOLDの正式ResolutionおよびHistorical RecordはHOLD Ledgerに従う。

解消済みHOLDを本章からActive HOLDとして再Openしてはならない。

### Publication Status Compatibility Resolution

Publication Statusの責務、\`NOT_PUBLISHED\` / \`PUBLISHED\`の2値モデルおよびHistorical StatusとのCompatibility整理は、Applicable Source of Truthに反映された正式な解消済み事項として扱う。

過去のPublication Status Compatibility HOLDのResolutionおよびHistorical RecordはHOLD Ledgerに従う。

本章は、解消済みPublication Status Compatibility事項をActive HOLDとして再登録または再Openしない。

---

本章終了時点で継続するActive HOLDは、正式HOLD Ledgerの最新状態に従う。

Resolution前は、Chapter 5へのVersion Criteria反映だけを理由として\`HOLD-ARTIFACT-VERSION-01\`を自動的にRESOLVEDとせず、最終Compatibility確認および最終横断再監査のPASSが要求されていた。

これらのResolution条件は完了し、\`HOLD-ARTIFACT-VERSION-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

Repository Rule v1.0のResolution前の最終横断監査では、少なくとも以下が確認された。

- \`HOLD-ARTIFACT-VERSION-01\`のChapter 5 Criteriaが本章へ正しく反映されていること
- \`HOLD-PUBLICATION-TRACKING-01\`の承認済みDecisionを超える事項を本章が暗黙に確定していないこと
- 解消済みHOLDをActive HOLDとして再Openしていないこと
- Repository IntegrationまたはRe-IntegrationがVersion Incrementの自動Triggerとして扱われていないこと
- AutomationがVersion Decisionを推測していないこと
- Audit Placementの正式Decisionが維持されていること
- 必要なHistorical Traceabilityが維持されていること
- 専用\`archive/\` Directory、Retention Period、Automatic Deletion Scheduleまたは追加Database / Metadata FieldをVersion管理上の都合から新設していないこと

---

## 7.18 Core Integration Principle

ProjectORIGINにおけるRepository Integrationの基本原則は、

\*\*正式な上流工程を経た対象を、Identity、Version、Status、Metadata、Dependency、TraceabilityおよびExisting Artifact Integrityを維持した状態でRepositoryへ統合すること\*\*

とする。

標準Production FlowにおけるRepository Integrationへの基本的な上流関係は、

Required Production / Publication Audits PASS
↓
Applicable Final Flow Audit PASS
↓
Applicable Human Approval Decision = APPROVED
↓
Repository Integration

とする。

ただし、対象ArtifactまたはProduction FlowについてApplicable Source of Truthが追加の正式Gateを要求する場合、それを省略してはならない。

Repository Integrationは、

- Required Production / Publication Audit
- Final Flow Audit
- Human Approval
- Publication
- Database Schema Definition
- Artifact Version Decision
- Source of Truth Conflict Resolution

の代替ではない。

以下の責務境界を維持する。

Human Approval Decision = APPROVED
↓
Repository Integration
↓
Applicable Publication Process

ただし、

Human Approval
≠
Repository Integration
≠
Publication

とする。

また、

Repository Integration
≠
Database Schema Definition

とする。

Production ArtifactのVersion DecisionはChapter 5に従う。

Repository IntegrationまたはRe-Integrationそれ自体をVersion Incrementの根拠としてはならない。

したがって、

Repository Integration
≠
Automatic Version Increment

Re-Integration
≠
Automatic Version Increment

とする。

Repository上にFileが存在することだけを理由として、正式なRepository Integrationが成立したものとみなしてはならない。

Required Production / Publication AuditがPASSしていることだけを理由として、Final Flow AuditがPASSしているとみなしてはならない。

Final Flow AuditがPASSしていることだけを理由として、Human Approval Decisionが\`APPROVED\`であるとみなしてはならない。

Human Approval Decisionが\`APPROVED\`であることだけを理由として、Repository Integrationが完了したものとみなしてはならない。

Workflow Statusが\`APPROVED\`であることだけを理由として、Repository Integrationが完了したものとみなしてはならない。

Repository Integrationが完了したことだけを理由として、Publication Statusを\`PUBLISHED\`へ変更してはならない。

Database Updateが完了したことだけを理由として、Repository Integrationが完了したものとみなしてはならない。

Repository Integrationが完了したことだけを理由として、Database Updateが完了したものとみなしてはならない。

Artifact Versionが大きいこと、Timestampが新しいことまたはFilenameが最新版に見えることだけを理由として、正式なIntegration対象またはCurrent Versionを決定してはならない。

既存Approved ArtifactまたはPublished Artifactを、正式な根拠なしに上書きしてはならない。

新Versionが存在するという理由だけでHistorical Versionを上書きまたは削除してはならない。

Historical Versionの保持はCurrent Applicabilityを意味しない。

Repository IntegrationによってStable Identifier、Dependency、Required Audit Traceability、Final Flow Audit Traceability、Human Decision Traceabilityまたは必要なHistoryを失ってはならない。

Failure、Conflict、Missing RequirementまたはSource of Truth Conflictを検出した場合、それを隠したままIntegration成功として扱ってはならない。

Active HOLDの対象となる未確定仕様を、Repository Integration、AutomationまたはDatabase Integrationの都合によって暗黙に決定してはならない。

本章終了時点のActive HOLDは、正式HOLD Ledgerの最新状態に従う。

\`HOLD-ARTIFACT-VERSION-01\`についてResolution前に必要とされたCompatibility確認および最終横断再監査はPASSしており、正式HOLD Ledger上でRESOLVEDとして管理されている。

\`HOLD-PUBLICATION-TRACKING-01\`については、本章から新しいArtifact-level Tracking体系を推測してはならない。

解消済みHOLDを、本章によってActive HOLDへ戻してはならない。

Repository Integration後も、対象CaseおよびProduction Artifactが、Applicable Source of Truth、Production Flow、Required Production / Publication Audit、Final Flow Audit、Human Approval Decision、Repository Structure、DatabaseおよびPublication状態との間で追跡可能かつ整合した状態を維持することを最優先とする。

不明な状態を推測によって正常化することよりも、未解決事項、ConflictまたはHOLDを可視化した状態で保持することを優先する。
# Chapter 8

# Repository Integrity and Traceability

## 8.1 Purpose

本章は、ProjectORIGIN RepositoryにおけるRepository IntegrityおよびTraceabilityの正式な管理原則を定義する。

ProjectORIGINでは、Case、Production Artifact、Version、Audit、Human Decision、Repository Integration、Publication、Database、Assetその他の関連情報が長期的に増加する。

そのため、Repository上にFileが存在することだけではなく、

- 何のCaseに属するか
- 何のArtifactであるか
- どのVersionであるか
- どの上流Artifactから生成されたか
- どのAuditが適用されたか
- どのHuman Decisionが適用されたか
- Repository上でどの正式状態にあるか
- Publicationとの関係がどうなっているか
- 過去VersionおよびRevisionとどのような関係にあるか

を必要な範囲で追跡できる状態を維持しなければならない。

本章はRepository IntegrityおよびTraceabilityの原則を定義するものであり、Production Workflow、Audit Criteria、Human Approval Criteria、Database Schema、Artifact Version Increment Criteriaその他の専門仕様を独自に再定義しない。

それらはApplicable Source of Truthに従う。

---

## 8.2 Repository Integrity Principle

Repository Integrityとは、Repository上の正式なCase、Artifact、Version、Placement、Status、Dependencyおよび関連情報が、Applicable Source of Truthおよび正式なProduction状態と矛盾せず、識別可能かつ追跡可能な状態を維持していることをいう。

Repository Integrityは、単にDirectory Structureが正しいことだけを意味しない。

以下のような状態は、Repository Integrity上の問題として扱う。

- Case Identityを確認できないArtifact
- Artifact Identityを確認できないArtifact
- Applicable Versionを確認できないArtifact
- 同一Artifact / Versionについて正式対象を一意に確認できない状態
- Repository PlacementとArtifact Identityが矛盾する状態
- Production Layer間で責務が混在している状態
- Required Auditとの関係を追跡できない状態
- Applicable Final Flow Auditとの関係を追跡できない状態
- Applicable Human Decisionとの関係を追跡できない状態
- Repository Integrationの正式状態を確認できない状態
- Publication状態との関係を確認できない状態
- Revision前後の関係を追跡できない状態
- Historical VersionとCurrent Versionを区別できない状態
- DatabaseとRepositoryの正式状態が矛盾し、どちらがApplicableか確認できない状態
- AssetまたはReferenceが誤ったCase / Artifactへ関連付けられている状態
- Source of Truth Conflictが存在する状態
- publication-tracking.jsonと対象Case / Publication Artifactとの対応を確認できない状態
- ApplicableなPublication ArtifactについてArtifact-level ApplicabilityまたはProduction StateとのTraceabilityを確認できない状態
- Applicable Audit Referenceが対象Case、対象Artifact、Applicable VersionまたはApplicable Auditと整合しない状態
- Applicable Audit Referenceを一意にValidationできない状態

Repository Integrityに問題を検出した場合、Timestamp、Filename、Version番号、Directory位置その他の表面的な情報だけを根拠として正式状態を推測してはならない。

確認可能なSource of TruthおよびTraceabilityから正式状態を確認する。

一意に判断できない場合は、Conflictまたは未確認状態として保持する。

---

## 8.3 Traceability Principle

ProjectORIGIN Repositoryでは、正式なProduction Artifactおよび関連成果物について、Applicableな範囲で生成、監査、承認、統合、RevisionおよびPublicationの関係を後から確認可能な状態に維持する。

Traceabilityは、単に関連Fileが同じDirectoryに存在することだけでは成立しない。

Applicableな範囲で少なくとも以下の関係を確認可能にする。

- Case Identity
- Artifact Identity
- Artifact Type
- Applicable Version
- Repository Placement
- Upstream Artifact
- Downstream Artifact
- Required Production / Publication Audit
- Applicable Final Flow Audit
- Applicable Human Approval Decision
- Repository Integration
- Publication Status
- Revision Relation
- Historical Version Relation
- Metadata
- Asset Reference
- Applicable Dependency
- Artifact-level Applicability
- Artifact-level Production State
- Applicable Audit Reference
- Applicable Audit Referenceと対象Caseの関係
- Applicable Audit Referenceと対象Artifactの関係
- Applicable Audit ReferenceとApplicable Versionの関係
- Applicable Audit ReferenceとApplicable Audit Artifactの関係
FREEおよびCLASSIFIEDのArtifact-level Trackingに関するTraceabilityは、

cases/FILE-XXX/publication-tracking.json

をPrimary Source of Truthとして維持する。

ただし、Artifact-level TrackingからCase-level Workflow Status、Publication Status、Audit ResultまたはHuman Approval Decisionを自動導出してはならない。

同様に、それらの状態またはRepository上のFile存在だけを根拠としてArtifact-level Trackingの値を推測してはならない。
ただし、本Listを新しいDatabase Schema、Metadata SchemaまたはManifest Formatとして扱ってはならない。

具体的なField、Format、Storage、Reference Methodその他の実装仕様はApplicable Source of Truthに従う。

Traceabilityを維持する目的だけを理由として、未定義のDatabase Field、Metadata Field、Directory、Filename ConventionまたはAutomation Structureを新設してはならない。

---

## 8.4 Case Identity Integrity

Repository上のArtifactは、その所属Caseを一意に確認できる状態を維持する。

Case Directory、Stable Identifier、Applicable Database Recordその他の正式情報との間で、Case Identityが矛盾する状態を作ってはならない。

異なるCaseのArtifactを、所属Caseを確認できない状態で混在させてはならない。

Case Title、表示名、略称その他の可変情報だけを根拠としてCase Identityを決定してはならない。

Case Identity Conflictを検出した場合、より新しいFile、より新しいTimestampまたはより大きいVersion番号を自動的に正しいCaseへ属するものとして扱ってはならない。

Stable IdentityおよびApplicable Source of Truthから正式な所属を確認する。

正式な所属を一意に判断できない場合は、推測によってCaseを再割当てせず、Conflictまたは未確認状態として保持する。

---

## 8.5 Artifact Identity Integrity

Production Artifactは、対象Case内でそのArtifact Identityを識別可能な状態で管理する。

Artifact IdentityはFilenameだけによって成立するものではない。

Applicableな範囲で、

- Case Identity
- Artifact Type
- Production Layer
- Applicable Version
- Repository Placement
- Production Flow
- Traceability

との関係から正式なArtifactを確認する。

Filenameを変更しただけで、新しいArtifact Identityが自動的に成立したものとみなしてはならない。

同様に、同じFilenameを持つことだけを理由として、異なるArtifactを同一Artifactとして扱ってはならない。

Artifact Identity Conflictを検出した場合、既存Artifactを無条件に上書き、削除または統合してはならない。

正式なRelationを確認できない場合はConflictとして保持する。

---

## 8.6 Version Traceability

Production ArtifactのVersionは、対象Artifactとの関係を識別可能な状態で管理する。

Production ArtifactのVersion表記、Major Version Increment、Minor Version Increment、No Version Increment、Current Version SelectionおよびHistorical Version RetentionはChapter 5の正式Criteriaに従う。

本章はChapter 5のVersion Criteriaを独自に再定義、置換または推測しない。

複数Versionが存在する場合、少なくとも各Versionと対象Artifactとの関係を追跡できる状態を維持する。

Version番号が大きいことだけを理由としてCurrent Versionと判断してはならない。

Timestampが新しいことだけを理由としてCurrent Versionと判断してはならない。

Filenameが最新版に見えることだけを理由としてCurrent Versionと判断してはならない。

Repository Integrationが最後に実行されたVersionであることだけを理由としてCurrent Versionと判断してはならない。

Current VersionはChapter 5および確認可能なTraceabilityに基づいて判定する。

Chapter 5および確認可能なTraceabilityからCurrent Versionを一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

Historical Versionを保持することは、そのVersionがCurrentまたは現在Applicableであることを意味しない。

したがって、

Historical Preservation
≠
Current Applicability

とする。

新しいVersionが存在することだけを理由としてHistorical Versionを削除または上書きしてはならない。

Historical Versionは、必要なTraceabilityを維持できる状態で管理する。

ただし、Historical Version Retentionを理由として、本章から専用\`archive/\` Directory、Retention Period、Automatic Deletion Schedule、Archive Filename Convention、追加Metadata FieldまたはDatabase Fieldを新設してはならない。

---

## 8.7 Version and Audit Traceability

Audit Resultは、そのAuditが対象としたArtifactおよびApplicable Versionとの関係を追跡できる状態で管理する。

あるVersionに対して成立したAudit Resultを、別Versionへ自動的に適用してはならない。

新しいVersionが生成された場合、旧Versionに成立していたAudit Resultを新Versionへ自動継承したものとして扱ってはならない。

Re-Auditの必要性およびApplicable AuditはAudit Rule、Production Flowその他のApplicable Source of Truthに従う。

Version Increment自体を理由としてAudit Resultを自動生成してはならない。

Audit ResultがPASSであることだけを理由として、そのArtifact VersionがCurrent、Approved、IntegratedまたはPublishedであるとみなしてはならない。

同様に、Current Versionであることだけを理由としてAudit ResultがPASSであると推測してはならない。

Audit Artifactの正式な物理Repository Placementは、

cases/FILE-XXX/audit/

とする。

Audit Artifactは、少なくとも所属Case、対象Artifact、Applicable VersionおよびAudit ResultとのTraceabilityを維持する。
FREEおよびCLASSIFIEDのApplicable Audit Referenceは、

cases/FILE-XXX/publication-tracking.json

において、対象Publication ArtifactにApplicableなAudit ArtifactへのRepository-relative Referenceとして管理する。

Applicable Audit ReferenceはAudit Resultそのものではなく、Audit Resultを複製するFieldとして扱ってはならない。

Applicable Audit ReferenceのReference Validationでは、少なくとも、

- 対象Case
- 対象Artifact
- Applicable Version
- Applicable Audit

との対応を確認する。

Referenceが存在しない、別Caseを参照している、対象Artifactが一致しない、Applicable Versionが一致しない、またはApplicable Auditを一意に確認できない場合、Reference Validationを成功として扱ってはならない。

Reference Validation FAILそれ自体をAudit Result \`BLOCKER\`と同一視してはならない。

曖昧なApplicable Audit ReferenceをAI AgentまたはAutomationによって推測、補完または自動修復してはならない。

このPlacementからAudit Artifact Filename Convention、Audit Artifact Versioning、\`audit/\`配下のSubdirectory、Retention / Archive Placement、追加Database / Metadata Fieldまたは具体的Automation実装を自動的に導出してはならない。

---

## 8.8 Version and Human Decision Traceability

Human Approval Decisionその他のApplicable Human Decisionは、そのDecisionが対象としたArtifactおよびApplicable Versionとの関係を追跡できる状態で管理する。

あるVersionに対して成立したHuman Approval Decisionを、別Versionへ自動的に継承してはならない。

新しいVersionが生成された場合、旧VersionのHuman Approval Decisionが新Versionにも成立していると推測してはならない。

Revision後に再Human Approvalが必要かどうかはApplicable Production Flowおよび正式なSource of Truthに従う。

Human Approval Decisionが\`APPROVED\`であることだけを理由として、対象ArtifactがRepository Integration済みまたはPublishedであるとみなしてはならない。

同様に、Repository IntegrationまたはPublicationが成立していることだけを理由として、Applicable Human Approval Decisionを推測してはならない。

Version、Audit Result、Human Approval Decision、Repository IntegrationおよびPublication Statusは、それぞれ異なる責務として維持する。

---

## 8.9 Repository Integration Traceability

Repository Integrationは、対象Case、対象ArtifactおよびApplicable Versionとの関係を追跡できる状態で管理する。

Repository Integrationが実行されたことだけを理由として、Artifact VersionをIncrementしてはならない。

したがって、

Repository Integration
≠
Automatic Version Increment

とする。

Re-Integrationについても同様とする。

Re-Integration
≠
Automatic Version Increment

Repository IntegrationまたはRe-Integrationに伴ってArtifact Contentが変更された場合、そのVersion DecisionはChapter 5の正式Criteriaに従う。

Repository Integration履歴が存在することだけを理由として、そのArtifactがCurrent、ApprovedまたはPublishedであると判断してはならない。

Repository Integrationと、

- Artifact Version
- Audit Result
- Final Flow Audit Result
- Human Approval Decision
- Publication Status

の関係を混同しない。

Repository Integrationに関する詳細な責務およびEntry ConditionはChapter 7に従う。

---

## 8.10 Revision Traceability

Production ArtifactにRevision、Correctionその他の変更が発生した場合、変更前後のArtifact Relationを必要な範囲で追跡可能な状態に維持する。

Revisionが発生したことだけを理由として、Major VersionまたはMinor Versionを自動的にIncrementしてはならない。

変更内容が、

- Major Version Increment
- Minor Version Increment
- No Version Increment

のいずれに該当するかはChapter 5の正式Criteriaに従う。

Audit Correction、Content Revision、Publication Revision、Human Approval後のRevisionまたはRepository Integration後のRevisionというRevision Typeだけを根拠として、Major / Minorを固定的に決定してはならない。

実際の変更内容およびApproval Boundaryへの影響を確認する。

Chapter 5および確認可能なTraceabilityからVersion Decisionを一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

Revisionによって新Versionが生成された場合、旧VersionのAudit Result、Final Flow Audit Result、Human Approval Decision、Repository IntegrationまたはPublication状態を新Versionへ自動継承してはならない。

Revision Historyを保持することは、旧Versionが現在Applicableであることを意味しない。

---

## 8.11 Production Flow Traceability

Repository上のArtifact Relationは、Applicable Production Flowを逆転、短縮または省略したものとして記録してはならない。

Applicableな範囲で、

Upstream Production
↓
Required Audit
↓
Applicable Approval
↓
Downstream Production

その他の正式なProduction Relationを追跡可能にする。

ただし、本章はProduction Workflowそのものを新たに定義しない。

具体的なStage、Gate、Workflow Status、Audit RequirementおよびHuman Approval RequirementはAGENTS.md、Audit Ruleその他のApplicable Source of Truthに従う。

Repository上にDownstream Artifactが存在することだけを理由として、Upstream AuditまたはApprovalが完了していると推測してはならない。

同様に、上流Artifactが存在することだけを理由として、後続工程への使用が承認されているとみなしてはならない。

---

## 8.12 Publication Traceability

Publication Artifactについて、対象Case、Artifact Identity、Applicable Version、Publication区分、Artifact-level TrackingおよびPublication Statusとの関係を必要な範囲で追跡可能にする。

FREE ArtifactとCLASSIFIED Artifactは異なるArtifact Identityを持つ。

一方のArtifactのApplicability、Production State、Applicable Audit Reference、Audit ResultまたはPublication Statusを、他方のArtifactへ自動的に適用してはならない。

FREEおよびCLASSIFIEDのArtifact-level Trackingは、

cases/FILE-XXX/publication-tracking.json

をCase-level Repository-managed Operational Metadata Artifactとして管理する。

FREEおよびCLASSIFIEDそれぞれについて、Applicable Repository Rule Sectionで正式に定義された、

- Applicability
- Production State
- Applicable Audit Reference

とのTraceabilityを維持する。

Artifact-level Applicabilityの正式なControlled Valuesは、

APPLICABLE
NOT_APPLICABLE

とする。

Artifact-level Production Stateの正式なControlled Valuesは、

NOT_STARTED
IN_PROGRESS
COMPLETE

とする。

\`NOT_APPLICABLE\`をProduction Stateとして扱ってはならない。

Applicable Audit Referenceは、対象Publication ArtifactにApplicableなAudit ArtifactへのRepository-relative Referenceとして扱う。

Publication Statusが\`PUBLISHED\`であることだけを理由として、

- Artifact-level Production State = COMPLETE
- Required Audit PASS
- Final Flow Audit PASS
- Human Approval Decision = APPROVED
- Repository Integration完了

を自動的に推測してはならない。

同様に、それらの上流状態が成立していることだけを理由としてPublication Statusを\`PUBLISHED\`へ変更してはならない。

Artifact-level Production Stateが\`COMPLETE\`であることだけを理由として、Audit Result、Human Approval Decision、Repository IntegrationまたはPublication Statusを推測してはならない。

Repository上にFREEまたはCLASSIFIED Artifactが存在することだけを理由として、そのApplicabilityまたはProduction Stateを推測してはならない。

\`publication-tracking.json\`の存在だけを理由として、その内部値を推測または補完してはならない。

本SectionはFREE / CLASSIFIED用の新しいCase-level Workflow Status、Publication Status、Audit Result、Database FieldまたはProduction Layerを追加しない。

---

## 8.13 Database and Repository Consistency

Repository上の正式状態とDatabase上の管理状態は、Applicable Source of Truthに従って整合性を維持する。

RepositoryとDatabaseの間に差異を検出した場合、どちらか一方を常に正しいものとして自動的に上書きしてはならない。

Applicable Source of Truth、Artifact、Version、Audit、Human Decision、Repository Integration、Publicationその他のTraceabilityから正式状態を確認する。

Repository上にFileが存在することだけを理由としてDatabase Recordを自動的に正しいものと判断してはならない。

Database Recordが存在することだけを理由としてRepository上のArtifactを正式Artifactと判断してはならない。

Database / Repository Conflictを解消するために、新しいDatabase Field、Controlled Value、Metadata FieldまたはMigration Ruleを本章から独自に作成してはならない。

Database Field、Data Type、Validation、Constraintその他の正式仕様はDatabase RuleおよびDatabase Schemaに従う。

---

## 8.14 Asset Traceability

Assetは、Applicableな範囲で対象Case、対象Artifactおよび必要なReferenceとの関係を追跡可能な状態で管理する。

Asset FileがRepositoryに存在することだけを理由として、そのAssetが特定Artifactへ正式に適用されているとみなしてはならない。

同様に、Artifact内にAsset Referenceが存在することだけを理由として、対象Assetの存在、正当性、License、ApprovalまたはCurrent Applicabilityを推測してはならない。

Assetの分類、Source、License、Caption、Visual Roleその他の専門仕様はImage Rule、Art Bibleその他のApplicable Source of Truthに従う。

Assetを差し替える場合、旧AssetとのRelationおよび必要なHistorical Traceabilityを失ってはならない。

ただし、本章はAsset Historyを理由として新しいAsset Archive Structure、Metadata FieldまたはDatabase Fieldを独自に定義しない。

---

## 8.15 Historical Integrity

ProjectORIGIN Repositoryでは、正式なRevision、Version変更、Integration、Publicationその他の変更によって、必要なHistorical Traceabilityを失ってはならない。

Historical Integrityは、すべての過去Fileを無条件かつ永久に保持することと同義ではない。

必要な履歴をどのように保持するかについて正式なRetention、ArchiveまたはDeletion Ruleが必要な場合、そのRuleを本章から推測によって作成してはならない。

Production ArtifactのHistorical Version RetentionはChapter 5の正式Criteriaに従う。

新Versionが存在することだけを理由として、旧Versionを上書きまたは削除してはならない。

一方、Historical Versionを保持していることだけを理由として、そのVersionをCurrentまたは現在Applicableとみなしてはならない。

Historical Preservation
≠
Current Applicability

とする。

Historical Traceabilityでは、Applicableな範囲で、

- Artifact Identity
- Version Relation
- Revision Relation
- Applicable Audit
- Applicable Final Flow Audit
- Applicable Human Decision
- Repository Integration
- Publication History
- Dependency

との関係を確認可能な状態に維持する。

本章から専用\`archive/\` Directory、Retention Period、Automatic Deletion Schedule、Archive Filename Convention、追加Metadata FieldまたはDatabase Fieldを新設してはならない。

---

## 8.16 Cross-Case Integrity

異なるCase間のIdentityおよびArtifact Relationを混同してはならない。

同一Source、同一Asset、類似Content、同一Artifact Typeまたは同一Version番号が複数Caseに存在することだけを理由として、それらのCase IdentityまたはArtifact Identityを統合してはならない。

一方、Applicable Source of Truthによって正式なCross-Case Relation、Shared Asset、Shared Sourceその他の関係が定義されている場合、その正式な関係までCross-Case Isolationを理由として削除してはならない。

つまり、

Cross-Case Isolation
≠
Prohibition of all Cross-Case Relations

とする。

正式なCross-Case Relationが存在する場合は、各CaseのIdentityを維持したまま、そのRelationを追跡可能な状態にする。

Cross-Case Misassociationを検出した場合、単に一方のReferenceを削除して問題を不可視化してはならない。

Applicableな範囲で、Artifact、Version、Required Production / Publication Audit、Applicable Final Flow Audit、Applicable Human Approval Decision、Repository Integration、Database、Asset、PublicationおよびHistorical Traceabilityへの影響を確認する。

正式な所属CaseまたはCross-Case Relationを判断できない場合、新しいRelationを推測によって作成せず、Conflictまたは未確認状態として扱う。

---

## 8.17 HOLD Dependencies and Resolution Reflection

本章のRepository Integrity and Traceabilityは、正式HOLD Ledgerに登録されたActive HOLDおよびRESOLVED Archiveとの責務境界を維持する。

HOLDの正式な状態はHOLD LedgerをSource of Truthとして確認する。

本章だけを根拠としてHOLDのStatus、Resolution、Human Decision RequirementまたはDispositionを変更してはならない。

### HOLD-ARTIFACT-VERSION-01

\`HOLD-ARTIFACT-VERSION-01\`について、Production Artifact Version Increment Criteriaに必要なHuman Decisionは完了し、Major Version Increment、Minor Version Increment、No Version Increment、Patch Component不採用、Current Version SelectionおよびHistorical Version Retentionの正式CriteriaがChapter 5へ反映されている。

本章はVersion IntegrityおよびTraceabilityについてChapter 5のCriteriaに従う。

本章からMajor / Minor / No Version Increment、Current Version SelectionまたはHistorical Version Retentionを独自に再定義、置換または推測してはならない。

Version変更によって、旧Versionと新VersionのRelation、Applicable Audit、Applicable Final Flow Audit、Human Approval Decision、Repository Integration、Publication Historyその他の必要なTraceabilityを失ってはならない。

Resolution前は、本章への反映だけでは\`HOLD-ARTIFACT-VERSION-01\`をRESOLVEDとせず、Applicable Source of Truthへの必要な反映、Compatibility確認および最終横断再監査のPASSが要求されていた。

これらのResolution条件は完了し、\`HOLD-ARTIFACT-VERSION-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

### HOLD-PUBLICATION-TRACKING-01

\`HOLD-PUBLICATION-TRACKING-01\`について、FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Trackingに必要なHuman Decisionは完了している。

正式に承認されたArtifact-level Trackingは、FREEおよびCLASSIFIEDそれぞれについて、

- Applicability
- Production State
- Applicable Audit Reference

を独立して管理する。

Artifact-level TrackingのPrimary Source of Truthは、

cases/FILE-XXX/publication-tracking.json

とする。

\`publication-tracking.json\`はCase-level Repository-managed Operational Metadata Artifactであり、Production Artifact、Audit Artifact、Database Recordまたは新しいProduction Layerではない。

Artifact-level TrackingとCase-level Workflow Status、Publication Status、Audit ResultおよびHuman Approval Decisionは独立した責務として維持する。

本章は、承認済みHuman Decisionを超えて新しいArtifact-level Production State、Applicability、Workflow Status、Publication Status、Audit Result、Database Field、Audit Filename ConventionまたはTracking Systemを追加してはならない。

Resolution前のActive状態はHuman Decision未確定を理由とするものではなく、Applicable Source of Truthへの必要な反映、Repository Integration、Automation Boundary、Existing Case Compatibilityおよび関連文書の最終横断再監査の完了を確認するためのものであった。

これらのResolution条件は満たされ、最終横断再監査はPASSしている。\`HOLD-PUBLICATION-TRACKING-01\`は正式HOLD Ledger上でRESOLVEDとして管理されている。

解消済みの本HOLDを本章からActive HOLDとして再Openしてはならない。

### HOLD-AUDIT-PLACEMENT-01

\`HOLD-AUDIT-PLACEMENT-01\`について、Case単位のAudit Artifact正式物理Repository Placementとして、

cases/FILE-XXX/audit/

を採用するHuman DecisionおよびRepository Ruleへの反映は完了している。

本章はこの正式Placementを使用し、所属Case、対象Artifact、Applicable VersionおよびAudit ResultとのTraceabilityを維持する。

ただし、Audit Placement DecisionからAudit Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、Subdirectory、追加Database / Metadata Fieldまたは具体的Automation実装を派生させてはならない。

本HOLDの正式ResolutionおよびHistorical RecordはHOLD Ledgerに従う。

解消済みHOLDを本章からActive HOLDとして再Openしてはならない。

### Publication Status Compatibility

Publication Statusの責務およびControlled Value Compatibilityは、Chapter 6およびApplicable Source of Truthの正式な定義に従う。

解消済みPublication Status Compatibility事項を、本章からActive HOLDとして再登録または再Openしてはならない。

Repository / Database ConsistencyまたはPublication Traceabilityを理由として、異なる責務を持つStatus体系を無整理に統合してはならない。

---

本章終了時点のActive HOLDは、正式HOLD Ledgerの最新状態に従う。

\`HOLD-ARTIFACT-VERSION-01\`についてResolution前に必要とされたCompatibility確認および最終横断再監査はPASSしており、正式HOLD Ledger上でRESOLVEDとして管理されている。

\`HOLD-PUBLICATION-TRACKING-01\`については、承認済みArtifact-level Tracking体系をApplicable Source of Truthに従って使用し、その正式Decisionを超える新しいTracking体系、Controlled ValueまたはStorage Structureを推測してはならない。

解消済みHOLDを、本章によってActive HOLDへ戻してはならない。

---

## 8.18 Automation and Integrity Boundary

Automationは、Repository IntegrityおよびTraceabilityの確認を支援できる。

ただし、Automationは確認可能な情報から一意に判定できない正式状態を推測によって作成してはならない。

AutomationはApplicableな範囲で、

- Case Identityの照合
- Artifact Identityの照合
- Version表記の確認
- Defined Repository Placementの確認
- Required Referenceの存在確認
- Required Audit Resultの確認
- Applicable Final Flow Audit Resultの確認
- Applicable Human Approval Decisionの確認
- Defined Dependencyの確認
- Repository / Database間の機械的差異確認
- Historical Relationの存在確認
- Artifact-level ApplicabilityのDefined Value確認
- Artifact-level Production StateのDefined Value確認
- Applicable Audit ReferenceのReference Validation
- Publication Production Gateの機械的確認

その他、正式仕様によって条件が確定している機械的確認を支援し得る。

ただし、本ListはAutomation実装仕様を新たに定義するものではない。

Automationは、

- Current VersionをVersion番号最大値だけから決定する
- Major / Minor / No Version Incrementを曖昧な状態で推測する
- Patch ComponentをProduction Artifactへ追加する
- Audit Resultを別Versionへ自動継承する
- Human Approval Decisionを別Versionへ自動継承する
- Repository IntegrationをVersion Increment Triggerとして扱う
- Missing Traceabilityを推測で補完する
- Repository / Database Conflictを一方の自動上書きで解消する
- Active HOLDの未確定仕様をDefault値で埋める
- 解消済みHOLDをActive HOLDとして再Openする
- Artifact-level ApplicabilityをFile存在から推測する
- Artifact-level Production StateをWorkflow Status、Publication Status、Audit ResultまたはFile存在から推測する
- 曖昧なApplicable Audit Referenceを推測、補完または自動修復する
- Reference Validation FAILをAudit Result \`BLOCKER\`へ自動変換する
- 未定義のArtifact-level Tracking Controlled Valueを作成する

ことを行ってはならない。

Chapter 5および確認可能なTraceabilityからVersion DecisionまたはCurrent Versionを一意に判定できない場合、Automationは推測によって処理を続行せず、Human Decisionを要求する。

---

## 8.19 Core Integrity Principle

ProjectORIGIN RepositoryにおけるRepository Integrity and Traceabilityの基本原則は、

\*\*正式なCase、Artifact、Version、Audit、Human Decision、Repository Integration、PublicationおよびHistorical Relationを、相互の責務を混同せず、後から確認可能な状態で維持すること\*\*

とする。

Repository Integrityは、単にFileが存在すること、Directory Structureが正しいことまたはVersion番号が付いていることだけでは成立しない。

Artifact VersionはChapter 5の正式Criteriaに従う。

本章はMajor、Minor、No Version Increment、Current Version SelectionまたはHistorical Version Retentionを独自に再定義しない。

以下の責務境界を維持する。

Artifact Version
≠
Audit Result
≠
Human Approval Decision
≠
Repository Integration
≠
Publication Status

新Versionが存在することだけを理由として、旧VersionのAudit Result、Final Flow Audit Result、Human Approval Decision、Repository IntegrationまたはPublication状態を新Versionへ自動継承してはならない。

Version番号が最大であること、Timestampが新しいこと、Filenameが最新版に見えることまたはRepository Integrationが最後に実行されたことだけを理由としてCurrent Versionを決定してはならない。

Historical Versionを保持することはCurrent Applicabilityを意味しない。

Repository IntegrationまたはRe-IntegrationはAutomatic Version Incrementを意味しない。

Repository / Database間にConflictが存在する場合、一方を自動的に正として他方を上書きしてはならない。

Audit Artifactの正式な物理Placementは、

cases/FILE-XXX/audit/

とし、対象Artifact、Applicable VersionおよびAudit ResultとのTraceabilityを維持する。

ただし、そのPlacementからAudit Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、追加Database / Metadata FieldまたはAutomation実装を推測してはならない。

Active HOLDの対象となる未確定仕様を、IntegrityまたはTraceability維持の都合によって暗黙に確定してはならない。

本章終了時点のHOLD状態は正式HOLD Ledgerに従う。

\`HOLD-ARTIFACT-VERSION-01\`についてResolution前に必要とされたCompatibility確認および最終横断再監査はPASSしており、正式HOLD Ledger上でRESOLVEDとして管理されている。

FREEおよびCLASSIFIEDのArtifact-level Trackingは、Applicable Repository Rule Sectionで正式に定義された範囲に従う。

Artifact-level TrackingのPrimary Source of Truthは、

cases/FILE-XXX/publication-tracking.json

とする。

Artifact-level TrackingのIntegrityは、値またはFileが存在することだけでは成立しない。

Applicableな範囲で、

対象Case
↓
対象Publication Artifact
↓
Applicability
↓
Production State
↓
Applicable Version
↓
Applicable Audit Reference
↓
Applicable Audit Artifact

とのTraceabilityを確認可能な状態に維持する。

Applicable Audit ReferenceはAudit Resultではない。

Reference Validation FAILはAudit Result \`BLOCKER\`ではない。

Artifact-level TrackingからCase-level Workflow Status、Publication Status、Audit ResultまたはHuman Approval Decisionを自動導出してはならない。

同様に、それらの状態またはFile存在だけを根拠としてArtifact-level Trackingの値を推測してはならない。

\`HOLD-PUBLICATION-TRACKING-01\`についてResolution前に必要とされた承認済みDecisionのApplicable Source of Truthへの反映および最終横断再監査は完了しており、正式HOLD Ledger上でRESOLVEDとして管理されている。

Resolution前にActiveであったこと、または現在RESOLVEDであることを理由として、すでに承認されたArtifact-level Tracking Decisionを未確定仕様へ戻してはならない。

承認済みDecisionを超える新しいTracking体系、Controlled Value、Database Field、Production Layer、Audit Filename ConventionまたはAutomation仕様を本章から推測してはならない。

解消済みHOLDを本章によってActive HOLDへ戻してはならない。

不明な状態を推測によって正常化することよりも、確認可能なTraceabilityを維持し、Conflictまたは未確認状態を可視化したまま正式な解決工程へ送ることを優先する。

# Chapter 9

# Repository Compatibility and Migration

## 9.1 Purpose

本章は、ProjectORIGIN RepositoryにおいてRepository Structure、Artifact Management Rule、Naming、Status、Reference、Metadata Relationその他のRepository管理仕様が変更される場合に、Existing Case、Existing Artifact、Existing Relationおよび必要なHistorical TraceabilityとのCompatibilityを維持するための原則を定義する。

ProjectORIGINのRepositoryは、Projectの継続的なDevelopment、Production、Operationおよび正式なSource of TruthのRevisionに伴って変更され得る。

ただし、新しいRepository仕様が正式化されたことだけを理由として、既存のCase、Artifact、Version、Audit、Final Flow Audit、Human Approval Decision、Repository Integration、Publication、Metadata、Asset Referenceその他の正式情報を、新仕様へ無条件に変換してはならない。

Repository Compatibilityの目的は、

\*\*新しい正式仕様を適用可能にしながら、既存の正式なIdentity、Relation、Decision、Version、HistoryおよびTraceabilityを不必要に破壊しないこと\*\*

とする。

MigrationはCompatibilityを実現するための手段となり得るが、Migrationそのものを目的として既存の正式情報を変更してはならない。

---

## 9.2 Compatibility Principle

Repository Structure、Naming、Version Representation、Status Management、Reference Method、Metadata Relationその他のRepository管理仕様を変更する場合、既存ArtifactとのCompatibility Impactを確認する。

新しい仕様への適合だけを理由として、既存の正式なIdentity、Version Relation、Audit Result、Final Flow Audit Result、Human Approval Decision、Repository Integration Relation、Publication Historyその他の正式情報を失ってはならない。

Compatibility対応では、

- Existing Case Identity
- Existing Artifact Identity
- Existing Version Relation
- Existing Audit Traceability
- Existing Final Flow Audit Traceability
- Existing Human Approval Decision
- Existing Repository Integration Relation
- Existing Publication History
- Existing Asset Relation
- Existing Dependency

をApplicableな範囲で維持する。

Compatibilityは、過去の正式状態を現在の仕様に見せかけるための書き換えを意味しない。

---

## 9.3 Migration Principle

Migrationは、正式に承認されたRepository仕様変更を既存Repositoryへ適用するために必要な場合に実施する。

Migrationを行う場合は、変更対象、変更理由、Applicable Source of Truth、影響範囲および必要なTraceabilityを確認する。

Migrationによって既存Artifactの意味、Identity、Approval StateまたはPublication Stateを暗黙に変更してはならない。

Migrationが必要であることだけを理由として、

- 新しいArtifactを生成する
- 新しいVersionを生成する
- Workflow Statusを変更する
- Publication Statusを変更する
- Human Approval Decisionを変更する
- Repository Integrationを成立させる
- Publicationを成立させる

ことはできない。

Migrationは、それぞれの正式な成立条件を代替しない。

---

## 9.4 Identity Preservation

CompatibilityまたはMigrationでは、Case IdentityおよびArtifact Identityを維持する。

Directory名、Filename、Placement、Reference MethodまたはMetadata Representationが変更された場合でも、それだけを理由として既存Artifactを別のArtifact Identityとして扱ってはならない。

一方、Applicable Source of Truthによって新しいArtifact Identityとして扱う必要があることが確認された場合は、既存Identityを便宜的に維持して同一Artifactとして扱ってはならない。

Identity Relationを一意に判断できない場合は、推測によって統合または分離せず、未確認状態として扱う。

---

## 9.5 Repository Structure Migration

Repository Structureを変更する場合、既存Artifactの所属Case、Artifact Type、VersionおよびRelationを維持する。

新しいDirectory Structureが正式化された場合でも、既存Artifactを一括移動することを自動的な必須処理とはしない。

Migrationの必要性および対象範囲は、Applicable Source of TruthとCompatibility Impactに基づいて判断する。

Directoryの移動またはPlacement変更それ自体を、Artifactの内容変更、Version Increment、Approval変更、Repository Integration完了またはPublication変更として扱ってはならない。

正式なMigrationを実施した場合は、必要なHistorical Traceabilityを維持する。

---

## 9.6 Naming Compatibility

Filename Conventionが変更された場合、新しいNaming Conventionへの適合だけを理由として既存ArtifactのIdentity、Version、Approval StateまたはPublication Stateを変更してはならない。

Filename Renameは、それ自体では新しいArtifactの生成またはVersion Incrementを意味しない。

つまり、

Filename Rename
≠
New Artifact

Filename Rename
≠
Automatic Version Increment

とする。

Naming変更によって旧Filenameと新FilenameのRelationを追跡する必要がある場合は、Applicable Source of Truthに基づいて必要なTraceabilityを維持する。

---

## 9.7 Version Compatibility

Production ArtifactのMajor Version Increment、Minor Version Increment、No Version Increment、Current Version SelectionおよびHistorical Version Retentionは、Chapter 5の正式Criteriaに従う。

本章は、Chapter 5に定義されたVersion Criteriaを独自に再定義、置換または推測してはならない。

Migration、Naming変更、Placement変更、Metadata変更、Reference変更またはVersion Representation変更それ自体を、Automatic Version Incrementの根拠としてはならない。

したがって、

Migration
≠
Automatic Version Increment

Name Change
≠
Version Increment

Placement Change
≠
Automatic Version Increment

とする。

Version番号が大きいこと、Timestampが新しいこと、新Naming Conventionへ適合していること、または新Structureに存在することだけを理由として、対象ArtifactをCurrent、Approved、IntegratedまたはPublished Versionとしてはならない。

Migration前後のVersion Relation、Applicable Audit Result、Applicable Final Flow Audit Result、Human Approval Decision、Repository IntegrationおよびPublication Historyについて、必要なHistorical Traceabilityを維持しなければならない。

MigrationまたはCompatibility処理によって新Versionが生成された場合でも、旧Versionに成立していたAudit ResultまたはHuman Approval Decisionを新Versionへ自動継承してはならない。

Historical Versionを保持することは、そのVersionがCurrentまたは現在Applicableであることを意味しない。

したがって、

Historical Preservation
≠
Current Applicability

とする。

CompatibilityまたはMigrationから、専用\`archive/\` Directory、Retention Period、Automatic Deletion Schedule、Archive Filename Convention、追加Metadata FieldまたはDatabase Fieldを独自に生成してはならない。

Chapter 5のCriteriaおよび確認可能なTraceabilityからVersion RelationまたはCurrent Versionを一意に判定できない場合、AI AgentまたはAutomationは推測によって決定してはならず、Human Decisionを要求する。

---

## 9.8 Workflow Status Compatibility

Repository CompatibilityまたはMigrationによって、Workflow Statusを独自に生成、変換または推測してはならない。

Workflow Statusの正式な名称およびControlled ValueはChapter 6およびApplicable Source of Truthに従う。

旧Representationから現行Representationへの変換が必要な場合も、意味上の対応関係を確認できないStatusを推測によってMappingしてはならない。

Migrationが完了したことだけを理由として、

Workflow Status = APPROVED

としてはならない。

Workflow StatusとMigration Stateは異なる概念として扱う。

---

## 9.9 Publication Status Compatibility

Publication Statusは、Chapter 6およびApplicable Source of Truthが定義する正式な責務およびControlled Valueに従う。

Repository Migration、Filename変更、Placement変更、Version Representation変更またはRepository Integrationだけを理由としてPublication Statusを変更してはならない。

特に、

Repository Integration
≠
Publication

Migration
≠
Publication

とする。

Publication StatusのCompatibility処理では、既存の正式なPublication Historyを失ってはならない。

Publication Status Compatibilityに関する解消済みHOLDを、本章によって再Openしてはならない。

---

## 9.10 Audit Compatibility

CompatibilityまたはMigrationによって、既存Audit Resultの対象ArtifactまたはApplicable VersionとのRelationを失ってはならない。

Audit Resultは、そのAuditが実際にApplicableであるArtifactおよびVersionとの関係を維持する。

旧Versionに対するAudit Resultを、新VersionまたはMigration後の異なるArtifactへ自動適用してはならない。

Migration自体をAudit PASSの代替として扱ってはならない。

Audit Artifactの正式な物理Repository Placementは、

cases/FILE-XXX/audit/

とする。

ただし、このPlacementからAudit Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、Subdirectory、追加Database / Metadata FieldまたはAutomation実装を独自に派生させてはならない。

解消済み\`HOLD-AUDIT-PLACEMENT-01\`をCompatibilityまたはMigrationを理由としてActive HOLDへ戻してはならない。

---

## 9.11 Final Flow Audit Compatibility

Applicable Final Flow Audit Resultは、そのResultが成立した対象Artifact、VersionおよびProduction Flowとの関係を維持する。

Migration、Rename、Placement変更、Re-Integrationその他の処理を理由として、旧Versionまたは旧Artifactに成立したFinal Flow Audit PASSを別Versionへ自動継承してはならない。

Required Production / Publication Audit PASSとApplicable Final Flow Audit PASSを同一概念として扱ってはならない。

Compatibility処理はFinal Flow Audit Gateを省略または代替しない。

---

## 9.12 Human Approval Compatibility

Human Approval Decisionは、そのDecisionがApplicableであるArtifactおよびVersionとのRelationを維持する。

Migration、Naming変更、Placement変更、Repository IntegrationまたはVersion Representation変更だけを理由として、Human Approval Decisionを別Artifactまたは別Versionへ自動継承してはならない。

Human Approval APPROVEDは、Migration完了またはRepository Integration完了と同一ではない。

Human Approval APPROVED
≠
Migration Complete

Human Approval APPROVED
≠
Repository Integration Complete

とする。

Compatibility処理によってHuman Approval Gateを省略してはならない。

---

## 9.13 Repository Integration Compatibility

Repository Integrationは、Applicable Source of Truthに従って成立したApproved Artifactを正式Repositoryへ統合する工程として扱う。

MigrationまたはCompatibility処理が行われたことだけを理由として、Repository Integrationが成立したものと扱ってはならない。

既存ArtifactをRe-Integrationする必要がある場合も、Re-Integrationそれ自体をAutomatic Version Incrementとして扱ってはならない。

Repository Integration後にArtifact内容が変更された場合のVersion判定はChapter 5の正式Criteriaに従う。

Repository Integration Relationを変更する場合は、旧Relationおよび新Relationについて必要なHistorical Traceabilityを維持する。

---

## 9.14 Database Compatibility Boundary

Repository CompatibilityまたはMigrationは、Database Schemaを独自に変更しない。

新しいRepository Structure、Naming、Version ManagementまたはTracking Requirementが発生した場合でも、それだけを理由として新しいDatabase Field、Data Type、Controlled Value、Nullability、ValidationまたはRelationshipを生成してはならない。

Databaseへの変更が必要となる場合は、Database Rule、Database Schemaその他のApplicable Source of Truthに従って正式に判断する。

RepositoryとDatabaseの間にConflictが確認された場合、一方を自動的に正として他方を上書きしてはならない。

---

## 9.15 Metadata Compatibility Boundary

Metadata Representationの変更が必要となった場合も、既存Metadataの意味およびRelationを確認せずに自動変換してはならない。

Repository Ruleに正式定義されていないMetadata Field、Metadata File、Metadata DirectoryまたはMetadata SchemaをCompatibility処理の都合によって追加してはならない。

Metadata Relationを一意に判断できない場合は、推測によって補完せず、未確認状態として扱う。

---

## 9.16 Asset Compatibility

Repository StructureまたはAsset Management Relationが変更された場合、既存Assetの所属Case、Source、License、Caption、Visual Roleその他ApplicableなRelationを失ってはならない。

Repository Compatibilityを理由として、Image Rule、Art Bibleその他の専門Source of Truthが保持するAsset仕様を変更してはならない。

AssetのPlacement変更だけを理由として、新しいAsset Identityを生成してはならない。

一方、正式な根拠から同一Assetであることを確認できない場合、Filenameまたは外観の類似だけを理由として統合してはならない。

---

## 9.17 Cross-Case Compatibility

MigrationまたはRepository再構成によって、異なるCaseのArtifact Identityを混同してはならない。

同一Filename、同一Version番号、同一Source、同一Assetまたは類似Contentが存在することだけを理由として、異なるCaseのArtifactを統合してはならない。

正式なCross-Case Relationが存在する場合は、そのRelationを維持しながら各Case Identityを保持する。

Cross-Case Relationを一意に確認できない場合は、推測によって新しいRelationを生成しない。

---

## 9.18 Historical Traceability

CompatibilityおよびMigrationでは、現在のRepository状態だけではなく、必要なHistorical Traceabilityを維持する。

Applicableな範囲で、

- Case Identity
- Artifact Identity
- Version Relation
- Revision Relation
- Naming Relation
- Placement Relation
- Applicable Audit Result
- Applicable Final Flow Audit Result
- Human Approval Decision
- Repository Integration
- Publication History
- Asset Relation
- Dependency

を追跡可能な状態に維持する。

Historical Recordを保持することは、そのRecordがCurrentまたは現在Applicableであることを意味しない。

Historical PreservationとCurrent Applicabilityを混同してはならない。

---

## 9.19 Conflict and Ambiguity Handling

CompatibilityまたはMigration中にConflict、Missing Relation、AmbiguityまたはIntegrity Failureを検出した場合、削除、上書き、Renameまたは推測によって問題を不可視化してはならない。

Applicable Source of Truthおよび確認可能なTraceabilityから一意に解決できない場合は、未確認またはConflict状態として扱う。

AI AgentまたはAutomationは、正式な根拠が不足している状態を「最も可能性が高い」状態へ自動的に正規化してはならない。

Human Decisionが必要な事項については、Human Decisionを要求する。

---

## 9.20 Automation Boundary

Automationは、正式に定義されたCompatibility RuleおよびMigration Procedureの範囲内でのみ処理を実行する。

Automationは、以下を独自に判断してはならない。

- Artifact Identityの統合または分離
- Major / Minor / No Version Increment
- Current Version Selection
- Audit ResultのApplicable範囲
- Final Flow Audit ResultのApplicable範囲
- Human Approval Decisionの継承
- Repository Integrationの成立
- Publication Statusの変更
- 未定義Metadataの生成
- 未定義Database Fieldの生成
- 未定義Directoryの生成
- Historical Versionの削除

一意に判定できない場合、Automationは推測によって処理を継続せず、Applicable Source of Truthに従ってHuman Decisionを要求する。

---

## 9.21 HOLD Dependencies and Resolution Reflection

本章は、正式HOLD Ledgerに登録されたActive HOLDおよびRESOLVED Archiveとの責務境界を維持する。

HOLDの正式な状態はHOLD LedgerをSource of Truthとして確認する。

**HOLD-ARTIFACT-VERSION-01**
`HOLD-ARTIFACT-VERSION-01`は、正式HOLD Ledger上でRESOLVEDとして扱う。
Production ArtifactのVersion Increment Criteriaについては、
Chapter 5に反映された正式基準に従う。
CompatibilityおよびMigrationは、
Chapter 5に定義されたVersion CompatibilityおよびVersion Increment Criteriaを維持し、
Repository Structure Migration、Directory移動、Path変更、Metadata移行、
Compatibility対応またはMigration Implementationそのものを理由として、
Production ArtifactのVersionを自動的に増加させてはならない。
既存ArtifactのVersionを一意に確認できない場合、
AI Agent、AutomationまたはMigration Implementationは
Versionを推測、補完または再採番してはならず、
Applicable Source of Truthに従って必要な正式確認工程またはHuman Decisionを要求する。
`HOLD-ARTIFACT-VERSION-01`のResolutionによって、
Chapter 5に定義されていない新しいVersion Convention、
Filename Convention、Migration Version RuleまたはAutomation Ruleが
追加されたものとして扱ってはならない。
また、CompatibilityまたはMigration上の都合を理由として、
正式HOLD Ledger上でRESOLVEDとなった
`HOLD-ARTIFACT-VERSION-01`を再度ActiveまたはOpenとして扱ってはならない。

### HOLD-PUBLICATION-TRACKING-01

FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Trackingについては、
Chapter 3およびApplicable Source of Truthに従い、

cases/FILE-XXX/publication-tracking.json

をCase-level Repository-managed Operational Metadata Artifactとして使用する。

\`publication-tracking.json\`は、FREE Publication ArtifactおよびCLASSIFIED Publication Artifactについて、
それぞれ独立して、

- Applicability
- Production State
- Applicable Audit Reference

を管理する。

CompatibilityまたはMigrationは、
既存Case、既存Publication Artifact、Workflow Status、Publication Status、
Audit Result、Human Approval Decision、Repository Integration State、
Filename、Version、Timestampまたは単なるFile / Directoryの存在から、
これらのTracking Valueを推測してはならない。

既存Caseに\`publication-tracking.json\`が存在しないことだけを理由として、
当該CaseまたはPublication Artifactを
Workflow Failure、Audit BLOCKER、Human Approval HOLDまたは
その他の異常状態として扱ってはならない。

Applicable Audit Referenceは、
対象Publication ArtifactにApplicableなAudit Artifactへの
Repository-relative Referenceとして扱う。

Applicable Audit ReferenceのCompatibilityまたはMigrationでは、
Case、Artifact、Applicable VersionおよびApplicable Auditとの対応を確認する。

確認可能な正式情報およびApplicable Source of Truthから
Tracking ValueまたはApplicable Audit Referenceを一意に確定できない場合、
AI Agent、AutomationまたはMigration Implementationは
推測、補完または自動修復してはならず、
Applicableな正式確認工程またはHuman Decisionを要求する。

CompatibilityまたはMigrationを理由として、
新しいWorkflow Status、Publication Status、Database Field、
Production Layer、Metadata Directory、Audit Result、
Human Approval Decisionまたは未定義のTracking Mechanismを
独自に生成してはならない。

また、\`publication-tracking.json\`の仕様反映またはMigration Implementationが
完了したことだけを理由として、
\`HOLD-PUBLICATION-TRACKING-01\`をRESOLVEDとしてはならない。

当該HOLDの正式なStatusおよびResolutionは、
正式HOLD LedgerおよびApplicableなHOLD Management Procedureに従う。

CompatibilityまたはMigrationを理由として、FREE / CLASSIFIED個別State用の新しいWorkflow Status、Publication Status、Metadata Field、Database FieldまたはTracking Systemを独自に生成してはならない。

### HOLD-AUDIT-PLACEMENT-01

\`HOLD-AUDIT-PLACEMENT-01\`は正式HOLD Ledger上で解消済みとして扱う。

Case単位のAudit Artifact正式物理Repository Placementは、

cases/FILE-XXX/audit/

とする。

CompatibilityまたはMigrationは、この正式Placementを維持する。

ただし、このDecisionからAudit Filename Convention、Audit Artifact Versioning、Retention / Archive Placement、Subdirectory、追加Database / Metadata FieldまたはAutomation実装を派生させてはならない。

解消済みHOLDを本章からActive HOLDへ再Openしてはならない。

---

## 9.22 No Automatic Destructive Migration

CompatibilityまたはMigrationを理由として、既存の正式Artifact、Historical Version、Audit Record、Approval Record、Publication Historyその他のTraceabilityを自動削除してはならない。

新しい仕様に適合しないことだけを理由として、旧Artifactまたは旧Recordを不要と判断してはならない。

削除または不可逆な変換が正式に必要となる場合は、Applicable Source of Truthおよび必要なHuman Decisionに従う。

本章はRetention Period、Automatic Deletion ScheduleまたはArchive Policyを独自に定義しない。

---

## 9.23 Core Compatibility Principle

ProjectORIGIN RepositoryのCompatibilityおよびMigrationでは、

\*\*新しい正式仕様へ適合させることと、既存の正式なIdentity、Version、Decision、RelationおよびHistoryを維持することを両立する。\*\*

Compatibilityは、既存状態を無条件に新仕様へ書き換えることではない。

Migrationは、新しいVersion、Approval、IntegrationまたはPublicationを自動的に成立させる工程ではない。

Version判断はChapter 5の正式Criteriaに従う。

不明なRelationまたは状態を推測によって正常化しない。

既存のHistorical Traceabilityを破壊しない。

Active HOLDの未確定仕様をCompatibilityの都合によって暗黙に確定しない。

そして、確認可能なSource of TruthおよびTraceabilityから一意に判断できない事項については、Human Decisionを要求する。

--

**Version History**
v1.0
Date: 2026-08-30
Initial Release
**Contents**

- Established the official Repository Rule for ProjectORIGIN.

- Defined the repository structure and Case-centered artifact management principles.

- Defined Production Artifact placement, identification, naming, and version management boundaries.

- Defined Workflow Status and Publication Status repository responsibility boundaries.

- Defined Audit Artifact placement and repository-level audit relationships.

- Defined Repository Integration, integrity, and traceability requirements.

- Defined `publication-tracking.json` as the Case-level Repository-managed Operational Metadata Artifact for FREE and CLASSIFIED Publication Artifact tracking.

- Defined Applicability, Production State, and Applicable Audit Reference management boundaries.

- Defined compatibility and migration principles for existing Cases and Artifacts.

- Defined AI Agent and Automation responsibility boundaries under the No-Assumption Principle.

- Established HOLD compatibility boundaries for unresolved and resolved repository-related specifications.
