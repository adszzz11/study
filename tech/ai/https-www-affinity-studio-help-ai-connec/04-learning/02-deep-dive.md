---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Deep Dive

## 논리 아키텍처

```text
사용자 prompt
    ↓
Claude Desktop                         MCP Host
    ↓ tool 선택·argument 생성
Affinity Connector                     MCP Client
    ↕ local MCP session / JSON-RPC
Affinity desktop 내 MCP Server
    ↓
Affinity Scripting API / document model
    ↓
현재 .af 문서, selection, layer, export
    ↓
실행 결과·preview·오류 → Claude → 사용자
```

MCP는 Host → Client → Server 구조, JSON-RPC message, capability negotiation을 정의한다. Server는 `tools`, `resources`, `prompts`를 노출할 수 있고, tool은 model-controlled action primitive다.

하지만 이 구조는 **논리 모델**이다. Affinity는 packaged Connector의 전체 tool schema와 구체적인 transport를 공개 API contract로 상세 문서화하지 않았다. 표준 MCP transport가 `stdio`와 `Streamable HTTP`라고 해서 특정 port나 내부 구현을 추정하면 안 된다.

## Prompt를 transaction처럼 설계하기

안전한 automation prompt는 다음 다섯 요소를 포함한다.

| 요소 | 질문 | 예시 |
|---|---|---|
| Target | 무엇을 대상으로 하는가? | active document의 selected artboards |
| Scope | 어디까지 바꾸는가? | unnamed layers only |
| Invariant | 무엇은 보존해야 하는가? | layout, style, source dimensions |
| Output | 결과는 어디에 어떤 규칙으로 쓰는가? | `./exports`, no overwrite |
| Verification | 성공을 어떻게 확인하는가? | planned count와 actual count 보고 |

```text
Target: 현재 선택된 artboard만.
Scope: 각 artboard를 1080×1080과 1080×1920 variant로 준비.
Invariant: 원본 artboard와 object hierarchy는 보존하고 파괴적으로 rasterize하지 말 것.
Output: 먼저 변경 계획과 예상 export filename을 표로 제시하고 아직 실행하지 말 것.
Verification: 승인 후 실행하고 생성/skip/error 수를 각각 보고할 것.
```

## Reusable automation의 성숙 단계

1. **Explore** — 복제 문서에서 자연어로 의도를 탐색한다.
2. **Constrain** — target, invariant, output, error behavior를 명시한다.
3. **Review** — generated script와 file I/O를 사람이 검토한다.
4. **Test** — 정상, empty selection, locked object, naming collision sample을 실행한다.
5. **Save** — Scripting panel에 version과 함께 저장한다.
6. **Operate** — production에서는 preview/dry-run, backup, result log를 사용한다.
7. **Maintain** — Affinity/Connector update마다 regression test한다.

## Custom dialog 설계

공식 사례처럼 pattern generator나 Roughen Curves 형태의 작은 tool을 만들 때는 parameter뿐 아니라 guardrail도 UI에 둔다.

- numeric range와 unit을 명시한다.
- destructive option은 기본값을 off로 둔다.
- selected-only와 duplicate-before-change를 제공한다.
- output preview와 cancel path를 둔다.
- 같은 seed/input에서 같은 결과가 필요한지 결정한다.

## 보안과 데이터 경계

- MCP tool은 문서 수정과 file export 같은 실질적인 action을 수행한다.
- 복제 문서, Affinity undo/history, versioned backup을 함께 사용한다.
- “모든 layer” 같은 넓은 표현 대신 selection과 object condition을 좁힌다.
- Affinity는 local content를 Canva가 접근하거나 AI training에 쓰지 않는다고 설명한다.
- Connector를 통해 Claude에 전달된 prompt, preview, tool result는 Claude 측 데이터 처리 정책의 적용 대상이다.

따라서 **Canva가 local content를 다루는 방식**과 **Claude에 실제 전달한 데이터의 처리 방식**을 같은 privacy claim으로 해석하지 않는다. 민감한 client asset은 조직 정책과 Claude plan의 데이터 조건을 별도로 확인한다.

## 실패 모드와 대응

| 실패 모드 | 대응 |
|---|---|
| 범위가 과도함 | selection-only, object count preview, 승인 gate |
| 파괴적 변경 | duplicate, adjustment layer, no rasterize invariant |
| overwrite/잘못된 export | explicit path, filename template, no-overwrite default |
| 문서 구조 차이 | representative fixture와 edge-case regression test |
| product update로 API 변화 | version pin 기록, smoke test, source review |
| token을 매번 소비 | 안정화한 workflow를 Scripting panel에 저장 |

## Sources

- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [MCP Server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index)
- [MCP Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- [Affinity automation examples](https://www.affinity.studio/blog/automate-design-tasks-affinity-claude)
- [Affinity privacy and Canva integrations](https://www.affinity.studio/canva-integrations)

