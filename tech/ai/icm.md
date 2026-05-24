---
date: 2026-05-24
tags:
  - tech
  - ai
  - icm
  - agent-architecture
  - no-framework
status: learning
type: tech-concept
---

# ICM — Interpretable Context Methodology

> **한 줄 정의**: "폴더가 곧 에이전트다" — 프레임워크 대신 번호 매긴 폴더 구조와 마크다운 파일로 AI 에이전트를 구성하는 방법론. 2026-02경 공개, 약 30,000명이 사용 중인 MIT 라이선스 프로토콜.

## 1. What - 개념 정의

ICM은 LangGraph/LangChain 같은 프레임워크 레벨의 오케스트레이션을 **파일시스템 구조로 대체**하는 접근이다. 번호가 붙은 폴더가 워크플로 단계를 나타내고, 각 폴더의 마크다운 파일이 해당 단계의 프롬프트와 컨텍스트를 담는다. 단일 AI 에이전트가 "지금 어느 폴더에 있는지"만 알면 멀티 에이전트 프레임워크 없이도 다단계 작업을 수행할 수 있다.

> **The folder IS the agent. Instructions are markdown. Knowledge is markdown. Tools are scripts.**

### 핵심 개념

- **자동화의 잘못된 레이어**: 대부분의 프레임워크는 "에이전트 간 메시지 패싱"을 추상화하는데, 솔로 빌더에게는 그 레이어가 불필요한 오버헤드
- **컨텍스트가 곧 프로그램**: 어떤 파일을 언제 읽히느냐가 에이전트의 동작을 결정
- **인간이 읽을 수 있는 상태**: 폴더와 마크다운만 보면 시스템 전체 동작이 파악됨

### 주요 용어

| 용어 | 설명 |
|------|------|
| **AGENTS.md** | 에이전트 동작 지시문이 담긴 루트 파일 (CLAUDE.md와 같은 사상) |
| **Numbered Stages** | `01-research/`, `02-draft/`, `03-review/` 식으로 번호 매긴 단계 폴더 |
| **Context Folder** | 참고 문서·도메인 지식이 들어가는 폴더 |
| **Workspace** | 에이전트 출력물이 쌓이는 폴더 |
| **Tool Scripts** | 재사용 가능한 Python/Bash 스크립트 (LLM이 함수 호출 대신 직접 실행) |

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- LangGraph/LangChain의 학습 곡선 + 보일러플레이트 — 솔로 프로젝트에서는 ROI가 낮음
- 프레임워크 추상화가 "에이전트가 지금 뭘 하는지" 가시성을 떨어뜨림
- 멀티 에이전트 메시지 패싱은 인간 리뷰가 끼는 시퀀셜 워크플로에는 과한 설계

### 기존 방식의 한계

| 문제 | 프레임워크 방식 | ICM |
|------|----------------|-----|
| 디버깅 | 그래프 시각화 도구 필요 | `ls`와 `cat`만 있으면 됨 |
| 상태 검사 | 직렬화된 state 객체 분석 | 폴더와 파일 직접 열어보기 |
| 버전 관리 | DB 마이그레이션 | git diff |
| 인계인수 | 코드 + 그래프 정의 학습 | 폴더 구조 따라가면 끝 |
| 의존성 | LangChain 등 무거운 패키지 | 표준 파이썬 + LLM 클라이언트 |

### 영감 받은 분야

- Unix pipeline (작은 도구의 조합)
- 멀티패스 컴파일러 (단계별 변환)
- Literate programming (도널드 커누스 — 문서와 코드의 융합)
- 모듈 분해 / 관심사 분리

---

## 3. How - 동작 원리

### 기본 폴더 구조

```
my-agent/
├── AGENTS.md                  # 루트 지시문 (역할·규칙·목표)
├── 01-research/
│   ├── PROMPT.md              # 이 단계의 지시
│   └── output/                # 단계 출력물
├── 02-draft/
│   ├── PROMPT.md
│   └── output/
├── 03-review/
│   ├── PROMPT.md
│   └── output/
├── context/                   # 참고 문서·도메인 지식
│   ├── style-guide.md
│   └── examples/
├── tools/                     # 재사용 스크립트
│   ├── search.py
│   └── fetch_transcript.py
└── workspace/                 # 최종 출력물
```

### 동작 흐름

1. 사용자가 에이전트(예: Claude Code)에게 `AGENTS.md` 읽게 함
2. 에이전트가 현재 단계(예: `01-research/`) 폴더로 이동, `PROMPT.md` 읽음
3. 필요한 `context/` 파일과 `tools/` 스크립트 활용해 작업 수행
4. 결과를 `01-research/output/`에 저장
5. 사용자가 검토 → OK면 다음 단계 `02-draft/`로 이동 지시
6. 단계마다 반복, 최종 출력은 `workspace/`로

### 핵심 메커니즘

- **상태 = 파일시스템**: 에이전트가 멈춰도 폴더만 보면 어디까지 됐는지 확인 가능
- **인간 게이트 자연 삽입**: 단계 전환 시 사용자가 검토하는 것이 디폴트
- **재시작·재실행 무료**: 특정 폴더 지우고 다시 시키면 끝
- **버전 관리 = git**: 워크플로 변경도 git diff로 추적

---

## 4. 실무 적용

### 예시: YouTube 리서치 에이전트

```
youtube-research/
├── AGENTS.md
├── 01-discover/
│   └── PROMPT.md           # "주제 X에 대한 영상 10개 후보 찾기"
├── 02-fetch-transcript/
│   ├── PROMPT.md           # "tools/fetch_transcript.py로 자막 수집"
│   └── output/             # transcript-*.txt
├── 03-summarize/
│   └── PROMPT.md           # "각 영상 핵심 포인트 5개 추출"
├── 04-synthesize/
│   └── PROMPT.md           # "전체 트렌드/대립 관점 합성"
├── context/
│   └── style-guide.md      # 출력 톤
├── tools/
│   └── fetch_transcript.py # YouTube API 호출
└── workspace/
    └── report.md
```

### Best Practices

- **AGENTS.md는 짧게**: 에이전트가 매번 읽기 때문에 토큰 낭비 주의
- **단계 폴더 안에 PROMPT.md 고정**: 에이전트가 "어디서 무엇을 읽어야 하는지" 추측하지 않게
- **`context/`는 참조용, `workspace/`는 출력용**: 두 폴더의 역할 혼선 금지
- **tools/는 순수 함수**: 부수효과 큰 스크립트는 별도 분리

### Anti-patterns

- 한 폴더에 너무 많은 책임 부여 — 단계가 흐려지면 ICM의 가시성 이점이 사라짐
- 폴더 구조를 LLM이 동적으로 만들게 함 — 인간이 한눈에 못 봄
- `AGENTS.md`에 모든 컨텍스트를 박아넣기 — 단계별 `PROMPT.md`로 분리해야 함
- 프레임워크 코드와 섞기 — ICM의 매력은 "프레임워크 없음" 자체

---

## 5. 비교 분석

### vs 대안 접근

| 비교 항목 | ICM | LangGraph | Claude Skills | CrewAI |
|-----------|-----|-----------|---------------|--------|
| **추상화 레벨** | 파일시스템 | 그래프 노드/엣지 | Markdown + 스크립트 | Agent + Task 클래스 |
| **학습 곡선** | 낮음 (Unix만 알면 됨) | 높음 | 중간 | 중간 |
| **디버깅** | `ls`, `cat`, `git diff` | LangSmith 등 도구 | 파일 직접 확인 | 로그 |
| **인간 리뷰** | 단계 전환 시 자연스러움 | 명시적 interrupt 노드 필요 | 자연스러움 | task 단위 |
| **프로덕션 적합도** | 솔로/소규모 ✅ / 팀 ⚠️ | 팀/엔터프라이즈 ✅ | 개인 + Claude Code ✅ | 중간 |
| **벤더 락인** | 없음 | 없음 (오픈소스) | Anthropic | 없음 |

### 선택 기준

- 솔로 빌더·개인 에이전트 → **ICM** (또는 Claude Skills)
- 팀이 협업하는 프로덕션 시스템 → **LangGraph 등 프레임워크**
- 빠른 PoC + 출력 검토가 중요 → **ICM**
- 멀티 에이전트 메시지 패싱이 본질인 시스템(시뮬레이션, 협상) → 프레임워크

---

## 6. 학습 체크리스트

### 이해도 점검

- [ ] "폴더가 에이전트다"의 의미를 한 문장으로 설명할 수 있다
- [ ] LangGraph 대비 ICM의 강점·약점을 각 2개씩 댈 수 있다
- [ ] AGENTS.md / PROMPT.md / context / tools / workspace 5요소 역할 구분
- [ ] 자기 워크플로 1개를 ICM 구조로 그릴 수 있다

### 추가 학습

- [ ] ICM 영상 시청 ([YouTube](https://youtu.be/956DPSPX4wg))
- [ ] AGENTS.md 표준 [agents.md](https://agents.md/) 확인
- [ ] Claude Code의 `CLAUDE.md` 패턴과 비교 분석

---

## 7. References

- [영상: You're Automating The Wrong Layer (2026-05)](https://youtu.be/956DPSPX4wg)
- [요약 뉴스레터: The simplest way to build AI agents in 2026](https://newsletter.owainlewis.com/p/the-simplest-way-to-build-ai-agents)
- 관련 노트: [[thin-harness-fat-skills]] · [[invisible-interface-agentic-ai]] · [[google-adk-deep-search]]
