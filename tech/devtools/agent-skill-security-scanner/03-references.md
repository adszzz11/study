---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# References

[[tech/devtools/agent-skill-security-scanner/README|README]]를 읽은 뒤, 구현·운영·사양 순서로 원문을 확인한다.

## Primary Sources

1. [NVIDIA/SkillSpector repository](https://github.com/NVIDIA/skillspector) — source, CLI, issue와 release 확인.
2. [Releases: v2.13.3](https://github.com/NVIDIA/skillspector/releases) — 2026-11-02 기준 최신 release.
3. [Scan Agent Skills Before Installation](https://docs.nvidia.com/skills/scanning-agent-skills) — scanner 사용 문서.
4. [A Trust Pipeline for Agent Skills](https://docs.nvidia.com/skills/agent-skill-trust-pipeline) — Tier와 publication governance.
5. [NVIDIA Verified Agent Skills](https://docs.nvidia.com/skills) — verified catalog의 맥락.

## Research and Standards

1. [SkillSpector paper](https://openreview.net/pdf?id=rVAPXHmGHN) — pre-publication control의 방법과 한계.
2. [OWASP Agentic Skills: Skill Scanner Integration](https://owasp.github.io/www-project-agentic-skills-top-10/skill-scanner-integration.html) — scanner integration guidance.
3. [Agent Skills Specification](https://agentskills.io/specification) — `SKILL.md`와 bundle structure의 기준.

## Complementary Tools

- [OSV-Scanner documentation](https://google.github.io/osv-scanner/)
- [Semgrep documentation](https://docs.semgrep.dev/)

비교 기준은 [[tech/devtools/agent-skill-security-scanner/02-ecosystem|Ecosystem]]을 참조한다.

## Sources

- https://github.com/NVIDIA/skillspector
- https://agentskills.io/specification
- https://openreview.net/pdf?id=rVAPXHmGHN
