---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent — References

> [[02-ecosystem|이전: Ecosystem]] · [[README|목차]] · [[04-learning/01-getting-started|다음: Getting Started]]

## Reading Order

1. 공식 저장소 README로 project scope, license, install entry point를 확인한다.
2. Quickstart로 현재 release의 실제 setup과 session workflow를 익힌다.
3. RLM Runtime 문서로 persistent kernel과 context boundary를 이해한다.
4. Architecture index에서 daemon, session, RPC와 운영 기능을 따라간다.
5. Prime Agent 논문에서 L0–L3 model과 benchmark methodology를 읽는다.
6. Refine skill과 Continual Harness 논문을 함께 읽고 “self-improving”의 범위를 구분한다.
7. 출시 보고서의 성능 수치를 독립 검증 전의 developer-reported claim으로 기록한다.

## Primary Sources

| 자료 | 읽을 내용 | 주의점 |
|---|---|---|
| [공식 저장소](https://github.com/PrimeIntellect-ai/prime-agent) | source, license, package 구조, 최신 README | branch와 release 시점 기록 |
| [Coding Agent README](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/README.md) | provider, package-level usage | 지원 목록은 변경 가능 |
| [Quickstart](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/quickstart.md) | 설치, 첫 session, 기본 workflow | 실행 전 현재 명령 재확인 |
| [Architecture index](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/index.md) | daemon, session, API 문서 지도 | client와 worker 경계에 주목 |
| [RLM Runtime](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/rlm-runtime.md) | IPython kernel, `rlm()`, context 처리 | lifecycle isolation과 sandbox 구분 |
| [Custom Models](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/models.md) | `models.json`, local endpoint | provider별 compatibility 검증 |
| [Refine skill](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/skills/refine/SKILL.md) | typed state와 refinement 절차 | diff review·rollback 확인 |

## Papers and Reports

### Prime Agent technical paper

- HTML: <https://arxiv.org/html/2608.23552>
- 확인할 질문:
  - L0–L3 계층은 실제 runtime component에 어떻게 매핑되는가?
  - RLM-native harness가 active context 사용량을 어떻게 바꾸는가?
  - benchmark별 model, harness version, budget와 stopping rule은 무엇인가?
  - competitor score는 자체 재실행인가, 공식 발표값인가?

### Continual Harness paper

- Abstract: <https://arxiv.org/abs/2605.09998>
- 핵심 구분:
  - model weight update가 아니다.
  - prompt notes, memories, skills, subagent specifications를 개선한다.
  - provenance, versioning, rollback이 안전성의 일부다.

### Launch report

- URL: <https://www.primeintellect.ai/blog/prime-agent>
- 성능 주장과 product framing을 파악하는 자료다.
- 개발사 보고서이므로 independent reproduction과 분리해 인용한다.

## Evidence Quality Checklist

- [ ] 조사 기준일(`2026-09-01`)과 사용한 commit/release 기록
- [ ] model 이름, provider, sampling setting, harness version 기록
- [ ] task budget, retry, concurrency, Best@k 정의 기록
- [ ] raw trajectory와 evaluation code 공개 여부 확인
- [ ] confidence interval/statistical significance 확인
- [ ] 비교 점수가 자체 재실행인지 경쟁사 공식 수치인지 구분
- [ ] data contamination과 benchmark-specific tuning 가능성 확인
- [ ] 독립 reproduction 유무 확인
- [ ] 실패 사례와 reward hacking도 함께 기록

## Claim Ledger

| 주장 | dossier 근거 | 현재 해석 |
|---|---|---|
| ARC-AGI-3 `95.5% RHAE Best@1` | 출시 보고서·기술 논문 | developer-reported result |
| 세 실행 `[95.0, 95.2, 95.5]` | 출시 보고서·기술 논문 | variance 정보가 제한된 초기 결과 |
| `99.97% Best@3` | 출시 보고서·기술 논문 | selection protocol과 cost를 함께 봐야 함 |
| long-context 경쟁력 | 기술 논문 | model/harness별 조건 확인 필요 |
| nanoGPT harness effect가 noise보다 작음 | 저자 분석 | harness 우위의 일반화를 제한하는 반례 |
| Factorio reward hacking | 실험 실패 사례 | refinement가 exploit도 보존할 수 있음 |

## Local Research Notes

새 release를 검토할 때 아래 형식으로 추가한다.

```markdown
### YYYY-MM-DD / version or commit

- Environment:
- Model/provider:
- Task and budget:
- Observed behavior:
- Raw artifact:
- Reproduction status:
- Security/refinement diff:
```

## Sources

- [Prime Agent 공식 저장소](https://github.com/PrimeIntellect-ai/prime-agent)
- [Prime Agent 기술 논문](https://arxiv.org/html/2608.23552)
- [Continual Harness 논문](https://arxiv.org/abs/2605.09998)
- [공식 출시 보고서](https://www.primeintellect.ai/blog/prime-agent)

