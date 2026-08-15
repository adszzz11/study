---
date: 2026-08-15
tags: [tech]
type: tech-tool-study
status: draft
---

# Switchyard Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

먼저 intelligent routing을 켜지 않고 `passthrough` route로 end-to-end protocol bridge를 검증한다. 그 뒤에 두 target과 router를 추가해야 translation 문제와 routing 문제를 분리해 진단할 수 있다.

## Prerequisites

- Rust-native server 또는 PyPI package를 실행할 수 있는 환경
- 사용할 upstream endpoint와 API key
- `curl` 또는 OpenAI/Anthropic-compatible client
- secret을 source control에 넣지 않는 환경변수 관리 방식

> [!important]
> v0.2.0은 pre-alpha다. 아래 흐름은 학습용이며, 정확한 option name과 TOML schema는 설치한 release tag의 공식 example로 확인한다. `main`의 Unreleased 문서와 v0.2.0 binary를 섞지 않는다.

## 1. Install And Inspect

Python package 경로를 사용할 경우 isolated environment에서 version을 고정한다.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install 'nemo-switchyard==0.2.0'
switchyard --help
switchyard-server --help
```

source build를 택했다면 v0.2.0 tag를 checkout하고 repository의 Getting Started를 따른다. 어떤 방식을 쓰든 실제 binary의 `--help`를 먼저 확인한다.

## 2. Model The Configuration

TOML은 세 계층으로 생각한다.

```text
llm_client "upstream-openai"
  ├─ base_url
  ├─ wire format: openai_chat
  ├─ api_key_env: UPSTREAM_API_KEY
  └─ retry policy

target "efficient"
  ├─ model: <actual-upstream-model-id>
  └─ llm_client: upstream-openai

route "assistant"
  ├─ client-facing model: assistant
  └─ algorithm: passthrough → efficient
```

이 구조를 공식 v0.2.0 sample TOML의 실제 field syntax로 옮긴다. API key 값 자체가 아니라 환경변수 이름만 configuration에 둔다.

```bash
export UPSTREAM_API_KEY='<secret>'
```

설정 파일을 commit한다면 model ID, endpoint 공개 범위도 함께 검토한다. secret이 포함되었는지는 별도로 scan한다.

## 3. Start The Server

설치한 v0.2.0 binary의 help와 Getting Started에 표시된 config option으로 server를 실행한다.

```bash
switchyard-server --help
# 공식 v0.2.0 문서에서 확인한 config option으로 시작
```

legacy 문서의 `switchyard serve`, YAML route bundle, FastAPI endpoint를 새 구성에 사용하지 않는다.

## 4. Verify Control Endpoints

```bash
curl -fsS http://127.0.0.1:PORT/health
curl -fsS http://127.0.0.1:PORT/v1/models
curl -fsS http://127.0.0.1:PORT/metrics
curl -fsS http://127.0.0.1:PORT/v1/stats
```

확인할 항목:

- health check가 성공하는가?
- client-facing route model이 `/v1/models`에 보이는가?
- request 전후 stats와 metrics가 증가하는가?
- log에 secret이나 전체 민감 prompt가 노출되지 않는가?

## 5. Send A Baseline Request

아래 request의 `model`에는 upstream model ID가 아니라 route가 노출한 client-facing model ID를 넣는다.

```bash
curl http://127.0.0.1:PORT/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "assistant",
    "messages": [{"role": "user", "content": "Reply with exactly: pong"}],
    "stream": false
  }'
```

같은 의미의 요청을 `/v1/responses`와 `/v1/messages`에도 보내 protocol translation을 확인한다. streaming과 tool call은 non-streaming text baseline이 통과한 뒤 추가한다.

## 6. Validate The Result

- [ ] HTTP status와 error envelope가 client protocol에 맞다.
- [ ] response `model`에 실제 serving target이 드러난다.
- [ ] routing header와 JSONL log의 target이 일치한다.
- [ ] input/output/cache token usage가 upstream과 합리적으로 맞는다.
- [ ] streaming 종료 event와 tool-call arguments가 손상되지 않는다.
- [ ] 잘못된 key, timeout, context overflow의 failure mode가 bounded하다.

## 7. Try A Coding-Agent Launcher

baseline server가 통과하면 launcher의 help를 확인하고 local experiment를 수행한다.

```bash
switchyard launch claude --help
switchyard launch codex --help
switchyard launch openclaw --help
```

launcher는 local proxy lifecycle과 agent endpoint 설정을 관리한다. 실행 전 현재 shell의 provider-related environment가 어떤 값으로 바뀌는지, 종료 후 복원되는지 확인한다.

## Troubleshooting

| 증상 | 먼저 확인할 것 |
|---|---|
| route model not found | `/v1/models`, route의 client-facing ID |
| 401/403 | `api_key_env` 이름, process environment, upstream auth 방식 |
| tool call parse error | inbound/outbound wire format, streaming 여부, schema fidelity |
| 예상과 다른 model | response `model`, routing header, session affinity |
| 중복 호출·비용 급증 | proxy와 upstream gateway의 retry 중복, escalation 횟수 |
| 종료했는데 upstream 사용 지속 | client disconnect known issue, timeout/concurrency 외부 제한 |

## Sources

- [Getting Started](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/getting_started.md)
- [Core Concepts](https://github.com/NVIDIA-NeMo/Switchyard/blob/main/docs/core_concepts.md)
- [v0.2.0 Release](https://github.com/NVIDIA-NeMo/Switchyard/releases/tag/v0.2.0)
- [PyPI 0.2.0](https://pypi.org/project/nemo-switchyard/0.2.0/)

