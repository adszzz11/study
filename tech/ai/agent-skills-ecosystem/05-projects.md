---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Skills Projects

## 1. PR quality gate

`pr-review` Skill로 diff 분석 → test 영향도 → 위험도 → reviewer checklist를 생성한다. 출력에는 근거가 된 파일·line·test command를 포함해 review가 검증 가능해야 한다.

## 2. Incident commander

`incident-response` Skill에 log 수집, timeline 정리, severity 판정, status update template을 둔다. 불확실성은 사실처럼 쓰지 않고, owner와 다음 확인 action을 명시한다.

## 3. Data contract validator

`data-contract` Skill은 schema migration, backward compatibility, sample-data validation을 자동화한다. schema diff를 input으로 받고, script 결과와 migration risk report를 output으로 만든다.

## 4. Architecture dossier

`architecture-review` Skill로 repository 탐색, dependency map, ADR 초안, diagram source 생성을 묶는다. 지식은 `references/`, graph 생성은 `scripts/`로 분리한다.

## 5. Security review

`security-audit` Skill은 authentication, secret exposure, input validation, dependency risk를 검사하고 evidence report를 만든다. 자동 검사는 finding의 후보일 뿐이므로, severity와 remediation은 사람이 검토한다.

## 공통 완료 조건

- trigger가 task에 맞게 구체적인가
- input, output, failure behavior가 문서화됐는가
- 자동화 결과가 재실행 가능하고 evidence를 남기는가
- 최소 1개의 realistic task set에서 평가됐는가

## Related Notes

- [[tech/ai/agent-skills-ecosystem/README|Agent Skills README]]
- [[tech/ai/agent-skills-ecosystem/04-learning/01-getting-started|시작하기]]
- [[tech/ai/agent-skills-ecosystem/04-learning/02-deep-dive|Deep Dive]]
- [[tech/ai/agent-skills-ecosystem/cheatsheet|Cheatsheet]]

## Sources

- https://github.com/anthropics/skills
- https://developers.openai.com/blog/skills-agents-sdk
