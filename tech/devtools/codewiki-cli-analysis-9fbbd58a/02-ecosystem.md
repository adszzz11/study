---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: CodeWiki와 Agent 사이의 조회 계층

## 작업 방식 비교

특정 경쟁 제품의 기능을 추정하지 않고, 제공된 README에 드러난 작업 방식만 비교한다.

| 접근 | 읽기 흐름 | codewiki-cli의 의미 | 검토점 |
|---|---|---|---|
| 전체 문서 읽기 | 전체 본문 확보 후 탐색 | 목록·본문 분리로 context 조절 | 최초 fetch는 full wiki |
| 수동 발췌 | 사람이 검색·복사 | 반복 조회를 터미널 명령으로 구성 | 섹션 선택 판단은 필요 |
| 소스 직접 읽기 | 구현을 따라 분석 | 문서를 이해의 출발점으로 활용 | 구현 검증은 별도 |
| 자체 문서 생성 pipeline | 소스 처리 후 문서 생성 | 기존 CodeWiki 문서 조회에 집중 | 자체 생성 기능 미확인 |
| Agent skill | 설치한 skill에서 CLI 사용 | 다른 프로젝트에 built CLI 배포 | 변경 후 bundle 갱신 필요 |

## 선택 기준

문서 탐색 비용을 줄이려면 먼저 `sections`의 제목·요약이 질문을 해결할 만한지 판단한다. 정확성이 중요한 결론은 소스로 검증한다. CodeWiki에 문서가 없거나 RPC가 바뀌는 경우를 고려해 소스 직접 읽기 같은 대체 경로를 둔다.

이 도구의 차별점은 문서 생성 능력이 아니라 **탐색 순서·출력 범위·cache 재사용**이다. Context 절약 정도와 응답 속도는 실험해야 하며 성능 향상 수치는 제공되지 않았다.

다음: [[tech/devtools/codewiki-cli-analysis-9fbbd58a/04-learning/01-getting-started|시작하기]] · [[tech/devtools/codewiki-cli-analysis-9fbbd58a/README|학습 진입점]]


## Sources

- https://github.com/miinhho/codewiki-cli — 제공된 dossier의 README 기반 정리. 실습 및 성능 검증은 미실행.
