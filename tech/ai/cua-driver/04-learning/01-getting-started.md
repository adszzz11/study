---
date: 2026-11-05
tags: [tech]
type: tech-tool-study
status: draft
---

# Cua Driver: 시작하기

[[tech/ai/cua-driver/README|Cua Driver 목차]] · [[tech/ai/cua-driver/04-learning/02-deep-dive|심화]]

## 목표

무해한 Calculator에서 window 관찰, element action, 결과 검증까지 한 번 완주한다. 실제 명령과 tool 이름은 설치한 Driver 버전의 `--help`와 공식 Quickstart를 우선한다.

## 1. 환경 진단

```bash
cua-driver doctor
cua-driver call list_apps
```

- macOS에서는 Accessibility와 Screen Recording 권한을 허용한다.
- `doctor` 결과에서 OS·display·permission 오류를 먼저 해결한다.
- 대상 app이 보인다고 곧 조작 가능한 것은 아니므로 window state를 확인한다.

## 2. Calculator 안전 실습

1. Calculator를 연다.
2. `list_windows`로 대상 window를 식별한다.
3. `get_window_state`에서 `element_token`과 현재 display를 읽는다.
4. 숫자 `6`, 연산자 `×`, 숫자 `7`, `=`를 token 기반 action으로 입력한다.
5. **새** `get_window_state`에서 `42`가 보이는지 확인한다.

좌표 click은 tree에 필요한 element가 없을 때만 fallback으로 쓴다. action 뒤 이전 screenshot을 재사용하지 않는다.

## 3. Codex 연결

```bash
cua-driver mcp-config --client codex
```

생성된 MCP 등록 내용을 확인한 다음 Codex를 재시작한다. 연결 후에는 작은 read-only 관찰부터 시도하고, login·upload·download·submit은 [[tech/ai/cua-driver/04-learning/02-deep-dive|심화의 승인 경계]]를 적용한다.

## Sources

- https://cua.ai/docs/cua-driver/quickstart
- https://cua.ai/docs/cua-driver/guides/connect-your-agent
- https://cua.ai/docs/cua-driver/concepts/platform-support
