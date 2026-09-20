---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# ByteByteGo

> **한 줄 정의**: ByteByteGo는 Alex Xu 중심의 System Design, distributed systems, AI engineering 학습 및 인터뷰 준비 콘텐츠 플랫폼이다.

## Overview

ByteByteGo는 대규모 backend를 설계할 때 필요한 **trade-off 설명 능력**을 기르는 데 초점을 둔다. 단일 정답을 외우기보다 요구사항, scale, latency, consistency, cost, failure handling을 함께 검토하는 방식을 시각 자료와 사례로 전달한다.

- 무료 newsletter와 guide로 핵심 컴포넌트를 빠르게 훑는다.
- 책과 interview prep 자료로 문제 풀이 구조를 익힌다.
- live cohort와 녹화 자료로 AI evals, production AI systems 같은 최신 주제를 확장한다.
- 공개 자료는 ByteByteGo 제품 자체의 서비스 인프라가 아니라, **ByteByteGo가 가르치는 instructional/system-design architecture**를 설명한다.

| 문서 | 목적 |
| --- | --- |
| [[01-overview]] | What/Why와 콘텐츠·학습 구조 이해 |
| [[02-ecosystem]] | 대안과 사용 맥락 비교 |
| [[03-references]] | 공식·보조 출처 모음 |
| [[04-learning/01-getting-started]] | 첫 설계 연습 시작 |
| [[04-learning/02-deep-dive]] | distributed systems와 AI track 심화 |
| [[05-projects]] | 구현 가능한 프로젝트 목록 |
| [[cheatsheet]] | 인터뷰·설계 점검표 |

## Learning Path

- [ ] [[01-overview|What/Why와 4-step interview framework]]를 읽고 학습 목표를 정한다.
- [ ] [[04-learning/01-getting-started|Getting Started]]에서 `HTTP → load balancing → cache → database → queue → CDN` 흐름을 한 바퀴 학습한다.
- [ ] URL shortener를 한 장의 diagram으로 설계하고 estimate를 적는다.
- [ ] [[04-learning/02-deep-dive|Deep Dive]]에서 consistency, retry, idempotency, DLQ를 failure scenario와 함께 연습한다.
- [ ] RAG 설계에 evaluation, observability, prompt-injection 방어를 추가한다.
- [ ] 45분 mock interview를 진행하고 [[cheatsheet]]로 회고한다.

## When To Use

- system design interview의 답변 구조와 대표 backend 컴포넌트를 빠르게 연결하고 싶을 때
- visual diagram과 사례를 시작점으로 storage, cache, queue의 선택 근거를 설명하고 싶을 때
- 전통적인 distributed systems 학습에서 production AI engineering까지 학습 범위를 넓힐 때

## When Not To Use

- 특정 클라우드 서비스의 운영 절차나 vendor API의 정확한 설정을 배워야 할 때
- storage engine, replication, stream processing의 이론을 깊게 파고드는 것이 최우선일 때 — *Designing Data-Intensive Applications* 같은 원전도 병행한다.
- 구현 검증 없이 interview pattern만 암기하려는 경우 — 작은 프로젝트와 failure test를 함께 수행한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Backend]]
- [[tech/backend/http/README|HTTP]]
- [[01-overview]]
- [[cheatsheet]]

## Sources

- https://blog.bytebytego.com/
- https://bytebytego.com/guides/system-design-blueprint-the-ultimate-guide/
- https://live.bytebytego.com/
- https://blog.bytebytego.com/p/ep46-step-by-step-guide-on-system
