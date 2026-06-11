---
date: 2026-06-07
tags: [tech, ai, codex, lazycodex, cheatsheet]
status: published
type: tech-tool-study
---

# cheatsheet — lazy codex 빠른 참조

## 설치
```bash
npx lazycodex-ai install          # Codex (Light)
bunx oh-my-openagent install      # OpenCode (Ultimate)
```

## 핵심 명령
```bash
/init-deep            # 계층 AGENTS.md 프로젝트 메모리
$ulw-plan "무엇을"    # 계획만(코드 X) → plans/<slug>.md
$start-work [plan]    # 체크리스트 실행 (ORCHESTRATION COMPLETE까지)
$ulw-loop "작업"      # Oracle 검증까지 자기-반복(≤500)
# 스킬: review-work, remove-ai-slops, frontend-ui-ux, programming, LSP, comment-checker
```

## 게으름 완화 프롬프트 (그냥 codex에도)
- ✅ "Persist until fully handled **end-to-end** this turn."
- ✅ "Default to implementing with reasonable assumptions; don't end with clarifications unless **truly blocked**."
- ✅ "Carry through implementation, **verification**, outcome explanation."
- ❌ upfront plan/preamble/status 요청 **빼기**(조기 중단 유발)
- effort: `medium` 기본 / `high`·`xhigh` 어려운 작업 · `codex exec` CI

## 거짓-완료 차단 5장치 (OmO)
| 장치 | 효과 |
|------|------|
| Hashline | 해시 앵커 편집, stale 거부 (6.7→68.3%) |
| Ralph Loop | 자기 출력 재독·재개 |
| Todo Enforcer | idle agent 강제 재engage |
| Oracle | 계획 대비 검증, 갭=실패 |
| durable `.omo/ulw-loop/` | 정확 재개 |

## 멀티에이전트
Prometheus(계획) · Sisyphus(오케스트레이터) · Hephaestus(워커) · **Oracle(검증)** · Librarian(검색)

## vs hermes (한 줄)
- OmO/lazycodex = **한 작업 거짓 없이 완수**(Oracle·Ralph)
- hermes = **24/7 안전 운영**(self-test 게이트 + 격리 워크트리 + PR 사람-머지 + RCX)
- 결합 = OmO 검증 규율 ⊕ hermes 운영/격리/사람 게이트

## 링크
[[lazy-codex/README|시리즈 처음]] · [[lazycodex]] · [[multi-agent-platforms]] · [[codex]]
