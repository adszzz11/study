---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# SkillSpector 시작하기

목표는 외부 API key 없이 safe sample skill에 static-only scan을 실행하고 report를 읽는 것이다. 전체 맥락은 [[tech/devtools/agent-skill-security-scanner/README|README]]와 [[tech/devtools/agent-skill-security-scanner/01-overview|Overview]]를 먼저 본다.

## 1. Skill Structure 확인

Agent Skills spec에서 최소 bundle과 frontmatter를 확인한다.

```text
my-skill/
├── SKILL.md          # name, description, allowed-tools
├── scripts/          # optional executable code
├── references/       # optional supporting material
└── assets/           # optional assets
```

`description`은 capability를 정확히 설명해야 하며 `allowed-tools`는 필요한 최소 범위만 선언해야 한다.

## 2. CLI 설치와 첫 Scan

```bash
uv tool install git+https://github.com/NVIDIA/skillspector.git
skillspector scan ./my-skill --no-llm
```

첫 실행에는 `--no-llm`을 써서 deterministic/static finding의 baseline을 만든다. 실제 설치 전 scan 대상은 신뢰할 수 있는 test sample로 제한한다.

## 3. Report 읽기

각 finding에서 다음을 확인한다.

- rule ID와 category: 어떤 policy가 탐지했는가
- file location: `SKILL.md`, script, manifest, MCP metadata 중 어디인가
- confidence와 evidence: 오탐 가능성은 어떤가
- remediation: 제거, permission 축소, pinning, review 중 무엇이 필요한가

JSON/SARIF로 재실행하면 baseline과 CI annotation에 쓸 수 있다. 다음 단계는 [[tech/devtools/agent-skill-security-scanner/04-learning/02-deep-dive|심화 학습]]이다.

## Sources

- https://github.com/NVIDIA/skillspector
- https://docs.nvidia.com/skills/scanning-agent-skills
- https://agentskills.io/specification
