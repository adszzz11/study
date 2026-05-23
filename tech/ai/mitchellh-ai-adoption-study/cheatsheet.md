# Cheatsheet: Mitchell Hashimoto AI 도입 여정

## 6단계 한눈에 보기

```
Step 1: Drop the Chatbot         → 에이전트로 전환
Step 2: Reproduce Your Own Work   → 두 번 일해서 전문성 구축
Step 3: End-of-Day Agents         → 비동기 시간 활용
Step 4: Outsource the Slam Dunks  → 확실한 것만 위임 + 알림 OFF
Step 5: Engineer the Harness      → 실수 → AGENTS.md/스크립트로 재발 방지
Step 6: Always Have an Agent      → 상시 에이전트 운영 (현재 10~20%)
```

---

## 핵심 원칙 7개

| # | 원칙 | 한 줄 설명 |
|---|------|-----------|
| 1 | 비동기 활용 | 일하지 않는 시간에 에이전트를 돌려라 |
| 2 | Harness Engineering | 실수마다 재발 방지 시스템 구축 |
| 3 | 인간이 인터럽트 제어 | 알림 끄기, 자연스러운 전환점에서 확인 |
| 4 | Negative Space | 에이전트를 쓰지 말아야 할 때를 아는 것도 효율 |
| 5 | 범위 외 파괴 주의 | AI는 목표 달성을 위해 다른 것을 깨뜨림 |
| 6 | 이해 없이 출시 금지 | "I'm not shipping code I don't understand" |
| 7 | Skill Formation | 위임 = 기술 미형성. 주니어는 특히 주의 |

---

## 워크플로우 패턴 빠른 참조

### 일일 루틴

```
09:00  에이전트 결과 리뷰 (warm start)
09:15  slam dunk 이슈 → 에이전트 위임 (알림 OFF)
09:20  직접 코딩 (흥미로운/어려운 작업)
~      자연스러운 전환점에서 에이전트 확인
16:30  End-of-Day 에이전트 시작
17:00  퇴근
```

### 세션 패턴

```
Planning  → "Don't write any code" → spec.md 저장
Execution → 좁은 범위 구현 → spec.md 참조
Scaffold  → 사람이 뼈대(TODO) → 에이전트가 채움
Anti-Slop → 에이전트 코드 정리 → 이해 강제
```

### Slop Zone 감지

```
같은 에러 3회 반복 → 즉시 중단 → 접근법 전환
```

---

## AGENTS.md 템플릿

```markdown
# AGENTS.md

## 빌드 & 실행
- 빌드: [명령어]
- 테스트: [명령어]
- 린트: [명령어]

## 코드 스타일
- [규칙들]

## 절대 하지 말 것
- [금지 사항들]

## 검증 방법
- 코드 수정 후: [검증 명령어]
- UI 변경 시: [검증 방법]

## 알아야 할 것
- [프로젝트 컨텍스트]
```

---

## 도구 선택 가이드

```
빠른 질문          → 챗봇 (ChatGPT, Claude)
코딩 작업          → 에이전트 (Claude Code, Amp, Cursor)
복잡한 계획        → Deep Mode (GPT-5.2-Codex, Oracle)
모델 비교          → 여러 체크아웃에서 동시 실행
```

---

## 에이전트 작업 판단 매트릭스

```
                    에이전트 적합
                        ↑
    테스트 코드    │  UI 구현
    보일러플레이트  │  API 엔드포인트
    컴파일에러 수정 │  리서치/조사
  ─────────────────┼─────────────────→ 에이전트 부적합
    리팩토링 (주의) │  아키텍처 설계
    스타일 통일     │  성능 최적화
                   │  Zig 코드
                        ↓
```

---

## 비용 참조

```
Hashimoto 월간: ~$500 (Amp $300 + Claude $200)
Ghostty 업데이트 기능: $15.98 (16세션, 8시간)
시작 추천: Claude Pro $20/월 or Claude Code 종량제
```

---

## 핵심 인용문

> "Instead of trying to do more in the time I have, try to do more in the time I don't have."

> "Anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again."

> "I'm not shipping code I don't understand."

> "I'm a software craftsman that just wants to build stuff for the love of the game."

> "Context switching is very expensive. It was my job as a human to be in control of when I interrupt the agent."

> "If you give an agent a way to verify its work, it more often than not fixes its own mistakes."

---

## 30일 빠른 도입 로드맵

```
Day 1-3:   에이전트 설치 + 첫 사용
Day 4-10:  "두 번 일하기" + AGENTS.md 시작
Day 11-18: 퇴근 전 루틴 + slam dunk 위임
Day 19-25: Harness Engineering + 검증 스크립트
Day 26-30: 회고 + 루틴 확정
```

---

*[[README|목차로 돌아가기]]*
