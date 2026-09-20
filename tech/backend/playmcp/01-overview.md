---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# PlayMCP Overview

## What

PlayMCP는 카카오가 운영하는 MCP 기반 개방형 플랫폼이다. 개발자는 Remote MCP server를 등록하고 실제 대화에서 Tool의 선택과 입출력을 시험한다. 사용자는 등록된 Tool을 Toolbox에 담아 외부 AI client에서 쓴다.

MCP server가 노출할 수 있는 기본 단위는 다음과 같다.

| 단위 | 의미 | PlayMCP에서의 중심성 |
|---|---|---|
| Tools | model이 실행하는 함수; JSON Schema input을 가짐 | 핵심 사용 사례 |
| Resources | client가 읽을 수 있는 데이터·문서 | server 설계에 따라 제공 |
| Prompts | 재사용 가능한 prompt template | 보조적 인터페이스 |

## Why

MCP 자체는 protocol이지 marketplace, 인증 대행, 테스트 환경은 아니다. 따라서 개발자는 다음을 별도로 다루게 된다.

- 어디에 server를 배포하고 client가 발견하게 할지
- 자연어 요청이 올바른 Tool과 schema를 선택하는지
- 사용자 동의, OAuth callback, token lifecycle을 어떻게 연결할지
- client별 endpoint 설정과 여러 Tool의 조합을 어떻게 줄일지

PlayMCP는 Catalog와 Preview로 발견·검증을, Toolbox로 선택한 Tool의 묶음을, Kakao account 기반 흐름으로 연결 경험을 제공한다.

## Key Characteristics

- **Catalog + playground**: 카카오 및 외부 개발자의 MCP server를 찾아보고 대화로 검증한다.
- **Toolbox aggregation**: 사용자가 선택한 MCP Tool을 하나의 연결점으로 관리한다.
- **Auth mediation**: 카카오 기술 설명에 따르면 PlayMCP는 OAuth 2.0 Client로서 Authorization Code Grant와 PKCE를 지원한다. server 운영자는 자신의 Authorization Server에 client를 등록하고 필요한 정보를 제공한다.
- **Kakao-native surface**: 나와의 채팅방, 톡캘린더, 카카오맵, 선물하기, 멜론 같은 서비스 연결이 초기 강점이다.
- **Remote connection**: 공개 connector 정보는 `https://playmcp.kakao.com/mcp`와 `streamable-http`를 안내한다. endpoint·OAuth·client 호환성은 연결 시점의 제품 문서로 재확인한다.

## Architecture

```text
MCP server developer
  └─ HTTPS Remote MCP server 배포·등록
       └─ PlayMCP (Catalog / Preview / Auth client / Toolbox)
            ├─ Kakao account 인증
            └─ 선택 Tool을 단일 Remote endpoint로 노출
                 └─ AI client → tools/list → tools/call → 원 server
```

## Sources

- [카카오 베타 발표](https://www.kakaocorp.com/page/detail/11674)
- [카카오 기술 블로그 — PlayMCP 개발](https://tech.kakao.com/posts/734)
- [MCP Server specification](https://modelcontextprotocol.io/specification/2025-06-18/server)
- [PlayMCP connector 정보](https://www.tooljunction.io/mcp/playmcp)
