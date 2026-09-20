---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Mobbin MCP — Cheatsheet

## Connection

```json
{
  "mcpServers": {
    "mobbin": {
      "url": "https://api.mobbin.com/mcp"
    }
  }
}
```

- Transport: hosted **Streamable HTTP**
- Authorization: 최초 사용 시 **OAuth**
- 운영: 로컬 server와 API key가 필요 없음
- 권한: Mobbin plan의 MCP entitlement를 먼저 확인

## Tools

| Tool | 언제 쓰나 | 예시 |
|---|---|---|
| `search_screens` | 개별 화면의 정보 hierarchy를 볼 때 | `biometric login screen 15개` |
| `search_flows` | 단계·전환·drop-off를 비교할 때 | `subscription cancellation flow` |
| `search_sections` | web page의 특정 section을 볼 때 | `B2B SaaS pricing hero social proof` |

## Research recipe

```text
검색 → 후보 묶기 → 공통/예외 분리 → 제품 제약 반영 → 결정 기록 → 코드화
```

1. task, platform, industry, 표본 수를 query에 넣는다.
2. 결과마다 source link와 관찰을 기록한다.
3. pattern을 정답으로 취급하지 않고 accessibility·compliance·brand 제약과 대조한다.
4. 구현 요청에는 채택한 이유와 제외한 이유를 함께 준다.

## Prompt templates

```text
[industry]의 [task] [screen/flow/section]을 [N]개 찾아라.
[관찰 항목]을 표로 비교하고 공통 패턴과 예외를 분리해라.
각 권고안에 Mobbin 원본 링크, 위험, 우리 제품의 구현 영향을 붙여라.
특정 제품의 copy, asset, layout을 복제하지 마라.
```

```text
[feature] flow를 조사해 drop-off 방지 패턴을 추출해라.
사용자 목표, primary CTA, error recovery, reassurance, accessibility 관점으로 정리하고,
우리의 [제약]을 고려한 채택/제외 결정을 제안해라.
```

## Do / Don't

| Do | Don't |
|---|---|
| first-party endpoint와 OAuth를 사용한다. | 비공식 cookie-scraping MCP를 새로 도입하지 않는다. |
| reference를 evidence와 hypothesis로 사용한다. | 단일 사례를 UX 정답으로 간주하지 않는다. |
| source link와 제품 제약을 함께 기록한다. | copy·asset·독특한 layout을 복제하지 않는다. |
| Figma MCP와 내부 구현 문맥을 연결한다. | 외부 reference만 보고 내부 design system을 무시하지 않는다. |

## Sources

- [Mobbin MCP](https://mobbin.com/mcp)
- [Official MCP server repository](https://github.com/mobbin/mobbin-mcp-server)
- [Archived unofficial implementation](https://github.com/pdcolandrea/mobbin-mcp)
