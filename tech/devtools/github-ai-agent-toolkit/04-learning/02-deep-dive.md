---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 경계와 운영 검증

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 도구는 편리한 만큼 실행 경계가 중요하다.

## Harness와 credential boundary

- ECC의 rules, hooks, MCP server, commands를 설치 전에 분리해 검토한다.
- hook은 trigger, command, network destination, write scope, 실패 시 동작을 문서화한다.
- Agent-Reach의 로그인 session 재사용은 별도 browser profile과 secondary account로 격리한다.
- security-audit-skill은 명시적으로 허가된 own codebase에서 source-first evidence를 남기는 defensive audit에만 쓴다.

## Rendering과 media

HyperFrames는 `HTML/CSS/JS composition → preview → deterministic frame render → video` 순서다. 5–10초 product intro로 fonts, asset license, frame rate, render 재현성을 확인한다. VoiceStudio의 cloning·dubbing은 동의와 사용권이 확인된 음성만 대상으로 한다.

## Serving benchmark

DeepInfer는 vLLM/SGLang과 같은 환경에서 비교한다. model, quantization, batch, prompt length, GPU, driver를 고정하고 아래 지표를 기록한다.

| 지표 | 의미 |
|---|---|
| Prefill throughput | 입력 token 처리량 |
| Decode latency | 생성 token 지연 |
| GPU utilization | 병목과 비용 신호 |
| Error/retry rate | 운영 안정성 신호 |

실전 적용: [[tech/devtools/github-ai-agent-toolkit/05-projects|Projects]]

## Sources

- https://github.com/affaan-m/ECC
- https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md
- https://github.com/heygen-com/hyperframes/blob/main/docs/quickstart.mdx
- https://github.com/deepseek-ai/DeepInfer
