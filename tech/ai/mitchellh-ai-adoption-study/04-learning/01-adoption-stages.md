# 01. AI 도입 6단계 여정

## 📌 핵심 개념

Mitchell Hashimoto의 AI 도입 여정은 **6단계로 구성된 점진적 성숙 과정**이다. 각 단계는 이전 단계의 학습을 기반으로 하며, 건너뛸 수 없다. 이 프레임워크의 핵심은 **모든 새로운 도구 도입에 적용 가능한 범용적 접근법**이라는 점이다.

### 도구 도입의 3단계 (메타 프레임워크)

```
Phase 1: 비효율 → "생산성이 오히려 떨어진다"
Phase 2: 적정   → "이전과 비슷한 수준으로 돌아온다"
Phase 3: 발견   → "삶이 바뀌는 순간이 온다"
```

> "In most cases, I have to force myself through phase 1 and 2 because I usually have a workflow I'm already happy and comfortable with."

대부분의 사람이 Phase 1에서 "이 도구는 쓸모없다"고 판단하고 포기하지만, 진짜 가치는 Phase 3에서 발견된다.

---

## Step 1: Drop the Chatbot (챗봇을 버려라)

### 배경

Hashimoto의 첫 "와우 모먼트"는 Zed 에디터의 커맨드 팔레트 스크린샷을 Google Gemini에 붙여넣고 SwiftUI로 재현을 요청한 것이었다.

> "I was flabbergasted that it did it very well."

이 코드는 Ghostty macOS 커맨드 팔레트의 기반이 되었고, 가벼운 수정만으로 출시되었다.

### 챗봇의 한계

하지만 **브라운필드 프로젝트**(기존 코드베이스에서 작업)에서는 챗봇이 지속적으로 나쁜 결과를 냈다:

> "You're mostly hoping they come up with the right results based on their prior training, and correcting them involves a human to tell them they're wrong repeatedly."

### 전환점: 에이전트

```
챗봇: 사람이 컨텍스트를 제공 → AI가 응답 → 사람이 검증
에이전트: AI가 스스로 컨텍스트를 수집 → 실행 → 검증 → 수정 → 반복

에이전트 최소 요구사항:
  ✅ 파일 읽기
  ✅ 프로그램 실행
  ✅ HTTP 요청
```

---

## Step 2: Reproduce Your Own Work (두 번 일하라)

### Forcing Function (강제 훈련)

이 단계의 핵심 행동은 **모든 작업을 의도적으로 두 번 수행**하는 것이다:

```
1. 수동으로 작업 완료 → git commit
2. 같은 작업을 에이전트로 재현 시도 (수동 결과를 보여주지 않고!)
3. 차이 분석 → 에이전트의 강점/약점 파악
```

> "I literally did the work twice."

### 고통스럽지만 필수적

> "This was excruciating, because it got in the way of simply getting things done."

하지만 마찰이 생산적이었다:

> "Expertise formed. I quickly discovered for myself from first principles what others were already saying, but discovering it myself resulted in a stronger fundamental understanding."

### 3가지 핵심 발견

| # | 발견 | 설명 |
|---|------|------|
| 1 | **작업 분할** | 하나의 거대 세션이 아닌 "separate clear, actionable tasks"로 분할 |
| 2 | **계획-실행 분리** | 모호한 요청을 "planning vs. execution sessions"으로 나눔 |
| 3 | **자기 검증 제공** | "If you give an agent a way to verify its work, it more often than not fixes its own mistakes" |

### Negative Space (부정적 공간)

> "Part of the efficiency gains here were understanding when **not** to reach for an agent."

에이전트가 실패할 가능성이 높은 작업을 미리 파악하여 **시도하지 않는 것** 자체가 효율 향상이다.

### 이 단계의 결론

> "I was finding adequate value with agents that I was happy to use them in my workflow, but still didn't feel like I was seeing any net efficiency gains."

→ Phase 2(적정 수준)에 도달. 아직 "삶을 바꾸는" 수준은 아님.

---

## Step 3: End-of-Day Agents (퇴근 시간 에이전트)

### 핵심 통찰

> "Instead of trying to do more in the time I have, try to do more in the time I don't have."

**매일 퇴근 30분 전**에 에이전트 작업을 시작하여, 자신이 일할 수 없는 시간(밤, 식사, 휴식)에 에이전트가 작업한다.

### 효과적인 작업 유형 3가지

| 유형 | 설명 | 예시 |
|------|------|------|
| **딥 리서치** | 광범위한 조사 | 특정 언어/라이선스의 모든 라이브러리 조사 + 장단점 분석 |
| **병렬 탐색** | 아이디어 탐구 | 막연한 아이디어를 에이전트로 시작 → unknown unknowns 발견 |
| **이슈/PR 트리아지** | GitHub 관리 | `gh` CLI로 이슈 분류하고 **보고만** (직접 응답 금지) |

### 중요한 제한

> "I did not go as far as others went to have agents running in loops all night."

대부분의 에이전트 작업은 **30분 이내** 완료. 밤새 돌리는 것이 아니라, 다음 날 아침 **warm start**를 만드는 것이 목적.

### 이 단계의 결론

> "I was happy, and I was starting to feel like I was doing more than I was doing prior to AI, if only slightly."

→ Phase 2에서 Phase 3으로 넘어가기 시작.

---

## Step 4: Outsource the Slam Dunks (확실한 것만 위임)

### 핵심 원칙

에이전트가 **거의 확실히 성공할 작업**만 위임한다:

```
아침 루틴:
1. 전날 밤 트리아지 에이전트 결과 리뷰
2. "slam dunk" 이슈 식별 (에이전트가 높은 확률로 해결 가능)
3. 에이전트에게 위임 (1개씩, 병렬 아님)
4. 인간은 흥미로운/어려운 작업에 집중
```

### 핵심: 알림을 꺼라

> "Very important at this stage: turn off agent desktop notifications. Context switching is very expensive."

에이전트가 인간을 인터럽트하는 것이 아니라, **인간이 에이전트를 인터럽트**해야 한다.

### Skill Formation 트레이드오프

Anthropic의 기술 형성 연구에 대한 Hashimoto의 견해:

> "You're trading off: not forming skills for the tasks you're delegating to the agent while continuing to form skills naturally in the tasks you continue to work on manually."

→ 위임하는 작업에서는 기술이 형성되지 않지만, 수동으로 하는 작업에서는 여전히 기술이 형성된다.

### 전환점

> "At this point I was firmly in the 'no way I can go back' territory."

→ AI 없는 작업 방식으로 돌아갈 수 없는 단계. Phase 3 진입.

---

## Step 5: Engineer the Harness (하네스를 설계하라)

### 핵심 철학

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

에이전트가 실수할 때마다, 그 실수를 **시스템적으로 방지**하는 메커니즘을 구축한다.

### 두 가지 구현 방법

**1. Implicit Prompting (AGENTS.md)**

프로젝트별 지시 파일에 에이전트의 과거 실수를 반영:

```markdown
# AGENTS.md 예시 (Ghostty)
- 빌드 시 `zig build` 대신 `make` 사용
- 테스트 실행 시 `--filter` 플래그 필수
- config 파일은 절대 경로로 참조
- SwiftUI 뷰에서 @State 대신 @Binding 사용할 것
```

> Ghostty의 AGENTS.md에서 "each line in that file is based on a bad agent behavior, and it almost completely resolved them all."

**2. Programmed Tools (스크립트)**

에이전트가 호출할 수 있는 검증/유틸리티 스크립트:

```bash
# 예: 스크린샷 캡처 스크립트
./scripts/take-screenshot.sh --window ghostty

# 예: 필터된 테스트 실행
./scripts/run-tests.sh --scope ui --filter "command-palette"
```

→ AGENTS.md에 스크립트 존재를 알려줘서 에이전트가 자율적으로 활용.

### 이 단계의 가치

에이전트가 **처음부터 올바른 결과를 내거나, 최소한의 수정만 필요한 결과**를 내면 효율이 극대화된다. Harness Engineering은 이를 시간이 지남에 따라 **누적적으로 개선**하는 전략이다.

---

## Step 6: Always Have an Agent Running (항상 에이전트를 돌려라)

### 목표 (아직 달성 중)

> "If an agent isn't running, I ask myself: is there something an agent could be doing for me right now?"

### 현재 상태

- 근무 시간의 **10~20%**에서만 달성
- **1개 에이전트만** 동시 운영
- 에이전트를 돌리기 위해 돌리지 않음 — 의미 있는 작업이 있을 때만

> "I don't want to run agents for the sake of running agents. I only want to run them when there is a task I think would be truly helpful to me."

### 미래 과제

> "Part of the challenge of this goal is improving my own workflows and tools so that I can have a constant stream of high quality work to do that I can delegate."

→ 에이전트에게 위임할 양질의 작업 스트림을 만드는 것 자체가 과제.

---

## 💻 실전 예시: Ghostty 자동 업데이트 기능

Hashimoto는 "Vibing a Non-Trivial Ghostty Feature" 글에서 이 6단계를 실전에 적용한 사례를 공개했다:

| 항목 | 내용 |
|------|------|
| 기능 | macOS 자동 업데이트 알림 (비간섭적) |
| 도구 | Amp (16 세션) |
| 비용 | $15.98 |
| 시간 | 약 8시간 (2일) |
| 방식 | 계획 → 프로토타입 → 구현 → 정리 → 시뮬레이션 → 리뷰 |

핵심 원칙: "I'm not shipping code I don't understand."

---

## ✅ 체크포인트

- [ ] 6단계를 순서대로 설명할 수 있는가?
- [ ] 챗봇과 에이전트의 근본적 차이를 이해했는가?
- [ ] "두 번 일하기"의 목적(전문성 형성)을 설명할 수 있는가?
- [ ] "비동기 시간 활용"의 핵심 통찰을 설명할 수 있는가?
- [ ] Harness Engineering의 두 가지 구현 방법(AGENTS.md, 스크립트)을 구분할 수 있는가?
- [ ] 에이전트 위임 시 Skill Formation 트레이드오프를 이해했는가?

## ⚠️ 주의사항

| 주의 | 설명 |
|------|------|
| 단계를 건너뛰지 말 것 | Step 2(두 번 일하기)를 건너뛰면 에이전트의 강점/약점을 모른 채 위임하게 됨 |
| 알림을 반드시 끌 것 | Step 4에서 에이전트 알림이 켜져 있으면 컨텍스트 스위칭 비용이 이득을 상쇄 |
| 에이전트를 억지로 돌리지 말 것 | Step 6는 양질의 작업이 있을 때만 의미 있음 |
| 주니어의 기초를 간과하지 말 것 | 기본기 없이 위임하면 장기적 역량 손실 |

## 🔗 더 알아보기

- [[02-ai-tools-workflow|다음: 사용한 AI 도구들과 워크플로우]]
- [[../01-overview|이전: 개요]]
- [원문: My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)
- [실전 사례: Vibing a Non-Trivial Ghostty Feature](https://mitchellh.com/writing/non-trivial-vibing)
