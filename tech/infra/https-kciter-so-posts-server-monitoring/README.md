---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 서버 모니터링 분석 가이드

> **한 줄 정의**: 서버 모니터링은 사용자 영향 지표와 시스템 내부 지표를 함께 관찰·상관분석하여 장애를 조기 탐지하고 원인을 좁히는 observability 실천이다.

## Overview

이 노트는 `CPU가 높다`는 원인 후보가 아니라 traffic·latency·error라는 사용자 증상에서 시작하는 분석법을 다룬다. Metrics, logs, traces를 공통 시간축과 metadata로 연결하고 SLI/SLO 및 error budget으로 정상 여부를 판단한다.

- [[01-overview|개요]]: symptom-first 관찰, 핵심 signal, capacity의 기본
- [[02-ecosystem|에코시스템]]: OSS·SaaS 선택지와 운영 trade-off
- [[03-references|참고 자료]]: 원문과 공식 문서

## Learning Path

- [ ] [[01-overview|Overview]] — observability와 분석 순서 이해
- [ ] [[02-ecosystem|Ecosystem]] — 환경에 맞는 backend와 collector 선택
- [ ] [[03-references|References]] — 공식 문서의 기준점 확인
- [ ] [[04-learning/01-getting-started|Getting started]] — RED/host/DB dashboard 구성
- [ ] [[04-learning/02-deep-dive|Deep dive]] — SLO, traces, saturation, incident 분석
- [ ] [[05-projects|Projects]] — 세 가지 실전 구축 과제 수행
- [ ] [[cheatsheet|Cheatsheet]] — PromQL과 장애 분류 빠른 참조

## When To Use

- 서비스의 latency, error rate, availability를 사용자 관점에서 관리할 때
- VM, container, Kubernetes, DB, cache, 외부 API 사이의 장애 원인을 좁힐 때
- alert fatigue를 줄이고 SLO 기반 대응·release gate를 만들 때

## When Not To Use

- 일회성 batch의 성공·실패만 확인하면 충분하고 장기 지표 분석이 필요 없을 때
- 수집할 signal·보존 기간·cardinality의 비용 한계가 전혀 정의되지 않았을 때
- 개인정보와 비밀값을 redaction 없이 logs/traces로 전송하려는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Infra]]
- [[kubernetes/README|Kubernetes]]

## Sources

- https://kciter.so/posts/server-monitoring-analysis-guide/
- https://sre.google/sre-book/service-level-objectives/
- https://opentelemetry.io/docs/
- https://prometheus.io/docs/introduction/overview/
