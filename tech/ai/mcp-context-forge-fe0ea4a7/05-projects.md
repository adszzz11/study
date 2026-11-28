---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 도입 가설을 검증하는 PoC

아래 프로젝트는 실행 제안이며 완료한 작업이 아니다. Synthetic data와 읽기 전용 tool부터 시작한다.

## 1. 업무별 Virtual Server

- **가설:** 여러 backend의 tool을 업무별로 구성하면 client 설정이 단순해진다.
- **구현:** 두 test MCP backend를 등록하고 필요한 tool만 선택해 Virtual Server 하나를 만든다.
- **완료 기준:** 목록·정상 호출·제외 tool 접근 결과를 기록하고 직접 연결 구성과 비교한다.
- **산출물:** 물리 backend ↔ tool ID ↔ Virtual Server 매핑과 권한 검증표.

Tool grouping과 authorization은 별도로 평가한다.

## 2. 기존 API를 MCP로 제공

- **가설:** 기존 contract를 유지하면서 REST/gRPC 기능을 AI client에 제공할 수 있다.
- **구현:** 읽기 전용 REST endpoint 하나를 adaptation한다. gRPC는 reflection 가능한 test service가 있을 때 별도 실험한다.
- **완료 기준:** 정상·누락 필드·잘못된 타입·upstream 오류의 결과가 원 API 의미와 일치한다.
- **산출물:** 원 contract와 MCP schema 비교표, tool 설명 개선안, timeout·retry 관측 기록.

## 3. 인증 및 Trace 운영 실험

- **가설:** 중앙 Gateway에서 장애 위치와 credential 경계를 설명할 수 있다.
- **구현:** 두 test 사용자와 mock upstream, OTLP backend를 연결한다.
- **완료 기준:** 사용자별 접근 결과, header/credential 적용 결과, timeout trace를 재현한다.
- **산출물:** 인증 matrix, 민감정보를 제거한 trace 예시, 장애 복구 기록.

## 도입 판단표

| 판단 질문 | 남길 증거 |
|---|---|
| Client 구성이 실제로 줄었는가? | 직접 연결 대비 설정 비교 |
| 변환 후 호출 의미가 유지되는가? | Contract별 입출력 결과 |
| 접근 제어를 설명할 수 있는가? | 사용자·tool별 허용/거부 결과 |
| 중앙 운영 부담을 감당하는가? | 장애 영향, 복구 시간, 운영 담당 |
| 관측 비용이 수용 가능한가? | 동일 부하의 latency·자원 사용 비교 |

[[tech/ai/mcp-context-forge-fe0ea4a7/04-learning/01-getting-started|최소 실습]] · [[tech/ai/mcp-context-forge-fe0ea4a7/04-learning/02-deep-dive|검증 항목]] · [[tech/ai/mcp-context-forge-fe0ea4a7/README|학습경로]]

## Sources

- https://github.com/IBM/mcp-context-forge — 제공된 repository 발췌 dossier의 원 출처.
- https://github.com/IBM/mcp-context-forge/blob/main/README.md — 설치·기능·배포 설명의 확인 지점. `main`은 변경될 수 있다.

> 근거는 제공된 dossier다. 저장소의 현재 상태, 명령 실행, 성능 및 보안은 직접 검증하지 않았다. 버전·수치·지원 범위는 발췌 시점의 프로젝트 설명이다.
