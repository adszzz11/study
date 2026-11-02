---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — 시작하기: Domain Due Diligence

> [[tech/devtools/buildindex-domain-assessment/README|목차]] · [[tech/devtools/buildindex-domain-assessment/03-references|이전: References]] · [[tech/devtools/buildindex-domain-assessment/04-learning/02-deep-dive|다음: Deep Dive]]

## 목표

도메인이 복구되거나 새 제품 정보가 나타나더라도, 구매·credential 입력·private integration 전에 공식 주체와 데이터 처리 조건을 확인한다.

## 1. 증거 수집 범위 정하기

다음 항목별로 URL, 관찰 시각, 원문 또는 screenshot hash, 판정을 기록한다.

- domain ownership과 registrar/RDAP
- DNS record와 TLS certificate subject/issuer/validity
- redirect chain 및 official social/GitHub organization
- 법인명, support email, privacy policy, Terms
- 제품 문서, pricing, API, security/compliance statement

## 2. 도메인 확인 체크리스트

```text
[ ] DNS가 기대한 hostname/IP로 해석되는가?
[ ] HTTPS certificate의 subject/SAN과 발급자가 일관적인가?
[ ] redirect 최종 목적지가 공식 문서와 같은 운영 주체인가?
[ ] privacy policy와 Terms에 법인·연락처·효력일이 있는가?
[ ] GitHub organization과 공식 사이트가 상호 링크되는가?
```

한 출처가 아니라 최소 두 개의 독립적인 공식 채널에서 동일한 운영 주체를 확인한다. 정보가 충돌하거나 비어 있으면 `unverified`로 남기고 구매·연동을 중단한다.

## 3. 공개 URL 분석의 주의점

urlscan.io 같은 도구는 페이지가 요청한 DOM, 리소스, cookie, network activity를 조사할 수 있다. public scan의 가시성 정책을 읽고, staging URL, password reset URL, signed URL, query token이 포함된 URL은 제출하지 않는다.

## 4. 서비스 발견이 실제 목적일 때

목적이 조직 내 서비스 발견이면 검증 불가능한 도메인을 기다리지 말고, Backstage의 최소 catalog를 먼저 만든다.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: checkout-api
  description: Checkout API
  annotations:
    github.com/project-slug: acme/checkout-api
spec:
  type: service
  lifecycle: production
  owner: group:platform
  system: commerce
```

첫 단계에서는 `Component`, `System`, `Owner`, repository URL, documentation만 정확히 채운다. 예시는 Backstage의 일반 metadata 형식이며 `buildindex.dev`의 기능을 뜻하지 않는다.

## Sources

- https://docs.urlscan.io/about
- https://docs.urlscan.io/pages/faq
- https://backstage.io/docs/features/software-catalog/
