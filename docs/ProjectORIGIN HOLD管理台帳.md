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

## HOLD-TAGS-01 — Tags Controlled Values / 正式Tag一覧

### Status

HOLD

### 発生元

Database Schema Chapter 6 / Tags Field Definition

### 対象

`tags`に保持できる具体的な正式Tag Controlled Values一覧。

### 発生理由

`tags`はProjectORIGINの正式なClassification Fieldとして確認されている。

Human DecisionおよびDatabase Schema Chapter 6 / Tags Field Definitionへの正式反映により、Tagsの基本責務、Data Type、Required / Optional、Tag Controlled ValuesのSingle Source of Truth、「有効なTag」の判定条件、代表タグ判定、Default Value、Unset Value、重複Tagの扱い、および主要Constraintsは確定した。

一方、`tags`に保持できる具体的な正式Tag Controlled Values一覧については、現時点で一意に確定できていない。

また、既存の正式事件データから初期Tag Controlled Valuesを抽出できる十分な正式データ母集団も、現時点では確認できていない。

具体的な正式Tag Controlled Values一覧を推測によって確定すると、正式Source of Truthに存在しないTag値を新たに作成することになるため、本HOLDを維持する。

### 確認済み事項

- `tags`はProjectORIGINの正式なClassification Fieldである。
- `tags`は、Category、Classその他の正式Classification Fieldだけでは表現しきれない事件の特徴について、検索、絞り込みおよび事件横断での関連付けに使用する補助的なClassification情報を保持する。
- Tagsは既存の正式Fieldの責務を代替するために使用しない。
- Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldで正式に管理できる情報を、同一の意味を持つTagとして重複管理しない。
- Data Typeは`array<string>`とする。
- `tags`フィールド自体は、正式な事件データでは必須とする。
- 正式Tagが設定されていない場合も、`tags`フィールド自体を保持する。
- Tagsは順序付き一覧として管理する。
- `tags`に保持できる値は、正式なTag Controlled Valuesとして登録された値のみとする。
- Tag Controlled ValuesのSingle Source of Truthは、Database Schema Chapter 6 / Tags Field Definition / Allowed Valueとする。
- Tag Controlled Valuesを別の正式管理元へ重複定義しない。
- Tag Controlled Valuesは、将来の正式な判断によって拡張可能とする。
- 未承認のTag値を正式Tagとして使用しない。
- AI、Database層、Application層その他の処理が、新しいTag値を自動的に正式Controlled Valueへ追加しない。
- 「有効なTag」とは、Tags Field DefinitionのAllowed Valueに正式なTag Controlled Valueとして登録されている値を指す。
- 正式Allowed Valueと一致しない値を、有効なTagとして扱わない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名、類似表現その他を理由として、未登録値を有効なTagとして扱わない。
- AIその他の処理が、意味的に類似していることのみを理由として未登録値を有効なTagへ変換または補完しない。
- 代表タグは、`tags`を先頭から順に確認し、最初に登録されている有効なTagから取得する。
- 代表タグを別フィールドへ重複保存しない。
- Tagsが空の場合、代表タグは未設定として扱う。
- 有効なTagが存在しない場合も、代表タグは未設定として扱う。
- Tagの登録順序は保持する。
- 同一Tagを同一`tags`配列内へ複数回保持しない。
- Tagの重複によって代表Tagの優先度、重要度その他の意味を表さない。
- Default Valueは設定しない。
- 空配列、特定のTag値その他を暗黙のDefault Valueとして自動設定しない。
- 正式なUnset Valueは`[]`とする。
- `tags: []`は、正式なTagが1件も設定されていない状態を表す。
- `null`、空文字または`tags`フィールド自体の欠落を正式なUnset Valueとして使用しない。
- 1事件だけにしか意味を持たない固有表現は、原則として正式Tagへ昇格させない。
- 複数事件へ適用可能であることをTag候補の原則とする。
- 固定件数のみを理由としてTag昇格条件を定義しない。
- Tagの意味または用途が既存の正式Tagと実質的に重複する場合、別Tagとして追加しない。
- 新しいTag Controlled Valueの追加は、正式な判断を経てAllowed Valueへ反映する。

### 未確認事項

- 具体的な正式Tag Controlled Values一覧

### 依存関係

Database Schema Chapter 6 / Tags Field Definitionに依存する。

本HOLDの解消は、具体的な正式Tag Controlled Values一覧を一意に決定できる正式な判断に依存する。

既存の正式事件データから初期Tag Controlled Valuesを抽出する場合は、その判断に使用できる十分な正式データ母集団が確認できることに依存する。

具体的な正式Tag Controlled Values一覧を確定した場合、その一覧をDatabase Schema Chapter 6 / Tags Field Definition / Allowed Valueへ正式反映することに依存する。

代表タグ判定は、Allowed Valueへ正式登録されたTagを「有効なTag」として使用する。

他のClassification Field、専用Field、過去の記憶、一般的な分類体系または未承認の既存データからTag Controlled Valuesを自動的に導出しない。

### 禁止事項

- AIが正式に定義されていないTag値を独自生成してはならない。
- 未確認または未承認のTag一覧を正式Controlled Valuesとして採用してはならない。
- 具体的な正式Tag Controlled Values一覧を推測によって補完してはならない。
- 未登録Tagを正式な有効Tagとして扱ってはならない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名、類似表現その他を理由として、未登録値を正式Tagとして扱ってはならない。
- AI、Database層、Application層その他の処理が、新しいTag値を自動的に正式Controlled Valueへ追加してはならない。
- 他のClassification Fieldまたは専用Fieldの値を、正式な判断なくTag Controlled Valuesへ転用してはならない。
- Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldで正式に管理できる情報を、同一の意味を持つTagとして重複管理してはならない。
- 同一Tagを同一`tags`配列内へ複数回保持してはならない。
- Tagの重複によって優先度、重要度その他の意味を表してはならない。
- `null`、空文字またはフィールド欠落をTagsの正式なUnset Valueとして使用してはならない。
- HOLD解消前に、具体的な正式Tag Controlled Values一覧が確定済みであるものとして扱ってはならない。
- HOLD解消前にTags Field Definition全体をPASSとして扱ってはならない。

### 次のAction

具体的な正式Tag Controlled Values一覧を確定するための正式な判断を行う。

既存の正式事件データから初期Tag Controlled Valuesを抽出する方法を採用する場合は、その判断に使用できる十分な正式データ母集団が存在することを確認する。

十分な正式データ母集団を確認できない場合は、未確認データまたはAIによる推測からTag Controlled Valuesを生成せず、必要な正式判断を行う。

具体的な正式Tag Controlled Values一覧が確定した後、Database Schema Chapter 6 / Tags Field Definition / Allowed Valueへ正式反映する。

反映後、Tags Field Definition全体を再監査する。

### 解消条件

以下を満たすこと。

1. 具体的な正式Tag Controlled Values一覧を正式に確定する。
2. 確定したTag Controlled Values一覧が、Tagsの正式なPurposeおよびConstraintsと整合していることを確認する。
3. Category、Class、Status、Risk Level、Date、Location、Countryその他の専用Fieldとの責務重複がないことを確認する。
4. 確定したTag Controlled Values一覧をDatabase Schema Chapter 6 / Tags Field Definition / Allowed Valueへ正式反映する。
5. 「有効なTag」の判定条件および代表タグ判定との整合性を確認する。
6. 重複Tag禁止を含む既存Constraintsとの整合性を確認する。
7. Tags Field Definition全体を再監査し、本HOLDに関する矛盾または未解決の依存関係が残っていないことを確認する。
8. 最終再監査がPASSする。

### 解消根拠

未確定。

具体的な正式Tag Controlled Values一覧の正式確定を必要とする。

### 反映先

Database Schema Chapter 6 / Tags Field Definition / Allowed Value

必要に応じて、同Field Definition内の関連記述との整合性を確認する。

### 最終監査結果

未実施。

具体的な正式Tag Controlled Values一覧の確定および正式反映後に、Tags Field Definition全体の最終再監査を実施する。

---

# 5. Resolution Review

現在登録なし。

---

# 6. RESOLVED Archive

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

Category関連HOLD、`HOLD-CLASS-01`、`HOLD-CLASS-02`および`HOLD-TAGS-01`は、本HOLDとは独立した別論点として扱う。

これらの別HOLDの状態を理由として、`HOLD-STATUS-01`を未解決状態へ戻さない。

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

Database Schema Chapter 6 / Status Field Definitionへ、以下の仕様を正式反映した。

- Purpose：事件そのものの解決状態
- Data Type：`string | null`
- Controlled Values：
  - `Unresolved`
  - `Partially Resolved`
  - `Resolved`
  - `Undetermined`
- Unset Value：`null`
- 調査中または移行中のみ、Status分類未設定の場合に一時的な`null`を許容
- 正式公開データでは`null`を禁止
- 正式公開データでは4つのControlled Valueのいずれかを必須とする
- Workflow StatusおよびPublication Statusとの責務を分離
- `null`と`Undetermined`の意味を分離

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

一方、HOLD登録時点では、現行の正式Source of Truthから`class`の正式なData Typeを一意に確定できる仕様を確認できていなかった。

そのため、以前候補として検討した`string | null`を正式なData Typeとして確定することはできなかった。

Data Typeが未確定であったため、`null`を正式なUnset Valueとして先行確定することもできなかった。

また、Class値が未設定となり得る場合について、調査中、移行中、正式公開時などのLifecycleごとのNullability条件も確認できていなかった。

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
- Class Controlled ValuesおよびCategoryとの関係は`HOLD-CLASS-01`の対象として分離して管理した。

### 未確認事項

なし。

`HOLD-CLASS-02`の解消対象としていたData Type、Nullability、Unset ValueおよびLifecycle条件について、未確認事項は残っていない。

### 依存関係

Database Schema Chapter 6 / Class Field Definitionへの正式反映に依存した。

ClassのData Type、Unset Value、NullabilityおよびLifecycle条件の正式確定に依存した。

Class Field Definition反映後の最終再監査に依存した。

これらの依存事項は確認済み。

`HOLD-CLASS-01`とは別論点として管理した。

`HOLD-CLASS-01`の状態を理由として、`HOLD-CLASS-02`を未解決状態へ戻さない。

### 禁止事項

- `class`に複数のClass値を保持してはならない。
- 非`null`のClass値に`string`以外のData Typeを使用してはならない。
- `null`をClassのControlled Valueとして扱ってはならない。
- 空文字、`"Unknown"`、`"Unclassified"`、`"N/A"`その他の疑似Class値を、正式なUnset Valueとして使用してはならない。
- `class`フィールド自体の欠落と`class: null`を同一の状態として扱ってはならない。
- 正式公開データで`null`を使用してはならない。
- 調査中または移行中でClass分類がすでに正式設定されている場合に、設定済みClass値を`null`へ置き換えてはならない。

### 次のAction

なし。

`HOLD-CLASS-02`の解消条件は満たされている。

本項目はActive HOLD / Pendingとして追跡せず、RESOLVED履歴として保持する。

### 解消条件

以下の条件をすべて満たしたことを確認した。

1. `class`の正式なData Typeを一意に決定できる正式仕様を確認または正式確定する。
2. Classの正式なUnset Valueを一意に決定する。
3. ClassのNullability条件を正式に確定する。
4. 必要な場合、調査中、移行中、正式公開時などのLifecycle別条件を正式に確定する。
5. 確定した仕様をDatabase Schema Chapter 6 / Class Field Definitionへ反映する。
6. Class Field Definition全体を再監査し、本HOLDの対象事項に矛盾または未解決の依存関係がないことを確認する。

**上記6条件：すべて達成済み。**

### 解消根拠

Human Decisionにより、ClassのData Type、Unset Value、NullabilityおよびLifecycle条件を正式確定した。

Database Schema Chapter 6 / Class Field Definitionへ、以下の仕様を正式反映した。

- Classは単一値として保持する。
- Non-null Data Type：`string`
- Data Type：`string | null`
- Unset Value：`null`
- `null`はClassのControlled Valueとして扱わない。
- `class`フィールド自体の欠落と`class: null`を分離する。
- 調査中または移行中は、Class分類がまだ正式に設定されていない場合に限り、一時的な`null`を許容する。
- 正式公開データでは`null`を禁止する。

反映後、Class Field DefinitionおよびChapter 6の状態整合性について最終再監査を実施した。

Data Type、Required / Optional、Unset Valueおよび関連ConstraintsはPASSし、`HOLD-CLASS-02`の対象事項に未解決の矛盾が残っていないことを確認した。

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

一方、HOLD登録時点では、正式Class Controlled Valuesを一意に決定できる仕様を確認できていなかった。

また、Class Controlled Valuesの正式管理元についても一意に確定できていなかった。

CategoryとClassについて、正式な階層関係または依存関係が存在するか、またCategoryの値によって使用可能なClass値を制限する正式規則が存在するかについても、一意に確定できていなかった。

これらを推測によって確定すると、正式Source of Truthに存在しないClass値、階層関係またはAllowed Value制約を新たに作成することになるため、HOLDとして保持した。

### 確認済み事項

Human DecisionおよびDatabase Schema Chapter 6への正式反映により、以下を確定した。

- `Class`はProjectORIGINの正式なClassification Fieldである。
- Classは、事件または現象の性質および中心となる現象タイプを表す。
- `class`は単一のClass値を保持する。
- 正式Class Controlled Valuesは以下の7値とする。
  - `Encounter`
  - `Disappearance`
  - `Anomaly`
  - `Discovery`
  - `Transmission`
  - `Transformation`
  - `Disturbance`
- Class Controlled ValuesのSingle Source of Truthは、Database Schema Chapter 6 / Class Field Definition / Allowed Valueとする。
- Class Controlled Valuesを別の正式管理元へ重複定義しない。
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

Category自体に残る未解決事項は、本HOLDとは分離し、Recovery Logで継続管理する。

### 依存関係

Database Schema Chapter 6 / Class Field Definitionへの正式反映に依存した。

正式Class Controlled Valuesの確定に依存した。

Class Controlled ValuesのSingle Source of Truthの確定に依存した。

CategoryとClassの正式な関係の確定に依存した。

CategoryによるClass Allowed Value制約の有無の確定に依存した。

Class Field Definition反映後の最終再監査に依存した。

これらの依存事項は確認済み。

Category自体には未解決事項が残っているが、CategoryとClassを独立したClassification Fieldとして正式確定したため、Category自体の未解決HOLDは本HOLDの解消を妨げない。

Category自体のHOLDを、本HOLDの解消を理由としてRESOLVEDとして扱わない。

`HOLD-CLASS-02`はClassのData Type、Nullability、Unset ValueおよびLifecycle条件を担当した別論点であり、既にRESOLVEDとして管理する。

### 禁止事項

- `Encounter`、`Disappearance`、`Anomaly`、`Discovery`、`Transmission`、`Transformation`、`Disturbance`以外の値を正式なClass値として使用してはならない。
- 正式に定義されていない自由入力値を、新しい正式Class値として使用してはならない。
- 正式に定義・承認されていないClass値を、AI、Database層、Application層その他の処理が正式値として独自に生成または補完してはならない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名その他の表示上の差異を理由として、新しいClass値を独自に作成してはならない。
- `Unknown`を正式なClass Controlled Valueとして使用してはならない。
- Class Controlled Valuesを複数の正式管理元へ重複定義してはならない。
- CategoryをClassの上位分類として扱ってはならない。
- ClassをCategoryの下位分類として扱ってはならない。
- Categoryの値によって使用可能なClass値を制限してはならない。
- CategoryからClass値を自動導出してはならない。
- ClassからCategory値を自動導出してはならない。
- Categoryとの組み合わせを理由として、新しいClass値を生成してはならない。
- 複数のClass値を同時に保持してはならない。
- 他のClassification Fieldの値から、正式な分類判断を経ずにClass値を推測または自動補完してはならない。
- 事件本文その他の情報から、正式な分類判断を経ずにClass値を推測または自動補完してはならない。
- 本HOLDの解消を理由として、Category自体の未解決事項を解消済みとして扱ってはならない。

### 次のAction

なし。

`HOLD-CLASS-01`の解消条件は満たされている。

本項目はActive HOLD / Pendingとして追跡せず、RESOLVED履歴として保持する。

### 解消条件

以下の条件をすべて満たしたことを確認した。

1. 正式Class Controlled Valuesを一意に決定できる正式仕様を確認または正式確定する。
2. Class Controlled Valuesの正式管理元を確認または正式確定する。
3. CategoryとClassの正式な階層関係または依存関係の有無を確認または正式確定する。
4. CategoryによるClass Allowed Value制約が存在する場合、その正式な条件を確認または正式確定する。
5. 確定した仕様をDatabase Schema Chapter 6 / Class Field Definitionへ反映する。
6. 関連するCategory仕様との整合性を確認する。
7. Class Field Definition全体を再監査し、本HOLDに関する矛盾または未解決の依存関係が残っていないことを確認する。

**上記7条件：すべて達成済み。**

### 解消根拠

Human Decisionにより、Class Controlled Values、Controlled Valuesの正式管理元、およびCategoryとの関係を正式確定した。

Database Schema Chapter 6 / Class Field Definitionへ、以下の仕様を正式反映した。

- Classは事件または現象の性質および中心となる現象タイプを表す。
- 正式Class Controlled Values：
  - `Encounter`
  - `Disappearance`
  - `Anomaly`
  - `Discovery`
  - `Transmission`
  - `Transformation`
  - `Disturbance`
- Class Controlled ValuesのSingle Source of Truthは、Database Schema Chapter 6 / Class Field Definition / Allowed Valueとする。
- Class Controlled Valuesを別の正式管理元へ重複定義しない。
- CategoryとClassは独立したClassification Fieldとする。
- CategoryをClassの上位分類として扱わない。
- ClassをCategoryの下位分類として扱わない。
- Categoryの値によってClass Allowed Valueを制限しない。
- CategoryからClassを自動導出しない。
- ClassからCategoryを自動導出しない。
- 複数候補に該当する場合は、事件の中心となる現象タイプを1つだけ採用する。
- `Unknown`を正式Class Controlled Valueとして採用しない。

反映後、Class Field DefinitionおよびCategoryとの責務整合性について最終再監査を実施した。

Field Name、Purpose、Data Type、Required / Optional、Allowed Value、Default Value、Unset Value、Constraintsの全項目がPASSした。

Category自体には未解決HOLDが残っているが、CategoryとClassの独立関係が正式確定されたため、本HOLDの解消を妨げる依存関係ではないことを確認した。

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

## Category関連HOLD

### Recovery Status

確認継続中。

### 確認済み事項

Database Schema Chapter 6により、Categoryに未解決HOLDが存在することは確認済み。

CategoryのField Definitionは、監査済みのCategory Repository Working Draftを正式な作業基準とする。

未解決HOLDが存在する事項について、暫定値または推測値を正式仕様として採用しない。

Classについては、Categoryとは独立したClassification Fieldとして正式確定している。

`HOLD-CLASS-01`の解消は、Category自体の未解決事項を解消するものではない。

### 未確認事項

現時点で確認可能な正式Source of Truthから、以下を一意に確認できていない。

- Category関連HOLDの正式ID
- Category Repository Working Draft本体
- 個別HOLDの正式な対象
- 個別HOLDの発生理由
- 個別HOLDの確認済み事項
- 個別HOLDの未確認事項
- 個別HOLDの依存関係
- 個別HOLDの禁止事項
- 個別HOLDの解消条件
- 個別HOLDの解消根拠
- 個別HOLDの反映先
- 個別HOLDの最終監査結果

### Recovery方針

Categoryに未解決事項が存在すること自体は記録として保持する。

一方、正式IDまたは正式HOLD Recordを確認できるまで、新しいHOLD IDを推測によって発行しない。

Category Repository Working Draftまたは既存の正式HOLD記録を確認できた時点で、現在も未解決であるかを証拠ベースで確認する。

確認後、Active HOLD / Pendingへの正式登録判定を実施する。

### 禁止事項

- Category関連HOLDの正式IDを推測によって作成してはならない。
- 未確認のCategory HOLD内容を正式記録として復元してはならない。
- Category Repository Working Draftの内容を推測によって作成してはならない。
- Category関連HOLDが未特定であることを理由として、CategoryをPASSとして扱ってはならない。
- Recovery Logへの記録だけを理由として、Active HOLD / Pendingへ正式登録済みとして扱ってはならない。
- `HOLD-CLASS-01`の解消を理由として、Category自体の未解決事項をRESOLVEDとして扱ってはならない。

### Current Classification Status

**Category: HOLD**

### Active Registration

未実施。

---

# 8. Current Ledger State

## Active HOLD / Pending

- `HOLD-TAGS-01` — Tags Controlled Values / 有効Tag判定

**Active HOLD / Pending Count: 1**

## Resolution Review

現在登録なし。

**Resolution Review Count: 0**

## RESOLVED Archive

- `HOLD-STATUS-01` — Status Meaning / Data Type / Controlled Values / Nullability
- `HOLD-CLASS-02` — Class Data Type / Nullability / Lifecycle
- `HOLD-CLASS-01` — Class Controlled Values / Category依存関係

**RESOLVED Archive Count: 3**

## Recovery Log

- Category関連HOLD — 正式ID / 正式Record確認待ち

**Recovery Log Count: 1**

---

# 9. Audit Status

本台帳v1.0は、現時点で確認できたHOLD記録および正式Source of Truthに基づいて構成する。

`HOLD-TAGS-01`は、現在も未解決であることを確認したActive HOLD / Pendingとして保持する。

`HOLD-STATUS-01`は、必要な仕様確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

`HOLD-CLASS-02`は、ClassのData Type、Nullability、Unset ValueおよびLifecycle条件の正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

`HOLD-CLASS-01`は、Class Controlled Values、Controlled ValuesのSingle Source of Truth、Categoryとの独立関係およびCategoryによるClass Allowed Value制約なしの正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

Category関連HOLDについては、未解決事項の存在のみを確認済みとし、正式IDまたは正式HOLD Recordを確認できていないためRecovery Logへ保持する。

`HOLD-CLASS-01`の解消はCategory自体の未解決事項を解消するものではない。

Category関連HOLDについて、未確認のHOLD IDまたはHOLD内容を推測によって正式登録しない。

Active HOLD / Pendingが存在すること自体は、本台帳の構造上の不備を意味しない。

**Ledger Audit Status: PASS**

新規REVISION：0  
新規HOLD：0  
BLOCKER：0

**ProjectORIGIN HOLD管理台帳 v1.0 — PASS**

---

# 10. Version History

## v1.0

ProjectORIGIN HOLD管理台帳の正式初版。

既存の正式HOLD管理構造に従い、以下の4領域で構成した。

- Active HOLD / Pending
- Resolution Review
- RESOLVED Archive
- Recovery Log

以下の記録を統合した。

- `HOLD-TAGS-01`をActive HOLD / Pendingとして保持。
- Resolution Reviewは現在登録なしとして保持。
- `HOLD-STATUS-01`をRESOLVED Archiveへ保持。
- `HOLD-CLASS-02`をRESOLVED Archiveへ保持。
- `HOLD-CLASS-01`について、Class Controlled Values、Controlled ValuesのSingle Source of Truth、Categoryとの独立関係およびCategoryによるClass Allowed Value制約なしの正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認し、Active HOLD / PendingからRESOLVED Archiveへ移行。
- Category関連HOLDをRecovery Logへ保持し、正式IDまたは正式Record確認前の推測登録を禁止。
- `HOLD-CLASS-01`の解消によってCategory自体の未解決事項を解消済みとして扱わない。
- HOLD解消後も履歴を保持する構造を維持。

`HOLD-CLASS-01`解消反映後の台帳整合性を確認し、新規REVISION 0、新規HOLD 0、BLOCKER 0でPASS。

本Versionを `ProjectORIGIN HOLD管理台帳 v1.0` の正式管理状態として維持する。