---
date: 2026-06-24
tags:
  - tech
  - ai
  - hankweave
  - cheatsheet
type: tech-tool-study
parent: "[[README]]"
---

# Hankweave - Cheatsheet

> [[05-projects|이전: 프로젝트]] | [[README|목차로 돌아가기]]

---

## 한 줄

Hankweave = `hank.json` declarative workflow로 codon sequence를 실행하고, checkpoint·rollback·sentinel·event journal·budget으로 long-horizon agent workflow를 repairable하게 만드는 runtime.

## 핵심 명령

```bash
bunx hankweave@latest --init
bunx hankweave@latest --validate
bunx hankweave@latest
bunx hankweave@latest --headless --autostart
bunx hankweave@latest --headless --autostart --max-cost 10
```

## 핵심 개념

| 개념 | 기억할 말 |
|------|-----------|
| Hank | `hank.json`에 정의된 declarative AI program |
| Codon | 하나의 agent task unit |
| Context firewalling | `fresh` context와 file handoff로 controlled forgetting |
| Checkpoint | codon 완료 시 Git commit 기반 snapshot |
| Rollback | 실패 시 특정 checkpoint로 복구 |
| Sentinel | event stream을 보는 secondary observer agent |
| Harness abstraction | Claude Code, Codex, Gemini CLI 등을 shim으로 실행 |
| Preflight validation | token 쓰기 전에 key/model/path/schema 확인 |

## Config에서 볼 항목

```json
{
  "codons": [
    {
      "id": "step-id",
      "prompt": "prompts/step.md",
      "model": "provider/model",
      "continuationMode": "fresh",
      "trackedFiles": ["work/input.md"],
      "checkpointedFiles": ["work/output.md"],
      "outputFiles": ["results/final.md"],
      "requirements": {
        "env": ["MODEL_API_KEY"]
      },
      "budget": {
        "maxDollars": 2.0
      }
    }
  ]
}
```

## Context mode 선택

| Mode | 쓸 때 | 주의 |
|------|------|------|
| `fresh` | codon 간 drift를 막고 file handoff를 강제 | handoff file 품질이 중요 |
| `continue-previous` | 같은 reasoning thread가 꼭 필요 | long context 누적과 숨은 상태 의존 증가 |

## Sentinel 아이디어

| Sentinel | 감시할 failure mode |
|----------|---------------------|
| Citation | source 없는 claim, stale source |
| Cost | budget 근접, token spike |
| Drift | initial goal 이탈 |
| Convention | repo style/schema/naming 위반 |
| Completeness | outputFiles 누락, checklist 미완료 |

## 운영 체크리스트

- [ ] `bun`, `git`, Node `>=20`, provider key 준비
- [ ] `--validate`를 token 사용 전 실행
- [ ] codon output이 file로 명시됨
- [ ] `continuationMode: "fresh"`를 기본값으로 검토
- [ ] `checkpointedFiles`와 `outputFiles` 구분
- [ ] codon `budget.maxDollars`와 run `--max-cost` 설정
- [ ] sentinel은 하나의 failure mode만 감시
- [ ] Docker/CI에서는 `/executions`와 `/results` volume 분리

## 언제 쓰나

| 쓰기 좋음 | 덜 적합 |
|-----------|---------|
| long-running research/report workflow | 짧은 one-shot prompt |
| generated artifact가 많고 rollback이 필요한 작업 | deterministic script가 충분한 작업 |
| 기존 CLI harness를 재사용해야 하는 팀 | agent loop를 직접 코드로 만들고 싶은 팀 |
| 비용과 drift를 감시해야 하는 batch job | 사람이 interactive하게 계속 조정하는 실험 |

## 관련 링크

- [[README|Hankweave 시리즈]]
- [[study/tech/ai/agent-orchestration]]
- [[study/tech/ai/lazy-codex]]
- [[study/tech/ai/model-context-protocol-mcp]]
- [[study/tech/ai/multi-agent-platforms]]
