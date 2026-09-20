---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — Getting Started

## 목표

Mobbin entitlement를 확인하고 MCP-compatible client에 remote endpoint를 등록한 뒤 OAuth를 완료한다. 이어서 screen, flow, section을 각각 한 번씩 검색해 결과 단위의 차이를 익힌다.

## 1. 계정과 권한 확인

1. Mobbin 유료 plan에서 MCP entitlement가 활성화됐는지 확인한다.
2. 사용할 client가 remote MCP와 OAuth authorization을 지원하는지 확인한다.
3. 조직 계정이라면 실제 사용자가 Mobbin library에 접근할 권한이 있는지 확인한다.

Pro·Team 제공 여부는 Mobbin landing page를, Enterprise 포함 여부는 plugin 문서를 참고하되 계약별 권한은 현재 billing 화면을 기준으로 판단한다.

## 2. endpoint 등록

client의 MCP 설정 형식에 맞춰 다음 remote server를 등록한다.

```json
{
  "mcpServers": {
    "mobbin": {
      "url": "https://api.mobbin.com/mcp"
    }
  }
}
```

일부 client는 다음처럼 transport type을 명시해야 한다. 이 예시는 범용 JSON이 아니라 해당 client의 공식 설정 문서를 우선해야 한다.

```json
{
  "mcpServers": {
    "mobbin": {
      "type": "streamableHttp",
      "url": "https://api.mobbin.com/mcp"
    }
  }
}
```

## 3. OAuth 완료

처음 tool을 호출할 때 browser login과 Mobbin authorization 화면이 열릴 수 있다. 로그인·승인을 마친 뒤 client에서 연결 성공과 tool 목록을 확인한다. API key를 복사하거나 로컬 process를 띄우는 방식이 아니라 hosted server의 OAuth 흐름을 쓴다.

## 4. 세 종류의 검색 실습

| 단위 | 실습 prompt | 관찰점 |
|---|---|---|
| Screen | `fintech 앱의 biometric login screen 15개를 찾아라.` | 개별 화면의 hierarchy와 permission 설명 |
| Flow | `subscription cancellation flow를 비교해 drop-off 방지 패턴을 추출하라.` | 단계 전환, reassurance, alternative offer |
| Section | `B2B SaaS pricing hero와 social proof section 사례를 찾아라.` | webpage의 정보 순서와 proof 형태 |

검색 결과는 바로 코드로 복사하지 않는다. 먼저 후보를 묶고, 공통점과 예외를 분리해 제품 제약에 맞는 결정을 문장으로 적는다.

## Troubleshooting

- **로그인 창이 열리지 않음:** client의 OAuth/remote MCP 지원과 browser handoff 설정을 점검한다.
- **도구가 보이지 않음:** entitlement, config 저장 위치, client 재시작 필요 여부를 공식 client guide에서 확인한다.
- **결과가 너무 넓음:** platform, industry, task, flow 단계, 원하는 분석 기준을 prompt에 추가한다.
- **권한 오류:** 다른 Mobbin 계정으로 OAuth된 것은 아닌지, 조직 plan에 권한이 있는지 확인한다.

## Sources

- [Mobbin MCP](https://mobbin.com/mcp)
- [Client setup overview](https://docs.mobbin.com/mcp/clients/overview)
- [Official MCP server repository](https://github.com/mobbin/mobbin-mcp-server)
