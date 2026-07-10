---
date: 2026-07-11
tags:
  - tech
  - ai
  - codex
  - gpt-5-6
  - overview
type: tech-tool-study
parent: "[[README]]"
---

# GPT-5.6 in Codex - 개요

> [[README|목차로 돌아가기]] | [[02-ecosystem|다음: 생태계]]

---

## 1. What - 무엇인가?

> **한 줄 정의**: GPT-5.6은 Codex, ChatGPT Work, API에서 쓰이는 최신 OpenAI frontier reasoning/agentic model family이며, "Codex 5.6"은 비공식적 표현에 가깝다.

### 이름 정리

| 표현 | 정확도 | 설명 |
|------|--------|------|
| Codex 5.6 | 낮음 | 공식 제품명으로 보기 어렵다. 사용자가 체감하는 Codex 모델 업그레이드 표현 |
| GPT-5.6 | 높음 | OpenAI의 공식 model family 명칭 |
| GPT-5.6 in Codex | 높음 | Codex surface에서 GPT-5.6 tier와 effort를 쓰는 상황 |

### 기본 구조

```text
User task
  -> Codex / ChatGPT Work / API
      -> GPT-5.6 model family
          -> Sol / Terra / Luna
              -> reasoning effort: none..max
              -> tool use / multi-agent / computer use
```

## 2. Why - 왜 중요한가?

GPT-5.6의 목표는 "벤치마크 점수만 높은 단일 모델"이 아니라, 실제 업무에서 오래 걸리는 agentic work를 더 효율적으로 처리하는 것이다.

- **Agentic coding**: 대형 codebase 탐색, refactor, test 작성, PR review 같은 연속 작업.
- **Long-running knowledge work**: 문서 조사, 비교, 정리, 반복 검증.
- **Computer use**: UI/browser/desktop 환경을 사용하는 task.
- **Cybersecurity/science tasks**: high capability 영역이므로 더 강한 safeguards와 monitoring이 필요.

Codex 사용자에게는 특히 다음 변화가 크다.

| 변화 | 의미 |
|------|------|
| `Sol/Terra/Luna` | 작업 난이도와 비용에 맞춰 모델 tier를 고를 수 있음 |
| `max` effort | quality-first task에서 더 깊은 reasoning 사용 |
| `ultra` mode | Codex가 여러 agent를 병렬 조율하는 고성능 모드 |
| Programmatic Tool Calling | tool call orchestration을 JavaScript 실행으로 압축 |
| Multi-agent beta | API에서도 multi-agent 패턴을 직접 설계 가능 |

## 3. 핵심 특징

### 3-tier model family

| 모델 | 포지션 | 적합한 작업 |
|------|--------|-------------|
| `gpt-5.6-sol` | flagship | 어려운 coding, research, reasoning-heavy task |
| `gpt-5.6-terra` | cost/performance balance | 일반 업무 자동화, 반복 개발, 중간 난이도 분석 |
| `gpt-5.6-luna` | high-volume/low-cost | 대량 처리, 단순 변환, 빠른 triage |
| `gpt-5.6` | alias | dossier 기준 Sol로 라우팅 |

### Reasoning effort

| effort | 용도 |
|--------|------|
| `none` | 거의 reasoning이 필요 없는 변환/추출 |
| `low` | 빠른 답변, 단순 coding assist |
| `medium` | 기본값 후보. 일반 개발/분석 |
| `high` | 복잡한 설계, 디버깅, 리뷰 |
| `xhigh` | 더 깊은 추론이 필요한 난제 |
| `max` | 비용보다 품질이 우선인 difficult task |

### Codex surfaces

| Surface | 설명 |
|---------|------|
| ChatGPT desktop/web | 대화형 coding/work assistant |
| Codex CLI | local project directory에서 agent 실행 |
| IDE extension | editor 안에서 task, diff, review 흐름 연결 |
| Codex cloud | isolated cloud environments에서 병렬 task 실행, GitHub/Linear/Slack trigger 지원 |

## 4. Programmatic Tool Calling

Programmatic Tool Calling은 모델이 JavaScript를 작성하고 실행해서 여러 tool calls를 조율하는 패턴이다. 목적은 intermediate output을 줄이고, round trip과 token 사용량을 줄이는 것이다.

```javascript
// 개념 예시: 여러 검색 결과를 코드로 필터링한 뒤 필요한 결과만 모델에 반환
const results = await tools.search({ query: "GPT-5.6 Codex max ultra" });
const official = results.filter((item) =>
  item.url.includes("openai.com") || item.url.includes("developers.openai.com")
);
return official.slice(0, 5);
```

일반 tool calling이 `model -> tool -> model -> tool` 왕복을 반복한다면, Programmatic Tool Calling은 일부 조율 로직을 code execution 안으로 넣어 더 조밀한 workflow를 만든다.

## 5. Safety stack

GPT-5.6 system card는 Sol/Terra/Luna를 cyber 및 bio/chemical risk에서 High capability로 본다. 따라서 단순 성능 향상만 볼 것이 아니라 다음 운영 조건을 함께 봐야 한다.

- **real-time checks**: 위험한 요청/행동을 실행 중 확인.
- **monitoring**: high-risk capability 사용 흐름 관찰.
- **trust-based access**: 사용자/조직 신뢰도에 따라 접근 제어.
- **stronger safeguards**: cyber, bio/chemical 영역에서 강화된 제한.

## 관련 노트

- [[study/tech/ai/lazy-codex]] - Codex agent 작업의 검증/완료 신뢰성
- [[study/tech/ai/model-context-protocol-mcp]] - tool calling과 외부 system integration 맥락
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI 기반 agent orchestration 비교

## References

- [OpenAI GPT-5.6 release](https://openai.com/index/gpt-5-6/)
- [GPT-5.6 system card](https://deploymentsafety.openai.com/gpt-5-6)
- [OpenAI latest model guide](https://developers.openai.com/api/docs/guides/latest-model)
- [Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling)
