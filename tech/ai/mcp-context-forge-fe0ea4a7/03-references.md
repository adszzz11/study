---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 관리

## 자료 범위

이 study는 사용자가 제공한 repository 발췌 dossier를 정리한 것이다. 외부 링크를 실시간 확인하거나 설치·부하 테스트를 수행한 결과가 아니다. 원문 dossier는 ecosystem 비교 표 중간에서 종료된다.

## 원문 확인 경로

| 확인 대상 | 출처 | 읽을 때 확인할 항목 |
|---|---|---|
| 프로젝트 범위 | https://github.com/IBM/mcp-context-forge | Gateway·registry·proxy 역할 |
| 기능 및 설치 안내 | https://github.com/IBM/mcp-context-forge/blob/main/README.md | Python, secrets, 배포 방식, transport |
| 버전 고정 | https://github.com/IBM/mcp-context-forge/releases | 실습에 쓸 release와 변경 사항 |

Release 페이지는 버전 고정을 위한 후속 확인 경로이며 이 노트의 기능 주장을 검증한 자료로 사용하지 않았다. 재현 시 tag 또는 commit SHA와 확인 날짜를 기록한다.

## 사실·주장·분석 구분

| 구분 | 예시 | 취급 |
|---|---|---|
| 발췌에 명시된 기능 | Virtual Server, reflection, 필수 secrets | 해당 시점 문서상의 기능 |
| 프로젝트 수치·표현 | 40+ plugins, 7,000+ tests, zero-overhead | 독립 측정이 없는 주장 |
| 구조에서 도출한 분석 | 중앙 장애 지점과 credential 관리 부담 | 도입 검토 가설 |
| 미확인 | 권한 격리 세부, header 우선순위, failover | 실험·원문 확인 필요 |

## 후속 확인 질문

- 선택 버전에서 production arm64 지원과 image architecture는 무엇인가?
- `X-Upstream-Authorization`과 관리 credential의 우선순위·검증 규칙은 무엇인가?
- Virtual Server별·사용자별 접근 제한은 어떻게 집행되는가?
- Retry 대상 오류, timeout 범위, 중복 실행 방지 방식은 무엇인가?
- TOON 적용 조건·압축률과 agent routing 기준은 무엇인가?
- Federation의 state consistency와 failover 책임은 어디에 있는가?

## 관련 노트

[[tech/ai/mcp-context-forge-fe0ea4a7/04-learning/02-deep-dive|검증 실험 설계]] · [[tech/ai/mcp-context-forge-fe0ea4a7/README|학습경로]]

## Sources

- https://github.com/IBM/mcp-context-forge — 제공된 repository 발췌 dossier의 원 출처.
- https://github.com/IBM/mcp-context-forge/blob/main/README.md — 설치·기능·배포 설명의 확인 지점. `main`은 변경될 수 있다.

> 근거는 제공된 dossier다. 저장소의 현재 상태, 명령 실행, 성능 및 보안은 직접 검증하지 않았다. 버전·수치·지원 범위는 발췌 시점의 프로젝트 설명이다.
