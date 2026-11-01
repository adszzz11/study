---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem 비교

[[tech/devtools/github-ai-agent-toolkit/README|README]]에서 다룬 도구는 대체 관계보다 서로 다른 운영 계층에 가깝다.

| 도구 | 주 용도 | 선택 기준 / 주의점 |
|---|---|---|
| Ponytail | 과잉구현 방지 | 작은 patch와 YAGNI가 목표일 때 |
| Taste Skill | AI frontend 품질 | visual direction·browser inspection이 필요할 때 |
| Impeccable | UI/UX 개선 skill | design system·접근성 기준을 넣을 때 |
| Cloudflare Security Audit Skill | defensive source audit | 명시적 audit 요청과 허가된 codebase에서만 |
| ECC | cross-harness 운영 | 강력하지만 install 범위·hooks 검토 필요 |
| Agent-Reach | login-gated/public research | read-only, secondary account 권장 |
| FreeLLMAPI | multi-provider gateway | self-hosting·key 관리·fallback이 필요할 때 |
| DeepInfer | DeepSeek inference | GPU cluster와 serving 최적화가 필요할 때 |
| HyperFrames | HTML-to-video | editable web-native video 제작 |
| VoiceStudio | voice/media | cloning·dubbing·transcription workflow |
| Ghidra | binary RE | malware, firmware, native binary 연구 |

## 선택 순서

1. 작은 bug fix에 Ponytail을 적용해 diff가 줄어드는지 측정한다.
2. Taste Skill로 UI 결과를 비교하고 accessibility를 눈으로 검토한다.
3. FreeLLMAPI는 localhost/VPN에서만 시작하고 auth·backup을 갖춘다.
4. GPU cluster 수요가 확인된 뒤 DeepInfer benchmark를 별도 환경에서 수행한다.

[[tech/devtools/github-ai-agent-toolkit/04-learning/01-getting-started|시작하기]]에서 최소 위험 경로를 따른다.

## Sources

- https://github.com/cloudflare/security-audit-skill
- https://github.com/Leonxlnx/taste-skill
- https://github.com/pbakaus/impeccable/releases
- https://github.com/NationalSecurityAgency/ghidra/blob/master/GhidraDocs/GettingStarted.md
