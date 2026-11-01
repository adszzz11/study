---
date: 2026-11-01
tags: [tech]
type: tech-tool-study
status: draft
---

# GitHub AI Agent 도구군 개요

[[tech/devtools/github-ai-agent-toolkit/README|README]]의 도구군은 모델을 바꾸기보다 agent의 작업 절차와 실행 환경을 확장한다.

## What

| 계층 | 도구 | 역할 |
|---|---|---|
| Agent skill | Ponytail, Taste Skill, Impeccable, security-audit-skill | 지침과 검증 loop 배포 |
| Agent harness | ECC | rules, hooks, MCP convention, skills 이식 |
| Access/research | Agent-Reach | read-only channel과 fallback backend 통합 |
| Serving/routing | FreeLLMAPI, DeepInfer | OpenAI-compatible gateway와 inference runtime |
| Production | HyperFrames, VoiceStudio, Ghidra | video·voice·reverse engineering 작업 |

## Why

매 세션마다 prompt로 품질 기준을 설명하면 재사용과 검증이 어렵다. `SKILL.md`와 hook은 일관된 절차를 만들지만, 실행 권한도 함께 넓힌다. 따라서 생산성 평가에는 결과물뿐 아니라 permission, install ownership, rollback 가능성도 포함해야 한다.

## 핵심 특징

- **Ponytail**: YAGNI를 중심에 두고 가장 작은 patch를 유도한다.
- **Taste Skill / Impeccable**: visual direction, render inspection, design system·accessibility 기준을 workflow에 넣는다.
- **ECC**: 여러 harness로 규칙을 옮기지만, 큰 설치 범위와 hook supply chain을 검토해야 한다.
- **Agent-Reach**: 일부 channel이 별도 browser profile의 로그인 session을 재사용한다. secondary account가 적합하다.
- **FreeLLMAPI**: `/v1` gateway, provider fallback/routing, encrypted SQLite credential storage를 제공한다.
- **DeepInfer**: 대규모 DeepSeek serving에서 prefill/decode 성능을 겨냥한다.

다음: [[tech/devtools/github-ai-agent-toolkit/02-ecosystem|Ecosystem]]

## Sources

- https://github.com/DietrichGebert/ponytail
- https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md
- https://github.com/deepseek-ai/DeepInfer

## 추가 조사: Ponytail — 최소 변경(Minimal Change) skill

- `SKILL.md`는 YAGNI(You Aren't Gonna Need It), 기존 코드 재사용, 표준 라이브러리 우선의 **ladder**를 제시한다. 기능을 더하기 전에 “이 변경이 정말 필요한가”와 호출부·테스트 영향을 확인하는 방식이다.
- 단순 prompt collection이 아니라 여러 coding harness용 plugin/rule/hook을 함께 제공하므로, 설치 전 `hooks/`, 설치 스크립트, 설정 파일의 write 범위를 diff로 확인한다.
- 현재 실습: 실제 bug fix 하나에서 적용 전후의 변경 파일 수, LOC, 테스트 결과, 요구 밖 변경 수를 기록한다. “코드가 적다”는 성공 지표일 뿐 요구를 누락했으면 실패다.

```text
요구사항 → 기존 구현 탐색 → 최소 patch → 필요한 test → 제외한 범위와 잔여 위험 보고
```

## 추가 조사: Taste Skill — art direction과 browser check

- Taste Skill은 agent에게 art direction, reference image, 브라우저 검수(browser check)를 주어 정형화된 AI UI를 피하는 frontend skill이다.
- 디자인 지시만으로 완료 처리하지 말고, 실제 viewport에서 typography, spacing, contrast, keyboard focus, responsive breakpoint를 screenshot으로 확인한다.
- 실습은 같은 화면을 baseline과 skill 적용 버전으로 만들고 다음 표를 채운다.

| 검수 항목 | 증거(Evidence) | 통과 기준 |
|---|---|---|
| 시각적 계층(Visual hierarchy) | desktop/mobile screenshot | 제목·CTA가 한눈에 구분됨 |
| 접근성(Accessibility) | keyboard tab, contrast check | focus가 보이고 텍스트 판독 가능 |
| 반응형(Responsive) | 좁은 viewport screenshot | overflow·겹침 없음 |

## 추가 조사: Impeccable — 디자인 vocabulary와 critique

- Impeccable은 coding agent에 polish, critique, audit 중심의 디자인 어휘(vocabulary)를 제공하는 skill 계열이다. 생성 단계와 review 단계를 분리해 “예쁘다” 같은 모호한 피드백을 구체적 결함으로 바꾼다.
- 적용 시 기존 design token, component library, 접근성 규칙을 먼저 읽힌다. 새 스타일 체계를 덮어쓰는 용도보다 현재 UI의 일관성·AI slop 탐지가 우선이다.
- 실습 산출물은 화면 하나의 전/후 screenshot, 발견 항목, 수정 근거, regression 여부다.

## 추가 조사: Cloudflare Security Audit Skill — 다단계 defensive audit

- 이 skill은 coding agent가 다단계 보안 감사(multi-phase security audit)를 수행하고, 독립 검증 가능한 기계 판독 finding을 남기도록 설계되어 있다.
- 허가된 own codebase에서만 실행하고, finding마다 공격 전제조건, 영향 범위, 재현 evidence, remediation, false-positive 검토를 분리한다.
- agent의 결과를 취약점 확정으로 취급하지 않는다. reviewer가 source와 test로 독립 검증한 뒤에만 issue 또는 수정 작업으로 승격한다.
