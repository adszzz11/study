# Part 2: AI 도구 생태계 & 워크플로우

## Hashimoto가 언급한 AI 도구들

### 도구별 비교

| 도구 | 카테고리 | 사용 목적 | 평가 |
|------|----------|-----------|------|
| **ChatGPT** | 챗봇 | 일상 질의응답 | 코딩에서는 가치 제한적 |
| **Google Gemini** | 챗봇/멀티모달 | SwiftUI 코드 생성 (스크린샷 기반) | 첫 "와우 모먼트" 제공 |
| **Claude Code** | 터미널 에이전트 | 본격적 에이전트 코딩 시작 | 에이전트 전환의 계기 |
| **Amp** | 에이전트 플랫폼 | 현재 주력 도구 | 가장 자주 사용 |
| **Amp Deep Mode** | 에이전트 (GPT-5.2-Codex) | 복잡한 작업 | 30분+ 소요, 높은 품질 |

### 챗봇 vs 에이전트: 근본적 차이

```
챗봇 (Chatbot):
  사람 → 질문 → AI 응답 → 사람이 복사/붙여넣기 → 사람이 검증 → 반복

  문제점: "you're mostly hoping they come up with the right results
           based on their prior training, and correcting them involves
           a human to tell them they're wrong repeatedly."

에이전트 (Agent):
  사람 → 지시 → AI가 파일 읽기/실행/수정/검증 → 자율적 반복

  최소 요구사항:
  ├── 파일 읽기 (Read files)
  ├── 프로그램 실행 (Execute programs)
  └── HTTP 요청 (Make HTTP requests)
```

> "To find value, you must use an agent."

### Hashimoto의 도구 선택 기준

1. **에이전트 능력**: 파일 시스템 접근, 코드 실행, 자기 검증 가능해야 함
2. **모델 경쟁**: 같은 프롬프트로 여러 모델/에이전트를 동시에 테스트
3. **Oracle 모드**: 계획 수립 시 느리지만 더 정확한 모델 선택
4. **비용 대비 효과**: 월 $400~500 수준에서 충분한 가치 확인

## 워크플로우 패턴

### 1. 모델 경쟁 (Model Competition)

> "I will run different models and different agents on different code bases on the same task with the same prompt. It's a competition."

Ghostty 프로젝트에서 여러 코드 체크아웃(ghostty, ghostty2, ghostty3, ghostty4)을 유지하며 같은 작업을 다른 모델에 동시 할당한다.

### 2. 계획-실행 분리 (Planning vs Execution)

```
Phase 1: Planning (Oracle 모드 = 느린 고성능 모델)
  └── "Don't write any code. Consult the oracle"
  └── 결과를 spec.md에 저장

Phase 2: Execution (일반 모드 = 빠른 모델)
  └── spec.md를 참조하여 구현
  └── 좁은 범위의 작업으로 분할
```

### 3. 비동기 에이전트 활용

```
퇴근 30분 전:
├── 딥 리서치 세션 시작 (라이브러리 조사, 라이선스 분석 등)
├── 아이디어 탐색 에이전트 실행 (unknown unknowns 발견)
└── 이슈/PR 트리아지 에이전트 실행 (GitHub CLI 활용)

다음날 아침:
├── 에이전트 결과 리뷰
├── "slam dunk" 작업 식별 → 에이전트 위임
└── 인간은 흥미로운/어려운 작업에 집중
```

### 4. Scaffolding Pattern (뼈대 채우기)

Hashimoto가 자주 쓰는 패턴: 함수 시그니처와 TODO 주석으로 뼈대를 만들고, 에이전트가 구현을 채운다.

```swift
// 사람이 작성
func updateNotificationView(status: UpdateStatus) -> some View {
    // TODO: status에 따라 다른 UI 표시
    // TODO: 애니메이션 적용
    // TODO: 접근성 레이블 추가
}

// 에이전트가 채움 → 사람이 리뷰
```

> "AI is very good at fill-in-the-blank or draw-the-rest-of-the-owl."

### 5. 프로젝트별 차등 품질 기준

| 프로젝트 유형 | 리뷰 수준 | 예시 |
|-------------|----------|------|
| 장기 오픈소스 | 모든 라인 리뷰 | Ghostty (성능: 프레임당 9us까지 중요) |
| 일회성 프로젝트 | 코드 리뷰 없음 | 가족 결혼식 웹사이트 |

## 비용 현황 (2025년 말 ~ 2026년 초)

| 월 | Amp | Claude | 합계 |
|----|-----|--------|------|
| 2025.10 | ~$400 | ~$200 | ~$600 |
| 2025.11 | ~$400 | ~$200 | ~$600 |
| 2025.12 | ~$300 | ~$200 | ~$500 |

## 관련 도구 생태계

Hashimoto의 접근법과 관련된 도구들:

| 도구 | 설명 | Hashimoto와의 관계 |
|------|------|-------------------|
| AGENTS.md / CLAUDE.md | 프로젝트별 AI 지시서 | 핵심 Harness Engineering 도구 |
| GitHub CLI (`gh`) | 이슈/PR 관리 | 트리아지 에이전트의 핵심 도구 |
| Ghostty | 고성능 터미널 에뮬레이터 | AI 에이전트의 실행 환경 |
| Sparkle | macOS 업데이트 프레임워크 | AI로 구현한 기능의 대상 |
