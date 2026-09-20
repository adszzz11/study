---
date: 2026-09-08
tags: [tech]
type: tech-tool-study
status: draft
---

# Ruflo Getting Started

> [[../03-references|이전: 참고자료]] · [[../README|목차]] · [[02-deep-dive|다음: 심화]]

## 목표

첫 실습의 목표는 대규모 autonomous swarm이 아니다. disposable repository에서 version과 command surface를 확인하고, **작은 read-heavy task 하나**를 single-agent baseline과 비교한다.

## 1. 사전 점검

- Node.js/npm 환경과 coding agent client 준비
- Git으로 추적되는 test repository 또는 disposable sandbox 사용
- API key는 repository 파일이 아니라 environment/secret store에 보관
- 중요한 workspace와 분리하고 initial commit을 남김

```bash
node --version
npm --version
npm view ruflo version
npx ruflo@latest --help
```

문서의 명령이 현재 help에 없으면 추측해 실행하지 말고 해당 version의 README/changelog를 확인한다.

## 2. Version pinning

재현 가능한 학습을 위해 확인한 version을 명시한다.

```bash
# dossier snapshot 예시; 실행 시 latest를 다시 확인
npx ruflo@3.38.23 --help
```

`@latest`는 탐색에는 편하지만 team workflow, CI, production에는 release drift를 만든다. 검증된 version과 config를 함께 pin한다.

## 3. 초기화와 진단

실제 subcommand/flag는 설치 version의 help를 source of truth로 삼는다.

```bash
npx ruflo@3.38.23 --help
npx ruflo@3.38.23 init --help
npx ruflo@3.38.23 doctor --help
```

초기화 전에 다음 질문에 답한다.

- 생성·수정될 파일 목록은 무엇인가?
- MCP server가 노출할 tool namespace는 무엇인가?
- hook은 어떤 shell/file/network action을 실행하는가?
- memory backend와 저장 위치는 어디인가?
- telemetry가 수집하는 data와 opt-out 방법은 무엇인가?

## 4. 첫 task 설계

```text
Task: 작은 module의 behavior 조사와 test gap 보고
Roles: researcher + tester + reviewer
Topology: hierarchical-mesh
Write permission: report file 한 곳만
Forbidden: dependency install, network write, destructive shell
Exit criteria: evidence, test command, unresolved risks
```

처음에는 최대 agent 수를 2~3으로 제한한다. 같은 파일을 여러 agent가 수정하게 하지 말고 researcher는 read-only, tester는 test 결과, reviewer는 evidence 검토처럼 output boundary를 나눈다.

## 5. Baseline 비교

| 측정값 | Single agent | Ruflo swarm |
|---|---:|---:|
| task 성공 여부 |  |  |
| wall-clock time |  |  |
| input/output token |  |  |
| tool call 수 |  |  |
| merge conflict 수 |  |  |
| human correction time |  |  |
| 발견한 defect 수 |  |  |

## 6. MCP 최소 노출

314개 tool을 모두 노출하는 대신 실습에 필요한 swarm/status/memory 검색 namespace만 선택한다. write, shell, browser, credential 관련 tool은 명시적 필요와 approval path가 생긴 뒤 추가한다.

```text
Default deny
  ├─ allow: task/status read
  ├─ allow: scoped memory search
  ├─ conditional: repository write
  └─ deny: destructive shell / secret access / external publish
```

## 완료 checklist

- [ ] 실행 version을 기록했다.
- [ ] 생성된 config와 hook을 diff로 검토했다.
- [ ] 2~3 agents로 작은 task를 완료했다.
- [ ] single-agent baseline과 cost/quality를 비교했다.
- [ ] 최소 MCP namespace만 노출했다.
- [ ] 작업 후 memory와 log에 secret이 없는지 확인했다.
- [ ] rollback 또는 clean removal 절차를 기록했다.

## Sources

- https://www.npmjs.com/package/ruflo?activeTab=versions
- https://github.com/ruvnet/ruflo/blob/main/README.md
- https://github.com/ruvnet/ruflo/blob/main/v3/implementation/init/CONFIGURATION.md

