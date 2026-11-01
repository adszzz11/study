---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 빠른 도입 판단표다.

| 목표 | 우선 도구 | 첫 안전장치 |
|---|---|---|
| 작은 patch | Ponytail | 요구 밖 refactor 금지, test 실행 |
| frontend 품질 | Taste Skill / Impeccable | render inspection, accessibility 점검 |
| source audit | security-audit-skill | 명시적 허가, evidence 기록 |
| 여러 harness | ECC | hook·MCP·install ownership 검토 |
| web research | Agent-Reach | read-only, secondary account/profile |
| model routing | FreeLLMAPI | localhost/VPN, auth, encrypted backup |
| DeepSeek serving | DeepInfer | 동일 workload benchmark |
| video/voice | HyperFrames / VoiceStudio | asset license, voice consent |
| binary analysis | Ghidra | 격리 환경과 샘플 취급 정책 |

## 설치 전 60초 점검

```text
[ ] source / release / maintainer 확인
[ ] shell, file, network, credential 권한 확인
[ ] test profile·test key·localhost에서 시작
[ ] uninstall/rollback과 책임자 확인
[ ] 결과, 버전, evidence URL 기록
```

## 운영 원칙

- **Least privilege**: 필요한 경로·계정·network만 허용한다.
- **Source first**: README가 아니라 source, install script, hook definition을 확인한다.
- **Observable**: provider fallback, retry, 비용, audit finding을 기록한다.
- **Reversible**: plugin·hook 변경은 제거 절차와 함께 배포한다.

더 자세한 비교: [[tech/devtools/github-ai-agent-toolkit/02-ecosystem|Ecosystem]]

## Sources

- https://github.com/cloudflare/security-audit-skill
- https://github.com/affaan-m/ECC
- https://github.com/NationalSecurityAgency/ghidra
