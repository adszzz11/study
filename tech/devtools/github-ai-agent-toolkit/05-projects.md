---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 도구를 한꺼번에 도입하지 않고 경계가 작은 프로젝트로 검증한다.

## Internal Agent Starter Kit

Ponytail + Taste Skill + Cloudflare security audit을 CI/PR review checklist에 연결한다. 성공 기준은 small diff, visual regression, evidence가 있는 finding이며, hook·plugin upgrade owner를 지정한다.

## Private AI Gateway

FreeLLMAPI를 localhost 또는 VPN 내부에 배포한다. provider health check, budget, fallback policy를 코드와 runbook으로 관리하며, secret backup은 암호화·접근 통제를 분리한다.

## Research Copilot

Agent-Reach의 read-only channel로 YouTube transcript, GitHub issue, public web evidence를 수집한다. 로그인 계정, browser profile, credential lifecycle을 별도로 관리하고 인용 URL을 결과와 함께 저장한다.

## Marketing Video Pipeline

HyperFrames로 landing page 기반 editable product video를 만들고 VoiceStudio로 narration/dubbing을 후처리한다. source asset 사용권과 voice consent를 release checklist에 둔다.

## Model-serving Benchmark Lab

DeepInfer를 vLLM/SGLang과 분리된 동일 환경에서 비교한다. prefill throughput, decode latency, GPU utilization, 비용을 표준 workload로 측정한다.

빠른 점검: [[tech/devtools/github-ai-agent-toolkit/cheatsheet|Cheatsheet]]

## Sources

- https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/README.md
- https://github.com/heygen-com/hyperframes/blob/main/docs/introduction.mdx
- https://github.com/debpalash/VoiceStudio/releases
- https://github.com/deepseek-ai/DeepInfer
