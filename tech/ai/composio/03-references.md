---
date: 2026-07-19
tags: [tech]
type: tech-tool-study
status: draft
---

# Composio — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Reading Order

| 순서 | 자료 | 읽을 포인트 |
|---:|---|---|
| 1 | 공식 docs | 제품 범위와 quickstart 진입점 |
| 2 | How Composio works | Session, user, auth, state mental model |
| 3 | Configuring Sessions | allowlist, preload, connected account 선택 |
| 4 | Sessions vs direct execution | dynamic/fixed/direct 선택 기준 |
| 5 | Auth Configs / Connected Accounts | multi-tenant auth data model |
| 6 | Sessions via MCP | portability와 SDK hook trade-off |
| 7 | Custom tools | local extension과 execution boundary |
| 8 | Changelog / migration | pre-1.0 SDK와 abstraction 변화 확인 |

## Official Documentation

### Concepts and execution

- [Composio Docs](https://docs.composio.dev/docs) — 공식 문서 진입점
- [How Composio works](https://docs.composio.dev/docs/how-composio-works) — Session 중심 개념
- [Configuring Sessions](https://docs.composio.dev/docs/configuring-sessions) — tool access와 preload
- [Sessions vs direct execution](https://docs.composio.dev/docs/sessions-vs-direct-execution) — 실행 mode 비교
- [API Reference](https://docs.composio.dev/reference) — 현재 API surface와 toolkit catalog

### Authentication

- [Auth Configs](https://docs.composio.dev/reference/api-reference/auth-configs) — OAuth/API key blueprint
- [Connected Accounts](https://docs.composio.dev/docs/auth-configuration/connected-accounts) — user connection lifecycle

### MCP and extensions

- [Sessions via MCP](https://docs.composio.dev/docs/sessions-via-mcp) — Session별 hosted MCP endpoint
- [Custom tools and toolkits](https://docs.composio.dev/docs/extending-sessions/custom-tools-and-toolkits) — standalone/extension/custom toolkit

### Product history and migration

- [Introducing Tool Router (beta)](https://composio.dev/blog/introducing-tool-router-%28beta%29) — 2025-10 공개 배경
- [MCP servers to Sessions migration](https://docs.composio.dev/docs/migration-guide/mcp-servers-to-sessions) — Sessions 중심 abstraction으로 이동
- [Changelog](https://docs.composio.dev/reference/changelog) — SDK version과 breaking change 확인
- [GitHub repository](https://github.com/composiohq/composio) — MIT-licensed TypeScript/Python monorepo

## Version Snapshot

```yaml
observed_at: 2026-07-19
sdk_snapshot:
  python:
    package: composio
    version: 0.18.0
    changelog_date: 2026-07-16
  typescript:
    package: "@composio/core"
    version: 0.13.1
    release_window: 2026-06
catalog_claim: "1,000+ toolkits"
warning: "pre-1.0; pin versions and re-check changelog"
```

## Source Evaluation Notes

- 수량과 기능은 vendor 공식 표기이며 독립 benchmark가 아니다.
- 1,000+와 과거 500+ 표기는 조사 시점과 page update 차이로 해석한다.
- blog의 beta 설명보다 현재 docs와 migration guide를 우선한다.
- deprecated API가 검색 결과에 남을 수 있으므로 code sample의 version/date를 확인한다.
- pricing, quota, supported auth mode는 도입 직전 dashboard와 공식 page에서 다시 확인한다.

## Verification Checklist

- [ ] package lockfile에 실제 SDK version을 기록했다.
- [ ] 해당 version의 changelog와 migration guide를 읽었다.
- [ ] 필요한 toolkit의 current version과 action schema를 확인했다.
- [ ] managed/custom auth 지원 여부와 요구 scope를 확인했다.
- [ ] hosted MCP가 필요한 hook/custom tool을 우회하지 않는지 확인했다.
- [ ] source 확인 날짜를 architecture decision record에 남겼다.

## Sources

- https://docs.composio.dev/docs
- https://docs.composio.dev/reference
- https://docs.composio.dev/reference/changelog
- https://github.com/composiohq/composio
- https://composio.dev/blog/introducing-tool-router-%28beta%29
- https://docs.composio.dev/docs/migration-guide/mcp-servers-to-sessions

