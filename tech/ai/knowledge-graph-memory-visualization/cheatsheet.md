---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: AI 메모리 그래프 점검표

## 개념 빠르게 구분하기

| 개념 | 핵심 의미 | 자동으로 따라오지 않는 것 |
|---|---|---|
| Node | 파일·출력물·엔터티 표현 | 안정적인 ID와 중복 제거 |
| Edge | 두 노드의 관계 표현 | 검증된 의미·인과관계 |
| Graph visualization | 사람이 연결 구조를 탐색 | graph database 사용 |
| Shared memory | 여러 클라이언트의 공통 메모리 구상 | 동일 맥락·최신성·답변 정확도 |
| Provenance | 원문·버전·생성 경로 추적 | 주장 자체의 진실성 |
| 조직도 | 부서와 에이전트 배치 표현 | 실행 권한·위임 제어 |

## 관계 패턴

```text
Output --근거로 사용--> File --언급--> Entity
Output --생성 주체--> Agent
Output --생성 실행--> Run
```

첫 줄은 학습용 관계 예시다. 나머지 두 줄은 운영 기록을 연결하기 위한 설계 제안이며 확인된 제품 schema가 아니다.

## 검토할 다섯 질문

- [ ] 연결선의 유형·방향·생성 기준을 설명할 수 있는가?
- [ ] 주장에 해당하는 원문 위치로 돌아갈 수 있는가?
- [ ] 갱신·삭제·상충 버전이 드러나는가?
- [ ] 출력물을 생성한 에이전트·실행 기록을 찾을 수 있는가?
- [ ] 규모가 커져도 필요한 관계를 찾을 수 있는가?

## 근거 수준 표시

- **요약에서 관찰:** 그래프·CRM·대시보드·조직도 화면.
- **제시된 구상:** Claude·Codex 등 여러 클라이언트의 공유 메모리.
- **미확인:** 저장 엔진, API·protocol, 검색, 동기화, 권한, 실행·성과.
- **설계 제안:** 본 노트의 schema, 충돌 정책, 프로젝트, 실험 방법.

## 탐색

[[tech/ai/knowledge-graph-memory-visualization/03-references|근거 범위]] · [[tech/ai/knowledge-graph-memory-visualization/README|전체 학습 경로]]

## Sources

- 사용자 제공 dossier: Orbit Agents 홍보 영상 요약. 원본 영상·제품 URL 미제공으로 직접 확인 불가.
- Obsidian 공식 사이트: https://obsidian.md/ — 비교 대상의 공식 진입점인 보조 자료이며 Orbit Agents 기능의 근거가 아니다.
- Obsidian Help: https://help.obsidian.md/ — 노트 작성·그래프 탐색을 추가 학습하기 위한 보조 자료. 본 노트의 제품 비교는 dossier 범위로 제한한다.
