# 04. 실전 적용 팁

## 📌 핵심 개념

Hashimoto의 여정에서 추출한 **즉시 적용 가능한 실전 기법**들이다. 각 팁은 구체적인 행동 지침과 함께 제시된다.

---

## Tip 1: 퇴근 30분 전 에이전트를 시작하라

### 행동 지침

```
17:00 퇴근이라면:

16:30 - 현재 작업 상태 정리 (커밋 또는 스태시)
16:35 - 에이전트 작업 1개 이상 시작:
        ├── 딥 리서치: "X 라이브러리 조사해줘"
        ├── 탐색: "이 이슈 해결 접근법 시도해봐"
        └── 트리아지: "최근 이슈 분류해줘"
17:00 - 퇴근 (에이전트는 계속 실행)

09:00 (다음 날) - 에이전트 결과 리뷰로 시작
```

### 주의

- 밤새 돌리지 않아도 됨 — 대부분 30분 이내 완료
- 목표는 **warm start** — 다음 날 컨텍스트 로딩 시간 절약

---

## Tip 2: 작업을 "두 번 하는" 훈련을 최소 2주 하라

### 행동 지침

```
Week 1-2 훈련 루틴:

1. 수동으로 작업 완료 → git commit
2. 새 브랜치에서 같은 작업을 에이전트로 시도
3. 결과 비교:
   - 에이전트가 더 나은 부분은?
   - 에이전트가 실패한 부분은?
   - 어떤 프롬프트가 효과적이었나?
4. 발견사항을 기록

Week 3부터: 에이전트 강점 영역은 바로 위임
```

### 왜 이것이 중요한가

> "Expertise formed. I quickly discovered for myself from first principles what others were already saying, but discovering it myself resulted in a stronger fundamental understanding."

남이 하는 말을 듣는 것과 직접 발견하는 것은 다르다.

---

## Tip 3: AGENTS.md를 즉시 시작하라

### 행동 지침

프로젝트 루트에 AGENTS.md (또는 CLAUDE.md) 파일을 생성하고, **에이전트가 실수할 때마다 한 줄씩 추가**한다.

```markdown
# AGENTS.md

## 빌드 & 실행
- 빌드: `npm run build` (webpack 아님)
- 테스트: `npm test -- --filter=<파일명>`
- 린트: `npm run lint` (push 전 반드시 실행)

## 코드 스타일
- import 순서: React → 외부 라이브러리 → 내부 모듈 → 스타일
- 컴포넌트 파일명: PascalCase.tsx
- 유틸 파일명: camelCase.ts

## 절대 하지 말 것
- package.json의 dependencies를 직접 수정하지 말 것 → npm install 사용
- .env 파일을 읽거나 출력하지 말 것
- main 브랜치에 직접 커밋하지 말 것

## 알아야 할 것
- API 엔드포인트는 /api/v2/ 접두사 사용
- 인증 토큰은 Authorization 헤더에 Bearer 형식으로
- DB 마이그레이션은 prisma migrate dev
```

### 핵심 원칙

> "Each line in that file is based on a bad agent behavior."

추상적 지침이 아니라, **실제 발생한 실수에 기반한 구체적 규칙**을 작성한다.

---

## Tip 4: 에이전트 알림을 끄라

### 행동 지침

```bash
# macOS에서 알림 끄기
# System Settings → Notifications → [에이전트 앱] → 알림 허용 OFF

# 또는 집중 모드 활용
# "코딩" 집중 모드 생성 → 에이전트 앱 알림 차단
```

### 대안: 자연스러운 전환점에서 확인

```
좋은 확인 타이밍:
  ✅ 현재 함수/기능 구현 완료 후
  ✅ 커밋 후
  ✅ 커피 브레이크 후
  ✅ 코드 리뷰 완료 후

나쁜 확인 타이밍:
  ❌ 복잡한 로직 작성 중
  ❌ 디버깅 세션 중
  ❌ 아키텍처 설계 중
```

---

## Tip 5: 계획과 실행을 분리하라

### 행동 지침

```
잘못된 접근:
  "이 이슈를 해결해줘" → 에이전트가 바로 코딩 시작 → 방향 잘못 잡음

올바른 접근:
  Session 1 (Planning):
    "이 이슈를 분석하고 해결 방법 3가지를 제안해줘.
     코드는 작성하지 마. plan.md에 저장해."

  [인간이 계획 리뷰 → 방향 결정]

  Session 2 (Execution):
    "plan.md의 방법 2를 구현해줘.
     범위: src/components/UpdateView.tsx만 수정."
```

### Oracle 패턴 (Amp Deep Mode)

계획 세션에는 **느리지만 더 정확한 모델**을 사용:

> "Don't write any code. Consult the oracle."

---

## Tip 6: 에이전트에게 검증 수단을 제공하라

### 행동 지침

에이전트가 자기 작업을 스스로 검증할 수 있게 하면, 실수를 **자율적으로 수정**한다:

```markdown
# AGENTS.md에 추가

## 검증 방법
- 코드 수정 후 반드시 `npm test` 실행
- UI 변경 시 `./scripts/screenshot.sh` 로 스크린샷 촬영
- API 변경 시 `curl localhost:3000/api/health` 로 확인
- 타입 체크: `npx tsc --noEmit`
```

> "If you give an agent a way to verify its work, it more often than not fixes its own mistakes and prevents regressions."

---

## Tip 7: Slop Zone을 인식하고 pivot하라

### 행동 지침

```
Slop Zone 감지 기준:
  - 같은 에러가 3회 이상 반복
  - 에이전트가 이전에 적용한 수정을 되돌림
  - 에러 메시지가 변하지 않음

감지 시 행동:
  1. 즉시 세션 중단
  2. 문제를 직접 분석 (에이전트 없이)
  3. 접근법 전환 결정
  4. 새 세션에서 다른 접근법으로 시작
```

Hashimoto는 Ghostty 자동 업데이트 기능에서 세션 11~14가 Slop Zone이었고, 15에서 접근법을 전환하여 해결했다.

---

## Tip 8: 모델 경쟁을 활용하라

### 행동 지침

```bash
# 프로젝트 디렉토리를 여러 개 유지
cp -r myproject myproject-claude
cp -r myproject myproject-amp

# 동일 프롬프트로 다른 모델에 동시 요청
# myproject-claude/: Claude Code로 작업
# myproject-amp/: Amp으로 작업

# 결과 비교
diff -r myproject-claude/src myproject-amp/src
```

**활용 시점**: 새로운 기능의 첫 구현 시, 어떤 모델이 해당 도메인에 강한지 파악

---

## Tip 9: Scaffolding 패턴을 기본으로 사용하라

### 행동 지침

전체 기능을 에이전트에게 맡기지 말고, **뼈대를 직접 작성하고 구현을 채우게 하라**:

```typescript
// 사람이 작성하는 뼈대
export class NotificationManager {
  private sparkle: SparkleFramework;

  constructor(config: NotificationConfig) {
    // TODO: Sparkle 초기화
    // TODO: 업데이트 확인 주기 설정
  }

  async checkForUpdates(): Promise<UpdateResult> {
    // TODO: Sparkle API로 업데이트 확인
    // TODO: 결과를 UpdateResult 타입으로 변환
    // TODO: 에러 핸들링 (네트워크 실패, 타임아웃)
  }

  showNotification(update: UpdateInfo): void {
    // TODO: 비간섭적 UI 알림 표시
    // TODO: "지금 업데이트" / "나중에" 버튼
    // TODO: 접근성 레이블
  }
}
```

> "AI is very good at fill-in-the-blank or draw-the-rest-of-the-owl."

---

## Tip 10: Anti-Slop 세션을 반드시 수행하라

### 행동 지침

에이전트가 생성한 코드를 **정리하고 재구조화**하는 전용 세션:

```
Anti-Slop 세션 체크리스트:
  □ 불필요한 코드 삭제
  □ 네이밍 컨벤션 통일
  □ 함수 분리 / 합치기
  □ 주석 정리 (에이전트의 장황한 주석 제거)
  □ 에러 핸들링 확인
  □ 타입 안전성 검증
  □ 문서 추가 (다음 에이전트 세션을 위해)
```

### 왜 중요한가

1. 코드를 **이해**하게 만드는 강제 메커니즘
2. 다음 에이전트 세션의 **품질 향상** (깨끗한 코드 = 더 나은 결과)
3. **기술 부채 방지**

---

## 💻 실전 예시: 일일 루틴 (Hashimoto 스타일)

```
09:00 - 에이전트 결과 리뷰 (전날 밤 warm start)
09:15 - Slam dunk 이슈 식별 → 에이전트 1개 시작
09:20 - 직접 코딩 시작 (흥미로운/어려운 작업)
        [에이전트 알림 OFF]
11:00 - 자연스러운 전환점 → 에이전트 결과 확인
11:10 - Anti-Slop 세션 or 다음 slam dunk 위임
11:20 - 직접 코딩 재개
12:00 - 점심 (필요 시 Breakage Delegation)
13:00 - 에이전트 결과 확인 → 코딩 재개
16:30 - End-of-Day 에이전트 시작
        ├── 리서치 에이전트
        └── 트리아지 에이전트
17:00 - 퇴근
```

---

## ✅ 체크포인트

- [ ] 퇴근 전 30분 루틴을 자신의 일과에 통합할 수 있는가?
- [ ] AGENTS.md를 자신의 프로젝트에 만들었는가?
- [ ] 에이전트 알림을 끄고 자연스러운 전환점에서 확인하는 습관이 있는가?
- [ ] Slop Zone을 감지하는 기준(3회 반복 실패)을 기억하는가?
- [ ] Scaffolding 패턴을 일상적으로 사용하고 있는가?

## ⚠️ 주의사항

| 주의 | 설명 |
|------|------|
| 모든 팁을 한꺼번에 적용하지 말 것 | 1~2개씩 점진적으로 도입 |
| AGENTS.md를 다른 사람의 것을 복사하지 말 것 | 자신의 에이전트 실수에서 쌓아야 효과적 |
| 모델 경쟁에 과도한 비용 쓰지 말 것 | 초기 탐색 시에만 사용 |
| Anti-Slop 세션을 건너뛰지 말 것 | "이해 못하는 코드 = 기술 부채" |
| Scaffolding 없이 "전체 구현" 요청하지 말 것 | 범위가 넓을수록 품질 하락 |

## 🔗 더 알아보기

- [[05-apply-to-my-workflow|다음: 나의 워크플로우에 적용하기]]
- [[03-key-insights|이전: 핵심 인사이트와 교훈]]
- [Ghostty AGENTS.md 예시](https://github.com/ghostty-org/ghostty)
- [Claude Code CLAUDE.md 가이드](https://docs.anthropic.com/en/docs/claude-code)
