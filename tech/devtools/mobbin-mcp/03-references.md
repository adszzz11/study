---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — References

## Primary sources

| 자료 | 확인할 내용 |
|---|---|
| [Mobbin MCP landing page](https://mobbin.com/mcp) | 제공 plan, 가치 제안, 설치 흐름 |
| [Official MCP server repository](https://github.com/mobbin/mobbin-mcp-server) | endpoint, OAuth, client별 Streamable HTTP 설정 |
| [Agent Plugin repository](https://github.com/mobbin/mobbin-agent-plugin) | plugin 배포 및 제공 tool의 개요 |
| [Client setup overview](https://docs.mobbin.com/mcp/clients/overview) | MCP client별 연결 절차 |
| [Feature documentation](https://docs.mobbin.com/mcp/features) | screens, flows, sections 기능 범위 |
| [MCP introduction](https://modelcontextprotocol.io/docs/getting-started/intro) | protocol과 client/server 기본 모델 |
| [MCP Registry entry](https://github.com/mcp/com.mobbin/mobbin) | Registry의 Mobbin package 정보 |

## 비권장 소스

[pdcolandrea/mobbin-mcp](https://github.com/pdcolandrea/mobbin-mcp)는 first-party server 이전의 비공식 구현이다. 내부 endpoint reverse-engineering과 browser cookie를 요구하며 2026-05-15 archive되었다. 저장소 작성자도 official MCP로의 이동을 권한다. 보안·유지보수·약관 관점에서 새 설정의 기반으로 삼지 않는다.

## 검증 습관

- 설치 전에는 공식 landing page와 client setup 문서에서 현재 entitlement와 endpoint를 확인한다.
- client별 config schema는 서로 다를 수 있다. 특히 일부 client(Cline 등)는 `type: "streamableHttp"` 명시가 필요할 수 있다.
- corpus 규모, 요금제, plugin 배포 경로는 변동 가능하므로 이 노트의 날짜보다 최신 문서를 우선한다.
- 외부 comparison은 각 서비스의 공식 문서에서 읽기/쓰기 범위를 재확인한다.

## Sources

- [Mobbin MCP server repository](https://github.com/mobbin/mobbin-mcp-server)
- [Mobbin docs — clients](https://docs.mobbin.com/mcp/clients/overview)
- [Mobbin docs — features](https://docs.mobbin.com/mcp/features)
- [Model Context Protocol introduction](https://modelcontextprotocol.io/docs/getting-started/intro)
