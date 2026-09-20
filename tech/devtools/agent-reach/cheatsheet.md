---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach — Cheatsheet

[[tech/devtools/agent-reach/README|목차]] · [[tech/devtools/agent-reach/04-learning/01-getting-started|설치 실습]]

## 기준

**2026-09-09의 `main` 기준**이다. v1.5.0을 설치했다면 해당 tag의 도움말·문서를 먼저 확인한다. 아래 명령은 실행 예시이며 이 노트의 실측 결과가 아니다. `VIDEO_URL`, `BV_ID`, `query`는 실제 공개 대상에 맞게 바꾼다.

## Agent Reach CLI

| 목적 | 명령 | 조건·의미 |
|---|---|---|
| 옵션 확인 | `agent-reach --help` | 설치된 revision의 interface 확인 |
| 환경 점검 | `agent-reach install --env=auto` | 현재 main의 check-only 기본값 |
| 설치 계획 | `agent-reach install --env=auto --dry-run` | system 모드가 할 작업 미리 보기 |
| 도구 설치·설정 | `agent-reach install --env=auto --system` | 외부 도구·설정 변경을 선택한 경우 |
| 선택 channel | `agent-reach install --env=auto --system --channels=opencli` | desktop backend가 필요한 경우 |
| 상태 보기 | `agent-reach doctor` | channel별 message까지 읽기 |
| JSON 진단 | `agent-reach doctor --json` | 실제 URL 결과는 별도 확인 |
| 업데이트 조회 | `agent-reach check-update` | 자동 업데이트 성공을 뜻하지 않음 |
| 전사 도움말 | `agent-reach transcribe --help` | key·provider·출력 옵션 확인 |

## 실제 읽기는 upstream 호출

```bash
# 공개 URL → Jina Reader
curl --fail --show-error --location 'https://r.jina.ai/https://example.com'

# GitHub: gh 설치 및 필요한 인증 후
gh search repos 'agent reach'

# Exa: mcporter와 exa MCP 설정 후
mcporter call exa.web_search_exa query='agent reach' numResults=5

# YouTube: metadata와 자막을 따로 확인
yt-dlp --dump-json 'VIDEO_URL'
yt-dlp --list-subs 'VIDEO_URL'

# Bilibili: 검색은 bili, 자막은 desktop OpenCLI
bili search 'query' --type video -n 5
opencli bilibili subtitle BV_ID

# Reddit: OpenCLI 연결 + Reddit 로그인 필요
opencli reddit search 'query' -f yaml

# Instagram: 사용자 검색이며 게시물 keyword 검색이 아님
opencli instagram search 'query' -f yaml
```

이 명령들은 각 upstream이 준비된 환경에서 사용한다. Exa의 무료 경로에도 rate limit이 있으며, `doctor`가 `ok`라고 표시해도 MCP 설정과 실제 응답을 확인한다.

## 인증·전사 빠른 참조

```bash
# 숨김 입력을 사용하는 설정 명령; 값은 공개 노트에 쓰지 않는다.
agent-reach configure twitter-cookies
agent-reach configure xhs-cookies
agent-reach configure groq-key

# provider key와 오디오 전송 조건을 확인한 뒤 선택적으로 실행
agent-reach transcribe 'VIDEO_URL'
```

- Twitter 직접 호출에는 같은 프로세스 환경의 `TWITTER_AUTH_TOKEN`, `TWITTER_CT0`가 필요하다. `configure`가 현재 shell을 설정하지 않는다.
- XiaoHongShu Cookie 설정은 OpenCLI의 Chrome session에 Cookie를 주입하지 않는다.
- 설정 파일: `~/.agent-reach/config.yaml`. 공개 vault에 저장할 파일이 아니다.
- 현재 전사 auto 모드는 첫 configured provider만 사용한다. `--allow-provider-fallback`은 다른 provider에도 같은 오디오를 보낼 수 있는 명시적 옵션이다.

## 실패 해석

| 관찰 | 가능한 의미 | 다음 확인 |
|---|---|---|
| `warn`, `active_backend: null` | 설치 부족 또는 인증 검증 생략 | message와 해당 channel 소스 |
| `ok`인데 결과 없음 | probe 범위와 실제 작업 차이 | 대상 URL의 본문·자막·MCP 설정 |
| metadata만 확보 | 자막 검증은 아직 안 됨 | 자막 목록과 실제 파일 |
| OpenCLI bridge 연결됨 | 플랫폼 로그인은 별도일 수 있음 | 대상 플랫폼의 실제 read 명령 |
| 자막 URL의 빈 응답 | 일시적인 URL 만료 가능 | video reference의 제한된 재시도 |
| CLI 경로만 존재 | 실행 파일 또는 venv가 깨졌을 수 있음 | 가벼운 명령 실행과 오류 |
| 429 / 인증 오류 | 빈도 제한·session 문제 가능 | 빈도 낮추기, 사용자가 인증 상태 확인 |

## 기억할 원칙

**버전 확인 → doctor 해석 → upstream 실행 → 관련된 비어 있지 않은 콘텐츠 확인 → 출처와 한계 기록.**

## Sources

- [현재 Install guide](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md)
- [CLI 구현](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/cli.py)
- [Social reference](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/social.md)
- [Video reference](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/video.md)
- [Twitter 진단](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/twitter.py)
- [Config](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/config.py)
- [Exa MCP](https://exa.ai/docs/reference/exa-mcp)
