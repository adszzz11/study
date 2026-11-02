---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# 적용 Projects

[[tech/devtools/agent-skill-security-scanner/README|SkillSpector]]를 조직 workflow에 넣을 때는 scanner verdict, human approval, runtime control을 분리한다.

## 1. 사내 Skill Registry Gate

PR에서 변경된 `skills/**`를 static scan하고 SARIF를 Code Scanning에 업로드한다.

- HIGH/CRITICAL: merge 차단
- MEDIUM: security approval 요구
- LOW: report와 baseline에 기록

## 2. Skill Onboarding Bot

Git URL 또는 ZIP을 받은 bot이 `scan_skill()` 결과의 `safe_to_install`, score, finding summary를 Slack 또는 issue에 남긴다. 승인 전에는 agent install을 허용하지 않으며, archive size/member cap 거부도 audit log에 기록한다.

## 3. MCP Catalog Audit

MCP tool/parameter description과 declared permission을 정기 scan한다. hidden instruction, Unicode deception, underdeclared capability를 찾은 뒤 실제 tool implementation과 review한다.

## 4. Defense-in-Depth Release

SkillSpector, Semgrep, OSV-Scanner, TruffleHog를 병렬 실행하고 release artifact에 skill card, benchmark 결과, detached signature를 남긴다. 도구별 책임은 [[tech/devtools/agent-skill-security-scanner/02-ecosystem|Ecosystem]]에서 비교한다.

## Sources

- https://docs.nvidia.com/skills/agent-skill-trust-pipeline
- https://docs.nvidia.com/skills/scanning-agent-skills
- https://github.com/NVIDIA/skillspector
