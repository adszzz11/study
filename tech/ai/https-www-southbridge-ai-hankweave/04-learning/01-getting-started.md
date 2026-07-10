---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - getting-started
  - hands-on
type: tech-tool-study
parent: "[[../README]]"
---

# Hankweave - 시작하기

> [[../03-references|이전: 참고자료]] | [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

---

## 1. 준비물

| 항목 | 설명 |
|------|------|
| `bun` | Hankweave 실행에 사용되는 runtime/package runner |
| `git` | checkpoint/rollback의 기반 |
| Model provider key | 최소 1개 provider API key |
| Node `>=20` | 2026-06-24 기준 `release/alpha` package metadata의 engine 요구사항 |

```bash
node --version
bun --version
git --version
```

## 2. Starter project 생성

```bash
bunx hankweave@latest --init
```

생성 후 먼저 확인할 구조:

```text
.
├── hank.json
├── prompts/
├── data/
└── outputs/ 또는 results/
```

핵심은 `hank.json`이 agent workflow의 실행 계획이라는 점이다. prompt, model, codon 순서, tracked/output files, budget, requirements를 config로 확인한다.

## 3. Preflight validation

실행 전에 validation을 먼저 돌린다.

```bash
bunx hankweave@latest --validate
```

확인할 항목:

- API key가 설정되어 있는가?
- config에 적힌 model을 provider가 사용할 수 있는가?
- `prompts/`, `data/`, output path가 존재하거나 생성 가능한가?
- sentinel schema와 rig config가 유효한가?
- budget guardrail이 지나치게 낮거나 누락되지 않았는가?

## 4. TUI 실행과 headless 실행

로컬에서 관찰하며 실험할 때:

```bash
bunx hankweave@latest
```

CI/automation에서 시작과 동시에 실행할 때:

```bash
bunx hankweave@latest --headless --autostart
```

비용 상한을 runtime에서 추가로 제한할 때:

```bash
bunx hankweave@latest --headless --autostart --max-cost 5
```

## 5. 첫 실습: codon 2개 만들기

목표는 `fresh`와 `continue-previous`의 차이를 체감하는 것이다.

| Codon | 목적 | Context 전략 | Output |
|-------|------|--------------|--------|
| `gather` | 자료 수집과 요약 | `fresh` | `work/gather.md` |
| `synthesize` | gather 결과 기반 최종 정리 | `fresh` 또는 `continue-previous` 비교 | `results/report.md` |

```json
{
  "codons": [
    {
      "id": "gather",
      "prompt": "prompts/gather.md",
      "continuationMode": "fresh",
      "outputFiles": ["work/gather.md"],
      "budget": { "maxDollars": 1.0 }
    },
    {
      "id": "synthesize",
      "prompt": "prompts/synthesize.md",
      "continuationMode": "fresh",
      "trackedFiles": ["work/gather.md"],
      "outputFiles": ["results/report.md"],
      "budget": { "maxDollars": 1.0 }
    }
  ]
}
```

## 6. Guardrail 추가

작은 workflow라도 다음 항목은 초기에 넣어본다.

| 설정 | 목적 |
|------|------|
| `checkpointedFiles` | checkpoint에 포함할 산출물 명시 |
| `outputFiles` | codon의 완료 산출물 명시 |
| `requirements.env` | 필요한 API key/env 확인 |
| `budget.maxDollars` | codon 단위 비용 제한 |
| `--max-cost` | run 전체 비용 제한 |

## 7. 완료 기준

- [ ] `--init` project의 `hank.json` 구조를 설명할 수 있다.
- [ ] `--validate`가 token 사용 전 무엇을 검사하는지 이해한다.
- [ ] TUI 실행과 `--headless --autostart` 실행의 차이를 안다.
- [ ] codon 2개로 file handoff를 구현했다.
- [ ] 최소 하나의 budget guardrail을 넣었다.

## 관련 노트

- [[study/tech/ai/codex]] - Hankweave가 실행할 수 있는 coding harness
- [[study/tech/ai/lazy-codex]] - agent 실행 검증 패턴
- [[study/tech/devtools/git]] - checkpoint/rollback 이해에 필요한 Git 기초
