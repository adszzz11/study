---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Hermes Agent Server와 NotebookLM — Projects

> [[04-learning/02-deep-dive|이전: Deep Dive]] · [[README|목차로 돌아가기]]

## 프로젝트 아이디어

| 프로젝트 | 난이도 | 결과물 | 핵심 학습 |
|---|---:|---|---|
| 1. 수동 Study Note loop | ★ | Google Doc 1개 + NotebookLM notebook | claim/evidence/provenance 작성 |
| 2. Hermes draft prompt | ★★ | 재사용 prompt와 Markdown schema | source 사실과 해석 분리 |
| 3. 승인형 Drive publisher | ★★★ | MCP adapter 또는 script 설계 | least privilege, preview, confirmation |
| 4. Enterprise ingest PoC | ★★★★ | API source 생성 PoC | Cloud/IAM, Preview risk, lifecycle |

## 1. 수동 Study Note loop

### 목표

하나의 학습 주제에 대해 Hermes research → 검토 → Google Doc → NotebookLM 복습의 전체 loop를 한 번 완주한다.

### 완료 조건

- [ ] 원문 URL 3개 이상을 포함한 Study Note를 만들었다.
- [ ] 각 claim에 confidence와 evidence를 적었다.
- [ ] Hermes interpretation을 별도 section에 넣었다.
- [ ] NotebookLM 질문 3개와 틀린 답/추가 질문을 기록했다.
- [ ] source 문서를 수정하고 동기화 여부를 확인했다.

## 2. Hermes draft prompt

### 목표

매번 같은 형태로 검토 가능한 초안을 받는 prompt를 만든다.

```text
주제: <topic>
입력 source URL: <url list>

다음 Markdown schema만 사용해 초안을 작성해줘.
1. source가 직접 지지하는 Claim
2. 각 Claim의 Evidence와 원문 URL
3. Hermes interpretation (추론/가설로 명시)
4. Confidence와 검증 필요 항목
5. Questions / mistakes / next actions

URL이 없는 주장은 Claim으로 쓰지 말고 Open questions로 옮겨줘.
```

### 평가 기준

| 기준 | 통과 조건 |
|---|---|
| Traceability | 모든 claim이 URL로 돌아감 |
| Separation | source fact와 interpretation이 분리됨 |
| Restraint | 모르는 내용은 추측 대신 open question으로 남김 |
| Reviewability | 사람이 5분 안에 publish 여부를 판단 가능 |

## 3. 승인형 Drive publisher

### 목표

Hermes에 Drive write 권한을 넓게 주지 않고, 정해진 folder의 승인된 문서만 갱신한다.

```text
Hermes
  └─ MCP Drive Publisher
       ├─ create_draft(folder_allowlist, title, markdown)
       ├─ preview_diff(doc_id, markdown)
       └─ publish_approved(doc_id, revision, approval_id)
```

### 안전 설계

- `folder_allowlist` 밖의 파일을 읽거나 쓰지 않는다.
- `preview_diff`와 `publish_approved`를 하나의 tool call로 합치지 않는다.
- publish에는 사람이 만든 `approval_id` 또는 명시적 confirmation을 요구한다.
- source URL, revision, actor, timestamp만 audit log에 남기고 note 본문·token은 최소화한다.
- 첫 버전은 update가 아닌 새 draft 생성과 수동 merge부터 시작한다.

## 4. Enterprise ingest PoC

### 목표

Enterprise entitlement가 있는 조직에서 API Preview 기능으로 notebook/source lifecycle을 검증한다.

### 사전 질문

- 우리 계정과 region에서 Gemini Notebook Enterprise API가 실제로 사용 가능한가?
- 누가 Cloud project, IAM role, source ownership을 관리하는가?
- Drive/Docs/raw text 중 어떤 source type이 retention·compliance 정책에 맞는가?
- source 삭제·권한 회수·재처리 시 notebook에는 어떤 lifecycle이 필요한가?

> [!NOTE]
> 이 프로젝트는 consumer NotebookLM의 personal workflow를 대체하는 출발점이 아니다. 조직의 Cloud/IAM 운영 책임이 준비됐을 때만 진행한다.

## Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
