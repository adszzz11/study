# 02. 사용한 AI 도구들과 워크플로우

## 📌 핵심 개념

Hashimoto의 AI 워크플로우는 **"올바른 도구를 올바른 상황에"** 라는 원칙에 기반한다. 챗봇, 에이전트, 심층 모드를 각각 다른 목적으로 사용하며, **모델 경쟁**과 **계획-실행 분리** 패턴이 핵심이다.

---

## 도구별 상세 분석

### 1. 챗봇 (ChatGPT, Gemini)

**역할**: 일상적 질의응답, 아이디어 탐색

```
사용하는 경우:
  ✅ 빠른 질문/답변 (API 문법, 라이브러리 사용법)
  ✅ 스크린샷 기반 UI 재현 (Gemini)
  ✅ 브레인스토밍

사용하지 않는 경우:
  ❌ 기존 코드베이스에서의 코딩 (brownfield)
  ❌ 복잡한 멀티스텝 작업
  ❌ 파일 시스템 접근이 필요한 작업
```

> "Chatbots have real value and are a daily part of my AI workflow, but their utility in coding is highly limited."

**첫 와우 모먼트**: Zed의 커맨드 팔레트 스크린샷 → Gemini → SwiftUI 코드 → Ghostty에 탑재

### 2. Claude Code (터미널 에이전트)

**역할**: 에이전트 코딩의 시작점

```
장점:
  ✅ 터미널 기반 = 기존 워크플로우에 자연스럽게 통합
  ✅ 파일 읽기/쓰기, 프로그램 실행 가능
  ✅ CLAUDE.md로 프로젝트별 지시 가능

Hashimoto의 사용 이력:
  - Step 2 "두 번 일하기"에서 주로 사용
  - 이후 Amp으로 주력 이동
```

### 3. Amp (현재 주력)

**역할**: 일상적 에이전트 코딩

```
특징:
  ✅ 에이전트 플랫폼 (파일/실행/HTTP 통합)
  ✅ Deep Mode (GPT-5.2-Codex 기반) 지원
  ✅ 비동기 작업에 최적화

비용: 월 $300~$400
```

### 4. Amp Deep Mode (GPT-5.2-Codex)

**역할**: 복잡하고 시간이 오래 걸리는 작업

```
특징:
  - 소규모 변경에도 30분+ 소요
  - 대신 높은 품질의 결과
  - 비동기 작업(Step 3)에 이상적
```

---

## 핵심 워크플로우 패턴

### 패턴 1: 모델 경쟁 (Model Competition)

```
ghostty/   → Agent A (Claude) 실행
ghostty2/  → Agent B (GPT-5.2) 실행
ghostty3/  → Agent C (Gemini) 실행
ghostty4/  → 예비 체크아웃

같은 프롬프트, 같은 작업, 다른 모델
→ 결과 비교 → 최선의 결과 채택
```

> "I will run different models and different agents on different code bases on the same task with the same prompt. It's a competition."

**활용 시점**: 새로운 기능 구현 시작 시, 어떤 모델이 해당 작업에 강한지 모를 때

### 패턴 2: 계획-실행 분리 (Planning-Execution Split)

```
Session 1: Planning (Oracle/Deep Mode)
  프롬프트: "Don't write any code. Consult the oracle."
  결과: spec.md에 저장
  목표: 아키텍처 결정, 접근법 탐색

Session 2~N: Execution (일반 모드)
  프롬프트: "spec.md를 참조하여 [구체적 작업] 구현"
  결과: 코드 생성 + 테스트
  목표: 좁은 범위의 구현
```

### 패턴 3: 비동기 에이전트 (End-of-Day Pattern)

```
17:30 (퇴근 30분 전):
  ├── 딥 리서치 에이전트 시작
  │   "Zig의 HTTP 라이브러리 중 MIT 라이선스인 것들을
  │    조사하고 장단점 정리해줘"
  │
  ├── 탐색 에이전트 시작
  │   "이 이슈를 해결할 수 있는 접근법 3가지를 코드로 시도해봐"
  │
  └── 트리아지 에이전트 시작
      "gh issue list로 최근 이슈를 분류하고 보고해줘"

09:00 (다음 날 아침):
  ├── 에이전트 결과 리뷰 (warm start)
  ├── slam dunk 작업 식별 → 에이전트 위임
  └── 어려운 작업 → 직접 수행
```

### 패턴 4: Scaffolding (뼈대 채우기)

```swift
// 사람이 작성하는 뼈대
struct UpdateNotificationView: View {
    @Binding var status: UpdateStatus

    var body: some View {
        // TODO: status별 다른 아이콘 표시
        // TODO: 프로그레스 바 (다운로드 중)
        // TODO: "지금 업데이트" 버튼
        // TODO: 애니메이션 전환
        // TODO: VoiceOver 접근성
    }
}

// 에이전트에게 위임: "TODO를 구현해줘"
// 에이전트가 채운 뒤 → 사람이 라인별 리뷰
```

> "AI is very good at fill-in-the-blank or draw-the-rest-of-the-owl."

### 패턴 5: Breakage Delegation (파손 위임)

```
상황: 대규모 리팩토링으로 컴파일 에러 다수 발생

사람: "I broke a bunch of things, please fix my mess"
     → 회의 참석

에이전트: 컴파일 에러 수정 (타입 불일치, 임포트 누락 등)

사람: 회의 후 결과 리뷰
```

회의, 점심 등 **자리를 비울 때** 에이전트가 기계적 수정 작업을 수행.

### 패턴 6: 영감으로서의 AI (Inspiration, Not Implementation)

```
1. 에이전트에게 구현 요청
2. 생성된 코드를 읽고 아이디어만 흡수
3. 코드 전체를 삭제
4. 새로운 이해를 바탕으로 직접 작성
```

> 에이전트를 "my muse"(뮤즈)로 활용. 결과물이 아닌 **아이디어**를 얻는 용도.

---

## 💻 실전 예시: Ghostty 자동 업데이트 (16 세션 분석)

| 세션 | 유형 | 내용 | 결과 |
|------|------|------|------|
| 1 | Planning | Sparkle 프레임워크 조사 (Oracle) | spec.md 생성 |
| 2-3 | Prototyping | UI만 구현 (전체 기능 X) | SwiftUI 뷰 |
| 4-6 | Implementation | 뼈대 채우기 (Scaffolding) | 기능 구현 |
| 7-10 | Iteration | 버그 수정, 엣지 케이스 | 안정화 |
| 11-14 | Slop Zone | 같은 버그 반복 실패 | **위험 구간** |
| 15 | Pivot | 접근법 전환 | 문제 해결 |
| 16 | Review | "What else am I missing?" | 최종 리뷰 |

**핵심 교훈**:
- 세션 11~14의 "Slop Zone"을 인식하고 pivot하는 판단력이 중요
- 총 비용 $15.98 (커피숍 비용보다 저렴)
- **"I'm not shipping code I don't understand"** — 최종 수동 리뷰 필수

---

## 프로젝트별 차등 기준

| 기준 | Ghostty (장기 OSS) | 일회성 프로젝트 |
|------|-------------------|---------------|
| 코드 리뷰 | 모든 라인 | 없음 |
| 성능 기준 | 프레임당 9us | N/A |
| AI 공개 | 필수 (CONTRIBUTING.md) | N/A |
| AGENTS.md | 상세 유지 | 최소한 |

---

## ✅ 체크포인트

- [ ] 챗봇과 에이전트를 언제 사용할지 구분할 수 있는가?
- [ ] 모델 경쟁 패턴을 자신의 프로젝트에 적용할 수 있는가?
- [ ] 계획-실행 분리를 실천할 준비가 되었는가?
- [ ] Scaffolding 패턴으로 에이전트에게 작업을 위임할 수 있는가?
- [ ] "Slop Zone"을 인식하고 pivot할 판단 기준이 있는가?

## ⚠️ 주의사항

| 주의 | 설명 |
|------|------|
| 챗봇으로 복잡한 코딩 시도하지 말 것 | 브라운필드 프로젝트에서는 에이전트 필수 |
| 모델 경쟁은 시작 시에만 | 매번 경쟁시키면 비용 낭비 |
| Deep Mode의 시간 비용 고려 | 30분+ 소요 → 비동기 작업에만 적합 |
| Slop Zone에서 집착하지 말 것 | 3~4회 실패 시 접근법 전환 |
| Zig 코드는 아직 AI 한계 | Hashimoto 본인도 "hopeless"로 평가 |

## 🔗 더 알아보기

- [[03-key-insights|다음: 핵심 인사이트와 교훈]]
- [[01-adoption-stages|이전: AI 도입 단계별 여정]]
- [Vibing a Non-Trivial Ghostty Feature (16세션 전문)](https://mitchellh.com/writing/non-trivial-vibing)
