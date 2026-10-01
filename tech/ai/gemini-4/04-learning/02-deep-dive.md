---
date: 2026-10-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Gemini 4 Argon — 심화

> [[../README|목차로 돌아가기]] | [[01-getting-started|이전: 시작하기]]

## 1. Long-horizon Agent Loop

긴 output capacity는 자동 실행 권한이 아니다. agent는 계획·실행·검증·승인의 상태 머신으로 설계한다.

```text
Plan → Select allowlisted tool → Execute in sandbox → Validate evidence
  ↑                 │                                      │
  └──── retry with bounded budget ──── Human approval ←─────┘
```

| 상태 | 필수 통제 |
|---|---|
| Plan | 목표, 제약, 허용 도구, 비용·시간 budget을 명시 |
| Tool call | scoped credential, allowlist, input validation 적용 |
| Execute | disposable sandbox 또는 staging에서만 수행 |
| Validate | test, lint, policy check, source evidence 확인 |
| Approve | write, deploy, security scan 확대 전 사람이 승인 |

## 2. Evaluation Harness

Argon의 provider benchmark를 그대로 제품 KPI로 사용하지 않는다. repository migration, 계약 비교, incident 분석처럼 조직에 맞는 task set과 rubric을 준비한다.

| 축 | 예시 metric |
|---|---|
| 품질 | task success, build/test pass rate, factuality |
| 근거 | citation fidelity, evidence coverage, source freshness |
| 운영 | latency, input/output tokens, retry rate, cost |
| 안전 | prompt-injection 성공률, policy violation, tool misuse |
| 협업 | human-review 시간, 수정 횟수, 승인 거절률 |

## 3. Prompt-injection Defense

untrusted document, issue, webpage, OCR text에는 “규칙을 무시하라” 같은 instruction이 섞일 수 있다. 이 입력은 모델의 명령이 아니라 검토 대상 데이터다.

```text
Trusted policy + task instruction
            │
Untrusted document ──→ data boundary ──→ model context
            │                                  │
            └── never grants tool permission ──┘
```

- tool allowlist와 least privilege를 적용한다.
- tool argument를 schema와 policy로 검증한다.
- 외부 URL fetch, file read, network egress를 업무별 scope로 제한한다.
- 민감한 write action은 결과 요약·diff·test evidence를 사람이 본 뒤 승인한다.

## 4. Defensive Cyber Workflow

허가된 repository 또는 staging URL에서만 다음 흐름을 실습한다.

1. scope와 authorization을 기록한다.
2. SAST 또는 제한된 test로 취약점 후보를 수집한다.
3. reproduction test와 영향 범위를 증거로 남긴다.
4. patch candidate를 생성하고 build·test·security 검사를 실행한다.
5. human security review 후에만 병합 또는 배포한다.

Fairwind 또는 CodeMender 등 별도 접근권이 필요한 capability는 권한이 없으면 가정하지 않는다. production 대상 자동 patch나 무단 penetration testing은 이 학습 범위에 포함하지 않는다.

## Sources

- https://deepmind.google/models/gemini/cyber/
- https://deepmind.google/fairwind-program/
- https://deepmind.google/blog/strengthening-our-frontier-safety-framework/
