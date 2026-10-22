---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Getting started

## 1. 기존 harness부터 탐색

```bash
pip install cli-anything-hub
cli-hub search <keyword>
```

이미 검증된 harness가 있다면 새로 생성하기 전에 command surface, 설치 방식, 최근 release를 확인한다. 외부 package 설치는 격리된 environment에서 수행하고 provenance를 검토한다.

## 2. open-source target으로 생성 학습

source와 실행 방법이 명확한 작은 target을 고른다.

```text
/cli-anything <target-path-or-repo>
```

처음에는 파일 하나를 만들고 다시 여는 workflow처럼 artifact가 명확한 범위를 고른다. destructive command, credential, network write는 첫 실습 범위에서 제외한다.

## 3. 설치 및 interface smoke test

생성된 project에서 다음을 실행한다.

```bash
pip install -e .
<generated-cli> --help
<generated-cli> <command> --json
<generated-cli> repl
```

`--help`에는 command와 argument가 발견 가능하게 나타나야 한다. `--json`은 사람이 읽는 log와 분리된 안정적인 object를 반환해야 하며, REPL에서는 state 생성·변경·종료를 확인한다.

## 4. 성공 조건 확인

- native backend가 만든 artifact가 실제로 존재하는가?
- 해당 app 또는 library로 artifact를 재오픈할 수 있는가?
- 성공과 실패 결과의 JSON shape가 예측 가능한가?
- test가 mock만 통과한 것이 아니라 실제 backend를 호출하는가?

누락 capability는 넓게 다시 만들지 말고 `/refine`으로 command와 acceptance criteria를 좁혀 보강한다.

## Sources

- https://github.com/HKUDS/CLI-Anything
- https://clianything.cc/
