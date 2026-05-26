---
date: 2026-05-24
updated: 2026-05-26
tags:
  - tech
  - ai
  - icm
  - agent-architecture
  - no-framework
  - arxiv-paper
status: studying
type: tech-concept
---

# ICM — Interpretable Context Methodology

> **한 줄 정의**: "폴더 구조가 곧 에이전트 아키텍처다" — sequential + human-reviewed AI 워크플로를 멀티 에이전트 프레임워크 없이 5계층 파일시스템 + 마크다운만으로 조직하는 프로토콜. 2026-03 arXiv 논문 [Van Clief & McDermott, Eduba.io / Univ. of Edinburgh] 이 5계층 컨텍스트 + 5개 설계 원칙 + 실증 데이터로 형식화. MIT.

> [!note] 노트 개정 이력
> 2026-05-24 초안은 YouTube 영상·뉴스레터 기반 — 일부 부정확. 2026-05-26 **원본 arXiv 논문(2603.16021)** 을 1차 소스로 전면 개정. Layer 0 파일명을 `AGENTS.md` → `CLAUDE.md` 로 정정, 폴더 명명 하이픈 → 언더스코어, 5계층 구조 추가.

## 1. What - 개념 정의

ICM은 CrewAI / LangChain / AutoGen 같은 **프레임워크 레벨 오케스트레이션을 파일시스템 구조로 대체**하는 프로토콜이다. 핵심 관찰: *"각 워크플로 단계의 prompt와 context가 이미 잘 정리된 폴더 계층 안의 파일들이라면, 여러 전문 에이전트를 관리할 coordination framework는 필요 없다. 한 명의 오케스트레이팅 에이전트가 적절한 순간에 적절한 파일을 읽기만 하면 된다."*

> **The folder structure tells it what to do at each step.**

폴더 번호가 실행 순서이고, 폴더 경계가 separation of concerns이며, 디스크 위 파일이 state이다. 단계 간 coordination은 한 폴더의 output이 다음 폴더의 input이 되는 것으로 끝난다.

### 주요 용어

| 용어 | 설명 |
|------|------|
| **Workspace** | ICM의 단위 — 하나의 폴더. Git 호환, 복사·전달 가능 |
| **Stage** | 워크플로의 한 단계 (`01_research/`, `02_script/`, `03_production/` ...). 번호 = 실행 순서 |
| **CLAUDE.md (Layer 0)** | "Where am I?" — 글로벌 identity 파일 (Claude Code 사용 시. 다른 에이전트면 `AGENTS.md` 등) |
| **CONTEXT.md (Layer 1·2)** | 워크스페이스 레벨(Layer 1) / 스테이지 레벨(Layer 2) routing |
| **Layer 3 — Reference (Factory)** | 런 간 *변하지 않는* 자료: voice/style/conventions. `references/`, `_config/`, `shared/`에 위치 |
| **Layer 4 — Working (Product)** | 런마다 *변하는* 산출물: 이전 스테이지 output, 사용자 입력. `output/`에 위치 |
| **Stage Contract** | 각 스테이지의 `CONTEXT.md`가 정의하는 `## Inputs / ## Process / ## Outputs` 3부 계약 |
| **Review Gate** | 스테이지 사이의 휴먼 검토 지점 (Fig. 4) |

---

## 2. Why - 등장 배경 & 필요성

### 해결하려는 문제

- 기존 프레임워크(LangChain·AutoGen·CrewAI)는 다단계 오케스트레이션·메모리·툴·에러 복구를 잘 처리하지만, **자기 구조 안에서**만 동작 → 단계 순서 바꾸기, 프롬프트 수정, 단계 추가/삭제, 오늘은 안 쓰는 단계 스킵 같은 **일상 운영이 코드 편집·재배포** 가 됨
- 그러나 **sequential + human-review 워크플로**에서 frameworks는 *존재할 필요 없는 coordination 문제*를 푼다 (논문 §1)
- Liu et al. — LLM은 긴 컨텍스트 중간에 묻힌 정보에서 **현저히 나쁜 성능**. 관련 없는 자료가 많을수록 중요한 자료도 망친다
- Jiang et al. — 프롬프트 압축으로 토큰 20배 절감 가능하지만, **더 단순한 접근은 애초에 관련 없는 컨텍스트를 로드하지 않는 것**

### 기존 방식의 한계 (논문 Table 1 요약)

**ICM이 단순화하는 6가지 차원**:

| 차원 | Framework | ICM |
|------|-----------|-----|
| 단계 순서 변경 | 오케스트레이션 코드 편집·재배포 | 폴더 이름 변경/재정렬 |
| 프롬프트 수정 | agent config 코드 편집 | 마크다운 파일 편집 |
| 단계 추가/삭제 | 새 agent 클래스, orchestrator 갱신 | 폴더 추가/삭제 |
| 중간 state 검사 | 로깅 추가, 대시보드 구축 | 폴더 열어서 파일 읽기 |
| 다른 사람에게 인계 | 환경·의존성·셋업 문서화 | 폴더 복사 |
| 누가 변경 가능 | 개발자 | 텍스트 에디터 쓰는 누구나 |

**Framework가 더 잘하는 4가지 차원**:

| 차원 | Framework | ICM |
|------|-----------|-----|
| 중간 에러 복구 | 내장 retry / fallback | 실패 스테이지 수동 재실행 |
| 조건 분기 | agent output 기반 프로그램 라우팅 | 사람이 단계 사이에서 결정 |
| 동시 실행 | 네이티브 병렬 | 설계상 sequential |
| 외부 서비스 연동 | 프로그램 API + auth 관리 | 로컬 스크립트 또는 MCP 연결 |

---

## 3. How - 동작 원리

### 3.1 다섯 가지 설계 원칙 (논문 §3.1)

1. **One stage, one job** — 각 스테이지는 워크플로의 한 단계를 담당, 자기 폴더에 output 작성. 데이터 fetch와 filter를 한 스테이지에서 같이 하지 말 것 (McIlroy의 Unix 원칙 + Parnas의 information-hiding)

2. **Plain text as the interface** — 스테이지 간 통신은 markdown + JSON. 바이너리·DB·proprietary 직렬화 금지. 텍스트 에디터로 누구나 워크플로 참여 가능 (Kernighan & Pike: "텍스트가 universal interface")

3. **Layered context loading** — 에이전트가 *현재 스테이지에 필요한 context만* 로드. 압축(compression)이 아니라 *예방(prevention)*. Layer 3(reference, 항상 같음)과 Layer 4(working, 매번 다름)를 구조적으로 분리 — model이 둘을 다른 방식으로 처리해야 하기 때문 (reference는 *제약*, working은 *입력*)

4. **Every output is an edit surface** — 각 스테이지의 중간 output은 사람이 열고·읽고·편집·저장 가능한 파일. 다음 스테이지가 시작되기 전. Horvitz의 mixed-initiative + Shneiderman의 direct manipulation 구현

5. **Configure the factory, not the product** — 워크스페이스는 한 번 셋업 (사용자 preference/brand/style/구조 결정). 이후 매 런은 같은 설정으로 새 산출물 생산. Continuous delivery 원칙

### 3.2 5계층 컨텍스트 아키텍처 (논문 Fig. 1)

| Layer | 파일 | 토큰 | 질문 | 역할 |
|-------|------|------|------|------|
| **0** | `CLAUDE.md` | ~800 | "Where am I?" | 글로벌 identity (Structural) |
| **1** | `CONTEXT.md` (workspace 루트) | ~300 | "Where do I go?" | 워크스페이스 routing |
| **2** | `CONTEXT.md` (스테이지) | 200-500 | "What do I do?" | 스테이지 contract |
| **3** | `references/`, `_config/`, `shared/` | 500-2k | "What rules apply?" | Reference (factory) |
| **4** | `output/` | 가변 | "What am I working with?" | Working artifacts (product) |

- **Layer 0-2 = Structural (routing)**, **Layer 3-4 = Content (factory / product)**
- 모델 관점: Layer 3는 "*write like this, use these colors, follow these conventions*" — **internalize as constraints**. Layer 4는 "*transform this research into a script*" — **process as input**. 한 컨텍스트 윈도우에서 섞이면 모델이 직접 sort 해야 함 → 폴더 구조로 분리해두면 이미 정리된 채로 도착

### 3.3 폴더 구조 (논문 Fig. 2)

```
workspace/
├── CLAUDE.md                 Layer 0  (~800 tok)
├── CONTEXT.md                Layer 1  (~300 tok)
├── stages/
│   ├── 01_research/
│   │   ├── CONTEXT.md        Layer 2  (200-500 tok)
│   │   ├── references/       Layer 3
│   │   └── output/           Layer 4
│   ├── 02_script/
│   │   ├── CONTEXT.md        Layer 2
│   │   ├── references/       Layer 3
│   │   └── output/           Layer 4
│   └── 03_production/
│       ├── CONTEXT.md        Layer 2
│       ├── references/       Layer 3
│       └── output/           Layer 4
├── _config/                  Layer 3  (voice.md, design-system.md...)
├── shared/                   Layer 3
└── setup/
    └── questionnaire.md
```

- **숫자 prefix = 실행 순서**
- **언더스코어 (`_`) — 하이픈 (`-`) 아님** — 논문 Figure 2 표기
- `_config/`, `shared/` 의 underscore prefix는 "Layer 3 — workspace-wide reference"

### 3.4 Stage Contract (논문 §3.3 코드 예시)

각 스테이지의 `CONTEXT.md`는 3부 계약:

```markdown
## Inputs
- Layer 4 (working): ../01_research/output/
- Layer 3 (reference): ../../_config/voice.md
- Layer 3 (reference): references/structure.md

## Process
Write a script based on the research output.
Follow the structure in structure.md.
Match the tone described in voice.md.

## Outputs
- script_draft.md -> output/
```

- Inputs 표가 명시적·편집 가능·감사 가능 → 에이전트가 워크스페이스 전부 로드하거나 자기 판단에 의존하지 않음
- 이게 *프레임워크가 코드로 하던 일을 파일시스템이 한다*는 핵심

### 3.5 실증: 컨텍스트 윈도우 구성 (논문 Fig. 3)

스크립트-투-애니메이션 워크스페이스의 실제 토큰 수:

| 스테이지 | Layer 0-2 (구조) | Layer 3 (reference) | Layer 4 (working) | 합계 |
|----------|-----------------|--------------------|--------------------|------|
| **01_research** | ~1.3k | ~2k | ~1.6k | **~4.9k** |
| **02_script** | ~1.3k | ~2k | ~2.2k | **~5.5k** |
| **03_production** | ~1.3k | ~2k | ~2.3k | **~5.6k** |
| **Monolithic (대조)** | 모든 instruction + 모든 reference + 모든 prior output | — | — | **~42k** |

Monolithic 접근의 ~42k 중 **대부분이 unused/irrelevant** (현재 단계와 무관한 다른 스테이지 명령·참고자료·prior output). ICM은 폴더 구조로 *애초에* 안 로드.

### 3.6 핵심 메커니즘

- **State = 파일시스템** — 폴더 번호 = 스테이지 시퀀싱, 폴더 계층 = 컨텍스트 스코핑, 디스크 파일 = state 관리
- **Coordination = 한 폴더의 output이 다음 폴더의 input** — application code 없이 filesystem이 chain을 만든다 (Wu/Terry/Cai의 AI Chains를 파일시스템 레벨에서)
- **자기-문서화** — `CONTEXT.md`가 동시에 (1) 에이전트에게 무엇을 하라는 instruction이자 (2) 사람에게 이 스테이지가 무엇을 expect/produce 하는지 알려주는 문서. Knuth의 literate programming과 같은 사상 — instruction과 documentation이 같은 artifact
- **Sub-agent도 같은 구조 활용** — Opus 4.6이 primary로 동작할 때 Sonnet 4.6에 sub-task 위임 (Agent Teams), 폴더 구조가 primary의 control surface이자 sub-agent에게 줄 context spec 역할

---

## 4. 실무 적용

### 4.1 검증된 환경 (논문 §4.1)

- **Primary agent**: Claude Code + **Claude Opus 4.6**
- **Sub-agents**: Claude Sonnet 4.6 via **Agent Teams capability**
- Primary agent는 워크스페이스의 `CONTEXT.md` 계층 + Layer 3 reference를 읽어 sub-agent들의 prompt를 채움
- **Model-agnostic** — 프로토콜은 폴더 구조 / 파일 포맷 / 명명 규칙만 정의. 동일 워크스페이스를 다른 모델에 가리키면 그대로 실행 가능 (결과 동등성은 별개 empirical 문제)

### 4.2 검증된 워크플로 예시 (논문 §4.2)

**Script-to-Animation 파이프라인**:

```
Stage 1 (01_research) — 주제·연구 brief 입력 → key points, narrative angles, supporting data
Stage 2 (02_script) — Stage 1의 output + voice.md + structure.md → script_draft.md
Stage 3 (03_production) — script_draft.md + production-spec.md → animation specification
```

각 스테이지 끝에 **Review Gate** — 사람이 `output/` 파일을 열어 검토·편집 후 다음 스테이지 실행. Wei et al.의 chain-of-thought 결과(추론을 중간 단계로 분해하면 LLM 성능 극적 향상)를 *아키텍처적으로* 적용 — 명시적 경계와 스테이지별 focused context.

### 4.3 Best Practices

- **Inputs 표를 명시** — 에이전트가 추측하지 않게 어느 파일이 어느 Layer인지 표시
- **Layer 3 / Layer 4 폴더 분리 유지** — 한 폴더에 섞으면 5계층 이점 상실
- **`CONTEXT.md` 짧게** — Layer 2는 200-500토큰 권장. 길어지면 reference로 빼기
- **`output/`만 다음 스테이지의 input** — 다른 스테이지의 internal file을 직접 읽지 말 것
- **워크스페이스 = Git 레포 (또는 폴더)** — 모든 변경 diff·되돌리기 가능. 인프라스트럭처 as code (Morris)를 AI 워크플로에 적용

### 4.4 Anti-patterns

- 한 스테이지에 두 가지 책임 부여 (fetch + filter) — One stage, one job 위배
- Layer 3(reference)와 Layer 4(working)를 같은 폴더에 — 모델이 둘을 다르게 처리해야 하는데 섞이면 효과 상실
- 모든 reference를 Layer 1·2(routing)에 박아넣기 — 토큰 폭증
- 하이픈 (`01-research/`) 사용 — 논문은 언더스코어
- 동적 폴더 생성을 LLM에게 위임 — 사람이 한눈에 못 봄 (가독성 = ICM의 핵심)
- Concurrent / branching이 본질인 시스템에 강요 — 이건 framework가 더 잘 함 (Table 1 마지막 4행)

---

## 5. 비교 분석

### 5.1 vs 대안 프레임워크

| 항목 | ICM | LangGraph | AutoGen | CrewAI | MCP |
|------|-----|-----------|---------|--------|-----|
| **레이어** | 컨텍스트 *전달* 메커니즘 | 그래프 노드/엣지 | 멀티 에이전트 대화 | Crew/Task 클래스 | 외부 도구 *접근* 표준 |
| **추상화** | 파일시스템 | 코드 그래프 | 메시지 배열 | OOP | RPC/리소스 |
| **디버깅** | `ls`, `cat`, `git diff` | LangSmith 등 도구 | 메시지 로그 | 로그 | trace |
| **state** | 디스크 파일 | 직렬화 state 객체 | 메시지 히스토리 | task ledger | 세션 |
| **인계** | 폴더 복사 | 코드 + state + env | 코드 + env | 코드 + env | 코드 + creds |
| **누가 편집** | 텍스트 에디터 사용자 | 개발자 | 개발자 | 개발자 | 개발자 |
| **vendor 락인** | 없음 (model-agnostic) | 없음 | OpenAI 친화 | 없음 | Anthropic 발 |

> **ICM과 MCP는 상보적** — MCP는 model이 외부 tool/data에 *어떻게* 접근하는지 표준화. ICM은 multi-stage workflow에서 *어떤 context를 받는지* 다룬다. 한 ICM 스테이지가 MCP 연결로 외부 서비스 접근 가능 — 폴더 구조는 그 스테이지가 *언제* 그 MCP에 접근할지를 결정 (논문 §2.2).

### 5.2 선택 기준

| 상황 | 추천 |
|------|------|
| Sequential + human-review 워크플로 (콘텐츠 제작, 컨설팅 deliverable, 정기 리포트) | **ICM** |
| 단일 빌더가 자기 워크플로를 반복·재사용 | **ICM** |
| 비개발자(편집자, 디자이너)가 prompt/structure 수정 필요 | **ICM** |
| 동시 다수 에이전트 협업·실시간 대화 (시뮬레이션, 협상, 게임) | **Framework** |
| 복잡한 conditional branching이 본질 | **Framework** |
| 빠른 conversational chatbot | **OpenAI Assistants** 등 |
| 외부 도구 접근만 표준화 | **MCP** (ICM 안에서도 같이 사용) |

> 논문 인용: *"ICM trades the flexibility of a programmatic orchestrator for the portability, inspectability, and editability of plain files. That tradeoff is the point."* (§3.2)

### 5.3 사상적 위치

- **Unix philosophy**의 직계 후예 (McIlroy, Kernighan & Pike, Raymond)
- **Plan 9의 "everything is a file"** 을 AI 워크플로로 확장 — 모든 state, context, instruction이 파일 네임스페이스에 존재
- **Parnas의 information hiding** + **Dijkstra의 separation of concerns**를 LLM 컨텍스트 윈도우에 적용
- **Knuth의 literate programming** — instruction과 documentation이 같은 artifact
- **Karpathy의 "context engineering"** (2025-06) — prompt engineering 너머의 더 넓은 학문, ICM은 그것의 *아키텍처적* 구현
- **Lance Martin (LangChain)의 4-strategy taxonomy** (write/select/compress/isolate) 중 **select + isolate** 를 폴더 구조로 강제

---

## 6. 학습 체크리스트

### 이해도 점검

- [ ] "폴더 구조가 에이전트 아키텍처"의 정확한 의미를 5계층 관점에서 설명할 수 있다
- [ ] Layer 3(reference, factory) vs Layer 4(working, product) 구분을 한 문장으로 말할 수 있다
- [ ] 5 설계 원칙(One stage one job / Plain text / Layered loading / Output as edit surface / Configure factory)을 외울 수 있다
- [ ] Stage Contract 3부(Inputs / Process / Outputs) 구조를 그릴 수 있다
- [ ] Table 1의 10개 차원 중 ICM이 이기는 6개·지는 4개를 구분할 수 있다
- [ ] ICM과 MCP가 어떻게 상보적인지 설명할 수 있다

### 추가 학습

- [ ] 논문 [arXiv:2603.16021](https://arxiv.org/abs/2603.16021) 완독 (~20p)
- [ ] GitHub repo [RinDig/Interpretable-Context-Methodology-ICM-](https://github.com/RinDig/Interpretable-Context-Methodology-ICM-) 의 working implementation 검토
- [ ] 자기 워크플로 1개를 5계층 구조로 그려보기 (CLAUDE.md / CONTEXT.md / stages/NN_*/CONTEXT.md / references/ / output/)
- [ ] Claude Code + Agent Teams (Opus 4.6 + Sonnet 4.6)로 ICM 워크스페이스 셋업 시도

---

## 7. References

### Primary

- **arXiv 논문**: [Interpretable Context Methodology: Folder Structure as Agent Architecture](https://arxiv.org/abs/2603.16021) — Van Clief & McDermott (Eduba.io / Univ. of Edinburgh, Palm Coast FL), 2026-03-17 v1 / 03-18 v2
- **GitHub**: [RinDig/Interpretable-Context-Methodology-ICM-](https://github.com/RinDig/Interpretable-Context-Methodology-ICM-) — working implementation, MIT
- **저자 연락처**: theceo@eduba.io

### Secondary / 유관 자료

- 영상: [You're Automating The Wrong Layer (2026-05)](https://youtu.be/956DPSPX4wg) — ICM 소개·30k 사용자 언급
- 뉴스레터: [The simplest way to build AI agents in 2026 (Owain Lewis)](https://newsletter.owainlewis.com/p/the-simplest-way-to-build-ai-agents) — Micro-Agent Architecture 관점 요약

### 사상적 뿌리 (논문 인용)

- McIlroy (1978) — Unix philosophy
- Parnas (1972) — Information hiding
- Dijkstra (1974) — Separation of concerns
- Kernighan & Pike (1984) — Programs vs relationships
- Raymond (2003) — Rules of Modularity / Transparency / Composition
- Shaw & Garlan — Pipe-and-filter pattern
- Feldman (1979) — Make / dependency graph
- Plan 9 — Everything is a file in per-process namespaces
- Knuth — Literate programming
- Wu, Terry, Cai (2022) — AI Chains
- Karpathy (2025-06) — Context engineering (term)
- Lance Martin (LangChain) — write/select/compress/isolate taxonomy
- Wei et al. — Chain-of-thought
- Liu et al. — Lost in the middle (long context degradation)
- Jiang et al. — Prompt compression
- Horvitz — Mixed-initiative
- Shneiderman — Direct manipulation, Human-Centered AI
- Rudin — Inherently interpretable systems
- EU AI Act — Human oversight 요구 (human-in-the-loop / on-the-loop / in-command)

### 관련 노트

- [[thin-harness-fat-skills]] · [[invisible-interface-agentic-ai]] · [[google-adk-deep-search]]
- 사용 모델: [[claude/]] (Opus 4.6 primary + Sonnet 4.6 sub-agents via Agent Teams)
