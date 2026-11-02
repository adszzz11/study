---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# BuildIndex.dev — Cheatsheet

> [[tech/devtools/buildindex-domain-assessment/README|목차]] · [[tech/devtools/buildindex-domain-assessment/05-projects|이전: Projects]]

## 상태 판단

| 신호 | 의미 | 다음 행동 |
|---|---|---|
| DNS 해석 실패 | service availability를 확인할 수 없음 | 공식 채널 확인 전 도입 보류 |
| 공식 docs/GitHub 없음 | 기능·운영 주체를 검증할 수 없음 | `unverified`로 기록 |
| 유사 이름 검색 결과 | lead일 뿐 동일성 증거가 아님 | domain·법인·certificate 대조 |
| privacy policy/Terms 없음 | 데이터 처리·계약 조건 불명 | credential·구매 중단 |
| public scan 필요 | 관찰 정보가 공개될 수 있음 | 민감 URL 제출 금지 |

## 도입 전 최소 증거

```text
[ ] Domain ownership / RDAP
[ ] DNS 및 TLS certificate
[ ] Official website와 redirect chain
[ ] Privacy policy / Terms / 법인 정보
[ ] Official GitHub organization 또는 product documentation
[ ] Security, retention, subprocessor, support contact
```

## IDP / Software Catalog 핵심 모델

```text
Component → System → Domain
     │
     ├─ owner
     ├─ repository
     ├─ documentation / runbook
     └─ on-call / lifecycle
```

## 기술스택 요약

- `buildindex.dev`의 실제 기술스택은 공개적으로 검증되지 않았다.
- 검증 가능한 대안인 Backstage는 TypeScript/Node.js 기반의 plugin-oriented developer portal이며 Git 기반 YAML catalog를 중심으로 동작한다.
- 상용 IDP는 Git, Kubernetes, CI/CD, cloud provider의 메타데이터를 수집해 service catalog를 구성한다.
- AI enrichment 사용 제품은 source code/documentation의 외부 전송, retention, 접근권한을 별도 보안 요건으로 평가한다.

## 빠른 결정

- **제품 검증 전**: 구매·credential·private integration 금지
- **서비스 발견이 목적**: Backstage catalog MVP부터 시작
- **SaaS 비교 중**: 같은 10개 서비스, 같은 보안 checklist로 평가
- **증거 부족**: 추측하지 말고 `insufficient evidence`로 종료

## Sources

- https://buildindex.dev/
- https://backstage.io/docs/features/software-catalog/
- https://docs.urlscan.io/pages/faq
