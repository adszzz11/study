---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 04-1. Getting Started

## 목표

작은 representative payload로 Headroom을 **관찰 → 적용 → 비교**하고, 실제 agent에 붙이기 전에 compression과 retrieval 경로를 확인한다.

## 1. 설치 전 확인

- Python/PyPI package에 CLI가 포함된다.
- TypeScript package는 독립 CLI가 아니라 local Headroom proxy client다.
- production traffic에 바로 넣지 말고 synthetic secret-free payload로 시작한다.
- package version, supported provider, configuration은 조사 시점 이후 바뀔 수 있으므로 공식 문서를 확인한다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install headroom-ai
headroom --help
```

> [!CAUTION]
> 설치는 package code를 실행 환경에 추가한다. 공식 PyPI package와 원하는 version을 확인하고 isolated environment에서 진행한다.

## 2. Transparent proxy 실행

```bash
headroom proxy --port 8787
```

application의 provider base URL을 local proxy에 연결한 뒤 평소와 같은 request를 보낸다. provider credential은 shell history나 note에 기록하지 않는다.

확인할 것:

- request와 response가 정상 통과하는가?
- 큰 JSON/log payload에 compression이 발생하는가?
- 짧은 prompt 또는 protected recent context가 passthrough되는가?
- provider의 tool-call ordering이 유지되는가?
- proxy 종료 시 application fallback 동작은 무엇인가?

## 3. Agent wrapper로 빠르게 시험

```bash
headroom wrap codex
```

지원 agent는 `claude`, `codex`, `copilot`, `aider`, `opencode` 등을 포함한다. 정확한 지원 목록과 추가 인자는 현재 CLI help를 기준으로 확인한다.

첫 workload는 다음처럼 결과가 크고 정답을 사람이 확인할 수 있는 작업이 좋다.

- repository 전체에서 pattern을 검색하고 anomaly 파일 찾기
- 반복되는 test log에서 최초 root cause 찾기
- 큰 JSON array에서 error row와 outlier 식별하기

## 4. Python API 개념

```python
from headroom import compress

compressed = compress(messages, model="provider/model")
```

실제 import path와 return type은 설치한 version의 공식 API 문서를 확인한다. application 통합에서는 다음을 함께 기록한다.

- before/after token count와 compression ratio
- content type과 skip reason
- compression latency
- CCR marker와 retrieval 성공 여부
- uncompressed baseline 대비 final answer 차이

## 5. Mode를 구분한다

| 축 | 선택지 | 질문 |
|---|---|---|
| SDK behavior | `audit`, `optimize`, `simulate` | 실제 payload를 바꿀 것인가, 관찰만 할 것인가? |
| Proxy cache strategy | `cache`, `token` | prefix cache 안정성과 token 절감 중 무엇을 우선할까? |

처음에는 관찰 가능한 mode로 baseline을 만들고, multi-turn agent에는 기본 `cache` mode부터 비교한다. option의 정확한 CLI/API 표기는 현재 configuration 문서를 따른다.

## 6. 최소 검증표

- [ ] uncompressed baseline을 같은 task로 저장했다.
- [ ] error, warning, outlier가 compressed output에 남았다.
- [ ] JSON/code/tool-call 구조가 손상되지 않았다.
- [ ] retrieval marker에서 원문을 되찾았다.
- [ ] TTL 만료와 store eviction 시 동작을 확인했다.
- [ ] `cache`와 `token` mode의 실제 provider 비용을 비교했다.
- [ ] telemetry와 Beacon 설정을 검토했다.

## 다음 단계

- 내부 pipeline: [[headroom/04-learning/02-deep-dive]]
- 평가 harness 만들기: [[headroom/05-projects]]
- 명령 빠른 참조: [[headroom/cheatsheet]]

## Sources

- https://docs.headroomlabs.ai/docs
- https://docs.headroomlabs.ai/docs/configuration
- https://docs.headroomlabs.ai/docs/ccr
- https://pypi.org/project/headroom-ai/
- https://www.npmjs.com/package/headroom-ai
