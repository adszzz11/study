---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# ContextForge 개요

## What / Why

AI client가 각 tool과 agent에 직접 연결하면 서비스마다 인증, transport, schema와 오류 처리를 구현해야 한다. ContextForge는 Gateway 자체를 MCP server로 제공하고, backend 연결 및 API adaptation을 중앙화한다. 단순 server 목록을 넘어 분산된 기능을 client용 논리적 서비스로 구성하는 운영 계층이다.

## 개념 구조

아래는 논리적 요청 경로이며 내부 실행 순서를 확정한 그림이 아니다.

```text
AI / MCP Clients
        |
        v
ContextForge
  MCP interface / Virtual Servers
  Tools / Prompts / Resources registry
  Auth / Input validation / Call policies
  Protocol adaptation / Transport bridging / Plugins
  Logs / Metrics / OpenTelemetry traces
        |
        +-- MCP Servers
        +-- REST APIs
        +-- gRPC Services
        +-- A2A / External Agents
```

## Registry와 Virtual Server

| 객체 | 자료상 기능 | 의미 |
|---|---|---|
| Tools | Native/adapted tools, input validation, concurrency controls | 호출 단위 관리 |
| Prompts | Jinja2 templates, multimodal, rollback/versioning | 중앙 재사용·변경 관리 |
| Resources | URI, MIME detection, caching, SSE updates | 데이터 접근 및 변경 전달 |
| Virtual Server | 선택한 tool ID를 `associated_tools`에 지정 | client에 보이는 tool 구성과 물리 backend 분리 |

Client 접속 경로 예시는 `/servers/<UUID>/mcp`다. Tool을 묶는 기능 자체가 접근 권한 격리를 증명하지는 않는다.

## Adaptation과 Bridging

- **Protocol/API adaptation:** REST API·gRPC method를 MCP tool로 표현한다. REST adapter에는 JSON Schema extraction, custom auth, timeout·retry·rate-limit 정책이 설명된다.
- **Transport bridging:** MCP server의 stdio를 SSE 또는 Streamable HTTP로 노출한다. `mcpgateway.translate` 예제에는 `/sse`와 `/mcp` 동시 노출이 등장한다.
- gRPC translation은 server reflection 기반 discovery와 method introspection을 사용한다. 대상 서비스의 reflection 가용성을 확인해야 한다.
- MCP protocol version 선택과 transport 선택은 별개다. 자료의 `2025-11-25`는 protocol version 예시다.

## 운영 특징과 한계

- Basic, JWT, custom authentication, user-scoped OAuth tokens를 소개한다.
- `JWT_SECRET_KEY`, `AUTH_ENCRYPTION_SECRET`은 로컬 개발을 포함한 모든 환경에서 필수라고 명시되어 있다.
- OpenTelemetry tracing과 Phoenix·Jaeger·Zipkin·OTLP backend 연계를 설명한다.
- PyPI, OCI container, Kubernetes 배포 경로와 PostgreSQL·Redis·Nginx를 포함하는 Compose 구성이 제시된다.
- Redis-backed cache/session storage와 federation이 소개되지만 state replication·consistency·failover 방식은 확인되지 않는다.
- 40개 이상의 plugin 및 내장 Admin UI를 소개한다. 내장 UI에는 HTMX 2.0.3·Alpine.js가 명시된다. 별도 Web UI의 기술 구성은 발췌가 불완전하다.

TOON 압축률, routing 선택 정책, observability overhead는 확인되지 않았다. “7,000+ tests”와 비활성화 시 “zero-overhead”는 프로젝트 주장으로 취급한다.

## 다음 단계

[[tech/ai/mcp-context-forge-fe0ea4a7/02-ecosystem|아키텍처 대안 비교]] · [[tech/ai/mcp-context-forge-fe0ea4a7/README|학습경로로 돌아가기]]

## Sources

- https://github.com/IBM/mcp-context-forge — 제공된 repository 발췌 dossier의 원 출처.
- https://github.com/IBM/mcp-context-forge/blob/main/README.md — 설치·기능·배포 설명의 확인 지점. `main`은 변경될 수 있다.

> 근거는 제공된 dossier다. 저장소의 현재 상태, 명령 실행, 성능 및 보안은 직접 검증하지 않았다. 버전·수치·지원 범위는 발췌 시점의 프로젝트 설명이다.
