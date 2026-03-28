---
date: 2026-03-28
tags:
  - tech
  - ai
  - claude
  - cowork
  - dispatch
  - computer-use
  - agent
status: learning
type: tech-series
---

# Claude Cowork & Dispatch

## 1. What - 개념 정의

> **한 줄 정의**: Claude가 데스크톱 앱에서 지속적으로 실행되며, 모바일에서 작업을 지시하면 컴퓨터를 직접 조작하여 작업을 완료하는 에이전트 시스템

### 핵심 개념

- **Cowork** (2026년 1월 출시): 코딩을 넘어 모든 지식 근로자를 위한 AI 생산성 도구. "Vibe Working" 컨셉
- **Dispatch** (2026년 3월 17일 출시): Cowork 내 기능으로, 모바일에서 작업을 지시하면 데스크톱에서 자율적으로 실행하는 영구 에이전트 스레드
- **Computer Use**: Claude가 화면을 보고, 클릭/타이핑/네비게이션을 수행하는 기능

### 주요 용어

| 용어 | 설명 |
|------|------|
| Cowork | Claude Desktop 내 AI 작업 환경 (코딩 이외 지식 업무 포함) |
| Dispatch | 모바일 → 데스크톱 원격 작업 지시 & 실행 기능 |
| Persistent Thread | 세션이 리셋되지 않는 영구 대화 스레드 (이전 컨텍스트 유지) |
| Computer Use | Claude가 데스크톱 UI를 직접 조작하는 기능 (클릭, 타이핑 등) |
| Task Routing | 작업 유형에 따라 Claude Code 또는 Cowork로 자동 라우팅 |
| Approval Workflow | 중요 의사결정 시 모바일로 승인 요청 알림 전송 |

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- AI 어시스턴트가 대화만 가능하고 실제 컴퓨터 작업을 수행하지 못함
- 자리를 비울 때 AI가 자율적으로 작업을 이어갈 수 없음
- 매 세션마다 컨텍스트가 리셋되어 연속적인 작업 관리 불가

### 기존 방식의 한계

- 기존 AI 채팅: 텍스트 응답만 가능, 실제 실행은 사용자 몫
- Claude Code: 터미널 기반, 코딩 작업 특화, 일반 데스크톱 작업 불가
- 일반 자동화 도구(Zapier 등): 사전 정의된 워크플로우만 가능, 유연성 부족

---

## 3. How - 동작 원리

### 아키텍처

```
┌──────────────┐          ┌─────────────────────────────┐
│  📱 Mobile    │  작업    │  💻 Desktop                  │
│  (iOS/Android)│─────────▶│  ┌───────────────────────┐  │
│              │          │  │  Claude Desktop App    │  │
│  작업 지시    │          │  │                       │  │
│  승인/거부    │◀─────────│  │  ┌─────────────────┐  │  │
│  결과 확인    │  알림     │  │  │ Dispatch Agent  │  │  │
│              │          │  │  │  - Computer Use │  │  │
└──────────────┘          │  │  │  - Task Routing │  │  │
                          │  │  │  - File Access  │  │  │
                          │  │  └─────────────────┘  │  │
                          │  └───────────────────────┘  │
                          │                             │
                          │  앱 실행, 브라우저 조작,      │
                          │  스프레드시트 편집, 파일 관리   │
                          └─────────────────────────────┘
```

### 동작 흐름

1. 모바일 Claude 앱에서 Dispatch 스레드에 작업 지시 (예: "이번 주 회의록 정리해줘")
2. Claude Desktop이 작업을 수신하고 유형에 따라 라우팅
   - 코딩 작업 → Claude Code로 전달
   - 리서치/데스크톱 작업 → Cowork에서 직접 처리
3. Computer Use로 데스크톱 앱들을 직접 조작 (브라우저, 스프레드시트 등)
4. 중요 의사결정이 필요한 경우 모바일로 승인 요청 알림
5. 작업 완료 후 결과를 모바일 앱에서 확인

### Computer Use 성능

| 벤치마크 | Sonnet 4.5 이전 | Sonnet 4.6 |
|----------|-----------------|------------|
| OSWorld (데스크톱 작업) | ~15% | **72.5%** |

---

## 4. 실무 적용

### 사용 사례

- **원격 파일 처리**: 스프레드시트에서 데이터 추출/정리
- **자동 리서치**: 웹 검색 → 정보 수집 → 문서 정리
- **프레젠테이션 생성**: 기존 자료를 기반으로 슬라이드 제작
- **이메일/문서 작성**: Gmail, Google Docs 등에서 직접 작성
- **코드 마이그레이션**: Spotify 사례 - 엔지니어링 시간 90% 절감

### Task Routing 예시

```
사용자: "PR #15 리뷰해줘"
  → Claude Code로 라우팅 → 코드 분석 → 결과 반환

사용자: "이번 달 매출 데이터 정리해줘"
  → Cowork로 라우팅 → 스프레드시트 열기 → 데이터 처리 → 결과 반환
```

### 요구사항

| 항목 | 내용 |
|------|------|
| 데스크톱 | Claude Desktop (macOS/Windows x64) - 항상 열려 있어야 함 |
| 모바일 | Claude iOS/Android 최신 버전 |
| 구독 | Pro 또는 Max 플랜 필수 |
| 네트워크 | 양쪽 디바이스 인터넷 연결 필요 |

### Best Practices

- 복잡한 작업은 단계별로 나눠서 지시
- 민감한 작업은 Approval Workflow를 통해 확인 후 실행
- Persistent Thread의 컨텍스트를 활용하여 연속 작업 관리

### Anti-patterns (주의사항)

- ❌ 데스크톱 앱이 닫혀있으면 Dispatch 사용 불가
- ❌ 별도 사용량 풀 없음 — 기존 플랜 사용량에서 차감
- ❌ 리서치 프리뷰 단계이므로 안정성 이슈 가능

---

## 5. Enterprise 기능

### Deep Connectors

| 서비스 | 기능 |
|--------|------|
| Google Drive | 문서 탐색, 데이터 합성 |
| Gmail | 이메일 초안 작성 |
| DocuSign | 조항 분석 |
| FactSet | 금융 데이터 접근 |

### Private Plugin Marketplace

- 기업이 승인된 에이전트를 조직 내 배포
- 관리자가 도구 접근 권한 통제
- 산업별 특화 플러그인 구성 가능

---

## 6. 학습 체크리스트

### 이해도 점검

- [ ] Cowork, Dispatch, Computer Use의 차이를 설명할 수 있다
- [ ] Dispatch의 동작 흐름을 이해한다
- [ ] Task Routing의 개념과 동작 방식을 설명할 수 있다
- [ ] Persistent Thread가 기존 채팅과 어떻게 다른지 안다

### 실습 과제

- [ ] Claude Desktop + 모바일 앱으로 Dispatch 사용해보기
- [ ] Computer Use로 간단한 데스크톱 작업 자동화해보기
- [ ] Approval Workflow 동작 확인하기

---

## 7. References

- [Claude Cowork Dispatch 가이드](https://www.analyticsvidhya.com/blog/2026/03/claude-cowork-dispatch/)
- [Tom's Guide - Cowork 사용기](https://www.tomsguide.com/ai/i-sent-claude-a-task-from-my-phone-and-it-finished-it-on-my-laptop-without-me-touching-a-thing)
- [Claude 도움말 - Dispatch](https://support.claude.com/en/articles/13947068-assign-tasks-to-claude-from-anywhere-in-cowork)
- 관련 노트: [[10-channels]], [[12-2026-updates]]
