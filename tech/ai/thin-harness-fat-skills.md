---
date: 2026-05-21
tags:
  - tech
  - concept
  - ai
  - agents
  - skills
  - architecture
status: learning
type: tech-concept
---

# Thin Harness, Fat Skills

> 출처: 트위터 공유 에세이 — Garry Tan/YC 진영 발신 추정 (Chase Center July 2026 Startup School 사례 포함). Steve Yegge "100x productivity" 인용으로 시작.

## 1. What - 개념 정의

> **한 줄 정의**: AI 코딩 에이전트의 100배 생산성은 더 똑똑한 모델이 아니라 **얇은 하니스(harness) + 두꺼운 스킬(skills)** 아키텍처에서 나온다.

### 핵심 명제

- **2x 사용자와 100x 사용자는 같은 모델을 쓴다** — 차이는 지능이 아니라 아키텍처
- 모델은 추론/합성/코딩 능력 충분하다 — **문제는 모델이 너의 데이터/스키마/관습을 모른다**는 것
- 2026-03-31 Claude Code 소스코드 51만 줄 유출이 이 명제를 입증 — "비밀은 모델이 아니라 모델을 감싸는 것(harness)"
- 정답 형태: **Fat Skills(두꺼운 스킬) + Thin Harness(얇은 하니스) + Deterministic Tools(결정적 도구)**

### 주요 용어

| 용어 | 설명 |
|------|------|
| Harness | LLM을 실행시키는 프로그램 (루프, 파일 I/O, 컨텍스트 관리, 안전 — 그게 전부) |
| Skill File | "어떻게 할지(process)" 가르치는 재사용 가능한 마크다운. 메서드 호출처럼 파라미터 받음 |
| Resolver | 컨텍스트의 라우팅 테이블 — "태스크 X일 땐 문서 Y 먼저 로드" |
| Latent space | 모델의 판단/합성/패턴 인식이 일어나는 곳 — 지능이 사는 곳 |
| Deterministic | 같은 입력 → 같은 출력. SQL, 컴파일 코드, 산술 — 신뢰가 사는 곳 |
| Diarization | 모델이 수십~수백 문서를 읽고 한 페이지 구조화 프로파일로 합성하는 단계 |
| Fat Skill | 두꺼운 스킬 — 판단 프로세스를 마크다운으로 인코딩, 가치의 90% 거주 |
| Thin Harness | 200줄짜리 CLI — JSON 입력 / 텍스트 출력 / 기본 read-only |

---

## 2. Why - 등장 배경 & 필요성

### 안티패턴: Fat Harness + Thin Skills

> "40+ tool definitions eating half the context window. God-tools with 2-to-5-second MCP round-trips. REST API wrappers that turn every endpoint into a separate tool. Three times the tokens, three times the latency, three times the failure rate."

- 너무 많은 툴 정의 → 컨텍스트 윈도우 절반 소진
- MCP 라운드트립 2-5초짜리 god-tools
- REST API 모든 엔드포인트 = 별도 툴 (낭비)
- 결과: 토큰 3배, 지연 3배, 실패 3배

### Steve Yegge의 100x 명제

> "10x to 100x as productive as engineers using Cursor and chat today, and roughly 1000x as productive as Googlers were back in 2005."

- 진짜 숫자다. 저자도 직접 경험.
- 사람들은 잘못된 설명에 손을 뻗는다 → "더 똑똑한 모델", "더 많은 파라미터"
- 실제 답: **인덱스 카드 한 장에 맞는 아키텍처 차이**

### 해결하려는 문제

- 컨텍스트 폭주 (Context bloat)
- 도구 다중화로 인한 토큰/지연 폭증
- 결정 가능한 작업이 latent space로 잘못 들어감 (예: 800명 좌석 배치 → 환각)
- 일회성 작업이 반복되는데 매번 수동 → 영구 자산 누락

### 기존 방식의 한계

| 항목 | 안티패턴 | Thin Harness + Fat Skills |
|------|---------|---------------------------|
| 가치 위치 | 하니스 | 스킬 (90%) |
| 컨텍스트 | 폭주 | 디스크립션 → 적시 로드 |
| 도구 | 40+ MCP god-tools | 100ms CLI 빠르고 좁게 |
| 결정적 작업 | 모델이 어림짐작 | 결정적 레이어로 위임 |
| 반복 작업 | 매번 수동 | 첫 회만 수동 → 스킬 → 크론 |
| 모델 업그레이드 효과 | 무관 | 모든 스킬 즉시 향상 |

---

## 3. How - 다섯 가지 정의

### Definition 1: Skill Files

스킬 파일 = **"무엇을 할지"가 아니라 "어떻게 할지"**를 가르치는 재사용 가능한 마크다운.

**핵심 통찰**: 스킬은 **메서드 호출처럼 파라미터를 받는다**.

```text
/investigate 스킬 (7단계):
  scope the dataset → build timeline → diarize every doc
  → synthesize → argue both sides → cite sources

파라미터: TARGET, QUESTION, DATASET

호출 1: TARGET=안전 과학자, DATASET=2.1M discovery emails
  → 의학 연구 분석가 (내부고발자 침묵 여부 조사)

호출 2: TARGET=shell company, DATASET=FEC filings
  → 포렌식 조사관 (캠페인 기부 추적)

같은 스킬. 같은 7단계. 같은 마크다운. 다른 세계.
```

> "This is not prompt engineering. This is software design, using markdown as the programming language and human judgment as the runtime."

마크다운은 프로세스/판단/컨텍스트를 모델이 사고하는 언어로 인코딩하기에 **소스코드보다 더 완벽한 캡슐화 도구**.

### Definition 2: The Harness

하니스 = LLM 실행 프로그램, **딱 4가지만** 한다:
1. 모델을 루프로 돌린다
2. 파일을 읽고 쓴다
3. 컨텍스트를 관리한다
4. 안전을 강제한다

그게 "Thin"의 의미.

**Good 패턴**:
- Playwright CLI — 브라우저 작업 각각 100ms
- Chrome MCP의 screenshot-find-click-wait-read 15초 vs 100ms → **75배 빠름**
- 소프트웨어는 더 이상 귀하지 않다. **딱 필요한 것만, 그 이상은 안 만든다**.

### Definition 3: Resolvers

리졸버 = **컨텍스트의 라우팅 테이블**.

> Skills tell the model **how**. Resolvers tell it **what to load and when**.

**예시**: 개발자가 프롬프트 수정 → 리졸버 없으면 그대로 ship → 리졸버가 `docs/EVALS.md` 먼저 로드 → "정확도 2% 이상 하락 시 revert" 규칙 작동.

**Claude Code의 내장 리졸버**: 모든 스킬의 `description` 필드 → 모델이 사용자 의도와 자동 매칭. `/ship` 존재를 외울 필요 없다.

**저자 고백**:
- 자기 `CLAUDE.md`가 **20,000줄**이었음 — 모든 quirk, 패턴, 교훈 다 박았더니 모델 어텐션 붕괴
- Claude Code가 직접 줄이라고 경고
- 수정안: **200줄로 축소** — 그냥 문서 포인터만
- 20,000줄 지식은 디스크에 있고, 리졸버가 적시 로드 → 컨텍스트 오염 없이 접근

### Definition 4: Latent vs. Deterministic

> Every step in your system is one or the other, and confusing them is the most common mistake in agent design.

| 차원 | 사는 곳 | 적합한 작업 |
|------|--------|-----------|
| Latent space | 지능 | 판단, 합성, 패턴 인식 |
| Deterministic | 신뢰 | SQL, 컴파일, 산술 |

**예시**:
- 8명 디너 테이블 좌석 배치 (성격, 사회 역학 고려) → **Latent 적합** ✓
- 800명 좌석 배치 → 모델이 그럴듯한 환각 차트 생성 → **Deterministic 작업이 잘못 latent에 들어감** ✗
- 800명은 조합 최적화 — 결정적 알고리즘에 위임

> "The worst systems put the wrong work on the wrong side of this line. The best systems are ruthless about it."

### Definition 5: Diarization

다이어라이제이션 = **모델이 수십~수백 문서를 읽고 한 페이지 구조화 판단을 작성하는 단계**.

- SQL 쿼리로 안 됨
- RAG 파이프라인으로 안 됨
- **모델이 직접 읽고, 모순을 머리에 유지하고, 시간에 따라 무엇이 바뀌었는지 알아채고, 구조화 인텔리전스로 합성**해야 함
- DB 룩업 vs 분석가의 브리프 차이

---

## 4. 아키텍처 — 3-Layer

```
┌─────────────────────────────────────────┐
│ Fat Skills (top)                        │  ← 가치의 90%
│ 마크다운 절차, 판단, 도메인 지식        │
│                                         │
│ 푸쉬 UP → 지능을 스킬로                 │
└─────────────────────────────────────────┘
              ↑
┌─────────────────────────────────────────┐
│ Thin CLI Harness (middle, ~200 LOC)     │  ← 통제 면 (얇음)
│ JSON in / text out, read-only by default│
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ Application (bottom)                    │  ← 결정적 토대
│ QueryDB, ReadDoc, Search, Timeline      │
│                                         │
│ 푸쉬 DOWN → 실행을 결정적 도구로        │
└─────────────────────────────────────────┘
```

**원리는 방향성**:
- 지능을 **위로** 푸쉬 (스킬)
- 실행을 **아래로** 푸쉬 (결정적 도구)
- 하니스는 얇게 유지

→ 모델 업그레이드되면 모든 스킬이 자동 향상, 결정적 레이어는 완벽 신뢰성 유지.

---

## 5. 실전 사례 — YC Startup School (Chase Center, July 2026)

### 시나리오
- 6,000명 창업자
- 각자: 신청서, 설문 답변, 1:1 어드바이저 챗 트랜스크립트, 공개 시그널(X 포스트, GitHub 커밋, Claude Code 트랜스크립트)
- 전통 접근: 15명 팀이 직감 → 200명에서 작동, 6,000명에서 붕괴

### 적용

**1) Enrichment (밤 크론)**
- `/enrich-founder` 스킬: 모든 소스 가져와 enrichment + diarization + "말하는 것 vs 실제 만드는 것" 갭 강조
- 결정적 레이어: SQL, GitHub 통계, demo URL 브라우저 테스트, 소셜 시그널, CrustData 쿼리
- 6,000 프로파일 항상 최신

**다이어라이제이션 예시**:
```text
FOUNDER: Maria Santos
COMPANY: Contrail (contrail.dev)
SAYS: "Datadog for AI agents"
ACTUALLY BUILDING: 80% of commits are in billing module.
  She's building a FinOps tool disguised as observability.
```

이 갭(말하는 것 vs 실제 빌딩)은:
- 임베딩 유사도 검색으로 못 찾음
- 키워드 필터로 못 찾음
- **모델이 전체 프로파일 읽고 판단**해야 함 → **latent space에 맞는 결정** ✓

**2) Matching (스킬을 메서드처럼)**

동일 매칭 스킬, 세 번 호출, 완전히 다른 전략:

| 호출 | 인원 | 그룹 크기 | 알고리즘 |
|------|------|----------|---------|
| `/match-breakout` | 1,200 | 30/방 | sector affinity 클러스터 + 결정적 배정 |
| `/match-lunch` | 600 | 8/테이블 | 섹터 횡단 serendipity + LLM이 테마 발명 → 결정적 배정 |
| `/match-live` | 현장 | 1:1 | 200ms nearest-neighbor + 이미 만난 사람 제외 |

**모델의 판단 호출 예시**:
- "Santos와 Oram은 둘 다 AI infra지만 경쟁자 아님 — Santos는 cost attribution, Oram은 orchestration. 같은 그룹으로."
- "Kim은 신청서에 'developer tools'라 적었지만 1:1 트랜스크립트는 SOC2 compliance 자동화 빌딩 중 → FinTech/RegTech으로 재분류"

이런 판단은 임베딩으로 못 한다. 모델이 **전체 프로파일을 읽어야** 한다.

**3) 학습 루프 (`/improve` 스킬)**

이벤트 후:
- NPS 설문 읽기
- "OK" 응답을 다이어라이즈 (나쁜 게 아니라 "거의 작동했지만 안 된" 케이스)
- 패턴 추출
- 새 규칙을 매칭 스킬에 **다시 써넣기**

```text
When attendee says "AI infrastructure"
    but startup is 80%+ billing code:
    → Classify as FinTech, not AI Infra.

When two attendees in same group
    already know each other:
    → Penalize proximity.
       Prioritize novel introductions.
```

다음 실행은 이 규칙을 자동 사용. **스킬이 스스로를 다시 쓴다**.

**결과**:
- 7월 이벤트: 12% "OK" 평가
- 다음 이벤트: **4%** "OK" 평가
- 누구도 코드를 다시 쓰지 않았다 — 스킬 파일이 "OK"의 의미를 학습

### 일반화 패턴

> retrieve → read → diarize → count → synthesize  
> 그리고: survey → investigate → diarize → rewrite the skill

2026년의 가장 가치 있는 루프. 모든 지식 노동 분과에 적용 가능.

---

## 6. 영구 업그레이드 룰 (저자의 OpenClaw 지시문)

> "You are not allowed to do one-off work. If I ask you to do something and it's the kind of thing that will need to happen again, you must:
> - do it manually the first time on 3 to 10 items
> - show me the output
> - if I approve, codify it into a skill file
> - if it should run automatically, put it on a cron
>
> The test: if I have to ask you for something twice, you failed."

→ 트위터에서 1k 좋아요, 2.5k 북마크
→ 사람들은 프롬프트 엔지니어링 트릭으로 오해 → 실은 **아키텍처**

**왜 영구 업그레이드인가**:
- 스킬은 절대 degrade 안 한다
- 절대 잊지 않는다
- 새벽 3시에도 돈다
- **다음 모델이 나오면 모든 스킬이 즉시 향상** — latent 단계 판단이 개선되고 결정적 단계는 그대로 신뢰성 유지

---

## 7. Best Practices

### Skill 작성

- "어떻게(how)"만 인코딩 — "무엇(what)"은 호출 측이 제공
- 파라미터화 가능하게 — 같은 절차를 다양한 세계에 적용
- 마크다운으로 — 모델 사고 언어
- 메서드 시그니처처럼 입력/단계/출력 명시

### Harness 유지

- 200줄 이하 목표
- JSON in / text out
- 기본 read-only
- 4가지 일만 (loop, file I/O, context, safety)

### Resolver 설계

- `description` 필드를 정확하게 — 모델이 의도와 매칭하는 키
- `CLAUDE.md`는 포인터만, 본문은 별도 문서
- 적시 로드 — 항상 로드하지 말 것

### Latent vs Deterministic 분리

- 결정 가능한 모든 작업은 결정적 레이어로 (SQL, 컴파일, 조합 최적화)
- 판단/합성/모순 보유는 latent에 (다이어라이제이션, 매칭 판단)
- 의심스러우면 둘 다 시도 → 신뢰성 차이 측정

### Anti-patterns

- 모든 REST 엔드포인트를 MCP 툴로 변환
- 40+ tool 정의로 컨텍스트 절반 소진
- 800명 좌석 배치를 LLM에 던짐 (결정적 문제 → latent)
- 20,000줄 CLAUDE.md
- 일회성 작업을 매번 수동으로 반복

---

## 8. 비교 분석

### vs Karpathy Autoresearch

| 항목 | [[autoresearch-study/README\|Autoresearch]] | Thin Harness/Fat Skills |
|------|---------|-------------------------|
| 도메인 | ML 학습 코드 진화 | 일반 지식 노동 자동화 |
| 자산 | `train.py` git history | `skill files` |
| 학습 메커니즘 | val_bpb 기반 keep/discard | NPS "OK" 다이어라이제이션 → 스킬 재작성 |
| 핵심 단위 | 5분 실험 | 스킬 호출 |
| 영구화 | git commit | skill markdown |

두 개 모두 **"사람이 잠든 동안 시스템이 개선되는"** 아키텍처. Autoresearch는 모델 학습 자체, Thin Harness/Fat Skills는 그 위 응용 레이어.

### vs Pete Trainor Invisible Interface

| 항목 | [[invisible-interface-agentic-ai]] | Thin Harness/Fat Skills |
|------|---------|-------------------------|
| 시선 | 사용자 측 UX | 시스템 측 아키텍처 |
| 핵심 변수 | Trust (신뢰 캘리브레이션) | Architecture (얇은 하니스/두꺼운 스킬) |
| 인터페이스 정의 | 신뢰 보정 도구 | (UI는 본 글 주제 아님) |
| 보완 관계 | Trainor: 사용자에게 어떻게 보일까 | 저자: 내부를 어떻게 짤까 |

두 글을 함께 읽으면 **사용자측 UX (Trainor) + 시스템측 아키텍처 (이 글)** = Agentic AI 시대의 풀스택 설계.

---

## 9. 학습 체크리스트

### 이해도 점검

- [ ] 5가지 정의를 외워서 순서대로 설명 가능 (Skill files, Harness, Resolvers, Latent/Deterministic, Diarization)
- [ ] 3-Layer 아키텍처를 그림으로 그릴 수 있다
- [ ] "Skill은 메서드 호출처럼 파라미터를 받는다"의 의미를 예제로 설명할 수 있다
- [ ] Latent vs Deterministic 경계를 본인 코드 한 곳에서 식별할 수 있다
- [ ] Diarization과 RAG/Embedding 검색의 차이를 구분할 수 있다

### 추가 학습 / 실천

- [ ] 본인 `CLAUDE.md` 분량 확인 — 200줄 이상이면 리졸버 패턴으로 리팩토링
- [ ] 자주 반복하는 작업 3개 식별 → SKILL.md로 승격
- [ ] 현재 사용하는 MCP/도구 중 god-tool 식별 → CLI로 대체 검토
- [ ] OpenClaw "두 번 시키면 실패" 룰 본인 작업에 도입
- [ ] Diarization 패턴을 본인 도메인 데이터에 시범 적용

---

## 10. 메모: 핵심 인용

> "The 2x people and the 100x people are using the same models. The difference isn't intelligence. It's architecture."

> "Markdown is, in fact, a more perfect encapsulation of capability than rigid source code."

> "Skills tell the model how. Resolvers tell it what to load and when."

> "Latent space is where intelligence lives. Deterministic is where trust lives."

> "The skill rewrites itself."

> "If I have to ask you for something twice, you failed."

> "Build it once. It runs forever."

---

## 11. References

- 원문 출처: 트위터 공유 에세이 (Garry Tan/YC 진영, 2026-04 추정) — Chase Center July 2026 Startup School 사례 포함
- 관련 노트:
  - [[invisible-interface-agentic-ai]] — UX 측 시각, "Trust is the new usability"
  - [[autoresearch-study/README|Karpathy Autoresearch]] — 자율 ML 실험 아키텍처
  - [[claude/13-2026-05-latest|Claude 2026-05 최신]] — Opus 4.7 Task Budgets, Adaptive Thinking
  - [[claude/05-skills|Claude Code Skills]]
  - [[claude/03-claude-code|Claude Code 개요]]
  - [[codex/01-overview|Codex Skills 패턴]]
- 외부 참조:
  - [Steve Yegge productivity claim 관련 HN](https://news.ycombinator.com/item?id=47577797)
  - [Garry Tan gstack (관련 패턴 구현체)](https://github.com/garrytan/gstack)
  - [TechCrunch - Garry Tan Claude Code 설정 논란](https://techcrunch.com/2026/03/17/why-garry-tans-claude-code-setup-has-gotten-so-much-love-and-hate/)
