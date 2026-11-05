---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver: Projects

[[tech/ai/cua-driver/README|Cua Driver 목차]] · [[tech/ai/cua-driver/cheatsheet|Cheatsheet]]

## 적용 아이디어

| 프로젝트 | 범위 | 핵심 안전장치 |
|---|---|---|
| legacy ERP/CRM 자동화 | 반복 입력과 PDF export | record allowlist, export 결과 검증, submit 승인 |
| desktop QA agent | 실제 화면 기반 UI regression 확인 | test account, step limit, screenshot/artifact 보관 |
| design/document workflow | GIMP·Inkscape·Office 초안 생성 | 원본 보존, save/export 전 human review |
| authenticated browser research | login된 Chrome에서 정해진 data를 CSV export | domain·field allowlist, download 승인 |
| hybrid automation | API/Playwright 이후 남은 GUI gap 처리 | GUI 단계를 최소화하고 fresh-state 검증 |

## 권장 구현 순서

1. API, MCP, Playwright로 대체 가능한 단계부터 제거한다.
2. GUI 단계별 expected state와 cancellation 조건을 명시한다.
3. 최소 권한 app/profile과 test data에서 pilot을 실행한다.
4. approval, audit log, 실제 결과 검증을 넣은 뒤 production 범위를 넓힌다.

## Sources

- https://cua.ai/docs/cua-driver
- https://cua.ai/docs/cua-driver/guides/permissions
- https://developers.openai.com/api/docs/guides/tools-computer-use
