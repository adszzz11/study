---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Atticus ecosystem

## 비교

| 제품/접근 | 주력 범위 | Atticus와의 관계·차이 |
|---|---|---|
| Atticus | 공시 문장의 evidence-backed verification, versioning, audit trail | Legal·IR·Finance의 최종 검증 단계에 특화 |
| Atticus Glide | 위 흐름의 agent-assisted first pass | 자동 승인 대신 human-in-the-loop와 materiality 중심 검토를 강조 |
| Workiva | connected reporting, linked data, SEC/XBRL, GRC·ESG | 작성·수치 연결·규제보고 범위가 더 넓다. IHG 사례에서는 Workiva로 drafting/data linking, Atticus로 기타 statement 검증을 병행했다. |
| DFIN / Toppan Merrill | SEC filing, EDGAR/XBRL production, disclosure distribution | 미국 규제 filing/제작 중심이다. Atticus는 filing engine보다 근거 기반 사실 검증에 가깝다. |
| Manual spreadsheet + email | 범용 협업 | 초기 도입은 쉽지만 evidence linkage, change propagation, role-based audit trail에 취약하다. |

## 선택 프레임

1. **작성과 수치 연결**이 병목이면 connected reporting suite를 먼저 평가한다.
2. **제출·배포**가 병목이면 filing production provider를 평가한다.
3. **문장별 사실성, evidence, 책임 추적**이 병목이면 Atticus를 중심으로 검토한다.
4. 이미 작성 플랫폼이 있다면 대체보다 release gate의 verification layer로 병행할 수 있다.

## 통합 시 주의점

- source-of-truth와 document version 식별자를 작성 시스템과 Atticus 사이에서 명확히 한다.
- verification completeness를 release 조건으로 정하되, suggestion acceptance를 자동 승인으로 취급하지 않는다.
- 외부 counsel·auditor에는 최소 권한과 reviewer 역할을 부여한다.

[[tech/ai/atticus-document-verification/05-projects|Projects]]의 disclosure-control integration 예시를 참고한다.

## Sources

- https://www.atticus.tech/uk/case-studies/ihg
- https://www.workiva.com/solutions/sec-reporting
- https://www.atticus.tech/au/verifying
