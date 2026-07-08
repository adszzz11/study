---
date: 2026-07-09
tags: [tech, ai, claude, codex, gemini, agent-harness, comparison]
status: published
type: tech-tool-study
---

# 02. Ecosystem — 비교와 역할 분배

## 1. 모델·도구 비교

| 도구/모델 | 강점 | 약점/주의 | 추천 역할 |
|---|---|---|---|
| Claude Fable 5 | 장시간 autonomous work, complex coding, reasoning, vision self-check, Claude Code 연동 | 비싸고 cyber/bio safeguard로 fallback/false positive 가능 | 가장 어려운 설계, migration, multi-day coding |
| Claude Sonnet 5 | agentic Sonnet, Fable보다 비용 효율, Claude Code 기본 작업에 적합 | 최상위 reasoning은 Fable/Opus보다 낮을 수 있음 | 일상 coding, PR fix, test 작성 |
| OpenAI Codex | cloud/container 기반 coding agent, CLI/IDE/Web, secure isolated execution, multi-agent 병렬 작업에 적합 | 생성 코드는 manual review 필요 | 구현, refactor, 테스트, 병렬 issue 처리 |
| Gemini CLI / Gemini API | 1M token context, Google Search grounding, multimodal, MCP, 무료 quota 강점 | coding agent UX는 Claude Code/Codex 대비 취향 차이 | 대규모 문서/검색/멀티모달 분석, 보조 reviewer |
| Cursor / GitHub Copilot / Devin / Jules | IDE-native 또는 PR/task automation 생태계 강함 | model 선택·권한·비용 관리 필요 | 팀 workflow 내 코드 작성·리뷰 자동화 |

## 2. Claude + Codex + Gemini 조합

지금 쓰는 조합은 역할을 분리하면 효율이 좋아진다.

| 역할 | 1순위 | 이유 | 프롬프트 방향 |
|------|------|------|---------------|
| Planner / Architect | Claude Fable 5 | 긴 reasoning, 제약 정리, multi-stage plan | “먼저 탐색하고 risk map과 단계별 plan을 작성” |
| Executor / Implementer | Codex | 파일 수정, 테스트 실행, 좁은 범위 구현 | “이 plan의 N단계만 구현하고 test까지 실행” |
| Researcher / Grounded Reviewer | Gemini | 긴 문서, 검색 grounding, 대규모 context | “공식 문서 기준으로 API 변화와 risk를 검증” |
| Final Reviewer | 다른 모델 | 같은 모델의 blind spot 제거 | “숨은 regression, security issue, test gap만 찾아라” |

## 3. 추천 워크플로우

```text
1. Gemini: 최신 공식 문서, release note, migration guide 조사
2. Claude Fable: architecture plan, risk map, task breakdown 작성
3. Codex: package/module 단위 구현과 test 실행
4. Claude Sonnet/Fable: 실패 원인 분석, 어려운 bug fix
5. Gemini 또는 Codex: adversarial review
6. 사람: diff 최종 확인 후 merge
```

## 4. 비용·품질 기준

| 작업 유형 | 추천 모델 | 이유 |
|-----------|-----------|------|
| 5분 내 단순 수정 | Codex 또는 Sonnet | Fable 비용을 쓸 이유가 낮음 |
| 구조 변경 전 설계 | Fable | hidden constraint와 장기 영향 분석 |
| 문서 100개 읽기 | Gemini | long context + search grounding |
| failing test 고치기 | Codex | 재현·수정·재실행 loop에 적합 |
| security-sensitive review | Claude + 별도 reviewer | safeguard 범위 안의 defensive review 중심 |
| UI fidelity 확인 | Fable 또는 vision-capable model | screenshot/design goal 비교 |

## 5. 생태계 관점

Fable 5는 “모델 자체”라기보다 다음 stack에서 가치가 커진다.

```text
frontier model
+ agent harness
+ project memory
+ MCP tools
+ sandbox / permissions
+ tests / verification
+ human review gate
```

이 stack을 다른 모델에도 붙이면 Fable의 일부 행동 원리를 재현할 수 있다. 핵심은 모델명을 바꾸는 것이 아니라 **탐색, 계획, 실행, 검증, 재시도, 요약을 강제하는 harness**다.

## 관련 노트

- [[codex/01-overview]] · [[claude/README]] · [[model-context-protocol-mcp/02-ecosystem]] · [[agent-orchestration/README]] · [[lazy-codex/02-ecosystem]]
