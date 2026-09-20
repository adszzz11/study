---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Jev Projects

> [[README|목차로 돌아가기]]

## 1. Support triage

ticket마다 `department`(Choice), `is_urgent`(Noul), `frustration`(Score)를 fan-out한다. SLA queue는 urgency·score·business rule로 정렬하고, `other` 또는 low confidence는 human queue로 보낸다.

**완료 기준**: labeled holdout에서 부서 routing accuracy, urgent recall, confidence bucket calibration, review volume을 보고한다.

## 2. Agent control plane

다음 tool 또는 subagent를 Choice의 allowlist로 제한한다. risk/approval Noul과 impact Score를 추가하고, high-risk tool은 confidence와 무관하게 human approval을 요구한다.

**완료 기준**: unauthorized tool call이 0건이며, timeout·ambiguous input에서 safe fallback trace가 남는다.

## 3. LLM guardrail

jailbreak 가능성, PII 포함, policy violation을 Noul/Score로 screen한다. 결과에 따라 block, redact, review를 선택하되, mandatory compliance rule은 deterministic detector와 함께 적용한다.

**완료 기준**: adversarial test set의 recall/false positive를 임계값별로 기록하고 escalation owner를 정한다.

## 4. Document enrichment

JSONL/CSV record의 taxonomy(Choice), severity(Score), extraction validity(Noul)를 batch fan-out한다. 결과에는 original record ID, model/version, schema version, timestamp를 붙여 재처리 가능하게 한다.

## 5. Model router

request complexity·risk·task type을 판단해 rule engine, cheap LLM, strong LLM, human 중 하나로 route한다. downstream output quality와 end-to-end cost를 feedback signal으로 저장한다.

## 6. Real-time UX

게임 NPC 행동 선택, UI intent classification, alert prioritization 같은 low-latency decision loop을 만든다. open-ended response가 필요해지는 순간에는 Jev result를 생성 model의 context 또는 route signal로 쓴다.

## Sources

- https://docs.typesafe.ai/introduction
- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/confidence
