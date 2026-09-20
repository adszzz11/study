---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Lazyweb MCP References

## 공식 Lazyweb

| 자료 | 용도 |
|---|---|
| [Agent Access](https://www.lazyweb.com/agent-access) | public MCP/HTTP endpoint, 공개 도구, 무료 접근 범위 |
| [Product](https://www.lazyweb.com/product) | Growth MCP의 positioning과 product workflow |
| [MCP Install](https://www.lazyweb.com/mcp-install) | client 연결 시작점 |
| [Upgrade](https://www.lazyweb.com/upgrade) | plan·trial·entitlement를 확인할 때 |
| [lazyweb-skill GitHub](https://github.com/aboul3ata/lazyweb-skill) | skill pack 설치·workflow 구현 확인 |

## 비교 대상 공식 문서

- [Mobbin MCP](https://mobbin.com/mcp)
- [21st MCP documentation](https://docs.21st.dev/mcp)
- [Figma MCP server documentation](https://developers.figma.com/docs/figma-mcp-server/)

## 읽는 순서

1. Agent Access에서 public endpoint와 public tool의 범위를 먼저 확인한다.
2. Product·Upgrade에서 authenticated product workflow와 plan 조건을 분리해 읽는다.
3. `lazyweb-skill` repository의 설치 문서로 local client 지원 여부를 확인한다.
4. 도입 직전에는 실제 MCP `tools/list`와 account 화면으로 tool schema·limit·권한을 재확인한다.

> [!note] source hierarchy
> live MCP schema와 account entitlement가 README나 블로그보다 우선한다. 비교·가격은 각 vendor의 공식 현재 페이지를 기준으로 하고, screenshot 안의 수치나 오래된 capture는 현재 상업 조건의 근거로 쓰지 않는다.

## Sources

- https://www.lazyweb.com/agent-access
- https://www.lazyweb.com/product
- https://www.lazyweb.com/mcp-install
- https://www.lazyweb.com/upgrade
- https://github.com/aboul3ata/lazyweb-skill
