---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 공유 메모리 평가

## 용어 빠른 구분

| 용어 | 핵심 질문 |
|---|---|
| Shared memory | 여러 클라이언트가 무엇을 함께 읽고 쓰는가? |
| Knowledge graph | 정보·관계의 의미와 근거는 무엇인가? |
| Provenance | 답변을 원본까지 추적할 수 있는가? |
| Freshness | 어떤 버전의 정보를 언제 조회했는가? |
| Entity resolution | 같은 이름의 대상을 올바르게 구분하는가? |
| Agent operations | 실행·권한·성과를 증거로 확인하는가? |

## 최소 검증 순서

- [ ] 지원 클라이언트와 연결 절차를 공식 자료에서 확인
- [ ] A가 기록한 결과를 저장소에서 확인
- [ ] B가 원본 재입력 없이 기록 조회
- [ ] 원본 수정 후 변경과 이전 출력물 상태 식별
- [ ] 답변에서 원본까지 출처 추적
- [ ] 중복·모순·동시 수정 처리 관찰
- [ ] 부서별 허용·차단 접근 확인
- [ ] 도구 결과와 대시보드 집계 대조

```text
판정 = 통과 / 실패 / 미검증
기록 = 항목 + 기대 결과 + 관찰 결과 + 근거 + 시각 + 버전
```

## 피해야 할 추론

| 관찰 | 입증되지 않는 것 |
|---|---|
| 노드와 연결선이 보임 | Graph DB·GraphRAG 사용 |
| Claude·Codex 이름이 등장 | 실제 연결·상호 쓰기·갱신 전파 |
| 부서별 조직도가 보임 | 접근 통제 강제 |
| 성과 지표가 보임 | 성공률의 정확성·산출 근거 |

## 기술스택 요약

- 클라이언트: Claude·Codex가 공통 메모리에 연결되는 구상이며 실제 연동 방식은 미확인이다.
- 메모리 표현: 파일·출력물·엔터티를 연결된 노드로 표시하며 저장 DB·검색 기술은 자료에 없다.
- 운영: Lead Finder·Email Outreach Agent, CRM, 성과 대시보드, 부서별 조직도가 소개된다.
- 도입: 읽기·쓰기·갱신·출처·실행 결과를 먼저 검증한다.

## 연결

[[tech/ai/shared-ai-client-memory/README|학습 안내]] · [[tech/ai/shared-ai-client-memory/03-references|근거와 자료 공백]] · [[tech/ai/shared-ai-client-memory/04-learning/01-getting-started|실험 절차]]

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·게시일·제품 버전은 제공되지 않았다.
- 출처 URL: 미제공. 제품 이름만으로 공식 사이트나 영상을 추정해 기재하지 않는다.
- 아래 실습·평가 기준은 dossier에서 도출한 학습 제안이며, 제품의 검증된 기능이나 공식 사용법이 아니다.
