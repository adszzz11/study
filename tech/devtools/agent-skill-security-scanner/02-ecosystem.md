---
date: 2026-11-03
tags: [tech]
type: tech-tool-study
status: draft
---

# Skill Security Ecosystem

[[tech/devtools/agent-skill-security-scanner/README|SkillSpector]]는 code-only scanner의 대체품보다, agent skill의 문서·metadata·code 경계를 잇는 첫 번째 gate에 가깝다.

## 비교

| 도구 | 주된 검사 대상 | Skill-aware 분석 | 적합한 역할 |
| --- | --- | :---: | --- |
| **SkillSpector** | agent skill bundle 전체 | 예 | 설치/배포 전 통합 security gate |
| Semgrep | application source code, SAST/SCA/secrets | 아니오 | 포함 code의 custom-rule 심층 검사 |
| OSV-Scanner | dependency, lockfile, SBOM, container | 아니오 | known vulnerable dependency/CVE 확인 |
| TruffleHog | repository·artifact 내 leaked credential | 아니오 | secret leakage 탐지·검증 |
| SkillEvaluator + NVIDIA trust pipeline | validation, duplication, quality, signing | 부분적 | catalog publication governance |

## Defense in Depth

```text
skill PR / onboarding input
  ├─ SkillSpector: instruction + metadata + code + MCP correlation
  ├─ Semgrep: source-level policy and dangerous patterns
  ├─ OSV-Scanner: dependency and SBOM vulnerabilities
  └─ TruffleHog: credential exposure
          ↓
  human review + signed approved artifact + skill card
```

SkillSpector score가 낮아도 approved artifact를 signature와 skill card로 추적하고, runtime에는 sandbox·egress control·least privilege를 별도로 둔다.

## 선택 기준

- skill의 claimed role과 실제 구현이 일치하는지: SkillSpector
- 조직 고유의 insecure API rule을 강제하는지: Semgrep
- dependency provenance와 공개 CVE를 확인하는지: OSV-Scanner
- 유출된 token을 검증·폐기 흐름으로 연결하는지: TruffleHog

## Sources

- https://docs.nvidia.com/skills/agent-skill-trust-pipeline
- https://docs.semgrep.dev/
- https://google.github.io/osv-scanner/
- https://owasp.github.io/www-project-agentic-skills-top-10/skill-scanner-integration.html
