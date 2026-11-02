---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# SkillSpector 심화 학습

[[tech/devtools/agent-skill-security-scanner/04-learning/01-getting-started|시작하기]]의 static baseline 뒤에는 report policy와 delivery workflow를 설계한다.

## Finding Triage

1. CRITICAL/HIGH은 installation 또는 merge를 멈추고 evidence와 data flow를 검토한다.
2. MEDIUM은 security approval queue로 보내며, accepted risk의 근거와 expiry를 기록한다.
3. LOW는 baseline에 남기되 반복되는 rule은 skill author guidance로 전환한다.
4. optional LLM semantic finding은 description-behavior mismatch의 review lead로만 쓴다. LLM 결과 단독으로 차단하지 않는다.

Score는 executable script에 1.3× multiplier가 적용된 aggregate signal이다. imported module, helper function, cross-file flow를 놓칠 수 있는 lightweight taint 한계를 review에 반영한다.

## CI와 SARIF

```bash
skillspector scan ./skills \
  --recursive \
  --no-llm \
  --format sarif \
  --fail-on-incomplete
```

SARIF 2.1.0 output을 GitHub Code Scanning에 올리고, HIGH/CRITICAL은 merge block, MEDIUM은 reviewer approval로 연결한다. Semgrep·OSV-Scanner·TruffleHog는 parallel job으로 실행한다. 구체적 조합은 [[tech/devtools/agent-skill-security-scanner/02-ecosystem|Ecosystem]]을 참조한다.

## MCP Guardrail

`scan_skill()`은 onboarding/install workflow 앞단에 둘 수 있다. HTTP transport는 loopback-only 및 무인증이므로 외부에 노출하지 않는다. 별도의 authentication, network boundary, runtime sandbox는 운영 환경에서 추가로 강제한다.

## Sources

- https://docs.nvidia.com/skills/scanning-agent-skills
- https://openreview.net/pdf?id=rVAPXHmGHN
- https://owasp.github.io/www-project-agentic-skills-top-10/skill-scanner-integration.html
