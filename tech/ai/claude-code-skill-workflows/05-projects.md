---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects — 적용 패턴

## Evidence-backed market scout

세 worker가 고객 고충, 경쟁, 가격 근거를 각각 수집한다. judge는 중복을 제거하고 source별 신뢰도를 표시해 MVP 가설과 인터뷰 질문을 만든다. 시장 규모를 추정으로 채우지 말고, 모르는 부분은 interview backlog로 남긴다.

## PR quality gate

구현 agent와 security reviewer, test reviewer, API contract reviewer를 분리한다. CI 결과가 없거나 acceptance criterion을 충족하지 못한 변경은 merge 후보에서 제외한다.

## Large-repo context optimizer

`CODEMAP.md`, API contract 요약, 실패 테스트 추출, session handoff template을 만든다. 작업 전후 token/시간, 재시도 횟수, regression을 기록해 context 절약이 품질 저하로 이어지지 않는지 확인한다.

## Brand-aware frontend audit

현재 design token, 접근성 기준, 반응형 요구, 브랜드 reference를 입력으로 준다. “보라색 gradient·Inter·범용 카드 UI 금지” 같은 규칙은 출발점일 뿐이다. checklist와 screenshot review로 콘텐츠 hierarchy 및 브랜드 적합성을 검증한다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/cheatsheet|Cheatsheet]]

## Sources

- https://github.com/ANVEAI/idea-hunt-skill
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
