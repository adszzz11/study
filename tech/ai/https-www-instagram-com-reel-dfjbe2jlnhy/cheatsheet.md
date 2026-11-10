---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — evidence-first Reel research

[[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/README|README]]의 빠른 실행표다.

| 상황 | 행동 |
| --- | --- |
| Reel URL만 있다 | `insufficient evidence`로 기록, 주제 추정 금지 |
| caption을 받았다 | 원문·수집 시각·작성자 귀속을 기록 |
| screenshot을 받았다 | frame ID, crop/OCR 여부, 민감정보를 확인 |
| transcript를 받았다 | timestamp, 전사 방식, 불명확 발화를 표시 |
| 제품명이 보인다 | vendor 공식 문서로 이름·버전·기능을 대조 |
| 주장을 쓴다 | claim마다 evidence ID와 confidence를 연결 |
| 접근이 제한된다 | 우회하지 않고 자료 제공 또는 재조사를 요청 |

## 최소 기록 schema

```yaml
evidence_id: frame-003
source_url: https://www.instagram.com/reel/DfjBE2Jlnhy/
captured_at: 2026-11-10
artifact: screenshot
claim: null
confidence: not-assessed
```

상세 절차: [[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/04-learning/01-getting-started|시작하기]] · 출처: [[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/03-references|References]]

## Sources

- https://www.w3.org/TR/prov-overview/
- https://spec.c2pa.org/specifications/specifications/1.4/index.html
