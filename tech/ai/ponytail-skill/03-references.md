---
date: 2026-06-24
tags:
  - tech
  - ai
  - agent-skills
  - references
  - ponytail
type: tech-tool-study
parent: "[[README]]"
---

# ponytail skill - 참고자료

> [[02-ecosystem|이전: 생태계]] | [[README|목차]] | [[04-learning/01-getting-started|다음: 시작하기]]

---

## 공식 문서와 스펙

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| Anthropic, Introducing Agent Skills | https://claude.com/blog/skills | Skills의 문제의식, 재사용성, progressive disclosure |
| Claude Code Docs, Extend Claude with skills | https://code.claude.com/docs/en/skills | Claude Code에서 skill을 배치하고 사용하는 방식 |
| Agent Skills Overview | https://agentskills.io/home | cross-platform open standard 개요 |
| Agent Skills Specification | https://agentskills.io/specification | `SKILL.md`, frontmatter, folder structure |
| Agent Skills Quickstart | https://agentskills.io/skill-creation/quickstart | 최소 skill 생성 흐름 |
| Agent Skills Best Practices | https://agentskills.io/skill-creation/best-practices | description, references, scripts 설계법 |
| Agent Skills Evaluating Skills | https://agentskills.io/skill-creation/evaluating-skills | activation, false positive, 품질 평가 |

## 소스 저장소

| 저장소 | URL | 용도 |
|--------|-----|------|
| agentskills/agentskills | https://github.com/agentskills/agentskills | Agent Skills 표준과 예제 확인 |
| anthropics/skills | https://github.com/anthropics/skills | Anthropic 공개 skills 예제 확인 |

## 연구 자료

| 자료 | URL | 읽을 포인트 |
|------|-----|-------------|
| EvoSkills 2026 | https://arxiv.org/abs/2604.01687 | agent skill 생성/진화 방향을 연구 관점에서 보기 |

## 읽는 순서

1. Agent Skills Overview로 전체 개념을 잡는다.
2. Specification에서 `SKILL.md` 구조와 metadata 필드를 확인한다.
3. Quickstart로 최소 skill을 만든다.
4. Best Practices로 `description`, `scripts/`, `references/` 분리 기준을 확인한다.
5. Evaluating Skills로 activation 정확도와 false positive를 평가한다.
6. GitHub examples에서 실제 skill folder 스타일을 비교한다.

## ponytail 검증 체크리스트

`ponytail`이라는 이름의 skill을 실제로 받았거나 발견했다면 아래를 확인한다.

| 체크 | 질문 |
|------|------|
| 출처 | 누가 만들었고 어느 repository/package에서 왔는가? |
| 표준성 | Agent Skills spec을 따르는 `SKILL.md`가 있는가? |
| metadata | `name: ponytail`과 `description`이 명확한가? |
| 실행 파일 | `scripts/`에 실행 가능한 파일이 있는가? |
| 권한 | filesystem, network, env var 접근이 필요한가? |
| activation | 어떤 task에서 켜지고 어떤 task에서 꺼져야 하는가? |
| test | 실제 task 3-5개로 결과를 검증했는가? |

## 관련 노트

- [[study/tech/ai/claude/05-skills]]
- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/codex]]
- [[study/tech/ai/thin-harness-fat-skills]]

