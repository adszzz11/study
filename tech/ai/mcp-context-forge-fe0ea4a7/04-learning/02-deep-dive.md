---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive: 경계와 운영 검증

## 1. 인증 경계를 분리한다

```text
Client -- Gateway 인증 --> ContextForge -- upstream credential --> Backend
```

Basic·JWT·custom auth 지원과 user-scoped OAuth tokens가 소개된다. 이 기능 목록만으로 모든 backend에서 동일한 권한 모델이 보장되지는 않는다.

`X-Upstream-Authorization`의 unconditional support가 명시되어 있지만, 관리자 credential과의 우선순위·검증 규칙은 발췌에 없다. 격리된 test backend로 아래를 확인한다.

| 실험 | 확인할 결과 |
|---|---|
| Gateway 인증 없음·만료 | 거부 위치와 오류 응답 |
| 사용자 A/B가 같은 tool 호출 | Backend에 전달되는 주체와 credential |
| 관리자 credential + 사용자 header | 실제 적용 credential과 정책 |
| 다른 Virtual Server/tool 접근 시도 | 목록 노출과 실행 권한을 각각 검증 |

## 2. 변환의 의미를 검증한다

- REST schema extraction 후 required·enum·오류 응답의 의미가 유지되는지 확인한다.
- gRPC reflection 가능 여부를 먼저 확인하고 method introspection 결과를 원본 contract와 비교한다.
- Agent가 tool 설명을 보고 올바른 호출을 선택하는지 별도 평가한다.
- 변경 작업은 retry로 중복 실행될 수 있는지 확인하고 backend idempotency 전략과 연결한다. 이는 검증 항목이며 현재 구현의 실패를 주장하는 것은 아니다.
- `mcpgateway.translate`의 stdio → `/sse`, `/mcp` bridging과 REST/gRPC adaptation을 혼동하지 않는다.

## 3. Observability를 연결한다

OpenTelemetry traces를 Phoenix·Jaeger·Zipkin 또는 OTLP backend로 연결하는 구성이 소개된다. Tool·prompt·resource·Gateway operation 및 federation 간 distributed tracing, token usage·cost·model performance 지표가 설명된다.

1. 정상 요청, schema 오류, upstream timeout을 각각 만든다.
2. Gateway·adapter·upstream 중 오류 위치를 trace에서 식별한다.
3. Tool별 latency·오류율을 관찰하고 backend 지표와 비교한다.
4. 활성화 전후 부하를 같은 조건에서 측정한다.
5. Credential과 민감한 payload가 telemetry에 포함되는지 확인한다.

지원 지표별 수집 조건과 overhead는 미확인이다. “zero-overhead”를 측정값으로 인용하지 않는다.

## 4. 확장 배포를 검토한다

Redis-backed cache/session storage, PostgreSQL, Nginx, federation이 소개되지만 multi-cluster consistency·state replication·failover 설계는 발췌에서 확인되지 않는다.

- Gateway·Redis·DB·upstream 장애를 개별 주입하고 영향과 복구 시간을 기록한다.
- 다중 instance에서 session과 설정이 어떻게 보이는지 확인한다.
- Plugin 도입 전 실행 권한, 실패 시 동작, latency 영향을 검증한다.
- Guardrails라는 소개를 특정 prompt-injection 방어·DLP·정책 언어 지원으로 확대 해석하지 않는다.

## 산출물

버전·구성·기대 결과·관측 결과·판정·미해결 질문을 한 표로 남긴다. 성능·보안·복구 보증은 측정 범위를 넘어서 주장하지 않는다.

[[tech/ai/mcp-context-forge-fe0ea4a7/05-projects|프로젝트로 검증하기]] · [[tech/ai/mcp-context-forge-fe0ea4a7/03-references|근거와 확인 질문]] · [[tech/ai/mcp-context-forge-fe0ea4a7/README|학습경로]]

## Sources

- https://github.com/IBM/mcp-context-forge — 제공된 repository 발췌 dossier의 원 출처.
- https://github.com/IBM/mcp-context-forge/blob/main/README.md — 설치·기능·배포 설명의 확인 지점. `main`은 변경될 수 있다.

> 근거는 제공된 dossier다. 저장소의 현재 상태, 명령 실행, 성능 및 보안은 직접 검증하지 않았다. 버전·수치·지원 범위는 발췌 시점의 프로젝트 설명이다.
