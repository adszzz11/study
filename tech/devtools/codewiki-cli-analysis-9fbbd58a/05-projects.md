---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 적용 아이디어

확인된 조회 기능에 기반한 제안이며 완성된 통합 기능을 뜻하지 않는다.

| 프로젝트 | 흐름 | 검증할 결과 |
|---|---|---|
| 저장소 onboarding assistant | 질문 → sections → 관련 content → 설명 | 질문과 관련된 문서만 읽었는가 |
| Architecture 조사 | 여러 저장소 검색 → 구조 섹션 선택 → 비교 | 선택 근거·문서 갱신 시점 기록 |
| Agent context budget 실험 | 전체·섹션·chunk 읽기 비교 | 입력량·응답 시간·누락 정도 |
| 문서 갱신 관찰 | refresh 전후 목록·본문 비교 | ID 변경과 내용 변경 구분 |

## 첫 프로젝트: onboarding assistant

1. 답할 질문을 정한다. 예: “이 저장소의 요청 처리 구조는 무엇인가?”
2. `search`로 대상을 찾고 `sections`에서 관련 제목·요약·anchor를 선택한다.
3. 선택한 ID로 `content`를 읽고 필요하면 `--chunks`로 나눈다.
4. 문서 근거와 추론을 구분해 설명하고 중요한 결론은 소스로 확인한다.
5. 저장소명·조회 시각·refresh 여부·선택한 제목·ID·근거를 기록한다.

완료 기준은 질문에 답하는 설명, 섹션 선택 근거, 구현 확인이 필요한 항목을 함께 남기는 것이다. 숫자 ID만 기록하면 갱신 뒤 근거를 추적하기 어렵다.

## 자동화 전 검토

우선 개인용 탐색과 Agent 보조에 적용한다. 중요한 자동화에는 undocumented RPC 실패 처리, cache 갱신 정책, wiki 미제공 시 대체 경로를 확인한 뒤 도입한다. 실패 시 소스 직접 읽기로 전환하는 흐름도 검토한다.

관련: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/02-deep-dive|실험 설계]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/02-ecosystem|대안 비교]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
