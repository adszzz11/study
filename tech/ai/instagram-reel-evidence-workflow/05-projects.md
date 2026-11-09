---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

## Mini project: Reel claim audit

입력은 사용자가 제공한 캡처, 자막, 또는 전사본 하나다. 목표는 영상의 내용을 창작하는 것이 아니라, 검증 가능한 주장 목록을 만드는 것이다.

- `evidence/`: 원본 파일명, 수신 시각, SHA-256 (민감 원본은 저장하지 않음)
- `frames/`: 인용한 frame의 ID와 timestamp
- `transcript.md`: 사람이 교정한 전사와 불명확 구간
- `claims.md`: claim ledger와 공식 URL
- `report.md`: 확인됨·반박됨·판단 불가의 분리

### 완료 기준

- 모든 claim에 영상 위치가 있거나 `영상 근거 없음`으로 표시된다.
- 기능 claim마다 공식 1차 URL이 있거나 `insufficient`로 표시된다.
- 독자가 원본 접근 권한 없이도 결론의 한계를 이해할 수 있다.

작업 중에는 [[tech/ai/instagram-reel-evidence-workflow/cheatsheet|Cheatsheet]]를 사용한다.
