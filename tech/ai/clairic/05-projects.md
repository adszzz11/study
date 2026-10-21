---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## 1. Invoice / expense ingestion

PDF OCR 결과에서 vendor, invoice ID, due date, line item, total을 추출해 accounting staging table에 적재한다.

- span viewer로 finance reviewer가 근거를 확인한다.
- line item은 code로 합산해 total과 대조한다.
- high-value invoice, low confidence, null critical field만 review queue로 보낸다.

## 2. Support-claims automation

ticket에서 order ID·damage·amount를 추출하고, Clef가 refund/repair/escalation을 정한다. LLM은 결정과 근거를 바탕으로 고객용 응답 초안을 만든다. 실제 refund는 policy engine과 사람 승인으로 분리한다.

## 3. Compliance evidence extraction

계약서·정책 문서에서 expiry, jurisdiction, obligation, source span을 뽑는다. 낮은 confidence뿐 아니라 고위험 obligation은 confidence와 무관하게 법무 검토로 보낸다.

## 4. Operations signal normalization

incident note·CSV·dashboard export에서 metric과 timestamp를 추출한다. 단기 forecast는 alert triage의 보조 신호로 쓰고, alert 발생·해소 기록으로 false positive와 calibration을 평가한다.

## 5. Document-review UX

structured result와 원문 span을 동시에 보여준다. reviewer의 accept/edit/reject 결과를 저장해 schema 개선과 regression corpus에 사용한다. 원문 보존 정책과 접근 제어는 문서 민감도에 맞춰 설계한다.

## 공통 평가 지표

| 지표 | 질문 |
| --- | --- |
| Field accuracy | field 값이 ground truth와 일치하는가? |
| Evidence validity | span이 실제 근거를 가리키는가? |
| Review precision | queue로 보낸 문서가 실제 오류를 잘 포착하는가? |
| Latency/cost | 기존 pipeline 대비 요청 시간과 비용이 개선됐는가? |
| Downstream safety | 잘못된 값이 write/action으로 새지 않았는가? |

## Sources

- https://blog.cloudflare.com/clairic-extraction-model/
- https://developers.cloudflare.com/workers-ai/models/clairic/
