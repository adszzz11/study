---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting Started: public MCP으로 적합성 평가

## 목표

key 없이 public endpoint를 연결해 Lazyweb이 조사 대상과 맞는지 평가한다. 이것은 실제 screen/flow data entitlement를 부여하는 설치가 아니다.

## 1. 업무 질문을 구체화한다

좋은 query에는 제품 유형, flow, 의사결정, target user가 들어간다.

| 피할 질문 | 더 나은 질문 |
|---|---|
| “paywall 예시를 찾아줘” | “B2B SaaS의 annual pricing 전환 전 trial paywall 사례를 조사해 CTA framing 가설 3개를 만들어줘” |
| “onboarding을 개선해줘” | “activation event가 workspace 생성인 팀 협업 제품의 onboarding 순서를 검토할 근거를 찾아줘” |

## 2. public endpoint를 연결한다

MCP client 설정의 개념적 예시는 다음과 같다. 실제 client configuration 위치·형식은 해당 client 문서를 따른다.

```json
{
  "mcpServers": {
    "lazyweb": {
      "url": "https://www.lazyweb.com/mcp/public"
    }
  }
}
```

연결 후 `tools/list`로 public tool을 확인한다. 예를 들어 `lazyweb_search`, `lazyweb_ask_anything`, `lazyweb_compare`, `lazyweb_page_tldr`는 공개 제품 정보와 출처를 얻는 데 쓰인다.

## 3. 조사 기록을 남긴다

각 결과에 아래 세 층을 분리한다.

```markdown
## Observation
- [출처/캡처 날짜] onboarding에서 가치 노출이 sign-up보다 앞섰다.

## Hypothesis
- 우리 제품도 first-value 후 sign-up을 요청하면 completion이 개선될 수 있다.

## Constraints
- SSO 정책, permission timing, mobile accessibility, brand tone을 유지해야 한다.

## Validation
- primary metric: activation completion
- guardrail: support contact rate, time to value
```

## 4. full MCP으로 넘어갈 시점

public discovery가 적합하다고 판단되면 account/plan을 검토하고, Bearer token을 secret manager 또는 client의 credential store에만 등록한다. 그 다음 live schema에서 `lazyweb_get_workflows`를 먼저 호출한다.

> [!warning] token hygiene
> token을 note, source control, prompt transcript에 남기지 않는다. 연결 성공은 데이터 범위나 유료 entitlement의 증거가 아니다.

## 완료 기준

- [ ] 조사 목적과 target flow를 한 문장으로 썼다.
- [ ] public MCP의 live tool list를 확인했다.
- [ ] source link가 있는 결과를 최소 2개 기록했다.
- [ ] 관찰, 가설, 자사 제약, 검증 metric을 분리했다.

## Sources

- https://www.lazyweb.com/agent-access
- https://www.lazyweb.com/mcp-install
