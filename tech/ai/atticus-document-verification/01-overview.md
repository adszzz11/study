---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Atticus overview

## What

**Atticus**는 annual report, prospectus, investor presentation 등 critical document의 claim을 evidence와 연결해 검증하는 enterprise SaaS다. PDF 등의 문서에서 statement·paragraph·page를 검증 단위로 지정하고, 각 단위에 owner와 reviewer를 배정한다.

## Why

공시 문서는 Finance, Legal, IR, ESG 팀과 외부 자문사가 동시에 고친다. email, spreadsheet, tracked changes만으로 관리하면 다음 문제가 발생한다.

- 어느 문장이 누구의 책임인지와 source-of-truth가 분리된다.
- 새 버전에서 바뀐 내용을 기존 검증과 대조하기 어렵다.
- 감사 또는 board review 시 판단 근거와 승인 시점을 재구성해야 한다.

Atticus는 claim마다 evidence와 상태를 연결해 이 검증 과정을 work queue와 audit trail로 바꾼다.

## 핵심 특징

| 기능 | 검증 흐름에서의 역할 |
|---|---|
| Document ingestion / annotation | PDF를 올린 뒤 Auto-highlight 또는 manual boxing으로 검증 대상을 지정 |
| Assignment workflow | statement, paragraph, page 단위로 SME·Legal·Finance·외부 검토자를 배정 |
| Evidence graph | supporting evidence를 claim에 붙이고 Evidence Finder의 후보를 검토 후 채택 |
| Smart version control | 새 버전의 변경을 탐지하고 재사용 가능한 검증·근거를 이전 |
| Audit-ready output | 누가 언제 어떤 evidence로 검증했는지 담은 interactive verification report 생성 |
| Glide agent layer | materiality, annotation, owner, evidence, status의 first-pass suggestion 제공 |

## Glide와 human-in-the-loop

Glide의 공개된 first-pass 순서는 `scan → materiality assessment → annotation suggestion → owner suggestion → evidence pre-link → verification-status suggestion → review`다. 기본 비활성화와 workspace별 activation을 표방하며, 기존 권한을 승계하고 사용자 승인 전 자동 실행하지 않는다는 설명이다. 따라서 Glide는 decision-maker가 아니라 reviewer가 확인할 우선순위와 후보를 제안하는 controlled assistant로 평가해야 한다.

보안·배포 관점에서 Atticus는 AWS 기반, jurisdiction별 isolated environment, ISO/IEC 27001:2022 및 SOC 2 Type II attestation을 공개한다. Glide는 고객 데이터를 저장하거나 model training에 사용하지 않는다고 안내한다. 도입 전에는 실제 계약·보안 문서로 해당 범위와 적용 region을 확인한다.

## Next

- [[tech/ai/atticus-document-verification/04-learning/01-getting-started|시작하기]]에서 verification matrix를 먼저 만든다.
- [[tech/ai/atticus-document-verification/02-ecosystem|Ecosystem]]에서 작성·filing 도구와의 경계를 비교한다.

## Sources

- https://www.atticus.tech/au/verifying
- https://www.atticus.tech/glide
- https://www.atticus.tech/frequently-asked-questions
