---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — Overview

> [[tech/devtools/buildindex-domain-assessment/README|목차]] · [[tech/devtools/buildindex-domain-assessment/02-ecosystem|다음: Ecosystem]]

## What

`buildindex.dev`는 조사일(2026-11-03) 기준 제품으로 식별·검증할 수 없는 도메인이다. 로컬 DNS 조회에서 hostname resolution이 실패했고, 공개 웹 접근 및 정확한 도메인 검색 결과도 확인되지 않았다. 따라서 이것을 build system, code indexer, software catalog 중 하나로 분류할 근거가 없다.

## Why

도메인명은 제품 성격의 증거가 아니다. 공식 채널을 확인하지 않은 채 SSO, source repository, cloud account, API token을 연결하면 다음 위험이 생긴다.

- 유사 명칭 서비스 또는 phishing domain에 credential을 제공할 수 있다.
- 데이터 처리자, retention, subprocessors, incident contact를 알 수 없다.
- 라이선스·가격·지원 SLA가 없어 procurement와 운영 책임을 평가할 수 없다.

## 확인된 상태와 미확인 영역

| 영역 | 조사 결과 |
|---|---|
| Public website | 접근 불가 |
| DNS | 2026-11-03 로컬 확인에서 해석 실패 |
| Search footprint | 정확한 도메인 검색 결과 없음 |
| 공식 문서 / GitHub / API | 확인 불가 |
| 운영사 / 라이선스 / 가격 | 확인 불가 |
| 보안·개인정보 처리 | 확인 불가 |
| 동명 서비스 | `buildindex.com.au`는 별도 proptech 서비스 |

## 특징 및 아키텍처

현재 `buildindex.dev` 자체에 대해 공개적으로 검증된 기능이나 아키텍처는 없다. 빈 칸을 일반적인 catalog 제품의 특징으로 채우지 않는 것이 이 조사에서 가장 중요하다.

반면 검증 가능한 Software Catalog는 보통 Git의 metadata YAML을 source of truth로 삼아 `Component`, `System`, `Owner`와 관계를 표현한다. 이 접근의 예시는 [[tech/devtools/backstage-io/README|Backstage.io]]이며, `.dev` 도메인의 구현 증거는 아니다.

## 다음 검증 순서

1. domain ownership, 등록기관 RDAP, DNS record와 TLS certificate를 확인한다.
2. redirect chain, certificate subject/issuer, privacy policy, Terms가 같은 운영 주체를 가리키는지 확인한다.
3. 공식 GitHub organization, 법인 정보, support contact를 상호 대조한다.
4. 제품이 확인된 뒤에만 권한 범위가 작은 sandbox PoC를 검토한다.

공개 URL 분석은 DOM, 요청 리소스, cookie, network activity를 기록할 수 있다. 그러나 public scan은 URL과 관찰 정보의 노출을 만들 수 있으므로 private URL·tokenized URL에는 사용하지 않는다.

## Sources

- https://buildindex.dev/
- https://docs.urlscan.io/about
- https://docs.urlscan.io/pages/faq
- https://www.linkedin.com/company/build-index
