---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - mcp
  - plugins
  - comparison
type: tech-tool-study
parent: "[[README]]"
---

# ponytail skill - 생태계 비교

> [[01-overview|이전: 개요]] | [[README|목차]] | [[03-references|다음: 참고자료]]

---

## 1. 위치 잡기

`ponytail`은 공식 공개 skill이라기보다 custom Agent Skill 이름으로 보는 것이 타당하다. 따라서 비교 대상은 `ponytail` 자체가 아니라, 같은 문제를 푸는 확장 방식들이다.

```text
Agent extension
├── Agent Skills / Claude Skills  ← ponytail custom skill에 가장 적합
├── MCP server                    ← 외부 tool/data 연결
├── Custom instructions           ← 짧은 지속 규칙
├── Plugins                       ← skills/hooks/MCP 묶음 배포
└── Prompt templates              ← 간단한 재사용 prompt
```

## 2. 접근 방식 비교

| 접근 | 역할 | 장점 | 한계/리스크 | `ponytail` 적용 관점 |
|---|---|---|---|---|
| Agent Skills / Claude Skills | 절차+지식+스크립트 패키징 | portable, version-controlled, on-demand loading | 악성 script, 과도한 권한 | `ponytail` custom skill 구현에 가장 적합 |
| MCP server | 외부 tool/data 연결 protocol | API, DB, SaaS 연동에 강함 | 서버 운영/권한 관리 필요 | skill 내부에서 MCP 사용 지침을 줄 수 있음 |
| Custom instructions / CLAUDE.md | 지속적 지침/프로젝트 규칙 | 단순하고 가벼움 | 긴 절차는 context cost 증가 | 짧은 규칙이면 충분, workflow면 skill이 낫다 |
| Plugins | skills, hooks, MCP 등을 묶는 배포 단위 | 팀 배포/설치 UX 좋음 | 플랫폼 종속 기능 가능 | `ponytail`을 plugin skill로 배포 가능 |
| Prompt templates | 재사용 prompt | 빠르게 만들 수 있음 | 파일/script/resource 관리 약함 | 임시 실험용 |

## 3. 언제 Skill이 맞나?

| 상황 | Skill 적합도 | 이유 |
|------|--------------|------|
| 반복 업무 절차가 5단계 이상 | 높음 | 절차, 예외, 검증을 `SKILL.md`에 묶을 수 있음 |
| 긴 도메인 문서를 자주 참조 | 높음 | `references/`로 분리해 필요할 때만 로드 |
| deterministic 변환/검증 필요 | 높음 | `scripts/`로 실행 가능 |
| 외부 SaaS API를 호출해야 함 | 중간 | MCP server가 더 직접적일 수 있음 |
| 프로젝트 전역 규칙 몇 줄 | 낮음 | `CLAUDE.md`나 custom instructions가 간단함 |
| 일회성 prompt 재사용 | 낮음 | prompt template만으로 충분 |

## 4. MCP와의 차이

[[study/tech/ai/model-context-protocol-mcp]]는 agent가 외부 tool/data/prompt를 발견하고 호출하는 protocol이다. Skill은 agent에게 “어떻게 일할지”를 알려주는 instruction package다.

| 구분 | Agent Skill | MCP |
|------|-------------|-----|
| 주된 질문 | Agent가 이 업무를 어떻게 수행할까? | Agent가 어떤 외부 tool/data를 호출할까? |
| 단위 | folder + `SKILL.md` | client-server protocol |
| 실행 | script 포함 가능 | server tool 호출 |
| 배포 | skill folder, plugin, repository | MCP server process/service |
| ponytail 관점 | 업무 절차 package | 필요하면 skill 안에서 MCP 사용 규칙을 안내 |

## 5. Plugins와의 관계

Plugin은 skill보다 더 큰 배포 단위가 될 수 있다. 예를 들어 `ponytail`을 팀 내부 표준 workflow로 배포한다면 plugin 안에 skill, hook, MCP config를 함께 넣을 수 있다.

```text
ponytail-plugin/
├── skills/
│   └── ponytail/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── hooks/
└── mcp/
```

## 6. 선택 가이드

| 목표 | 추천 |
|------|------|
| 반복 문서 작성 규칙 자동화 | Agent Skill |
| 내부 DB/API 연결 | MCP server |
| 팀 공통 코딩 규칙 주입 | CLAUDE.md/custom instructions |
| 여러 확장을 한 번에 설치 | Plugin |
| 임시 명령문 저장 | Prompt template |

## 관련 노트

- [[study/tech/ai/claude/05-skills]] - Claude Skills 학습 노트
- [[study/tech/ai/model-context-protocol-mcp]] - MCP protocol 비교 기준
- [[study/tech/ai/agent-orchestration/cli-agents]] - CLI agent 확장 방식
- [[study/tech/ai/lazy-codex]] - agent harness와 skill의 역할 분리

