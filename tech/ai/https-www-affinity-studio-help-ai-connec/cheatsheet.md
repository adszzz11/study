---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Affinity AI Connector Cheatsheet

## 설정 경로

```text
Claude Desktop
Customize/Settings → Connectors → Browse connectors → Affinity → Install

Affinity
Settings → Model Context Protocol → Enable MCP server
```

두 앱과 테스트용 `.af` 문서를 모두 연 상태에서 연결을 확인한다.

## 연결 확인

```text
Can you see the Affinity MCP server?
현재 active document와 selection의 요약만 알려 줘. 아무것도 수정하지 마.
```

## Prompt 공식

```text
Target: [active document / selected artboards / selected curves]
Scope: [바꿀 object와 property]
Invariant: [절대 바꾸지 않을 것]
Plan: 먼저 변경 계획과 count를 보여 주고 기다릴 것
Output: [path / format / naming / overwrite policy]
Verification: [created / skipped / failed count와 오류]
```

## 자주 쓰는 Prompt

### Rename

```text
선택된 artboard 안의 unnamed layer만 `{artboard}-{role}-{index}`로 rename해.
먼저 old → new mapping과 충돌을 보여 주고 승인 전에는 실행하지 마.
```

### Export

```text
선택된 artboard만 PNG로 export해. 출력은 `./exports`로 제한하고
`{artboard}-{width}x{height}.png`를 사용해. 기존 파일은 덮어쓰지 마.
먼저 filename preview를 보여 줘.
```

### Non-destructive adjustment

```text
원본 object를 직접 변경하거나 rasterize하지 말고 adjustment/layer 기반으로 적용해.
before/after 확인 방법과 rollback 절차를 함께 제시해.
```

### Reusable script

```text
이 workflow를 Scripting panel에서 재사용할 수 있게 정리해.
입력 조건, parameter, validation, error behavior, tested version을 주석으로 남겨.
```

## 실행 전 10초 점검

- [ ] 복제 문서 또는 versioned backup인가?
- [ ] active document와 selection이 맞는가?
- [ ] target과 변경 property를 좁혔는가?
- [ ] 보존할 layout/style/source를 명시했는가?
- [ ] preview/approval gate가 있는가?
- [ ] output path와 no-overwrite를 명시했는가?

## Tool 선택

| 필요 | 우선 검토 |
|---|---|
| 고정된 동일 절차 반복 | Macro / Batch Job |
| 문맥을 해석하는 Affinity automation | AI Connector |
| 장기 운영, test, version control | 직접 scripting |
| Generative Fill/Image/Vector | Canva AI Studio |

## 기억할 제한

- 2026-09-01 현재 beta다.
- macOS/Windows desktop integration이다.
- Affinity와 Claude Desktop이 모두 실행 중이어야 한다.
- 내부 port, transport, tool name을 공개 contract처럼 가정하지 않는다.
- Affinity local-content privacy 설명과 Claude로 전달된 데이터의 정책은 별개다.

## Sources

- [Affinity AI Connector 설정 가이드](https://www.affinity.studio/help/ai-connector-setup/)
- [Affinity integrations](https://www.affinity.studio/integrations)
- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

