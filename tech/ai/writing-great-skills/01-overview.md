---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# Writing Great Skills — Overview

> [[README|목차]] · [[02-ecosystem|다음: Ecosystem]]

## What

`writing-great-skills`는 다른 Agent Skill을 작성하고 진단하는 **meta-skill**이다. Skill은 보통 다음 요소로 반복 가능한 capability를 패키징한다.

```text
writing-great-skills/
├── SKILL.md          # 핵심 원칙과 진단 workflow
├── GLOSSARY.md       # 필요한 branch에서 읽는 reference
└── agents/
    └── openai.yaml   # agent/client 표시 metadata
```

이 Skill 자체는 `disable-model-invocation: true`로 선언된 user-invoked workflow다. 지원 client에서는 사용자가 `/writing-great-skills`처럼 명시적으로 시작한다. 단, 이 field는 core Agent Skills specification의 표준 field가 아니므로 모든 harness에서 통용된다고 가정하면 안 된다.

## Why

일반 prompt는 일회성 지시에 적합하지만, 반복 workflow의 절차·자료·도구 사용법을 매번 복사하면 context 비용과 drift가 커진다. 반대로 모든 지침을 system prompt에 상주시켜도 관련 없는 turn까지 비용을 지불한다. Skill은 discovery metadata만 상시 노출하고 본문과 resource를 필요할 때 적재한다.

Skill도 probabilistic하게 실패한다.

| Failure | 관찰되는 증상 |
|---|---|
| Misrouting | 필요한 Skill이 trigger되지 않거나 다른 Skill이 선택됨 |
| Premature completion | 일부 step만 수행하고 완료로 선언함 |
| Sprawl | 예외와 설명이 늘어 핵심 workflow가 묻힘 |
| No-op | “꼼꼼히” 같은 문장이 behavior를 바꾸지 않음 |
| Negation | 금지 대상이 context에서 오히려 활성화됨 |
| Sediment | 오래된 지침이 현재 project와 충돌함 |

따라서 여기서 determinism은 output equality가 아니다. brainstorming의 아이디어는 달라도 다음 process는 안정적이어야 한다.

```text
discover → select → load → execute steps → verify criteria → report
```

## Progressive Disclosure

표준적인 loading은 세 단계다.

1. **Metadata** — `name`, `description`이 discovery/index에 노출된다.
2. **Instructions** — 활성화 시 `SKILL.md` 본문 전체가 context에 들어간다.
3. **Resources/code** — 필요한 branch에서 references, scripts, assets를 읽거나 실행한다.

Pocock의 information hierarchy로 표현하면 다음과 같다.

```text
즉시 필요
  ↓
In-skill steps
  ↓
In-skill reference
  ↓
Disclosed/external reference
```

모든 branch에 필요한 것은 inline한다. 일부 branch에만 필요한 것은 “언제 읽는가”가 명확한 context pointer 뒤로 옮긴다. 예를 들어 `용어는 GLOSSARY.md 참고`보다 `routing 용어를 처음 정의하거나 비교할 때 GLOSSARY.md를 읽는다`가 더 안정적이다.

Specification은 `SKILL.md`를 5,000 tokens와 500 lines 이하로 유지하고 reference chain을 가능한 한 한 단계로 제한하도록 권장한다.

## Description As Routing Interface

Model-invoked Skill에서 `description`은 요약문이 아니라 probabilistic dispatch interface다.

- 무엇을 하는지와 언제 쓰는지를 함께 쓴다.
- 핵심 **leading word**를 앞쪽에 둔다.
- 서로 다른 branch마다 trigger 하나를 둔다.
- 같은 branch의 동의어를 나열하지 않는다.
- 구현 세부사항은 body로 내린다.
- third-person과 사용자의 실제 domain vocabulary를 쓴다.

```yaml
---
name: release-note-audit
description: Audits release notes for breaking changes when a user asks to upgrade, migrate, or assess version compatibility.
---
```

Core specification에서 `description`은 필수이며 최대 1,024자다.

## Leading Word

Leading word는 pretraining에 이미 자리 잡은 압축 개념을 behavioral anchor로 재사용한다.

| Word | 유도하는 behavior |
|---|---|
| `red` | test가 bug를 실제로 재현한 binary state |
| `tight loop` | 빠르고 반복 가능하며 feedback이 짧은 과정 |
| `tracer bullet` | architecture 전체를 관통하는 좁은 vertical slice |
| `fog of war` | 미래 step을 감추고 현재 step에 집중 |

이 표현은 description에서는 routing anchor, body에서는 execution anchor가 된다. 다만 효과는 모델과 task에 따라 달라지므로 반복 eval 없이 “좋아 보이는 단어”만 추가하면 no-op이 될 수 있다.

## Step And Completion Criterion

각 step에는 agent가 스스로 판정할 수 있는 exit condition이 있어야 한다.

| 수준 | 예시 |
|---|---|
| 약함 | 변경 목록을 만든다. |
| 강함 | 모든 modified model이 목록에 있는지 diff와 대조한다. |
| 더 강함 | 누락이 없고 각 항목에 검증 근거가 있을 때만 다음 step으로 간다. |

Criterion의 **clarity**는 조기 완료를 막고, **demand**는 필요한 legwork의 범위를 정한다. 먼저 criterion을 선명하게 만들고, 그래도 rush가 재현될 때 context boundary나 별도 실행 단계를 고려한다.

## Failure Mode와 처방

| Failure mode | 처방 |
|---|---|
| Premature completion | checkable하고 exhaustive한 completion criterion |
| Duplication | description/body/reference 사이 Single Source of Truth |
| Sediment | 주기적인 relevance review와 삭제 |
| Sprawl | branch별 reference/script 분리 |
| No-op | 문장별 behavioral delta 검사 |
| Negation | 금지문 대신 원하는 positive target 명시 |
| Negative Space | 생략된 결정을 찾아 branch나 default로 명시 |

`Negation`과 `Negative Space`는 v1.1에서 추가된 진단 개념이다. 특히 negative space는 쓰지 않은 내용을 모두 채우라는 뜻이 아니라, 중요한 결정이 우연히 model prior에 넘어갔는지를 검토하라는 뜻이다.

## Evidence Check

`SWE-Skills-Bench`는 공개 SWE Skill 49개 중 39개가 pass rate를 개선하지 못했고 평균 개선은 `+1.2%`였다고 보고한다. 잘 맞는 specialized skill은 최대 `+30%`였지만 version mismatch는 최대 `-10%`를 만들었다. 일반화하면 다음과 같다.

```text
Skill quality ≠ instruction volume
Skill quality ≈ scope fit × routing fit × context fit × evaluation
```

## Sources

- [원본 SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/SKILL.md)
- [GLOSSARY.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-great-skills/GLOSSARY.md)
- [공식 설명 페이지](https://www.aihero.dev/skills-writing-great-skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401)
- [v1.1 releases](https://github.com/mattpocock/skills/releases)

