---
date: 2026-09-01
tags: [tech]
type: tech-tool-study
status: draft
---

# Prime Agent — Getting Started

> [[../03-references|이전: References]] · [[../README|목차]] · [[02-deep-dive|다음: Deep Dive]]

## Goal

첫 실습의 목표는 production repository를 맡기는 것이 아니다. disposable workspace에서 현재 공식 Quickstart를 따라 설치하고, persistent REPL의 context filtering과 durable session 복구를 관찰하는 것이다.

## 0. Safety Boundary

> [!danger] Prime Agent는 security sandbox가 아니다.
> Python과 shell command가 현재 사용자 권한으로 실행되므로 production credential·민감한 home directory·내부 network를 노출하지 않는다.

- [ ] disposable clone 또는 throwaway container 준비
- [ ] read/write 가능한 directory를 실습 workspace로 제한
- [ ] production SSH key, cloud credential, `.env` 제거
- [ ] outbound network를 필요한 provider endpoint로 제한
- [ ] cost·time·turn·child concurrency 상한 결정
- [ ] immutable test와 외부 verifier 준비
- [ ] third-party package/skill source allowlist 결정

## 1. Pin the Source

```bash
git clone https://github.com/PrimeIntellect-ai/prime-agent.git
cd prime-agent
git rev-parse HEAD
```

조사 기준일은 `2026-09-01`이다. 설치 명령과 package 요구사항은 출시 초기 변경될 수 있으므로 clone한 revision의 다음 문서를 기준으로 실행한다.

- `packages/coding-agent/docs/quickstart.md`
- `packages/coding-agent/README.md`
- `packages/coding-agent/docs/models.md`

```bash
# 문서에 명시된 runtime/version과 install command를 먼저 확인한다.
sed -n '1,240p' packages/coding-agent/docs/quickstart.md
```

이 노트는 dossier에 없는 package manager나 executable 이름을 추정하지 않는다. 실제 명령은 pinned revision의 Quickstart를 따른다.

## 2. Configure a Provider

두 방식 중 하나를 선택한다.

| 방식 | 예시 | 확인 사항 |
|---|---|---|
| Subscription login | Claude, ChatGPT/Codex, GitHub Copilot | 지원 계정, login scope, session expiry |
| API/local endpoint | OpenAI, Anthropic, Gemini, OpenRouter, Ollama, vLLM, LM Studio 등 | key scope, base URL, model ID, context limit |

Local OpenAI-compatible endpoint는 `models.json` 형식을 공식 Custom Models 문서에서 확인한다. credential 값은 repository나 session artifact에 기록하지 않는다.

## 3. First Session

현재 Quickstart의 launch command로 새 session을 시작한 뒤, 작은 read-only task를 준다.

```text
Inspect this disposable repository. Use the persistent Python REPL to count
files by extension, print only the top five groups, and do not modify files.
```

관찰할 항목:

- [ ] session별 독립 IPython kernel이 생성되는가?
- [ ] file list 전체가 아니라 aggregate만 active context에 출력되는가?
- [ ] Python variable을 다음 turn에서도 재사용하는가?
- [ ] JSON event/history에서 tool output과 model message를 구분할 수 있는가?

REPL에서 기대하는 계산 패턴은 다음과 같다.

```python
from collections import Counter
from pathlib import Path

counts = Counter(p.suffix or "<none>" for p in Path(".").rglob("*") if p.is_file())
print(counts.most_common(5))
```

`counts` 전체는 L2에 남고 `print()` 결과만 L1으로 올라가는지 trajectory에서 확인한다.

## 4. Context Filtering Exercise

작은 synthetic log를 준비하거나 기존 non-sensitive test log를 사용한다.

```python
from pathlib import Path

lines = Path("build.log").read_text(errors="replace").splitlines()
errors = [line for line in lines if "ERROR" in line]
print({"total_lines": len(lines), "error_count": len(errors)})
print("\n".join(errors[:10]))
```

비교 기록:

| 항목 | 전체 log 출력 | REPL filtering |
|---|---:|---:|
| active context에 들어온 line 수 |  |  |
| task 완료 여부 |  |  |
| token/cost |  |  |
| 누락된 핵심 error |  |  |

## 5. Detach and Reattach

공식 session 문서의 명령으로 다음을 실습한다.

1. durable objective를 설정한다.
2. Python variable 하나를 만든다.
3. client를 detach한다.
4. daemon/worker 상태를 확인한다.
5. 같은 session에 reattach한다.
6. objective, variable, history가 유지되는지 검증한다.

검증 질문:

- client 종료와 worker 종료는 어떻게 구분되는가?
- crash recovery 뒤 kernel state와 disk history 중 무엇이 복구되는가?
- compaction 뒤 stable handle과 parent/child 관계가 유지되는가?

## 6. Minimal Child Experiment

격리된 read-only task 하나만 child에게 맡긴다.

```python
child = await rlm(
    "Read the test directory and report the three most important test gaps. Do not edit files.",
    name="test-gap-reviewer",
)
print(child.rlm_child_id, child.model)
```

- stable handle이 admission 직후 반환되는지 확인한다.
- parent가 기다리는 동안 다른 계산을 계속할 수 있는지 본다.
- child 결과가 `agent_message` 또는 filesystem artifact로 어떻게 도착하는지 기록한다.
- root와 descendant의 token, cost, time 합계가 맞는지 확인한다.

## Completion Criteria

- [ ] pinned revision과 environment를 기록했다.
- [ ] production credential 없는 격리 workspace에서 실행했다.
- [ ] large input을 L2에서 처리하고 최소 summary만 L1에 출력했다.
- [ ] detach/reattach 후 session state를 확인했다.
- [ ] child stable handle과 asynchronous result delivery를 관찰했다.
- [ ] 비용과 concurrency budget을 넘지 않았다.
- [ ] 파일 변경이 없거나 예상한 disposable artifact뿐임을 확인했다.

## Sources

- [공식 Quickstart](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/quickstart.md)
- [Coding Agent README](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/README.md)
- [Custom Models](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/models.md)
- [RLM Runtime Architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/main/packages/coding-agent/docs/rlm-runtime.md)

