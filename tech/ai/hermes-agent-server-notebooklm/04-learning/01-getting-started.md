---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started — 첫 Study Note를 NotebookLM으로 옮기기

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

- Hermes가 만든 학습 결과를 operational memory와 분리한다.
- 검토 가능한 Study Note를 주제별 Google Doc으로 발행한다.
- NotebookLM에서 Drive source를 연결하고 source-grounded 질문을 한다.
- 자동 동기화·권한·import 제약을 확인한다.

## 1. Hermes memory write에 승인 경계 두기

설정에서 `memory.write_approval: true`를 켠다. agent가 추측이나 일회성 세부 정보를 permanent memory에 기록하기 전에 사람이 검토할 수 있게 하기 위함이다.

```yaml
# 개념 예시 — 실제 설정 키와 위치는 설치한 Hermes version의 문서를 확인한다.
memory:
  write_approval: true
```

승인할 대상은 반복되는 사용자 선호, 검증된 안정적 사실, 다음 session에도 필요한 작업 규칙이다. 긴 조사 결과·원문 인용·오답은 Study Note로 보낸다.

## 2. Drive 문서 구조 만들기

Google Drive에 `Hermes Learning/` folder를 만들고, 학습 주제마다 Google Doc 하나를 만든다. 예: `2026-09_RAG-evaluation`.

문서 첫머리에 다음 metadata를 넣는다.

```markdown
# RAG Evaluation — Study Note

Updated: 2026-09-20
Scope: RAG 평가 지표와 실험 설계의 기초
Version: 0.1
Sensitivity: internal / personal
Confidence: medium

## Source URLs
- https://example.org/original-paper

## Open questions
- retrieval relevance와 answer faithfulness를 어느 실험에서 분리할까?
```

## 3. Hermes의 결과를 Study Note로 변환하기

다음 template으로 초안을 요청한다. 중요 원칙은 **source 사실과 Hermes의 해석을 같은 문장으로 섞지 않는 것**이다.

```markdown
## Claims
### Claim: <검증 가능한 한 문장>
- Evidence: <source가 말한 사실의 요약>
- Source: <원문 URL>
- Confidence: high | medium | low

### Hermes interpretation
- <연결, 비교, 가설. source의 직접 주장인지 아닌지 표시>

## Questions / mistakes
- <복습 질문 또는 이전에 틀린 이해>

## Next actions
- [ ] <재검증하거나 추가로 읽을 항목>
```

발행 전 URL이 실제 원문인지, claim이 source보다 강하게 말하지 않는지, secret·개인정보가 없는지 검토한다. 수정한 Markdown을 Google Doc 본문으로 옮기거나 승인된 Drive publishing workflow로 갱신한다.

## 4. NotebookLM에 Drive source 연결하기

1. NotebookLM에서 새 notebook을 만든다.
2. **Add source**에서 Google Drive의 해당 Google Doc을 선택한다.
3. source 제목과 문서 상단의 `Updated`/`Scope`를 대조한다.
4. Drive source의 auto-sync가 계정에 제공되는지 확인한다.
5. 문서를 한 번 수정한 후 NotebookLM source에 변경이 반영되는지 관찰한다.

첫 질문은 source를 벗어난 창작을 요구하기보다 다음처럼 근거를 확인하는 방식으로 한다.

```text
이 노트의 Claim을 Confidence 순서대로 표로 정리하고,
각 항목에 원문 URL과 아직 남은 Open question을 붙여줘.
```

## 5. 복습 산출물 만들기

NotebookLM에서 다음 산출물을 한 개씩 만든 뒤, 틀리거나 부족했던 내용을 Google Doc의 `Questions / mistakes`에 되돌려 적는다.

- claim 간 차이를 묻는 Q&A
- terminology를 구분하는 quiz
- 5분짜리 briefing 또는 Audio Overview
- 다음 읽을 자료를 정하는 open-question 목록

## 완료 체크리스트

- [ ] `memory.write_approval`의 동작을 설치한 Hermes version에서 확인했다.
- [ ] Drive에 주제별 Google Doc 하나를 만들었다.
- [ ] `Updated`, `Scope`, `Source URLs`, `Confidence`, `Open questions`를 본문에 넣었다.
- [ ] source 사실과 Hermes interpretation을 구분했다.
- [ ] NotebookLM에 Drive source를 추가했다.
- [ ] 문서 변경 후 동기화와 source 접근 권한을 확인했다.
- [ ] NotebookLM 결과에서 발견한 오해를 원문 노트에 기록했다.

## Troubleshooting

| 증상 | 먼저 확인할 것 |
|---|---|
| source가 갱신되지 않음 | auto-sync 제공 여부, 원본 Google Doc 변경 여부, 잠시 후 재확인 |
| source에 접근할 수 없음 | Drive permission, 파일 삭제·이동, notebook과 동일한 Google account |
| 인용이 NotebookLM에 안 보임 | footnote/comments가 아닌 문서 본문에 URL과 맥락을 넣었는지 |
| 답변이 모호함 | 한 문서의 scope가 넓은지, claim/evidence 구조와 source URL이 있는지 |
| agent memory가 비대해짐 | durable preference/fact만 승인하고 연구 기록은 Study Note로 이동 |

## Sources

- https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
- https://support.google.com/gemininotebook/answer/16215270?co=GENIE.Platform%3DDesktop&hl=en-6
- https://workspaceupdates.googleblog.com/2026/05/keep-your-sources-up-to-date-with-automatic-Drive-syncing-in-NotebookLM.html
