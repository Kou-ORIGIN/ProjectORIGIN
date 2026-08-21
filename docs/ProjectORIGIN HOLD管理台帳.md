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

## HOLD-CLASS-01 — Class Controlled Values / Category依存関係

### Status

HOLD

### 発生元

Database Schema Chapter 6 / Class Field Definition

### 対象

`class`の正式なControlled Values、Class Controlled Valuesの正式管理元、およびCategoryとClassの正式な依存関係。

### 発生理由

`Class`はProjectORIGINの正式なClassification Fieldとして確認できている。

一方、現行の正式Source of Truthからは、正式Class Controlled Valuesを一意に決定できる仕様を確認できていない。

また、Class Controlled Valuesの正式管理元についても一意に確定できていない。

CategoryとClassについて、正式な階層関係または依存関係が存在するか、またCategoryの値によって使用可能なClass値を制限する正式規則が存在するかについても、現行の正式Source of Truthから一意に確定できていない。

これらを推測によって確定すると、正式Source of Truthに存在しないClass値、階層関係またはAllowed Value制約を新たに作成することになるため、HOLDとして保持する。

### 確認済み事項

- `Class`はProjectORIGINの正式なClassification Fieldである。
- `class`フィールド自体は、正式な事件データで保持する。
- 正式に定義されていない自由入力値を、新しい正式Class値として使用しない。
- 正式に定義・承認されていないClass値を、AI、Database層、Application層その他の処理が正式値として独自に生成または補完しない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名その他の表示上の差異を理由として、新しいClass値を独自に作成しない。
- CategoryとClassの階層関係または依存関係を、正式な根拠なく設定しない。
- Categoryの値から使用可能なClass値を制限する規則を、正式な根拠なく設定しない。
- `HOLD-CLASS-02`は、ClassのData Type、Nullability、Unset ValueおよびLifecycle条件を担当する別論点として解消済みである。

### 未確認事項

- 正式Class Controlled Values
- Class Controlled Valuesの正式管理元
- CategoryとClassの正式な階層関係の有無
- CategoryとClassの正式な依存関係の有無
- Categoryの値によって使用可能なClass値を制限する正式規則の有無
- Category依存関係が存在する場合の具体的な制約条件

### 依存関係

Database Schema Chapter 6 / Class Field Definitionに依存する。

CategoryとClassの正式な依存関係が存在する場合は、その関係を正式に定義するSource of Truthの確認または正式確定に依存する。

Category関連HOLDに、本HOLDの解消に必要な正式仕様が含まれる場合は、その解消結果との整合確認を必要とする。

`HOLD-CLASS-02`とは別論点として管理する。

`HOLD-CLASS-02`が解消されたことだけを理由として、`HOLD-CLASS-01`をRESOLVEDとして扱わない。

### 禁止事項

- 正式Class Controlled Valuesを推測によって確定してはならない。
- 正式に定義・承認されていないClass値を、新しい正式Class値として独自に生成してはならない。
- 正式に定義されていない自由入力値を、新しい正式Class値として使用してはならない。
- AI、Database層、Application層その他の処理が、正式に定義されていないClass値を正式値として生成または補完してはならない。
- 表記揺れ、大文字・小文字の違い、略称、翻訳名その他の表示上の差異を理由として、新しいClass値を独自に作成してはならない。
- CategoryとClassの階層関係または依存関係を、正式な根拠なく設定してはならない。
- Categoryの値から使用可能なClass値を制限する規則を、正式な根拠なく設定してはならない。
- 他のClassification Fieldの値から、正式な根拠なくClass値を推測または自動補完してはならない。
- 事件本文その他の情報から、正式な分類判断を経ずにClass値を推測または自動補完してはならない。
- `HOLD-CLASS-02`の解消だけを根拠として、本HOLDを解消してはならない。
- HOLD解消前にClass Controlled ValuesまたはCategory依存関係を確定済みとして扱ってはならない。

### 次のAction

正式Class Controlled Valuesを一意に決定できる正式仕様または正式管理元を確認する。

CategoryとClassの正式な階層関係または依存関係の有無を確認する。

CategoryによってClass Allowed Valueが制限される場合は、その正式な条件を確認または正式確定する。

必要な仕様が確認または正式確定された後、Database Schema Chapter 6 / Class Field Definitionへ反映する。

反映後、Class Field Definition全体を再監査する。

### 解消条件

以下をすべて満たすこと。

1. 正式Class Controlled Valuesを一意に決定できる正式仕様を確認または正式確定する。
2. Class Controlled Valuesの正式管理元を確認または正式確定する。
3. CategoryとClassの正式な階層関係または依存関係の有無を確認または正式確定する。
4. CategoryによるClass Allowed Value制約が存在する場合、その正式な条件を確認または正式確定する。
5. 確定した仕様をDatabase Schema Chapter 6 / Class Field Definitionへ反映する。
6. 関連するCategory仕様との整合性を確認する。
7. Class Field Definition全体を再監査し、本HOLDに関する矛盾または未解決の依存関係が残っていないことを確認する。

### 解消根拠

未確定。

### 反映先

Database Schema Chapter 6 / Class Field Definition

### 最終監査結果

未実施。

---

## HOLD-TAGS-01 — Tags Controlled Values / 有効Tag判定

### Status

HOLD

### 発生元

Database Schema Chapter 6 / Tags Field Definition

### 対象

`tags`のAllowed Value、正式Tag Controlled Values、「有効なタグ」の判定条件、および代表タグ判定に直接関係する仕様。

### 発生理由

現行Database Schemaでは、Tagsを順序付き一覧として管理し、代表タグを先頭に登録された有効なタグから取得することは確認できる。

一方で、正式Tag Controlled Valuesおよび「有効なタグ」の具体的な判定条件を一意に決定できる正式仕様を確認できていない。

また、重複TagをSchema上禁止するかについても、正式仕様を確認できていない。

これらを推測によって確定すると、正式Source of Truthに存在しないTag値またはTag判定規則を新たに作成することになるため、HOLDとして保持する。

### 確認済み事項

- `tags`はProjectORIGINの正式なClassification Fieldである。
- Tagsは順序付き一覧として管理する。
- 代表タグは、先頭に登録された有効なタグから取得する。
- 代表タグを別フィールドへ重複保存しない。
- Tagsが空の場合、代表タグは未設定として扱う。
- Field Name `tags`はPASSしている。
- PurposeはPASSしている。
- Data Type `array<string>`はPASSしている。
- `tags`フィールド自体を保持するRequired / Optional設計はPASSしている。

### 未確認事項

- 正式Tag Controlled Values
- Tag Controlled Valuesの正式管理元
- 「有効なタグ」の正式判定条件
- 重複TagをSchema上禁止するか

### 依存関係

Database Schema Chapter 6 / Tags Field Definitionに依存する。

正式Tag Controlled Valuesおよび「有効なタグ」を一意に判定できる正式仕様または正式管理元の確認または正式確定に依存する。

代表タグ判定は、「有効なタグ」の正式判定条件に依存する。

重複Tagの扱いをConstraintsとして正式化する場合は、重複TagをSchema上禁止するかどうかの正式確定に依存する。

他のClassification Fieldに存在するControlled Valuesまたは判定規則を、本HOLDの解消根拠として自動的に転用しない。

### 禁止事項

- AIが正式に定義されていないTag値を独自生成してはならない。
- 未確認のTag一覧を正式Controlled Valuesとして採用してはならない。
- 「有効なタグ」の条件を推測によって定義してはならない。
- 正式根拠なく重複Tagの許可または禁止を確定してはならない。
- 他のClassification FieldのControlled Valuesまたは判定規則を、正式な根拠なくTagsへ転用してはならない。
- HOLD解消前にTags全体をPASSとして扱ってはならない。

### 次のAction

Tags Field Definitionのうち、HOLD-TAGS-01に依存しないDefault Value、Unset Value、Constraintsを継続して監査する。

その後、Tags Field Definition全体を再監査する。

正式Tag Controlled Values、「有効なタグ」の正式判定条件、および必要な重複Tag規則を一意に決定できる正式根拠が確認または正式確定された場合、本HOLDの解消判定を実施する。

### 解消条件

以下を満たすこと。

1. 正式Tag Controlled Valuesを一意に決定できる正式仕様を確認または正式確定する。
2. Tag Controlled Valuesの正式管理元を確認または正式確定する。
3. 「有効なタグ」を一意に判定できる正式条件を確認または正式確定する。
4. 重複TagをSchema上禁止するかどうかを正式に確定する。
5. 必要な仕様をDatabase Schema Chapter 6 / Tags Field Definitionへ反映する。
6. 代表タグ判定との整合性を確認する。
7. Tags Field Definition全体を再監査し、本HOLDに関する矛盾または未解決の依存関係が残っていないことを確認する。

### 解消根拠

未確定。

### 反映先

Database Schema Chapter 6 / Tags Field Definition

### 最終監査結果

未実施。

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

これらの別HOLDが未解決であることを理由として、`HOLD-STATUS-01`を未解決状態へ戻さない。

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
- 正式公開データでは、`HOLD-CLASS-01`の解消によって正式確定されたClass Controlled Valueのいずれかを必ず保持する。
- `HOLD-CLASS-01`は、Class Controlled ValuesおよびCategory依存関係を担当する別論点として維持する。

### 未確認事項

なし。

`HOLD-CLASS-02`の解消対象としていたData Type、Nullability、Unset ValueおよびLifecycle条件について、未確認事項は残っていない。

Class Controlled ValuesおよびCategory依存関係は`HOLD-CLASS-01`の対象であり、本HOLDの未確認事項として扱わない。

### 依存関係

Database Schema Chapter 6 / Class Field Definitionへの正式反映に依存した。

ClassのData Type、Unset Value、NullabilityおよびLifecycle条件の正式確定に依存した。

Class Field Definition反映後の最終再監査に依存した。

これらの依存事項は確認済み。

`HOLD-CLASS-01 — Class Controlled Values / Category依存関係`とは別論点として管理する。

`HOLD-CLASS-01`が未解決であることを理由として、`HOLD-CLASS-02`を未解決状態へ戻さない。

一方、`HOLD-CLASS-02`の解消だけを理由として、`HOLD-CLASS-01`をRESOLVEDとして扱わない。

### 禁止事項

- `class`に複数のClass値を保持してはならない。
- 非`null`のClass値に`string`以外のData Typeを使用してはならない。
- `null`をClassのControlled Valueとして扱ってはならない。
- 空文字、`"Unknown"`、`"Unclassified"`、`"N/A"`その他の疑似Class値を、正式なUnset Valueとして使用してはならない。
- `class`フィールド自体の欠落と`class: null`を同一の状態として扱ってはならない。
- 正式公開データで`null`を使用してはならない。
- 調査中または移行中でClass分類がすでに正式設定されている場合に、設定済みClass値を`null`へ置き換えてはならない。
- `HOLD-CLASS-02`の解消を理由として、未確定のClass Controlled ValuesまたはCategory依存関係を推測によって確定してはならない。
- `HOLD-CLASS-01`の未解決事項を、本HOLDの解消内容として扱ってはならない。

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
6. Class Field Definition全体を再監査し、矛盾または未解決の依存関係がないことを確認する。

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
- 正式公開データでは、`HOLD-CLASS-01`の解消によって正式確定されたClass Controlled Valueのいずれかを必須とする。
- Class Controlled ValuesおよびCategory依存関係は`HOLD-CLASS-01`へ分離して維持する。

反映後、Class Field DefinitionおよびChapter 6の状態整合性について最終再監査を実施した。

Data Type、Required / Optional、Unset Valueおよび関連ConstraintsはPASSし、`HOLD-CLASS-02`の対象事項に未解決の矛盾が残っていないことを確認した。

`Allowed Value`は`HOLD-CLASS-01`としてHOLDを維持しており、`HOLD-CLASS-02`の解消によって推測確定されていない。

### 反映先

Database Schema Chapter 6 / Class Field Definition

### 最終監査結果

PASS

`Field Name` — PASS  
`Purpose` — PASS  
`Data Type` — PASS  
`Required / Optional` — PASS  
`Allowed Value` — HOLD (`HOLD-CLASS-01`)  
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

# 7. Recovery Log

## Category関連HOLD

### Recovery Status

確認継続中。

### 確認済み事項

Database Schema Chapter 6により、Categoryに未解決HOLDが存在することは確認済み。

CategoryのField Definitionは、監査済みのCategory Repository Working Draftを正式な作業基準として扱う。

未解決HOLDが存在する事項について、暫定値または推測値を正式仕様として採用しない。

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

### Current Classification Status

**Category: HOLD**

### Active Registration

未実施。

---

# 8. Current Ledger State

## Active HOLD / Pending

- `HOLD-CLASS-01` — Class Controlled Values / Category依存関係
- `HOLD-TAGS-01` — Tags Controlled Values / 有効Tag判定

**Active HOLD / Pending Count: 2**

## Resolution Review

現在登録なし。

**Resolution Review Count: 0**

## RESOLVED Archive

- `HOLD-STATUS-01` — Status Meaning / Data Type / Controlled Values / Nullability
- `HOLD-CLASS-02` — Class Data Type / Nullability / Lifecycle

**RESOLVED Archive Count: 2**

## Recovery Log

- Category関連HOLD — 正式ID / 正式Record確認待ち

**Recovery Log Count: 1**

---

# 9. Audit Status

本台帳v1.0は、現時点で確認できたHOLD記録および正式Source of Truthに基づいて構成する。

`HOLD-CLASS-01`および`HOLD-TAGS-01`は、現在も未解決であることを確認したActive HOLD / Pendingとして保持する。

`HOLD-STATUS-01`は、必要な仕様確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

`HOLD-CLASS-02`は、ClassのData Type、Nullability、Unset ValueおよびLifecycle条件の正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認したため、RESOLVED Archiveへ保持する。

Category関連HOLDについては、未解決事項の存在のみを確認済みとし、正式IDまたは正式HOLD Recordを確認できていないためRecovery Logへ保持する。

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

- `HOLD-CLASS-01`をActive HOLD / Pendingとして登録。
- `HOLD-TAGS-01`をActive HOLD / Pendingとして登録。
- Resolution Reviewは現在登録なしとして保持。
- `HOLD-STATUS-01`をRESOLVED Archiveへ保持。
- `HOLD-CLASS-02`について、ClassのData Type、Nullability、Unset ValueおよびLifecycle条件の正式確定、Database Schema Chapter 6への反映、および最終再監査PASSを確認し、Active HOLD / PendingからRESOLVED Archiveへ移行。
- Category関連HOLDをRecovery Logへ保持し、正式IDまたは正式Record確認前の推測登録を禁止。
- HOLD解消後も履歴を保持する構造を維持。

`HOLD-CLASS-02`解消反映後の台帳整合性を確認し、新規REVISION 0、新規HOLD 0、BLOCKER 0でPASS。

本Versionを `ProjectORIGIN HOLD管理台帳 v1.0` の正式管理状態として維持する。