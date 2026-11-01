---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# 심화: 권한·비동기 발행·복구

[[tech/devtools/instagram-ai-publishing/README|README]] · [[tech/devtools/instagram-ai-publishing/04-learning/01-getting-started|시작하기]]

## OAuth와 최소 권한

Uplika의 remote MCP는 API key를 대화에 붙여 넣는 대신 OAuth 2.1 + PKCE authorization으로 연결한다. 필요한 scope는 역할에 따라 최소화한다.

| Scope | 용도 |
|---|---|
| `accounts:read` | 연결 가능한 account 확인 |
| `posts:read` | post 상태와 insight 조회 |
| `posts:write` | draft·예약·발행 생성 |
| `offline_access` | 승인된 세션의 장기 접근 |

## approval payload

발행 직전에 agent가 아래 항목을 사람이 읽을 수 있는 형식으로 출력하고, 명시적 승인 문자열 또는 UI 동작을 요구하게 한다.

```text
account: @brand
target: Instagram Reel + YouTube Short
media: /approved/video.mp4
caption: 418 chars
scheduledAt: 2026-11-04T09:30:00+09:00
approval: required
```

Instagram은 text-only post를 지원하지 않는다. caption은 최대 2,200자, carousel은 2–10 media, Reel은 video 1개라는 제약을 발행 전 검증한다. 게시 후 edit API 제약도 있으므로 승인은 되돌릴 수 없는 경계다.

## 비동기 lifecycle

`publish` 성공 응답은 최종 게시 완료가 아니다. `get_post`를 polling해 `published` 또는 `failed` 상태와 URL을 확인한다. 실패 시 전체 작업을 중복 실행하지 말고 실패한 target만 `retry_post`한다.

```text
draft → scheduledAt 또는 publish → processing
                                    ↓
                         get_post polling
                           ↙            ↘
                    published + URL     failed → retry target
```

예약 시에는 `scheduledAt`에 timezone offset을 반드시 넣는다. 서버의 기본 timezone에 의존하면 의도한 현지 시각과 달라질 수 있다.

## Sources

- https://uplika.com/en/docs/agent-publish
- https://uplika.com/en/docs/instagram
- https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro
