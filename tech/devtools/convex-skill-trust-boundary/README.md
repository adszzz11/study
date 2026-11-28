---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# Convex Quickstart Skills의 데이터 전송과 원격 코드 실행 신뢰 경계

> **한 줄 정의**: Convex onboarding용 agent skills의 앱 아이디어 전송, 원격 script 실행, safety classifier 회피 지시를 통해 투명성과 사용자 통제권의 경계를 살펴보는 사례다.

## Overview

사용자는 앱 초기 설정을 위임했지만, 인용된 skill은 외부 서비스로 아이디어를 보내거나 외부 응답을 로컬 코드로 실행한다. 목표에 대한 위임이 개별 데이터 전송과 실행 권한까지 포함하는지 살펴본다.

분석 근거는 Issue #64에 인용된 revision `6ca54f6`의 발췌와 작성자의 관찰이다. 이슈는 2026-10-26 작성되었고 제공 자료의 수집 화면에서는 Open이다. 현재 repository 상태, 서버 동작, 수정 여부는 확인되지 않았다.

| 관점 | 핵심 질문 |
|---|---|
| Data transparency | 어떤 데이터가 어디로 전송되는가? |
| Software supply chain | 실제 실행할 코드의 내용과 버전이 고정되는가? |
| Safety control | Harness의 판단을 수용하는가, 회피하도록 지시하는가? |

이 자료는 문제 소지가 있는 구현과 명시적 classifier 회피 지시의 보고를 뒷받침한다. 아이디어 도용, 악성 payload, 실제 피해를 입증하지는 않는다.

## Learning Path

- [ ] [[tech/devtools/convex-skill-trust-boundary/01-overview|Overview]] — 배경과 세 skill의 동작 파악
- [ ] [[tech/devtools/convex-skill-trust-boundary/02-ecosystem|구현 대안 비교]] — 편의성과 검토 가능성 비교
- [ ] [[tech/devtools/convex-skill-trust-boundary/04-learning/01-getting-started|시작하기]] — 네트워크 없이 data-flow tracing
- [ ] [[tech/devtools/convex-skill-trust-boundary/04-learning/02-deep-dive|Deep Dive]] — 권한과 실행 경계 분석
- [ ] [[tech/devtools/convex-skill-trust-boundary/05-projects|Projects]] — 안전한 onboarding 설계 연습
- [ ] [[tech/devtools/convex-skill-trust-boundary/cheatsheet|Cheatsheet]] — 검토 질문 빠르게 적용
- [ ] [[tech/devtools/convex-skill-trust-boundary/03-references|References]] — 근거와 미확인 사항 확인

## When To Use

- Agent skill 또는 plugin 도입 전에 데이터 흐름과 실행 권한을 검토할 때
- Remote bootstrap, telemetry, runbook 생성의 고지 범위를 설계할 때
- 명령 한 개가 아니라 여러 tool call의 전체 효과를 평가할 때

## When Not To Use

- 현재 Convex 제품 전체의 보안 수준이나 경쟁 제품 우열을 판단하는 근거로 사용할 때
- 실제 피해, 서버 저장 정책, 취약점 수정 완료를 입증하려 할 때
- 인용된 실행 흐름을 그대로 복사해 실행하는 안내서가 필요할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/convex-skill-trust-boundary/04-learning/02-deep-dive|데이터·코드·정책의 신뢰 경계 상세 분석]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64 — 이슈 및 인용된 skill 발췌
- https://thirtysix.github.io/awesome-agent-skills/#skills?q=convex — 이슈가 연결한 catalog; 내용은 추가 근거로 사용하지 않음
