---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# References

| 자료 | 용도 |
| --- | --- |
| [Clairic model page / API schema](https://developers.cloudflare.com/workers-ai/models/clairic/) | input/output schema, model ID, 제한 확인 |
| [Clairic 출시 Changelog — 2026-10-19](https://developers.cloudflare.com/changelog/post/2026-10-19-clairic-workers-ai/) | Preview 상태와 출시 맥락 |
| [Cloudflare 기술 블로그: System One extraction model](https://blog.cloudflare.com/clairic-extraction-model/) | architecture, cascade, benchmark 주장 |
| [Workers AI Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) | 최신 token 과금 확인 |
| [Workers AI Limits](https://developers.cloudflare.com/workers-ai/platform/limits/) | runtime·request 제한 확인 |
| [Workers AI Bindings](https://developers.cloudflare.com/workers-ai/configuration/bindings/) | `env.AI.run()` 설정 |
| [AI Gateway와 Workers AI 통합](https://developers.cloudflare.com/ai-gateway/usage/providers/workersai/) | gateway 연결 방식 |
| [AI Gateway observability](https://developers.cloudflare.com/ai-gateway/observability/) | request log·비용·cache 관찰 |
| [Clef model page](https://developers.cloudflare.com/workers-ai/models/clef/) | decision model과의 역할 분리 |

## 읽는 순서

1. model page에서 실제 API schema를 먼저 확인한다.
2. changelog와 blog로 Preview 제약 및 설계 의도를 읽는다.
3. pricing·limits·binding 문서로 production guardrail을 정한다.
4. Gateway 문서로 request-level observability와 retry/caching policy를 설계한다.

## Sources

- https://developers.cloudflare.com/workers-ai/models/clairic/
- https://developers.cloudflare.com/workers-ai/platform/pricing/
