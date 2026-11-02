---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# SkillSpector 개요

[[tech/devtools/agent-skill-security-scanner/README|SkillSpector]]는 AI agent skill을 설치하거나 공개하기 전 점검하는 NVIDIA의 open-source security scanner다. Verified Skills trust pipeline에서 Tier 1 validation 역할을 맡는다.

## What

입력은 local directory, 단일 `SKILL.md`, Git repository, HTTPS URL, ZIP일 수 있다. 도구는 이를 temporary skill directory로 정규화하고, Markdown·frontmatter·code·dependency manifest·MCP metadata를 shared state/graph에서 상관 분석한다.

remote/archive ingestion에는 100 MiB cap, ZIP에는 10,000 member cap을 적용해 zip bomb 같은 초기 수집 위험을 줄인다.

## Why

Agent skill은 tool, shell, network 권한을 가진 agent의 context에 로드된다. 따라서 다음 공격은 일반 SAST 또는 lockfile scanner만으로 충분히 연결해 보기 어렵다.

- hidden prompt injection과 anti-refusal instruction
- Unicode homoglyph, tool-description poisoning, system-prompt leakage
- credential/environment-variable exfiltration과 dangerous code
- declared permission과 manifest/code 행위의 불일치
- unpinned dependency, known CVE, MCP least-privilege 위반

## 핵심 특징

| 영역 | 검사 방식 |
| --- | --- |
| 정적 rule | 71개 pattern, 17개 category, YARA, Python AST |
| data flow | lightweight taint tracking |
| package | dependency manifest 및 OSV lookup |
| MCP | tool poisoning, permission, least-privilege 검사 |
| semantic | optional LLM으로 description-behavior mismatch 보강 |
| report | terminal, JSON, Markdown, SARIF 2.1.0 |

LLM-only finding은 자동 차단 근거가 아니라 human-review lead로 다루는 것이 논문의 권고다. deterministic taint 분석도 helper function, imported module, cross-file flow에서 우회될 수 있다.

## Risk Decision

CRITICAL/HIGH/MEDIUM/LOW finding을 합산하고 executable script에는 1.3× multiplier를 적용해 0–100 score를 만든다.

| Score | 권고 |
| ---: | --- |
| 0–20 | `SAFE` |
| 21–50 | `CAUTION` |
| 51 이상 | `DO NOT INSTALL` |

이 결과는 설치 결정을 설명 가능하게 만드는 signal이지, 안전성 보증서가 아니다. [[tech/devtools/agent-skill-security-scanner/04-learning/02-deep-dive|심화 학습]]에서 review policy를 함께 설계한다.

## Sources

- https://github.com/NVIDIA/skillspector
- https://docs.nvidia.com/skills/agent-skill-trust-pipeline
- https://openreview.net/pdf?id=rVAPXHmGHN
