# ProjectORIGIN HOLD管理台帳
## Version
v1.0
---
# 1. Purpose / Authority
本台帳は、ProjectORIGINにおいて正式仕様を一意に確定できない事項、依存関係の解消を必要とする事項、および正式な解消確認が完了していない事項を追跡するための正式管理台帳である。
HOLDは、未確認事項を推測によって補完することを防止し、正式なSource of Truth、Human Decision、必要なSchema反映、および監査結果に基づいて安全に解消するために使用する。
本台帳に登録されたActive HOLD / Pendingは、正式な解消条件を満たすまで未解決として扱う。
HOLDが解消された場合も記録を削除せず、RESOLVED Archiveへ保持する。
---
# 2. Ledger Rules
HOLD管理では、以下を原則とする。
- 正式Source of Truthから一意に確定できない仕様を推測によって補完しない。
- 存在を確認できないHOLD IDを推測によって発行しない。
- 未確認の仕様を暫定値として正式仕様へ昇格させない。
- Active HOLD / Pendingは、正式な解消条件を満たすまで維持する。
- HOLDの解消には、必要な仕様の確認または正式確定を必要とする。
- 必要な場合、Human Decisionによって未確定仕様を正式確定する。
- 解消にSchemaその他の正式文書への反映が必要な場合、その反映完了を確認する。
- HOLD解消前に、依存関係を確認する。
- HOLD解消前に、必要な最終再監査を実施する。
- 最終再監査がPASSするまで、HOLDをRESOLVEDとして扱わない。
- HOLD解消後も記録を削除しない。
- 解消済みHOLDはRESOLVED Archiveへ保持する。
- 別論点として登録されたHOLDを、一方の解消だけを理由として自動的に解消しない。
- 新しい正式仕様、Controlled Value、Data Type、Unset Value、依存関係その他の仕様を、HOLD管理上の都合だけを理由として生成しない。
- 過去の記憶のみを根拠としてHOLDを一括復元しない。
- 候補を発見しただけではActive HOLD / Pendingへ正式登録しない。
- 現在も未解決であることを証拠ベースで確認したものだけを正式登録する。
---
# 3. Ledger Structure
本台帳は、以下の4領域で管理する。
## A. Active HOLD / Pending
現在も未解決であり、正式に追跡する必要があるHOLDを保持する。
## B. Resolution Review
解消候補となったHOLDについて、解消条件、解消根拠、反映先、依存関係および最終監査結果を確認する領域。
調査または修正作業が終了したことだけを理由として、HOLDをRESOLVEDとして扱わない。
## C. RESOLVED Archive
正式な解消条件を満たし、必要な反映および最終再監査を完了したHOLDを履歴として保持する。
解消後も記録を削除しない。
## D. Recovery Log
過去の記録その他からHOLD候補を発見した場合に、その確認状況を管理する。
候補を発見しただけではActive HOLD / Pendingへ登録しない。
現在も未解決であること、正式ID、正式Recordその他の必要事項を証拠ベースで確認した後に正式登録を判定する。
---
# 4. Active HOLD / Pending

## HOLD-AUDIT-PLACEMENT-01 — Audit Artifact Repository Placement

### Status

HOLD

### 発生元

- ProjectORIGIN Repository Rule v1.0
- Repository Structure設計
- Audit Artifact Repository Placement検討

### 対象

Audit Artifactの正式な物理Repository Placement。

### 発生理由

ProjectORIGINではAudit LayerおよびAudit Artifactの論理的責務は確認されているが、Audit ArtifactをRepository上のどの物理Directoryへ正式配置するかについて、現時点で確定したSource of Truthを確認できない。

Audit Artifactの存在または論理的なAudit Layerを根拠として、未定義の物理Directoryを推測によって新設すると、Repository Structure、Traceability、Naming、Automationおよび将来のCompatibilityへ影響する可能性がある。

このため、Audit Artifactの物理Repository Placementを未確定事項として正式に追跡する。

### 確認済み事項

- AuditはProjectORIGIN Production Flowにおける正式工程である。
- Audit Artifactには対象ArtifactとのTraceabilityが必要である。
- 論理的なAudit Layerの存在だけでは、物理Directoryの存在を意味しない。
- Production ArtifactのRepository LayerとAudit ArtifactのRepository Placementは同一概念ではない。
- Audit ArtifactのNamingは、物理Placementとの関係を確認せずに正式化すべきではない。
- Repository RuleではAudit Artifactの物理Placementを推測によって確定しない方針が採用されている。

### 未確認事項

- Audit ArtifactをCase Directory配下へ保存するか
- Artifact TypeごとのDirectoryへ保存するか
- Case共通のAudit Directoryを設けるか
- Repository全体のAudit領域を設けるか
- Audit Artifact Filename Convention
- Audit Artifact Versioning
- Audit Artifact Retention / Archive Policy
- Production Artifactとの物理的Relationship
- AutomationがAudit Artifactを参照する際の正式Path

### 依存関係

- Repository Rule
- Audit Rule
- AGENTS.md
- Artifact Naming and Versioning
- Repository Integration
- Traceability
- Automation
- 必要に応じてDatabase / Operational Metadata

### 禁止事項

本HOLDがHOLD状態である間、以下を行ってはならない。

- Audit Artifactの物理Directoryを推測によって正式仕様として追加する
- 論理的なAudit Layerを物理Directoryと同一視する
- `audit/`その他のDirectory名を根拠なく正式化する
- Audit Artifact NamingをPlacement確認なしに正式化する
- 既存Source of Truthに存在しないAudit PathをAutomation前提として固定する

### 次のAction

1. Audit RuleおよびAGENTS.mdからAudit ArtifactのRepository要件を抽出する。
2. Repository RuleのCase Directory Structureとの整合を確認する。
3. Audit Artifactと対象Production ArtifactのTraceability要件を確認する。
4. 必要な物理Placement候補を比較する。
5. Automation、Naming、VersioningおよびCompatibilityへの影響を確認する。
6. 必要なHuman Decisionを行う。
7. 決定内容をApplicable Source of Truthへ正式反映する。
8. 関連Chapterを再監査する。

### 解消条件

以下をすべて満たすまで、本HOLDをHOLD状態として維持する。

- Audit Artifactの正式な物理Repository Placementが決定されている
- 対象ArtifactとのTraceabilityが維持されている
- Namingとの関係が確認されている
- Versioningとの関係が確認されている
- Repository Integrationへの影響が確認されている
- Automationへの影響が確認されている
- Existing Repository StructureへのCompatibility Impactが確認されている
- 必要なHuman Decisionが完了している
- Applicable Source of Truthへ正式反映されている
- 関連文書の再監査がPASSしている

### 解消根拠

未確定。

HOLD状態では解消根拠を作成しない。

### 反映先

解消時には少なくとも以下への影響を確認する。

- ProjectORIGIN Repository Rule
- Audit Rule
- AGENTS.md
- Artifact Naming and Versioning
- Repository Integration関連仕様
- Automation関連仕様

### 最終監査結果

PENDING

本HOLD解消後に最終監査結果を記録する。

---
## HOLD-ARTIFACT-VERSION-01 — Production Artifact Version Increment Criteria

### Status

HOLD

### 発生元

- ProjectORIGIN Repository Rule v1.0 Chapter 5
- Production Artifact Naming and Versioning設計

### 対象

Production Artifact Version Increment Criteria。

### 発生理由

Production ArtifactのFilename Identityとして`vX.Y`を使用する方針は確定しているが、`X`および`Y`をどの条件で増加させるかについて正式なProduction Artifact用ルールが確定していない。

公式Documentに存在するVersion Management RuleをProduction Artifactへ自動転用すると、Document VersionとArtifact Versionの責務を混同する可能性がある。

このためProduction Artifact固有のVersion Increment Criteriaを正式な未確定事項として追跡する。

### 確認済み事項

- Production ArtifactはVersionを識別可能である必要がある。
- 基本Version表記として`vX.Y`を使用する。
- Artifact VersionとWorkflow Statusは異なる概念である。
- Artifact VersionとPublication Statusは異なる概念である。
- FilenameをRenameしただけでは正式なVersion Updateは成立しない。
- Version更新によって必要なTraceabilityを失ってはならない。
- 公式DocumentのVersion RuleをProduction Artifactへ自動転用してはならない。

### 未確認事項

- `X`を増加させる具体的条件
- `Y`を増加させる具体的条件
- Patch ComponentをProduction Artifactへ導入するか
- Audit CorrectionとVersion Incrementの関係
- Content RevisionとVersion Incrementの関係
- Publication RevisionとVersion Incrementの関係
- Human Approval後の修正とVersion Incrementの関係
- Repository Integration後の修正とVersion Incrementの関係
- Current Versionの正式判定方法
- 旧VersionのRetention / Archiveとの関係

### 依存関係

- Repository Rule Chapter 5
- Repository Rule Chapter 6
- AGENTS.md
- Audit Rule
- Research Production
- Master Production
- Publication Production
- Repository Integration
- Compatibility
- Automation

### 禁止事項

本HOLDがHOLD状態である間、以下を行ってはならない。

- Semantic Versioningその他の一般慣行をProduction Artifactへ自動適用する
- Document Version RuleをProduction Artifactへ自動転用する
- `X`または`Y`のIncrement Criteriaを推測で確定する
- Patch Componentを根拠なく追加する
- Status変更だけをVersion Incrementの根拠とする
- Filename変更だけで正式Version Updateが成立したものと扱う

### 次のAction

1. Production Artifactで実際に発生するRevision Typeを整理する。
2. Audit Correction、Content Revision、Publication Revisionを分類する。
3. Human ApprovalおよびRepository Integrationとの関係を確認する。
4. `X` / `Y` Increment Criteria候補を設計する。
5. Patch Componentの必要性を判断する。
6. Existing ArtifactへのCompatibility Impactを確認する。
7. 必要なHuman Decisionを行う。
8. Repository Rule Chapter 5その他のApplicable Source of Truthへ正式反映する。
9. 関連文書を再監査する。

### 解消条件

以下をすべて満たすまで、本HOLDをHOLD状態として維持する。

- Production Artifact Versionの変更単位が正式に決定されている
- `X`のIncrement Criteriaが正式に決定されている
- `Y`のIncrement Criteriaが正式に決定されている
- Patch Componentを使用するか正式に決定されている
- Audit Correctionとの関係が決定されている
- Content Revisionとの関係が決定されている
- Publication Revisionとの関係が決定されている
- Human ApprovalおよびRepository Integrationとの関係が確認されている
- Existing ArtifactへのCompatibility Impactが確認されている
- 必要なHuman Decisionが完了している
- Applicable Source of Truthへ正式反映されている
- 関連文書の再監査がPASSしている

### 解消根拠

未確定。

HOLD状態では解消根拠を作成しない。

### 反映先

解消時には少なくとも以下への影響を確認する。

- ProjectORIGIN Repository Rule Chapter 5
- ProjectORIGIN Repository Rule Chapter 6
- AGENTS.md
- Audit Rule
- Production Artifact関連仕様
- Repository Integration関連仕様
- Automation関連仕様

### 最終監査結果

PENDING

本HOLD解消後に最終監査結果を記録する。

---
## HOLD-PUBLICATION-TRACKING-01 — FREE / CLASSIFIED Artifact-level Tracking

### Status

HOLD

### 発生元

- ProjectORIGIN Repository Rule v1.0 Chapter 6
- FREE / CLASSIFIED Publication Production設計

### 対象

FREE Publication ArtifactおよびCLASSIFIED Publication ArtifactのArtifact-level Production / Audit State Tracking。

### 発生理由

FREE Publication ArtifactとCLASSIFIED Publication Artifactは独立したArtifact IdentityおよびAudit工程を持つ。

一方、Case-level Workflow StatusではPublication Phaseを`PUBLICATION_PRODUCTION`および`PUBLICATION_AUDIT`として管理する設計が採用されている。

このため、FREEとCLASSIFIEDが異なるProductionまたはAudit進行状態にある場合、Case-level Workflow Status一値だけでは各Artifactの個別状態を完全には表現できない。

Artifact-level Trackingを正式に必要とするか、その場合どこをSource of Truthとするかが未確定であるため、本HOLDとして追跡する。

### 確認済み事項

- FREEとCLASSIFIEDは異なるPublication Artifact Identityを持つ。
- FREEとCLASSIFIEDは独立したProduction / Audit対象になり得る。
- Case-level Workflow StatusではFREE / CLASSIFIED別のStatus Tokenを採用しない。
- Case-level Publication Phaseは`PUBLICATION_PRODUCTION`および`PUBLICATION_AUDIT`で表す。
- Case-level Workflow StatusとArtifact-level Stateは同一概念ではない。
- Publication Statusは公開済みかどうかを表す独立概念である。

### 未確認事項

- FREE個別Production Stateを保持する必要があるか
- CLASSIFIED個別Production Stateを保持する必要があるか
- FREE個別Audit Stateを保持する必要があるか
- CLASSIFIED個別Audit Stateを保持する必要があるか
- Artifact-level StateのSource of Truth
- Database Fieldとして保持するか
- Repository Metadataとして保持するか
- Audit Artifactから導出するか
- 一方のみ完了した場合のCase-level Workflow Status
- Repository Integrationとの関係
- Automationとの関係
- Publication Statusとの関係

### 依存関係

- Repository Rule Chapter 4
- Repository Rule Chapter 5
- Repository Rule Chapter 6
- AGENTS.md
- Audit Rule
- FREE Production
- CLASSIFIED Production
- Database / Operational Metadata
- Repository Integration
- Automation

### 禁止事項

本HOLDがHOLD状態である間、以下を行ってはならない。

- FREE / CLASSIFIED用のArtifact-level Status体系を推測で新設する
- Case-level Workflow StatusをArtifact-level Stateと同一視する
- FREEとCLASSIFIEDの一方の状態から他方の状態を推測する
- `PUBLICATION_PRODUCTION`または`PUBLICATION_AUDIT`だけを根拠として両Artifactが同一進行状態にあると判断する
- 未定義のDatabase FieldまたはMetadataを正式仕様として追加する

### 次のAction

1. FREE / CLASSIFIEDの実Production Flowを確認する。
2. 各Artifactの個別状態を追跡するOperational Needを確認する。
3. Case-level Workflow Statusだけで管理可能か検証する。
4. Artifact-level Trackingが必要な場合、Source of Truth候補を比較する。
5. Database、Repository Metadata、Audit Resultとの関係を確認する。
6. AutomationおよびRepository Integrationへの影響を確認する。
7. 必要なHuman Decisionを行う。
8. Applicable Source of Truthへ正式反映する。
9. 関連文書を再監査する。

### 解消条件

以下をすべて満たすまで、本HOLDをHOLD状態として維持する。

- Artifact-level Trackingの必要性が正式に決定されている
- 必要な場合、管理対象となるStateが決定されている
- Source of Truthが決定されている
- Case-level Workflow Statusとの関係が決定されている
- Publication Statusとの関係が決定されている
- Audit Resultとの関係が決定されている
- Repository Integrationへの影響が確認されている
- Automationへの影響が確認されている
- Database / Metadataへの影響が確認されている
- Existing CaseへのCompatibility Impactが確認されている
- 必要なHuman Decisionが完了している
- Applicable Source of Truthへ正式反映されている
- 関連文書の再監査がPASSしている

### 解消根拠

未確定。

HOLD状態では解消根拠を作成しない。

### 反映先

解消時には少なくとも以下への影響を確認する。

- ProjectORIGIN Repository Rule Chapter 6
- AGENTS.md
- Audit Rule
- Database Schema / Database Rule
- Repository Integration関連仕様
- Automation関連仕様

### 最終監査結果

PENDING

本HOLD解消後に最終監査結果を記録する。

---
## HOLD-PUBLICATION-STATUS-COMPAT-01 — Publication Status Cross-Document Compatibility

### Status

HOLD

### 発生元

- ProjectORIGIN Repository Rule v1.0 Chapter 6
- Audit Rule
- Publication Status横断Compatibility監査

### 対象

Repository Ruleで定義するPublication Statusと、Audit Ruleに存在する既存Publication Status定義との責務およびControlled Value Compatibility。

### 発生理由

Repository Rule Chapter 6では、Publication状態をProduction Workflowから分離し、Publication Statusとして以下の2値を使用する設計が採用されている。

- `NOT_PUBLISHED`
- `PUBLISHED`

一方、現行Audit RuleにはPublication Statusとして、Production、Audit、ApprovalおよびPublication進行を含む複数の既存状態値が存在する。

同名の状態概念について異なる責務およびControlled Valueが存在するため、どちらか一方を暗黙に優先または無効化するとSource of Truth Conflictが発生する。

このため、両仕様の正式な責務整理およびCompatibility解消を本HOLDとして追跡する。

### 確認済み事項

- Repository RuleはWorkflow StatusとPublication Statusを分離する設計を採用している。
- Repository Rule Chapter 6では`NOT_PUBLISHED`および`PUBLISHED`をPublication Statusとして定義している。
- `APPROVED`と`PUBLISHED`は同一概念ではない。
- AGENTS.mdではProduction完了とPublication済みを混同しない。
- Audit RuleにはRepository Rule Chapter 6とは異なるPublication Status状態値が存在する。
- Audit Rule側の既存状態値にはProduction、AuditまたはApproval進行を示す意味が含まれている。
- Repository Ruleだけを根拠としてAudit Ruleの既存定義を無効化してはならない。
- Audit Ruleだけを根拠としてRepository Rule Chapter 6の2値モデルを暗黙に変更してはならない。

### 未確認事項

- Audit Rule側の既存Publication Status各値の最終的な責務分類
- Workflow Statusへ再分類すべき値
- Audit Resultへ再分類すべき値
- Human Approval Decisionへ再分類すべき値
- Publication Statusとして残すべき値
- `NOT_PUBLISHED / PUBLISHED`の2値モデルを最終確定するか
- Audit Rule改訂の必要性
- Databaseへの影響
- Existing CaseへのMigration Impact
- Automationへの影響
- Operational Metadataへの影響

### 依存関係

- Repository Rule Chapter 6
- Audit Rule
- AGENTS.md
- Database Schema
- Database Rule
- Human Approval
- Repository Integration
- Publication Flow
- Automation
- Compatibility

### 禁止事項

本HOLDがHOLD状態である間、以下を行ってはならない。

- Repository Rule側のPublication StatusがAudit Rule側を自動的に置換したものと扱う
- Audit Rule側のPublication StatusがRepository Rule側を自動的に置換したものと扱う
- 両方のControlled Valueを一つのFieldへ無整理で混在させる
- 同名Statusの意味をContextだけで推測する
- Audit Ruleの既存状態値を正式Decisionなしに削除または再分類する
- Repository Rule Chapter 6の2値モデルを正式Decisionなしに変更する

### 次のAction

1. Audit Ruleの既存Publication Status各値を責務別に分析する。
2. Workflow Status、Audit Result、Human Approval Decision、Publication Statusへ分類候補を整理する。
3. AGENTS.mdのProduction / Approval / Publication Flowとの整合を確認する。
4. DatabaseおよびOperational Metadataへの影響を確認する。
5. Existing CaseおよびAutomationへのCompatibility Impactを確認する。
6. `NOT_PUBLISHED / PUBLISHED`の2値モデルを維持するかHuman Decisionを行う。
7. Audit Rule側の正式改訂が必要か判断する。
8. 必要なSource of Truthを正式更新する。
9. Repository Rule Chapter 6との横断再監査を行う。

### 解消条件

以下をすべて満たすまで、本HOLDをHOLD状態として維持する。

- Repository Rule側Publication Statusの責務が正式確認されている
- Audit Rule側既存Publication Statusの責務が正式確認されている
- 各既存状態値の正式なDispositionが決定されている
- `NOT_PUBLISHED / PUBLISHED`を維持するか正式決定されている
- 必要なAudit Rule改訂の有無が決定されている
- 必要なDatabase / Metadata変更の有無が決定されている
- Existing CaseへのCompatibility Impactが確認されている
- Automationへの影響が確認されている
- 必要なHuman Decisionが完了している
- Applicable Source of Truthへの必要な変更が正式反映されている
- Repository Rule Chapter 6との横断再監査がPASSしている

### 解消根拠

未確定。

HOLD状態では解消根拠を作成しない。

### 反映先

解消時には少なくとも以下への影響を確認する。

- ProjectORIGIN Repository Rule Chapter 6
- Audit Rule
- AGENTS.md
- Database Schema
- Database Rule
- Repository Integration関連仕様
- Publication関連仕様
- Automation関連仕様

### 最終監査結果

PENDING

本HOLD解消後に最終監査結果を記録する。

---

**Active HOLD / Pending Count: 4**

---

---
# 5. Resolution Review
現在登録なし。
**Resolution Review Count: 0**
---
# 6. RESOLVED Archive
## HOLD-TAGS-01 — Tags Controlled Values / 正式Tag一覧
### Status
RESOLVED
### 発生元
Database Schema Chapter 6 / Tags Field Definition
### 対象
`tags`に保持できる具体的な正式Tag Controlled Values一覧。
### 発生理由
`tags`はProjectORIGINの正式なClassification Fieldとして確認されていた。
HOLD登録時点では、Tagsの基本責務、Data Type、Required / Optional、Tag Controlled ValuesのSingle Source of Truth、「有効なTag」の判定条件、代表タグ判定、Default Value、Unset Value、重複Tagの扱い、および主要Constraintsは確定していた。
一方、`tags`に保持できる具体的な正式Tag Controlled Values一覧については、一意に確定できていなかった。
既存の正式事件データから初期Tag Controlled Valuesを抽出できる十分な正式データ母集団も確認できていなかった。
そのため、未確認データまたは推測によってTag Controlled Valuesを生成せず、Human Decisionによる正式確定までHOLDとして保持した。
### 確認済み事項
Human DecisionおよびDatabase Schema Chapter 6 / Tags Field Definitionへの正式反映により、以下を確定した。
- `tags`はProjectORIGINの正式なClassification Fieldである。
- `tags`は、Category、Classその他の正式Classification Fieldだけでは表現しきれない事件または事例の特徴について、検索、絞り込みおよび事件横断の関連付けに使用する補助的なClassification情報を保持する。
- Data Typeは`array<string>`とする。
- `tags`フィールド自体は正式な事件データで必須とする。
- Tagsは順序付き一覧として管理する。
- Tag Controlled ValuesのSingle Source of Truthは、Database Schema Chapter 6 / Tags Field Definition / Allowed Valueとする。
- 未承認Tagを正式Tagとして使用しない。
- AI、Database層、Application層その他の処理が、未承認Tagを自動生成、補完または正式Controlled Valueへ追加してはならない。
- 同一Tagを同一`tags`配列内へ重複して保持しない。
- 正式なUnset Valueは`[]`とする。
- `null`、空文字または`tags`フィールド自体の欠落を正式なUnset Valueとして使用しない。
- 代表タグは、`tags`を先頭から確認した最初の有効なTagから取得する。
- 代表タグを別Fieldへ重複保存しない。
- Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldと同じ意味をTagとして重複管理しない。
具体的な初期Tag Controlled Valuesは、以下の11値とする。
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
上記11値を初期Tag Controlled Valuesとする。
Tag Controlled Valuesは、正式なHuman Decisionを経ることによって将来拡張可能とする。
### 未確認事項
なし。
`HOLD-TAGS-01`が対象としていた具体的な正式Tag Controlled Values一覧について、未確認事項は残っていない。
### 依存関係
Database Schema Chapter 6 / Tags Field Definitionへの正式反映に依存した。
TagsのPurposeおよびConstraintsとの整合性確認に依存した。
Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldとの責務分離確認に依存した。
「有効なTag」の判定条件、代表タグ判定および重複Tag禁止を含む既存Constraintsとの整合性確認に依存した。
Tags Field Definition反映後の最終再監査に依存した。
これらの依存事項は確認済み。
### 禁止事項
- Allowed Valueに登録されていないTagを正式Tagとして使用してはならない。
- AI、Database層、Application層その他の処理が未承認Tagを独自生成、補完または正式Controlled Valueへ自動追加してはならない。
- Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldと同じ意味をTagとして重複管理してはならない。
- 1事件だけにしか意味を持たない固有表現を、原則として正式Tag Controlled Valueへ追加してはならない。
- 同一Tagを同一`tags`配列内へ複数回保持してはならない。
- Tagの重複によって優先度または重要度を表してはならない。
- `null`、空文字またはField欠落をTagsの正式なUnset Valueとして使用してはならない。
- Tagの付与のみを根拠として、記録、痕跡、検出情報その他の真正性、信頼性、証拠能力、原因、起源、因果関係または事件に関する主張の真実性を認定してはならない。
- 新しいTag Controlled Valueを正式なHuman Decisionなしに追加してはならない。
### 次のAction
なし。
`HOLD-TAGS-01`の解消条件は満たされている。
本項目はActive HOLD / Pendingとして追跡せず、RESOLVED履歴として保持する。
### 解消条件
以下の条件をすべて満たしたことを確認した。
1. 具体的な正式Tag Controlled Values一覧を正式に確定する。
2. 確定したTag Controlled Values一覧が、Tagsの正式なPurposeおよびConstraintsと整合していることを確認する。
3. Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldとの責務重複がないことを確認する。
4. 確定したTag Controlled Values一覧をDatabase Schema Chapter 6 / Tags Field Definition / Allowed Valueへ正式反映する。
5. 「有効なTag」の判定条件および代表タグ判定との整合性を確認する。
6. 重複Tag禁止を含む既存Constraintsとの整合性を確認する。
7. Tags Field Definition全体を再監査し、本HOLDに関する矛盾または未解決の依存関係が残っていないことを確認する。
8. 最終再監査がPASSする。
**上記8条件：すべて達成済み。**
### 解消根拠
Human Decisionにより、具体的な初期Tag Controlled Valuesを正式確定した。
Database Schema Chapter 6 / Tags Field Definition / Allowed Valueへ、11個の初期Tag Controlled Valuesを正式反映した。
反映後、Tags Field Definition全体について最終再監査を実施した。
Field Definition Standardへの適合、既存Classification Fieldおよび専用Fieldとの責務分離、「有効なTag」の判定条件、代表タグ判定、重複Tag禁止、Default Value、Unset Valueおよび主要Constraintsとの整合性を確認した。
### 反映先
Database Schema Chapter 6 / Tags Field Definition / Allowed Value
同Field DefinitionのPurpose、Required / Optional、Default Value、Unset Value、Constraints、Audit StatusおよびCurrent Audit Resultとの整合性を確認した。
### 最終監査結果
PASS
`Field Name` — PASS
`Purpose` — PASS
`Data Type` — PASS
`Required / Optional` — PASS
`Allowed Value` — PASS
`Default Value` — PASS
`Unset Value` — PASS
`Constraints` — PASS
**Field Definition Structure: PASS**
**解消条件: PASS**
**解消根拠: PASS**
**反映先: PASS**
**依存関係: PASS**
**最終再監査: PASS**
新規REVISION：0
新規HOLD：0
BLOCKER：0
### Resolution
**HOLD-TAGS-01 — RESOLVED**
本項目をActive HOLD / Pendingとして扱わない。
解消後も記録を削除せず、RESOLVED履歴として保持する。
---
## HOLD-STATUS-01 — Status Meaning / Data Type / Controlled Values / Nullability
### Status
RESOLVED
### 発生元
Database Schema Chapter 6 / Status Field Definition
### 対象
`status`が表す正式な分類責務、Data Type、Controlled Values、Unset Value、Nullability、およびStatus値の未設定を許可するLifecycle条件。
### 発生理由
`Status`はProjectORIGINの正式なClassification Fieldとして確認できていた。
一方、HOLD登録時点では、現行の正式Source of Truthから以下を一意に確定できていなかった。
- `status`が具体的に何の状態を表すのか
- 正式なData Type
- 正式なControlled Values
- 正式なUnset Value
- Nullability
- Status値の未設定を許可するLifecycle条件
- Workflow StatusおよびPublication Statusとの正式な責務境界
これらを推測によって確定すると、正式Source of Truthに存在しないStatus仕様を新たに作成することになるため、HOLDとして保持した。
### 確認済み事項
Human DecisionおよびDatabase Schema Chapter 6への正式反映により、以下を確定した。
- `status`は、事件そのものの解決状態を表す正式なClassification Fieldとする。
- `status`をWorkflow Statusとして使用しない。
- `status`をPublication Statusとして使用しない。
- Data Typeは`string | null`とする。
- 正式なControlled Valuesは以下の4値とする。
 - `Unresolved`
 - `Partially Resolved`
 - `Resolved`
 - `Undetermined`
- 正式なUnset Valueは`null`とする。
- `null`はStatusのControlled Valueとして扱わない。
- `null`と`Undetermined`は異なる状態として扱う。
- 調査中または移行中の事件データでは、Status分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。
- 正式公開データでは`null`を許容しない。
- 正式公開データでは、4つのControlled Valueのいずれかを必ず保持する。
### 未確認事項
なし。
`HOLD-STATUS-01`の解消対象としていたStatus Field Definitionの中核仕様について、未確認事項は残っていない。
### 依存関係
Database Schema Chapter 6 / Status Field Definitionへの正式反映に依存した。
Field Definition Standardへの適合確認に依存した。
Workflow StatusおよびPublication Statusとの責務分離確認に依存した。
Status Field Definition反映後の最終再監査に依存した。
これらの依存事項は確認済み。
### 禁止事項
- `status`をWorkflow Statusとして使用してはならない。
- `status`をPublication Statusとして使用してはならない。
- Workflow Status、Publication Statusその他のStatus体系の値を`status`へ流用してはならない。
- `Unresolved`、`Partially Resolved`、`Resolved`、`Undetermined`以外の値を正式なStatus値として使用してはならない。
- 正式に定義されていない自由入力値を、新しい正式Status値として使用してはならない。
- 数値コードまたはbooleanを正式なStatus値として使用してはならない。
- `null`をStatusのControlled Valueとして扱ってはならない。
- `null`と`Undetermined`を同一の状態として扱ってはならない。
- 正式公開データで`null`を使用してはならない。
- Status値を推測によって補完してはならない。
### 次のAction
なし。
`HOLD-STATUS-01`の解消条件は満たされている。
本項目はActive HOLD / Pendingとして追跡せず、RESOLVED履歴として保持する。
### 解消条件
以下の条件をすべて満たしたことを確認した。
1. `status`の正式な分類責務を確定する。
2. 正式なData Typeを確定する。
3. 正式なControlled Valuesを確定する。
4. 正式なUnset Valueを確定する。
5. Nullabilityを確定する。
6. Lifecycle別のUnset許可条件を確定する。
7. Workflow Statusとの責務境界を確定する。
8. Publication Statusとの責務境界を確定する。
9. 確定した仕様をDatabase Schema Chapter 6 / Status Field Definitionへ反映する。
10. Field Definition Standardへの適合を確認する。
11. Status Field Definitionを再監査し、本HOLDに関する矛盾または未解決事項が残っていないことを確認する。
**上記11条件：すべて達成済み。**
### 解消根拠
Human Decisionにより、`status`の正式仕様を確定した。
Database Schema Chapter 6 / Status Field Definitionへ正式仕様を反映した。
反映後、Status Field Definitionについて最終再監査を実施し、Field Definition Standardの全項目がPASSした。
### 反映先
Database Schema Chapter 6 / Status Field Definition
### 最終監査結果
PASS
`Field Name` — PASS
`Purpose` — PASS
`Data Type` — PASS
`Required / Optional` — PASS
`Allowed Value` — PASS
`Default Value` — PASS
`Unset Value` — PASS
`Constraints` — PASS
**Field Definition Structure: PASS**
**解消条件: PASS**
**解消根拠: PASS**
**反映先: PASS**
**依存関係: PASS**
**最終再監査: PASS**
新規REVISION：0
新規HOLD：0
BLOCKER：0
### Resolution
**HOLD-STATUS-01 — RESOLVED**
本項目をActive HOLD / Pendingとして扱わない。
解消後も記録を削除せず、RESOLVED履歴として保持する。
---
## HOLD-CLASS-02 — Class Data Type / Nullability / Lifecycle
### Status
RESOLVED
### 発生元
Database Schema Chapter 6 / Class Field Definition
### 対象
`class`のData Type、Nullability、正式なUnset Value、およびLifecycle別のUnset Value許可条件。
### 発生理由
`Class`はProjectORIGINの正式なClassification Fieldとして確認できていた。
一方、HOLD登録時点では、現行の正式Source of Truthから`class`の正式なData Type、Unset ValueおよびLifecycle別のNullability条件を一意に確定できていなかった。
これらを推測によって確定すると、正式Source of Truthに存在しないClass仕様を新たに作成することになるため、HOLDとして保持した。
### 確認済み事項
Human DecisionおよびDatabase Schema Chapter 6への正式反映により、以下を確定した。
- `Class`はProjectORIGINの正式なClassification Fieldである。
- `class`は単一のClass値を保持する。
- Class値が設定されている場合のNon-null Data Typeは`string`とする。
- `class`の正式なData Typeは`string | null`とする。
- 正式なUnset Valueは`null`とする。
- `null`はClassのControlled Valueとして扱わない。
- `class`フィールド自体の欠落と`class: null`は異なる状態として扱う。
- `class`フィールド自体は、正式な事件データで保持する。
- 調査中または移行中の事件データでは、Class分類がまだ正式に設定されていない場合に限り、一時的に`null`を許容する。
- 正式公開データでは`null`を許容しない。
- 正式公開データでは、正式なClass Controlled Valueのいずれかを必ず保持する。
### 未確認事項
なし。
`HOLD-CLASS-02`の解消対象としていたData Type、Nullability、Unset ValueおよびLifecycle条件について、未確認事項は残っていない。
### 依存関係
Database Schema Chapter 6 / Class Field Definitionへの正式反映に依存した。
ClassのData Type、Unset Value、NullabilityおよびLifecycle条件の正式確定に依存した。
Class Field Definition反映後の最終再監査に依存した。
これらの依存事項は確認済み。
### 禁止事項
- `class`に複数のClass値を保持してはならない。
- 非`null`のClass値に`string`以外のData Typeを使用してはならない。
- `null`をClassのControlled Valueとして扱ってはならない。
- 空文字、`"Unknown"`、`"Unclassified"`、`"N/A"`その他の疑似Class値を、正式なUnset Valueとして使用してはならない。
- `class`フィールド自体の欠落と`class: null`を同一の状態として扱ってはならない。
- 正式公開データで`null`を使用してはならない。
### 次のAction
なし。
`HOLD-CLASS-02`の解消条件は満たされている。
本項目はActive HOLD / Pendingとして追跡せず、RESOLVED履歴として保持する。
### 解消条件
以下の条件をすべて満たしたことを確認した。
1. `class`の正式なData Typeを一意に決定する。
2. Classの正式なUnset Valueを一意に決定する。
3. ClassのNullability条件を正式に確定する。
4. Lifecycle別条件を正式に確定する。
5. 確定した仕様をDatabase Schema Chapter 6 / Class Field Definitionへ反映する。
6. Class Field Definition全体を再監査する。
**上記6条件：すべて達成済み。**
### 解消根拠
Human Decisionにより、ClassのData Type、Unset Value、NullabilityおよびLifecycle条件を正式確定した。
Database Schema Chapter 6 / Class Field Definitionへ正式反映し、反映後の最終再監査を実施した。
### 反映先
Database Schema Chapter 6 / Class Field Definition
### 最終監査結果
PASS
`Field Name` — PASS
`Purpose` — PASS
`Data Type` — PASS
`Required / Optional` — PASS
`Allowed Value` — PASS
`Default Value` — PASS
`Unset Value` — PASS
`Constraints` — PASS
**Field Definition Structure: PASS**
**HOLD-CLASS-02 解消条件: PASS**
**解消根拠: PASS**
**反映先: PASS**
**依存関係: PASS**
**最終再監査: PASS**
新規REVISION：0
新規HOLD：0
BLOCKER：0
### Resolution
**HOLD-CLASS-02 — RESOLVED**
本項目をActive HOLD / Pendingとして扱わない。
解消後も記録を削除せず、RESOLVED履歴として保持する。
---
## HOLD-CLASS-01 — Class Controlled Values / Category依存関係
### Status
RESOLVED
### 発生元
Database Schema Chapter 6 / Class Field Definition
### 対象
`class`の正式なControlled Values、Class Controlled Valuesの正式管理元、およびCategoryとClassの正式な依存関係。
### 発生理由
`Class`はProjectORIGINの正式なClassification Fieldとして確認できていた。
一方、HOLD登録時点では、正式Class Controlled Values、正式管理元、およびCategoryとClassの関係を一意に確定できていなかった。
これらを推測によって確定すると、正式Source of Truthに存在しないClass値、階層関係またはAllowed Value制約を新たに作成することになるため、HOLDとして保持した。
### 確認済み事項
Human DecisionおよびDatabase Schema Chapter 6への正式反映により、以下を確定した。
- `Class`はProjectORIGINの正式なClassification Fieldである。
- Classは、事件または現象の性質および中心となる現象タイプを表す。
- 正式Class Controlled Valuesは以下の7値とする。
 - `Encounter`
 - `Disappearance`
 - `Anomaly`
 - `Discovery`
 - `Transmission`
 - `Transformation`
 - `Disturbance`
- Class Controlled ValuesのSingle Source of Truthは、Database Schema Chapter 6 / Class Field Definition / Allowed Valueとする。
- CategoryとClassは独立したClassification Fieldとして扱う。
- CategoryをClassの上位分類として扱わない。
- ClassをCategoryの下位分類として扱わない。
- Categoryの値によって使用可能なClass値を制限しない。
- CategoryからClass値を自動導出しない。
- ClassからCategory値を自動導出しない。
- 複数のClass候補に該当し得る場合は、事件の中心となる現象タイプを1つだけ採用する。
- `Unknown`を正式なClass Controlled Valueとして使用しない。
### 未確認事項
なし。
`HOLD-CLASS-01`の解消対象としていたClass Controlled Values、Controlled Valuesの正式管理元、およびCategoryとの依存関係について、未確認事項は残っていない。
### 依存関係
Database Schema Chapter 6 / Class Field Definitionへの正式反映に依存した。
正式Class Controlled Values、Single Source of Truth、およびCategoryとClassの正式な関係の確定に依存した。
Class Field Definition反映後の最終再監査に依存した。
これらの依存事項は確認済み。
### 禁止事項
- 正式な7つのClass Controlled Values以外を正式Class値として使用してはならない。
- 未承認Class値を独自生成または補完してはならない。
- `Unknown`を正式なClass Controlled Valueとして使用してはならない。
- Class Controlled Valuesを複数の正式管理元へ重複定義してはならない。
- CategoryとClassを階層関係として扱ってはならない。
- Categoryによって使用可能なClass値を制限してはならない。
- CategoryからClassを自動導出してはならない。
- ClassからCategoryを自動導出してはならない。
- 複数のClass値を同時に保持してはならない。
### 次のAction
なし。
`HOLD-CLASS-01`の解消条件は満たされている。
本項目はActive HOLD / Pendingとして追跡せず、RESOLVED履歴として保持する。
### 解消条件
以下の条件をすべて満たしたことを確認した。
1. 正式Class Controlled Valuesを確定する。
2. Class Controlled Valuesの正式管理元を確定する。
3. CategoryとClassの正式な関係を確定する。
4. CategoryによるClass Allowed Value制約の有無を確定する。
5. 確定した仕様をDatabase Schema Chapter 6 / Class Field Definitionへ反映する。
6. 関連するCategory仕様との整合性を確認する。
7. Class Field Definition全体を再監査する。
**上記7条件：すべて達成済み。**
### 解消根拠
Human Decisionにより、Class Controlled Values、Controlled Valuesの正式管理元、およびCategoryとの関係を正式確定した。
Database Schema Chapter 6 / Class Field Definitionへ正式反映した。
反映後、Class Field DefinitionおよびCategoryとの責務整合性について最終再監査を実施した。
### 反映先
Database Schema Chapter 6 / Class Field Definition
### 最終監査結果
PASS
`Field Name` — PASS
`Purpose` — PASS
`Data Type` — PASS
`Required / Optional` — PASS
`Allowed Value` — PASS
`Default Value` — PASS
`Unset Value` — PASS
`Constraints` — PASS
**Field Definition Structure: PASS**
**HOLD-CLASS-01 解消条件: PASS**
**解消根拠: PASS**
**反映先: PASS**
**依存関係: PASS**
**Categoryとの責務整合性: PASS**
**最終再監査: PASS**
新規REVISION：0
新規HOLD：0
BLOCKER：0
### Resolution
**HOLD-CLASS-01 — RESOLVED**
本項目をActive HOLD / Pendingとして扱わない。
解消後も記録を削除せず、RESOLVED履歴として保持する。
---
# 7. Recovery Log
## Category Repository Working Draft / Category HOLD Record Recovery
### Recovery Status
CLOSED — HISTORICAL RECORD NOT RECOVERED
### 対象
過去のCategory Repository Working Draft、および同Working Draftで管理されていた可能性のあるCategory関連HOLD ID / HOLD Record。
### Recovery Result
Category Repository Working Draftおよび旧Category HOLD Recordは回収されていない。
正式ID、正式HOLD Recordおよび旧Working Draftの内容を、過去の記憶または推測によって復元しない。
Historical Record Recoveryは、旧Recordを未回収状態のまま保持してCLOSEDとする。
### Current Classification Status
**Category: PASS**
現行Category Field Definitionは、旧Category Repository Working Draftまたは旧Category HOLD RecordのRecoveryとは独立して、現存する正式Source of Truth、Human Decision、Database Schema Chapter 6への正式反映、および最終再監査によって確定している。
旧Category Repository Working Draftまたは旧Category HOLD Recordの未回収状態を、現行Category Field Definitionの未解決依存関係として扱わない。
### Recovery方針
旧Category Repository Working Draftまたは旧Category HOLD Recordを将来発見した場合は、Historical Recordとして内容を確認する。
発見したことのみを理由として、現行Category Field Definitionを自動変更してはならない。
発見した旧Recordに、現在も未解決であることを確認できる別論点が存在する場合は、その時点で正式Source of Truthおよび現行仕様との関係を監査し、必要なHOLD登録を別途判断する。
### 禁止事項
- Category関連HOLDの正式IDを推測によって作成してはならない。
- 未確認のCategory HOLD内容を正式記録として復元してはならない。
- Category Repository Working Draftの内容を推測によって作成してはならない。
- Historical Recordが未回収であることのみを理由として、現行Category Field DefinitionをHOLDへ戻してはならない。
- Recovery Logへの記録のみを理由として、Active HOLD / Pendingへ正式登録してはならない。
- 旧Recordを将来発見した場合、その内容を現行仕様へ自動適用してはならない。
### Active Registration
なし。
本Recovery RecordをActive HOLD / Pendingとして扱わない。
---
# 8. Current Ledger State

## Active HOLD / Pending

- `HOLD-AUDIT-PLACEMENT-01` — Audit Artifact Repository Placement
- `HOLD-ARTIFACT-VERSION-01` — Production Artifact Version Increment Criteria
- `HOLD-PUBLICATION-TRACKING-01` — FREE / CLASSIFIED Artifact-level Tracking
- `HOLD-PUBLICATION-STATUS-COMPAT-01` — Publication Status Cross-Document Compatibility

**Active HOLD / Pending Count: 4**

## Resolution Review

現在登録なし。

**Resolution Review Count: 0**

## RESOLVED Archive

- `HOLD-TAGS-01` — Tags Controlled Values / 正式Tag一覧
- `HOLD-STATUS-01` — Status Meaning / Data Type / Controlled Values / Nullability
- `HOLD-CLASS-02` — Class Data Type / Nullability / Lifecycle
- `HOLD-CLASS-01` — Class Controlled Values / Category依存関係

**RESOLVED Archive Count: 4**

## Recovery Log

- Category Repository Working Draft / Category HOLD Record — Historical Record Recovery CLOSED / Record NOT RECOVERED

**Recovery Log Count: 1**
---
# 9. Audit Status

本台帳v1.0は、現時点で確認できたHOLD記録、正式Source of Truth、Human Decision、正式文書への反映、および監査結果に基づいて構成する。

現在、Active HOLD / Pendingとして以下の4件を正式登録する。

- `HOLD-AUDIT-PLACEMENT-01`
- `HOLD-ARTIFACT-VERSION-01`
- `HOLD-PUBLICATION-TRACKING-01`
- `HOLD-PUBLICATION-STATUS-COMPAT-01`

上記4件は、Repository Rule制作および横断監査の過程で未解決論点の存在を確認し、現在も正式な解消条件を満たしていないため、Active HOLD / Pendingとして追跡する。

各HOLDは、必要なHuman Decision、Applicable Source of Truthへの反映、依存関係の確認および最終再監査PASSが完了するまでRESOLVEDとして扱わない。

`HOLD-TAGS-01`は、具体的な初期Tag Controlled ValuesのHuman Decision、Database Schema Chapter 6 / Tags Field Definitionへの正式反映、既存Fieldとの責務分離確認、既存Constraintsとの整合性確認、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

`HOLD-STATUS-01`は、必要な仕様確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

`HOLD-CLASS-02`は、ClassのData Type、Nullability、Unset ValueおよびLifecycle条件の正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

`HOLD-CLASS-01`は、Class Controlled Values、Controlled ValuesのSingle Source of Truth、Categoryとの責務分離および依存関係の正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

Category Repository Working Draftおよび旧Category HOLD Recordは回収されていない。

Category関連Historical Record Recoveryは、旧Recordを推測復元せず未回収状態を保持した上でCLOSEDとして扱う。

旧Category Repository Working Draftまたは旧Category HOLD Recordの未回収状態は、現行Category Field Definitionの未解決依存関係として扱わない。

確認できていないHOLD IDまたはHOLD Recordを推測によって追加してはならない。

新規REVISION：0

新規HOLD：4

BLOCKER：0

**Ledger Structure: PASS**

**Active HOLD / Pending: 4**

**Resolution Review: 0**

**RESOLVED Archive: 4**

**Recovery Log: 1**

**Overall Status: PASS**
---
# 10. Version History
## v1.0
ProjectORIGIN HOLD管理台帳の正式初版。
既存の正式HOLD管理構造に従い、以下の4領域で構成した。
- Active HOLD / Pending
- Resolution Review
- RESOLVED Archive
- Recovery Log
確認されたHOLDについて、解消後も履歴を削除せずRESOLVED Archiveへ保持する構造とした。
Category Repository Working Draftおよび旧Category HOLD Recordについては、推測復元を行わず、Historical Record Recoveryを未回収状態のままCLOSEDとして保持する。
`HOLD-STATUS-01`、`HOLD-CLASS-02`、`HOLD-CLASS-01`および`HOLD-TAGS-01`は、正式な解消条件、必要な正式文書への反映、および最終再監査PASSを確認し、RESOLVED Archiveへ保持する。
現時点のActive HOLD / Pendingは0件とする。

### Active HOLD Registration Update — 2026-08-27

Repository Rule制作および横断監査によって現在も未解決であることを確認した以下の4件を、Active HOLD / Pendingへ正式登録した。

- `HOLD-AUDIT-PLACEMENT-01` — Audit Artifact Repository Placement
- `HOLD-ARTIFACT-VERSION-01` — Production Artifact Version Increment Criteria
- `HOLD-PUBLICATION-TRACKING-01` — FREE / CLASSIFIED Artifact-level Tracking
- `HOLD-PUBLICATION-STATUS-COMPAT-01` — Publication Status Cross-Document Compatibility

Active HOLD / Pending Countを0件から4件へ更新した。

既存のRESOLVED Archive 4件およびCategory Historical Recovery Recordは変更せず維持した。

各Active HOLDは、正式な解消条件、必要なHuman Decision、Applicable Source of Truthへの反映、依存関係確認および最終再監査PASSが完了するまでRESOLVEDとして扱わない。