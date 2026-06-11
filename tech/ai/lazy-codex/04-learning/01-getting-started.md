---
date: 2026-06-07
tags: [tech, ai, codex, lazycodex, hands-on]
status: published
type: tech-tool-study
---

# 04-1. 시작하기 — 설치·첫 실행·완화 프롬프트

## 1. 설치 (전역 설치 금지, 항상 npx/bunx)

```bash
# Codex CLI 위에 (Light)
npx lazycodex-ai install

# OpenCode 위에 (Ultimate)
bunx oh-my-openagent install
```

선행: Codex CLI 설치·로그인(또는 OpenCode), Bun 런타임.

## 2. 첫 실행 흐름

```bash
/init-deep                 # ① 큰 저장소 컨텍스트(계층 AGENTS.md) 생성
$ulw-plan "무엇을 만들지"   # ② 계획만(코드 변경 X) — plans/<slug>.md
$start-work [plan]         # ③ 체크리스트 실행 ("ORCHESTRATION COMPLETE"까지)
$ulw-loop "작업"           # 또는: 모호한 작업을 Oracle 검증까지 반복
```

## 3. 게으름 완화 프롬프트 (하니스 없이도 즉효)

> Codex Prompting Guide 핵심. **"계획 말하라"는 빼고 "끝까지 하라"는 넣는다.**

- **자율/지속**: "Act as a senior engineer. Proactively plan, implement, test, refine **without waiting**. **Persist until fully handled end-to-end** this turn."
- **행동 편향**: "Default to implementing with reasonable assumptions; **do not end with clarifications unless truly blocked.**"
- **preamble 제거** ⚠️: upfront plan/preamble/status 요청을 **빼라**(조기 중단 유발).
- **완료 규율**: "Carry through implementation, **verification**, and outcome explanation."

## 4. 설정

| 항목 | 권장 |
|------|------|
| reasoning effort | `medium`(기본) · `high`/`xhigh`(어려운/장시간) |
| 비대화 실행 | `codex exec "작업"` (CI/자동화) |
| 장시간 컨텍스트 | Responses API `/compact` |
| 툴 기본 | `git`, `rg`, `read_file`, `apply_patch` · 병렬 읽기 |

## 5. 첫 검증 (Hello World)
```bash
# 작은 변경을 ulw-loop으로 돌려 Oracle 검증이 도는지 확인
$ulw-loop "README에 badge 한 줄 추가하고 빌드 깨지지 않는지 검증"
```

→ 다음: [[lazy-codex/04-learning/02-verified-completion|04-2. 검증 완료 메커니즘]]
