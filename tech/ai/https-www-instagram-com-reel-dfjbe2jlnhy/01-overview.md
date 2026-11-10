---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview — evidence-gated Reel study

[[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/README|README]]의 대상 Reel은 본 조사에서 원문 메타데이터와 media evidence를 확인할 수 없었다. 이 노트의 대상은 알려지지 않은 도구가 아니라, 그 공백을 다루는 연구 방식이다.

## What

**Evidence gate**는 최소 한 종류의 1차 입력이 수집되기 전까지 콘텐츠의 의미·저자·절차를 주장하지 않는 규칙이다.

| 입력 | 확인 가능한 것 | 한계 |
| --- | --- | --- |
| 캡션 | 작성자의 텍스트 주장, 링크 | 화면 데모를 증명하지 못함 |
| screenshot | UI, timestamp, 화면 문구 | 편집 전후·음성을 알 수 없음 |
| transcript | 발화한 주장·순서 | 화면 조작과 정확한 도구 버전은 불명 |
| 원본 media | 시간축의 화면·음성 | 권한·저작권·보관 정책 필요 |

## Why

짧은 영상은 맥락이 빠지고 편집될 수 있다. 추측을 채우면 tool name, 가격, 모델, workflow가 모두 허위 연결이 될 수 있다. W3C PROV의 entity–activity–agent 관점으로 무엇을 누구에게서 언제 받았는지 남기면 후속 검토와 수정이 가능하다.

## 특징

- **claim-level**: “영상은 X를 쓴다”가 아니라 증거와 연결된 한 문장만 기록한다.
- **source separation**: 작성자 원문, viewer capture, 연구자의 해석을 섞지 않는다.
- **revisable**: 새 증거가 오면 `draft`를 유지한 채 판정과 링크를 갱신한다.
- **permission-aware**: 로그인이 필요한 원문이나 private media의 접근 우회는 범위 밖이다.

다음: [[tech/ai/https-www-instagram-com-reel-dfjbe2jlnhy/04-learning/01-getting-started|시작하기]]

## Sources

- https://www.w3.org/TR/prov-overview/
- https://spec.c2pa.org/specifications/specifications/1.4/index.html
