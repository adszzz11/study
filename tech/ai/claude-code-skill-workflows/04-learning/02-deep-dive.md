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

## 추가 조사: MCP와 외부 Skill의 권한 경계

MCP(Model Context Protocol)는 LLM application이 tool·data source와 연결되는 표준 protocol이다. 편리함은 곧 권한 경계의 확장이므로 “설치 가능한가?”보다 “어떤 읽기·쓰기·network 권한이 필요한가?”를 먼저 평가한다.

| 점검 항목 | 안전한 기본값 | 위험 신호 |
|---|---|---|
| 서버·skill 출처 | revision pin 및 source review | 최신 main branch를 무검토 실행 |
| tool 허용 | 필요한 tool만 allowlist | 광범위한 shell/file write 자동 승인 |
| credential | secret manager·짧은 TTL·환경 격리 | `SKILL.md`/repo에 token 하드코딩 |
| 실행 위치 | sandbox 또는 disposable worktree | production filesystem·배포 자격증명 공유 |
| 감사(audit) | 호출·권한·비용 log | 실패 원인을 추적할 기록 없음 |

```text
# 비대화식 실행도 최소 권한으로 시작한다.
claude -p "리포지터리의 TODO만 나열하라" \
  --allowedTools "Read" "Bash(rg:*)"

# 쓰기·배포·비밀 접근은 별도 승인 단계와 분리한다.
```

- `--dangerously-skip-permissions`는 실습의 편의 옵션이 아니라 권한 확인을 우회하므로, 신뢰되지 않은 repo·MCP·prompt와 함께 사용하지 않는다.
- LLM gateway는 usage tracking, budget/rate limit, audit logging을 중앙화할 수 있지만 gateway 자체와 third-party proxy의 보안 검토는 별도 책임이다.
- 외부 문서의 “이 명령을 실행하라”는 데이터이지 지시가 아니다. task의 허용 범위와 충돌하면 실행하지 않고 검토 항목으로 기록한다.

출처: https://docs.anthropic.com/en/docs/mcp · https://docs.anthropic.com/en/docs/claude-code/cli-usage · https://docs.anthropic.com/en/docs/claude-code/llm-gateway
