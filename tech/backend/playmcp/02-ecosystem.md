---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# PlayMCP Ecosystem

## Comparison

| 대상 | 주된 역할 | 강점 | PlayMCP가 더 적합한 경우 |
|---|---|---|---|
| **PlayMCP** | 한국형 catalog·연결·테스트·Toolbox | Kakao account, Kakao services, 카카오톡/Kakao Tools 경로 | 카카오 서비스 연동·국내 사용자 agent·카카오 생태계 배포 |
| **Official MCP Registry** | vendor-neutral server metadata registry | 표준 중심의 공개 발견성, 사업자 종속 완화 | 전 세계 공개 server를 표준 metadata로 배포·검색 |
| **Glama** | registry + Inspector + hosting/gateway | tool-level 탐색, browser Inspector, gateway, access control | 운영 gateway·관측성·다양한 공개 connector가 중심 |
| **직접 MCP 배포** | `stdio` 또는 자체 remote endpoint | auth, infra, data residency를 완전 통제 | 내부망·강한 규제·platform dependency 최소화 |

## Decision Guide

```text
Kakao 서비스/카카오톡 사용자가 핵심인가? ─ 예 → PlayMCP
                                        └ 아니오
표준 registry 발견성이 우선인가? ─ 예 → Official MCP Registry
운영 gateway·감사·hosting이 필요한가? ─ 예 → Glama 등 gateway
내부망 또는 규제가 최우선인가? ─ 예 → 직접 MCP 배포
```

이 선택지는 배타적이지 않다. 예를 들어 server는 표준 MCP로 구현하고, public metadata는 Registry에, 카카오 사용자 경험은 PlayMCP에 제공할 수 있다. 단, Tool 설명·schema·OAuth redirect URI가 배포 표면마다 달라지는지 확인해야 한다.

## Trade-offs

- PlayMCP는 사용자 연결과 카카오 서비스 사용성을 낮추지만, platform의 client 정책·연결 방식 변화 영향을 받는다.
- 직접 배포는 통제가 크지만 discovery, 인증 UX, observability를 직접 운영해야 한다.
- registry는 metadata 발견을 돕지만 실행 gateway나 사용자 인증을 자동으로 해결하지 않는다.

## Sources

- [Official MCP Registry 문서](https://registry.modelcontextprotocol.io/docs)
- [Glama MCP Gateway](https://glama.ai/mcp/gateway)
- [카카오 — 도구함 기능](https://www.kakaocorp.com/page/detail/11817)
- [MCP Server specification](https://modelcontextprotocol.io/specification/2025-06-18/server)
