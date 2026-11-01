---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Claude Code Skills와 Multi-Agent 품질·비용 최적화 워크플로

> **한 줄 정의**: Claude Code의 Skills, subagent, MCP를 조합해 병렬 조사·자기비평·검증·비용 절감을 재사용 가능한 작업 절차로 만드는 방법론이다.

## Overview

이 주제는 특정 제품 하나가 아니라 `SKILL.md` 절차, 역할 분리, 외부 도구 연결, Git/CI 검증을 하나의 delivery loop로 묶는 방식이다. 핵심은 agent 수가 아니라 **독립성 있는 일을 병렬화하고, 결과는 근거와 테스트로 판정**하는 데 있다.

```text
Success criteria → coordinator → specialist workers → critic/judge
                                              ↓
                               evidence + tests + human approval
```

- Skills는 반복 프롬프트를 좁고 재사용 가능한 procedure로 고정한다.
- Multi-agent는 독립 조사·대안 비교·review에 유효하지만, 공유 파일 편집은 충돌 비용이 커 순차 처리가 안전하다.
- GitHub의 무료 skill도 실행 권한, 공급망, Claude 사용량 비용은 별도 검토 대상이다.

## Learning Path

- [ ] [[tech/ai/claude-code-skill-workflows/01-overview|Overview]] — What/Why와 설계 원칙
- [ ] [[tech/ai/claude-code-skill-workflows/02-ecosystem|Ecosystem]] — native 기능·community skill·MCP·orchestrator 비교
- [ ] [[tech/ai/claude-code-skill-workflows/04-learning/01-getting-started|시작하기]] — 첫 검증 루프와 좁은 Skill 만들기
- [ ] [[tech/ai/claude-code-skill-workflows/04-learning/02-deep-dive|Deep Dive]] — judge, budget, 안전 경계 설계
- [ ] [[tech/ai/claude-code-skill-workflows/05-projects|Projects]] — 시장조사·PR gate·frontend audit 적용
- [ ] [[tech/ai/claude-code-skill-workflows/03-references|References]] — 공식 문서와 community source
- [ ] [[tech/ai/claude-code-skill-workflows/cheatsheet|Cheatsheet]] — 역할 명세와 review checklist

## When To Use

- 서로 독립적인 조사, 코드 탐색, 경쟁 비교, UI audit를 동시에 수행할 때
- 반복되는 품질 절차를 `SKILL.md`로 문서화하고 싶을 때
- citation, 테스트, 보안 review처럼 명확한 acceptance criteria가 있을 때

## When Not To Use

- 한 파일·한 상태를 여러 agent가 동시에 수정하는 작은 작업
- test, source, human review 없이 다수결만으로 정답을 정하려는 작업
- 외부 skill/MCP의 권한과 코드를 검토할 수 없는 민감한 환경

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/claude-fable-principles/README|Claude Fable 원리]]

## Sources

- https://www.instagram.com/reel/DfLLn3DDG9C/
- https://docs.anthropic.com/en/docs/claude-code/getting-started
- https://docs.anthropic.com/en/docs/mcp
