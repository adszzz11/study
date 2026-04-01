# Part 1: Overview

## 저자 소개

**Mitchell Hashimoto**는 인프라 자동화 회사 **HashiCorp**의 공동 창립자로, Vagrant, Terraform, Vault, Consul 등 DevOps 생태계를 정의한 도구들을 만든 인물이다. 2023년 HashiCorp 경영진에서 물러난 뒤, 현재는 Zig 언어로 만든 고성능 터미널 에뮬레이터 **Ghostty**를 풀타임으로 개발하고 있다.

20년 이상의 소프트웨어 엔지니어링 경력을 가진 베테랑이면서도, AI 도구에 대해 **"찬반 어느 쪽도 아닌 실용적 관점"**을 유지하고 있다는 점이 이 글의 가장 큰 차별점이다.

> "I really don't care one way or the other if AI is here to stay. I'm a software craftsman that just wants to build stuff for the love of the game."

## 글의 맥락

- **게시일**: 2026년 2월 5일
- **명시적 선언**: "This blog post was fully written by hand, in my own words."
- **이해충돌 없음**: "I don't work for, invest in, or advise any AI companies."
- Hashimoto는 AI 도입을 권유하거나 반대하지 않으며, 자신의 경험을 공유할 뿐이라고 반복 강조한다

## 핵심 프레임워크: 도구 도입의 3단계

Hashimoto는 AI뿐 아니라 **모든 의미 있는 도구 도입**에 공통적인 3단계가 있다고 말한다:

```
1. Period of inefficiency     → 비효율의 시기 (생산성 하락)
2. Period of adequacy         → 적정 수준의 시기 (이전과 비슷)
3. Period of life-altering    → 삶을 바꾸는 발견의 시기
   discovery
```

> "In most cases, I have to force myself through phase 1 and 2 because I usually have a workflow I'm already happy and comfortable with."

대부분의 사람들이 1단계에서 포기하지만, Hashimoto는 의식적으로 1, 2단계를 **억지로 통과**하며 도구의 진짜 가치를 찾아갔다.

## 핵심 주장 6가지

| # | 주장 | 상세 |
|---|------|------|
| 1 | 챗봇을 버려라 | 코딩에서 챗봇의 유용성은 극히 제한적. 에이전트로 전환해야 한다 |
| 2 | 두 번 일해서 배워라 | 수동 작업 후 같은 작업을 에이전트로 재현하는 훈련이 전문성을 만든다 |
| 3 | 비동기 시간을 활용하라 | "내가 일할 수 없는 시간"에 에이전트를 돌려라 |
| 4 | 확실한 것만 위임하라 | 에이전트가 잘하는 작업과 못하는 작업을 구분하는 눈이 핵심 |
| 5 | 실수를 시스템으로 방지하라 | 에이전트 실수마다 AGENTS.md나 스크립트로 재발 방지 |
| 6 | 항상 에이전트를 돌려라 | 에이전트가 돌지 않는 시간은 기회 비용이다 |

## 6단계 여정 요약

```
Step 1: Drop the Chatbot         → 챗봇 → 에이전트 전환
Step 2: Reproduce Your Own Work   → 이중 작업으로 전문성 구축
Step 3: End-of-Day Agents         → 비동기 시간 활용
Step 4: Outsource the Slam Dunks  → 확실한 작업 위임
Step 5: Engineer the Harness      → 재발 방지 시스템 구축
Step 6: Always Have an Agent      → 상시 에이전트 운영
        Running
```

## 현재 상태 (2026년 2월 기준)

- 5단계(Harness Engineering)에 집중 중
- 6단계(상시 에이전트)는 **목표** 단계이며, 근무 시간의 10~20%에서만 달성
- 동시에 여러 에이전트를 돌리지 않고 **1개 에이전트만** 운영
- 월간 AI 도구 비용: 약 $400~$500 (Amp $300~$400 + Claude $200)

## AI 비관론과 낙관론에 대한 태도

Hashimoto는 **양쪽 모두에 거리를 둔다**:

- AI 회의론자: "I fully respect anyone's individual decisions regarding it."
- AI 만능론자: 과대 포장된 기대에 동의하지 않음
- 본인의 입장: "I'm not here to convince you!"

특히 **주니어 개발자의 기초 역량 약화**에 대해서는 깊은 우려를 표명:

> "The skill formation issues particularly in juniors without a strong grasp of fundamentals deeply worries me."

## 이 글이 중요한 이유

1. **신뢰할 수 있는 화자**: AI 회사와 이해관계가 없는, 검증된 시니어 엔지니어의 1인칭 경험
2. **재현 가능한 방법론**: 추상적 조언이 아닌 구체적 단계와 행동 지침
3. **정직한 한계 인정**: "아직 10~20%만 달성", "Zig 코드는 희망 없음" 등 솔직한 평가
4. **범용적 프레임워크**: AI에만 적용되는 것이 아닌, 모든 새로운 도구 도입에 적용 가능한 철학
