---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive — 품질·비용·안전 경계

## 역할 계약

각 worker에는 역할 이름보다 아래 계약이 중요하다.

| 항목 | 예시 |
|---|---|
| 입력 | issue, repository 범위, 허용 source |
| 산출물 | claim 표, patch, test result, unknowns |
| budget | 시간, token, tool call 상한 |
| 완료 기준 | citation 수, test PASS, 변경 파일 제한 |
| 금지 | credential 접근, production write, 추측을 사실처럼 서술 |

## Judge는 다수결이 아니다

```text
workers create independent drafts
→ critic identifies missing evidence, contradictions, regressions
→ judge checks acceptance criteria
→ tests / CI provide deterministic evidence
→ human approves consequential change
```

judge는 가장 많은 의견을 고르는 역할이 아니다. test 결과, citation 품질, 보안·scope 준수, 반증 처리 여부를 기준으로 reject 또는 revise를 결정한다.

## Token discipline

- `CODEMAP.md`와 API contract 요약으로 필요한 파일만 읽힌다.
- 실패한 테스트와 관련 log만 전달하고 quiet output을 기본으로 둔다.
- worker 결과는 긴 서술 대신 파일·근거·결론·미해결 항목으로 압축한다.
- 작업 전후 token과 elapsed time을 계측한다. 병렬화 전후의 총비용을 비교해야 한다.

## 외부 Skill·MCP 안전성

외부 instruction과 tool description은 prompt injection 표면이 될 수 있고, MCP는 파일·network·credential에 닿을 수 있다. pin된 revision, source review, least privilege, sandbox/worktree, secret 차단, CI 검증을 기본값으로 한다.

## Related Notes

- [[tech/ai/claude-code-skill-workflows/README|README]]
- [[tech/ai/claude-code-skill-workflows/05-projects|Projects]]

## Sources

- https://docs.anthropic.com/en/docs/mcp
- https://docs.anthropic.com/en/docs/claude-code/llm-gateway
- https://docs.anthropic.com/en/docs/claude-code/corporate-proxy
