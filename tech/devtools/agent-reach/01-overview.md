---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach — What / Why / 특징

[[tech/devtools/agent-reach/README|목차]] · [[tech/devtools/agent-reach/02-ecosystem|다음: Ecosystem]]

## What

Agent Reach는 AI Agent의 외부 콘텐츠 접근을 돕는 **capability layer**다. 도구 설치 여부와 설정 상태를 확인하고, 각 플랫폼에 적합한 backend 후보와 사용 절차를 제공한다. 본체는 Python 3.10 이상을 요구하며 MIT license로 배포된다. [패키지 정의](https://github.com/Panniantong/Agent-Reach/blob/main/pyproject.toml)

## Why

일반 웹 검색으로 페이지를 찾는 것과 Reddit 댓글, X 대화, Bilibili 자막, XiaoHongShu 리뷰를 읽는 것은 다른 문제다. 플랫폼별 인증·출력·browser session과 upstream 유지보수 상태를 따로 관리해야 한다.

Agent Reach의 가치는 새로운 검색 알고리즘보다 **Agent가 어떤 도구를 어떻게 써야 하는지에 관한 운영 지식의 패키징**에 있다. 설치와 상태 진단을 묶고, 실행 지침을 skill로 제공해 반복적인 integration 작업을 줄인다. [공식 개요](https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md)

## 실행 구조

```text
사용자 요청
    ↓
AI Agent ← SKILL.md / references: 명령과 fallback 절차
    ├─ Agent Reach CLI
    │    ├─ install / configure
    │    ├─ Channel registry
    │    └─ doctor → status / backends / active_backend
    └─ upstream 직접 호출
         ├─ curl → Jina Reader
         ├─ mcporter → Exa / 플랫폼 MCP
         ├─ gh / twitter / bili / yt-dlp
         └─ OpenCLI → browser session → 플랫폼
```

`Channel.can_handle()`는 URL 소속을 판별하고, `check()`는 가용성을 확인한다. `backends`는 순서가 있는 후보 목록, `active_backend`는 진단에서 선택된 backend다. `<channel>_backend` 설정이나 대응 환경변수는 선호 후보를 앞에 배치한다. 이 구조는 모든 데이터 요청을 중계하는 중앙 proxy를 뜻하지 않는다. [Channel 소스](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/base.py)

## 플랫폼과 backend

아래는 **2026-09-09의 `main` 기준** 요약이다. registry에는 Web·Exa Search·RSS를 포함해 15개 channel이 있다. v1.5.0 release에 적힌 13개와 기준을 섞지 않는다.

| 대상 | 주요 backend | 조건·범위 |
|---|---|---|
| Web | Jina Reader | URL 본문을 LLM 친화적인 텍스트로 변환 |
| Exa Search | Exa via mcporter | MCP 설정 필요, 무료 경로도 rate limit 존재 |
| GitHub | gh | CLI 인증과 명령별 권한 범위를 따름 |
| RSS | feedparser | feed 접근 가능 여부와 형식에 의존 |
| V2EX | 공개 API | 공개 API가 제공하는 범위 |
| YouTube | yt-dlp → OpenCLI → transcription | metadata 성공과 자막 성공은 별개 |
| Bilibili | bili-cli / OpenCLI | 검색·상세는 bili, 자막은 OpenCLI |
| X/Twitter | twitter-cli → OpenCLI | 명시적 Cookie 또는 browser session 필요 |
| Reddit | OpenCLI → rdt-cli | 프로젝트의 현재 경로는 로그인 필요 |
| XiaoHongShu | OpenCLI → xiaohongshu-mcp → legacy CLI | 기존 session 또는 명시적으로 제공한 Cookie |
| Facebook | OpenCLI | 로그인한 browser, 작업별 범위 확인 |
| Instagram | OpenCLI | 로그인한 browser; search는 사용자 검색 |
| LinkedIn | MCP / Jina | 작업에 따라 로그인 및 추가 설정 |
| Xueqiu | Cookie 기반 도구 | 인증 상태와 플랫폼 제약에 의존 |
| Xiaoyuzhou | 전사 도구 | API key 및 오디오 처리 도구 필요 |

근거: [registry](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/__init__.py), [플랫폼 문서](https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md).

## 버전 변화 읽기

| 시점 | 확인된 변화 | 학습 시 주의점 |
|---|---|---|
| CHANGELOG의 2025 기록 | v1.1.0 날짜가 `2025-02-25` | v1.3.0 날짜도 release 기록과 달라 최초 출시 연도를 확정하지 않음 |
| v1.4.2 | Douyin·Weibo·WeChat 제거, `transcribe`, `doctor --json` 추가 | 예전 지원 목록을 현재 목록으로 사용하지 않음 |
| v1.5.0, 2026-06-11 | ordered backends, OpenCLI, 실제 명령 probe, `active_backend` | release의 테스트 결과는 프로젝트 측 보고이며 이 노트의 실측이 아님 |
| 이후 `main` | check-only 설치, 인증 진단 제한 | release 명령 예시와 현재 설치 옵션을 구분 |

Bilibili의 yt-dlp 경로는 412 차단을 이유로 bili-cli/OpenCLI로 바뀌었다는 release 설명이 있다. 이를 모든 환경에서 영구적으로 같은 결과가 나온다는 측정치로 일반화하지 않는다.

## 비용과 데이터 경계

- MIT license와 전체 운영비 0원은 별개다. Exa의 무료 MCP 경로에는 rate limit이 있고, 전사에는 key와 provider별 비용 조건이 있다.
- 현재 구현의 설정 경로는 `~/.agent-reach/config.yaml`이다. 설치 문서 일부의 `config.json` 예시보다 구현을 기준으로 본다.
- 로컬 설정 저장과 외부 데이터 처리는 구분한다. Jina에는 읽을 URL, Exa에는 검색 요청, transcription provider에는 처리할 오디오가 전달될 수 있다.
- 공개 vault에는 Cookie·token·API key·개인 session 정보와 비공개 응답 원문을 넣지 않는다. 실습 결과는 출처와 비밀정보를 제거한 요약으로 남긴다.

## Sources

- [README](https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md)
- [Package / license](https://github.com/Panniantong/Agent-Reach/blob/main/pyproject.toml)
- [Channel interface](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/base.py)
- [Registry](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/__init__.py)
- [CHANGELOG](https://github.com/Panniantong/Agent-Reach/blob/main/CHANGELOG.md)
- [v1.4.2](https://github.com/Panniantong/Agent-Reach/releases/tag/v1.4.2) · [v1.5.0](https://github.com/Panniantong/Agent-Reach/releases/tag/v1.5.0)
- [Config 구현](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/config.py)
- [Exa MCP](https://exa.ai/docs/reference/exa-mcp)
- [Video reference](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/video.md)
