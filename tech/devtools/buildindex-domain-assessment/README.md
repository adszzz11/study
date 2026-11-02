---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — 공개 정보·서비스 상태 조사

> **한 줄 정의**: `buildindex.dev`는 2026-11-03 기준 DNS 해석과 공개 웹 인덱싱이 확인되지 않아 제품 기능을 검증할 수 없는 미확인 developer-tool 도메인이다.

## Overview

이 노트는 제품 소개가 아니라 공개 정보 기반의 due diligence 기록이다. 공식 웹사이트, 문서, GitHub organization, API, 운영사, 라이선스, 가격 및 보안 정책을 확인할 수 없으므로 기능이나 도입 적합성을 추정하지 않는다.

- 확인된 별도 서비스: 호주의 `buildindex.com.au`는 NSW 주택 건설업체 비교·compliance 정보를 다루는 proptech이며, `.dev`와 동일 서비스라는 증거가 없다.
- 비교 기준선: 조직 내 서비스 발견 문제에는 Internal Developer Portal (IDP) / Software Catalog가 검증 가능한 대안 범주다.
- 도입 원칙: 운영 주체와 공식 채널이 검증되기 전에는 구매, credential 입력, private repository 연동을 진행하지 않는다.

## Learning Path

- [ ] [[tech/devtools/buildindex-domain-assessment/01-overview|Overview]] — 확인된 사실, 불확실성, 조사 범위
- [ ] [[tech/devtools/buildindex-domain-assessment/02-ecosystem|Ecosystem]] — IDP/Software Catalog 대안 비교
- [ ] [[tech/devtools/buildindex-domain-assessment/04-learning/01-getting-started|시작하기]] — domain due diligence 순서
- [ ] [[tech/devtools/buildindex-domain-assessment/04-learning/02-deep-dive|Deep Dive]] — catalog 품질과 보안 평가
- [ ] [[tech/devtools/buildindex-domain-assessment/05-projects|Projects]] — 검증 및 catalog MVP 과제
- [ ] [[tech/devtools/buildindex-domain-assessment/03-references|References]] — 공식 문서와 원문 URL
- [ ] [[tech/devtools/buildindex-domain-assessment/cheatsheet|Cheatsheet]] — 판단 기준 빠른 참조

## When To Use

- 출처가 불명확한 developer-tool 도메인을 구매·연동 전에 검증할 때
- “서비스 발견” 요구를 IDP 또는 Software Catalog로 재정의할 때
- SaaS catalog의 source-code scanning, AI enrichment, data egress를 security review에 포함할 때

## When Not To Use

- 현재 상태만으로 `buildindex.dev`의 기능, 가격, 보안 수준을 확정해야 할 때
- 이름이 유사한 `buildindex.com.au`를 `.dev` 도메인의 운영사 또는 제품이라고 가정할 때
- 공개 scan 결과만으로 private 환경의 안전성을 보장하려 할 때

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/backstage-io/README|Backstage.io]]

## Sources

- https://buildindex.dev/
- https://backstage.io/docs/features/software-catalog/
- https://docs.urlscan.io/about
- https://docs.urlscan.io/pages/faq
