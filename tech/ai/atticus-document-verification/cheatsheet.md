---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Atticus cheatsheet

## 핵심 모델

```text
Document → Statement → Owner → Evidence → Verification status → Audit trail
```

## 용어

| 용어 | 실무 의미 |
|---|---|
| Verification unit | 검증·배정·승인할 최소 대상: statement, paragraph, page |
| Materiality | 오류·누락이 투자자, 규제, 의사결정에 미칠 중요도 |
| Evidence graph | 하나 이상의 근거를 claim에 연결하는 관계 |
| Smart version control | 새 버전의 변경을 식별해 재검토 대상을 좁히는 흐름 |
| Evidence Finder | evidence 후보를 찾는 AI-assisted search; 채택은 사람이 결정 |
| Glide | annotation·owner·evidence·status의 first-pass suggestion layer |

## Release gate

- [ ] material claim마다 owner와 reviewer가 지정되었다.
- [ ] evidence의 entity, period, calculation이 claim과 일치한다.
- [ ] changed statement는 재검토되었거나 재사용 근거가 기록되었다.
- [ ] open / overdue / exception 항목에 disposition이 있다.
- [ ] AI suggestion과 human approval이 구분된 audit trail이 있다.

## 빠른 판단

| 필요 | 우선 검토 |
|---|---|
| claim별 증빙·책임·감사 이력 | Atticus |
| 작성·linked data·SEC/XBRL·GRC | Workiva 등 connected reporting suite |
| EDGAR/XBRL 제출 제작·배포 | DFIN / Toppan Merrill 등 filing provider |

설계 순서는 [[tech/ai/atticus-document-verification/04-learning/01-getting-started|시작하기]], 심화 통제는 [[tech/ai/atticus-document-verification/04-learning/02-deep-dive|Deep Dive]]를 참고한다.

## Sources

- https://www.atticus.tech/au/verifying
- https://www.atticus.tech/glide
