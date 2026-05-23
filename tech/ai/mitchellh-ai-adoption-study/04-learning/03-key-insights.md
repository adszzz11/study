# 03. 핵심 인사이트와 교훈

## 📌 핵심 개념

Hashimoto의 여정에서 추출할 수 있는 **재사용 가능한 원칙**들을 정리한다. 이 인사이트들은 AI 도구에만 한정되지 않고, 새로운 도구 도입 전반에 적용 가능하다.

---

## 인사이트 1: 비동기 시간 활용 (Asynchronous Leverage)

> "Instead of trying to do more in the time I have, try to do more in the time I don't have."

### 왜 중요한가

대부분의 AI 생산성 논의는 **"같은 시간에 더 많이"**에 집중한다. Hashimoto의 전환점은 **"일하지 않는 시간에 더 많이"**로 관점을 바꾼 것이다.

```
기존 사고:
  8시간 근무 × 1.5배 효율 = 12시간분의 작업

Hashimoto 사고:
  8시간 근무 + 2시간 비동기 에이전트 = 10시간분의 작업
  (근무 시간의 효율은 그대로, 추가 시간이 "무료")
```

### 핵심 원칙

- 에이전트 작업은 대부분 **30분 이내** 완료
- 밤새 돌리는 것이 아니라 **warm start**를 만드는 것이 목적
- 퇴근 전 30분만 투자하면 다음 날 아침 시작이 빨라진다

---

## 인사이트 2: Harness Engineering (재발 방지 공학)

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

### 왜 중요한가

AI 에이전트의 가치는 **첫 번째 시도에서 올바른 결과를 낼 때** 극대화된다. Harness Engineering은 시간이 지남에 따라 에이전트의 정확도를 **누적적으로 향상**시키는 투자다.

```
시간 경과에 따른 가치:

Week 1:  에이전트 실수 빈번 → 수동 수정 시간 많음 → 순이익 낮음
Week 4:  AGENTS.md에 20개 규칙 → 실수 50% 감소 → 순이익 증가
Week 12: AGENTS.md에 80개 규칙 + 스크립트 10개 → 실수 90% 감소 → 순이익 높음
```

### 두 가지 구현

| 방법 | 적용 시점 | 예시 |
|------|----------|------|
| **AGENTS.md** (암묵적 프롬프팅) | 에이전트가 잘못된 명령, API 사용 시 | "빌드 시 `zig build` 대신 `make` 사용" |
| **Programmed Tools** (스크립트) | 에이전트가 검증할 방법이 없을 때 | 스크린샷 캡처, 필터 테스트 스크립트 |

### Ghostty AGENTS.md 사례

> "Each line in that file is based on a bad agent behavior, and it almost completely resolved them all."

모든 줄이 과거 에이전트 실수에서 파생된 규칙이며, 이 파일만으로 대부분의 실수가 해결되었다.

---

## 인사이트 3: 인간이 인터럽트를 제어한다

> "Context switching is very expensive. It was my job as a human to be in control of when I interrupt the agent."

### 왜 중요한가

에이전트 데스크톱 알림이 켜져 있으면, 에이전트가 작업을 완료할 때마다 인간의 집중이 깨진다. 이 컨텍스트 스위칭 비용은 에이전트가 절약하는 시간을 **상쇄하거나 초과**할 수 있다.

### 실천 원칙

```
❌ 에이전트 완료 알림 ON
   → 에이전트: "작업 완료!" → 인간: 집중 끊김 → 리뷰 → 다시 집중 (15~20분)

✅ 에이전트 완료 알림 OFF
   → 인간: 자기 작업 구간 완료 → 자연스러운 전환점에서 에이전트 결과 확인
```

---

## 인사이트 4: Negative Space의 가치

> "Part of the efficiency gains here were understanding when **not** to reach for an agent."

### 왜 중요한가

에이전트가 실패할 가능성이 높은 작업을 미리 파악하여 **시도하지 않는 것** 자체가 효율 향상이다. 에이전트가 30분간 실패하는 작업을 미리 식별하면, 그 30분이 절약된다.

### 에이전트가 잘 못하는 작업 (Hashimoto 기준)

| 작업 유형 | 이유 |
|----------|------|
| Zig 언어 코딩 | 학습 데이터 부족, 에이전트가 "hopeless" |
| 고성능 데이터 구조 | 컨텍스트 내에서 최적화 판단 어려움 |
| 아키텍처 결정 | 전체 시스템 이해 필요 → 인간의 영역 |
| 장기 코드베이스의 스타일 일관성 | 미묘한 컨벤션을 이해하지 못함 |

### 에이전트가 잘하는 작업

| 작업 유형 | 이유 |
|----------|------|
| SwiftUI UI 구현 | 패턴이 반복적, 학습 데이터 풍부 |
| 테스트 코드 생성 | 입력-출력 패턴이 명확 |
| 보일러플레이트 코드 | 규칙 기반, 창의성 불필요 |
| 컴파일 에러 수정 | 에러 메시지 → 수정 패턴 명확 |
| 리서치/문서 조사 | 광범위한 탐색에 강점 |

---

## 인사이트 5: AI는 목표 지향적이며 범위 외 파괴를 일으킨다

> "AI is goal-oriented and will break things outside its current task scope to achieve its immediate goal."

### 왜 중요한가

에이전트는 주어진 목표를 달성하기 위해 **목표 범위 밖의 코드를 변경하거나 파괴**할 수 있다. 이는 인간 개발자보다 훨씬 빈번하게 발생한다.

### 대응 전략

```
1. 테스트 커버리지를 인간 전용 개발보다 훨씬 넓게 유지
2. 에이전트에게 검증 도구 제공 (테스트 실행, 린팅 등)
3. AGENTS.md에 "절대 수정하지 말 것" 목록 명시
4. 작업 범위를 좁고 명확하게 지시
```

---

## 인사이트 6: 이해하지 못하는 코드는 출시하지 않는다

> "I'm not shipping code I don't understand."

### 왜 중요한가

Hashimoto는 이것이 "super super super important"하다고 세 번 강조했다. 에이전트가 생성한 코드를 그대로 출시하는 것은 **기술 부채의 극단적 형태**다.

### 실천 방법

```
1. Anti-Slop Sessions: AI 코드를 정리하고 재구조화하는 세션
   → 코드 이해를 강제하는 효과

2. Inspiration Pattern: AI 코드를 읽고 아이디어만 취한 뒤 전체 삭제
   → 직접 작성하여 완전한 이해 보장

3. Documentation-First: 세션 사이에 문서를 추가
   → 다음 에이전트 세션의 품질 향상 + 인간의 이해 심화
```

---

## 인사이트 7: Skill Formation 트레이드오프를 인식하라

> "You're trading off: not forming skills for the tasks you're delegating to the agent while continuing to form skills naturally in the tasks you continue to work on manually."

### 왜 중요한가

위임하는 작업에서는 **기술이 형성되지 않는다**. 이것은 시니어에게는 수용 가능한 트레이드오프일 수 있지만, 주니어에게는 **치명적**일 수 있다.

> "The skill formation issues particularly in juniors without a strong grasp of fundamentals deeply worries me."

### 균형 전략

| 경험 수준 | 권장 접근 |
|----------|----------|
| 주니어 (0~3년) | 에이전트 위임 최소화, Step 2 "두 번 일하기"에 집중 |
| 미드레벨 (3~7년) | 반복적 작업만 위임, 새로운 영역은 직접 수행 |
| 시니어 (7년+) | 확립된 기술의 반복 작업 위임, 아키텍처/설계는 직접 |

---

## 인사이트 8: 장인 정신과 AI는 공존할 수 있다

> "I'm a software craftsman that just wants to build stuff for the love of the game."

### Hashimoto의 균형

```
직접 하는 것:            에이전트에게 맡기는 것:
├── 아키텍처 설계         ├── 반복적 구현
├── 성능 최적화          ├── 보일러플레이트
├── 릴리즈 노트 작성      ├── 이슈 트리아지
├── 코드 리뷰            ├── 리서치/조사
└── 핵심 알고리즘         └── 컴파일 에러 수정
```

릴리즈 노트에 대한 그의 견해:

> "Changelogs are a boundary point where humans read what other humans should write. It's a social experience."

---

## 💻 실전 예시: 인사이트 적용 체크리스트

작업 시작 전:
```
□ 이 작업은 에이전트가 잘하는 유형인가? (Negative Space 확인)
□ 계획과 실행을 분리했는가?
□ 작업 범위가 좁고 명확한가?
□ 에이전트가 자기 검증할 수 있는 방법이 있는가?
```

작업 중:
```
□ 에이전트 알림을 껐는가?
□ Slop Zone(3~4회 반복 실패)을 감지했는가?
□ 생성된 코드를 이해하는가?
```

작업 후:
```
□ 에이전트 실수가 있었다면 AGENTS.md에 반영했는가?
□ Anti-Slop 세션(코드 정리)을 수행했는가?
□ 다음 에이전트를 위한 warm start를 준비했는가?
```

---

## ✅ 체크포인트

- [ ] 8가지 인사이트를 각각 한 문장으로 설명할 수 있는가?
- [ ] 비동기 시간 활용과 "같은 시간에 더 많이"의 차이를 이해했는가?
- [ ] 자신의 프로젝트에 Harness Engineering을 시작할 준비가 되었는가?
- [ ] Negative Space(에이전트를 쓰지 말아야 할 때)를 판단할 수 있는가?
- [ ] Skill Formation 트레이드오프에 대한 자신의 입장이 있는가?

## ⚠️ 주의사항

| 주의 | 설명 |
|------|------|
| 이해 없이 출시하지 말 것 | Hashimoto가 가장 강조한 원칙 |
| AGENTS.md 업데이트를 게을리하지 말 것 | 한 번 방치하면 같은 실수가 반복됨 |
| 주니어의 학습 기회를 빼앗지 말 것 | 반복 작업도 처음엔 학습 가치가 있음 |
| AI의 범위 외 파괴에 주의 | 테스트 커버리지를 넓게 유지 |

## 🔗 더 알아보기

- [[04-practical-tips|다음: 실전 적용 팁]]
- [[02-ai-tools-workflow|이전: AI 도구들과 워크플로우]]
- [Anthropic: AI와 기술 형성 연구](https://www.anthropic.com/research/skill-formation)
- [Ghostty CONTRIBUTING.md (AI 공개 정책)](https://github.com/ghostty-org/ghostty/blob/main/CONTRIBUTING.md)
