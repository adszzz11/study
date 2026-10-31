---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive — Memory, Provenance, Automation Boundary

> [[01-getting-started|이전: Getting Started]] · [[../README|목차로 돌아가기]] · [[../05-projects|다음: Projects]]

## 1. 세 종류의 상태를 섞지 않기

| 상태 | 질문 | 저장 위치 | 갱신 방식 |
|---|---|---|---|
| Working context | 지금 task를 끝내려면 무엇이 필요한가? | current session/context | task 종료 시 축소 또는 폐기 |
| Agent memory | 다음 session에도 agent가 알아야 하는 안정적 사실은? | Hermes memory 또는 external provider | 승인된 write와 retrieval |
| Study knowledge | 사람이 무엇을 근거와 함께 배우고 재검토할 것인가? | Google Doc → NotebookLM source | human-reviewed publishing |

이 구분이 무너지면 두 가지 오류가 생긴다. 첫째, agent memory에는 인용과 노이즈가 쌓여 retrieval이 흐려진다. 둘째, NotebookLM source에는 검증 전 추론이 섞여 source-grounded 답변의 신뢰성이 낮아진다.

## 2. provenance-first 문서 설계

Study Note는 요약문만으로 끝내지 않는다. claim마다 출처와 판단의 경계를 남긴다.

```markdown
## Claim register

| ID | Claim | Evidence | Source URL | Confidence | Status |
|---|---|---|---|---|---|
| C-01 | ... | source의 직접 진술 요약 | https://... | high | verified |

## Hermes interpretation
- I-01: C-01과 C-02를 연결한 가설. 추가 검증 필요.

## Change log
- 2026-09-20: C-01 URL 재확인, confidence를 medium → high로 변경.
```

`Evidence`에는 source가 직접 말한 범위를 요약한다. `Hermes interpretation`에는 source 간 연결, 비교, 추측을 넣는다. NotebookLM에게 질문할 때에도 “source가 직접 뒷받침하는 부분”과 “해석”을 구분해 달라고 요청한다.

## 3. 동기화와 version을 운영하는 법

Google Drive auto-sync가 있어도 notebook은 revision history를 대신하지 않는다. 다음 규칙을 둔다.

- Google Doc 상단의 `Updated`와 `Version`을 갱신한다.
- 주장 변경은 `Change log`에 이유와 영향을 기록한다.
- source URL이 사라지거나 내용이 바뀌면 claim confidence를 낮추고 재검토한다.
- notebook에서 만든 quiz/briefing의 오류는 문서의 `Questions / mistakes`에 환류한다.
- source에 대한 Drive access와 notebook access는 정기적으로 점검한다.

## 4. automation boundary

### 개인 학습: 승인형 publishing

가장 작은 안전한 자동화는 Hermes가 **draft만 생성**하고 사람이 publish를 승인하는 흐름이다.

```text
Hermes research
  → generate_draft(topic, sources)
  → preview_diff(doc)
  → human approval
  → publish_approved(doc_id, revision)
```

MCP adapter를 만들면 tool은 대상 Drive folder와 Doc ID를 allowlist하고, write operation에는 preview와 confirmation을 요구한다. token, Drive OAuth credential, 민감한 원문을 log나 note에 남기지 않는다.

### 조직 자동화: Enterprise API

Gemini Notebook Enterprise는 API로 notebook과 source를 만들 수 있지만 Preview이며 Cloud project, IAM, region, data handling을 설계해야 한다. consumer NotebookLM을 자동화하는 것처럼 가정하지 말고, 먼저 product entitlement와 API availability를 확인한다.

## 5. Hermes API Server의 노출 경계

Hermes는 tool을 실행할 수 있으므로 API Server가 곧 terminal/file/web 권한의 경계가 될 수 있다.

| 제어 | 목적 |
|---|---|
| loopback binding | local client만 endpoint에 닿게 함 |
| Bearer key | 무단 요청 차단 |
| 좁은 CORS | 예상한 browser origin만 허용 |
| 최소 tool surface | Drive publishing 등 필요한 MCP tool만 연결 |
| 승인형 write | memory와 document 업데이트를 사람 검토에 둠 |
| audit/redaction | secret과 개인정보가 기록·전송되지 않게 함 |

> [!WARNING]
> Drive publishing을 자동화한다고 해서 NotebookLM의 답변을 자동으로 사실로 채택하면 안 된다. 답변은 source를 읽는 보조 산출물이며, source와 원문을 다시 확인하는 절차를 유지한다.

## Sources

- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md
- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory-providers
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources
