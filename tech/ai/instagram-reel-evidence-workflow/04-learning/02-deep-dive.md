---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep dive — provenance와 주장 검증

## Claim ledger

주장마다 다음 형식을 유지한다.

```text
C-01: [검증할 정확한 주장]
영상 근거: E-03, 00:12, frame-012.png
1차 근거: [공식 문서 URL]
판정: supported | contradicted | insufficient
검토일: YYYY-MM-DD
```

## 검증 순서

1. 영상이 실제로 그 주장을 했는지 frame/자막으로 확인한다.
2. 제품의 공식 문서·release note에서 기능 존재와 조건을 확인한다.
3. 데모와 일반 제공 기능을 구분한다. preview, region, plan, API/GUI 조건을 기록한다.
4. 증거 파일의 hash, 도출된 frame, 전사본 간의 관계를 남긴다. W3C PROV의 entity·activity·agent 개념은 이 관계를 설명하는 데 유용하다.

원본에 개인 정보가 있으면 공개 vault에는 원본을 넣지 말고, 필요한 최소 인용과 비식별화된 관찰만 남긴다. 결과는 [[tech/ai/instagram-reel-evidence-workflow/05-projects|Projects]]의 패키지 형식으로 정리한다.
