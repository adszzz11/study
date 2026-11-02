---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# SkillSpector Cheatsheet

빠른 맥락은 [[tech/devtools/agent-skill-security-scanner/README|README]], 운영 판단은 [[tech/devtools/agent-skill-security-scanner/04-learning/02-deep-dive|심화 학습]]을 참조한다.

## Install / Scan

```bash
uv tool install git+https://github.com/NVIDIA/skillspector.git
skillspector scan ./my-skill --no-llm
skillspector scan ./skills --recursive --no-llm --format sarif --fail-on-incomplete
```

## Input Guardrails

| 입력 | 처리 |
| --- | --- |
| directory / `SKILL.md` | temporary skill directory로 정규화 |
| Git repository / HTTPS URL / ZIP | remote ingest 후 정규화 |
| remote/archive | 100 MiB ingest cap |
| ZIP | 10,000 member cap |

## Risk Bands

| Score | 권고 | 운영 action |
| ---: | --- | --- |
| 0–20 | `SAFE` | 다른 control 통과 후 설치 검토 |
| 21–50 | `CAUTION` | finding triage와 owner review |
| 51+ | `DO NOT INSTALL` | 차단, evidence 검토, remediation |

## 운영 원칙

- static-only baseline부터 시작하고 false positive를 기록한다.
- LLM semantic finding은 human-review lead이며 단독 차단 신호가 아니다.
- MCP HTTP transport는 loopback-only·무인증이므로 외부 노출 금지.
- runtime sandbox, egress control, signature 검증은 scanner와 별도다.

## Sources

- https://github.com/NVIDIA/skillspector
- https://docs.nvidia.com/skills/scanning-agent-skills
- https://openreview.net/pdf?id=rVAPXHmGHN
