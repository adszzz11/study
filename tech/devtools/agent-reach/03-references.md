---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach — References와 근거 읽기

[[tech/devtools/agent-reach/README|목차]] · [[tech/devtools/agent-reach/04-learning/01-getting-started|다음: Getting started]]

## 읽는 순서

| 순서 | 자료 | 확인할 질문 |
|---|---|---|
| 1 | [English README](https://github.com/Panniantong/Agent-Reach/blob/main/docs/README_en.md) | 해결하려는 문제와 지원 범위는 무엇인가? |
| 2 | [v1.5.0 release](https://github.com/Panniantong/Agent-Reach/releases/tag/v1.5.0) | 배포 시점에 무엇이 바뀌었는가? |
| 3 | [Install guide](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md) | 현재 설치의 변경 범위와 인증 전제는 무엇인가? |
| 4 | [SKILL.md](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/SKILL.md) | Agent는 실제로 어떤 도구를 호출하는가? |
| 5 | [Social](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/social.md) / [Video](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/references/video.md) | 플랫폼별 명령과 fallback 종료 조건은 무엇인가? |
| 6 | [Channel](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/base.py) / [doctor](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py) | 진단 결과가 실제로 보증하는 범위는 어디까지인가? |

## 근거의 성격

- **Release**: 배포 당시의 변경 설명이다. v1.5.0의 13개 channel 및 테스트 성공 보고를 이후 `main` 전체에 확대하지 않는다.
- **`main` 문서·소스**: 현재 개발 상태를 설명하지만 URL 내용은 바뀔 수 있다. 재현 실습 때는 commit SHA permalink와 upstream 버전을 함께 기록한다.
- **Issue**: 특정 환경에서 보고된 현상이다. 한 건의 보고를 모든 사용자에게 발생하는 결함으로 일반화하거나 이미 해결됐다고 단정하지 않는다.
- **이 노트**: 2026-09-09 dossier와 공식 자료에 근거한 study다. 명령 예시는 실습안이며 실행 성공 기록이 아니다.

## 확인해야 할 문서 불일치

| 항목 | 자료 간 차이 | 기록 원칙 |
|---|---|---|
| 출시 연도 | CHANGELOG의 v1.1.0 날짜와 다른 release 날짜 기록의 일관성 문제 | 최초 출시 연도 확정 보류 |
| 지원 수 | v1.5.0 release는 13개, 현재 registry는 15개 | 버전·집계 기준 병기 |
| 설치 | 예전 release 예시와 현재 check-only 기본값 차이 | 설치한 revision의 `install --help` 확인 |
| 설정 파일 | 설치 문서 표의 `config.json` 예시와 실제 `config.yaml` | 현재 Config 구현 기준 |
| 진단 | backend probe와 실제 콘텐츠 요청의 범위 차이 | target URL 호출을 별도 확인 |

## 이슈를 학습에 사용하는 방법

- [#580 — 진단 문서 관련 이슈](https://github.com/Panniantong/Agent-Reach/issues/580): 2026년 8월의 진단 설명과 실제 동작 간 차이를 읽는 자료다.
- [#623 — Exa 진단 오류 보고](https://github.com/Panniantong/Agent-Reach/issues/623): Exa MCP가 미설정인데 `ok`로 표시됐다는 사용자 보고다. `doctor`와 실제 호출을 함께 기록해야 하는 사례로 활용한다.
- [Twitter 구현](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/twitter.py): 현재 진단이 자동 Cookie 접근을 피하려 실시간 인증을 생략하는 이유를 확인한다.

실습 기록에는 다음 정보를 남긴다. 값은 실습 후 채우며, 민감한 원문 대신 정리된 관찰만 공개한다.

```text
checked_at:
agent_reach_revision:
upstream_versions:
platform_and_task:
public_target_url:
doctor_status_and_message:
active_backend:
actual_command:
nonempty_and_relevant_result:
limitations:
```

## Sources

- [공식 repository](https://github.com/Panniantong/Agent-Reach)
- [Releases](https://github.com/Panniantong/Agent-Reach/releases)
- [CHANGELOG](https://github.com/Panniantong/Agent-Reach/blob/main/CHANGELOG.md)
- [Registry](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/__init__.py)
- [Config](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/config.py)
- [Install guide](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md)
- [Issue #580](https://github.com/Panniantong/Agent-Reach/issues/580) · [Issue #623](https://github.com/Panniantong/Agent-Reach/issues/623)
- [Exa MCP의 무료 사용·rate limit 안내](https://exa.ai/docs/reference/exa-mcp)
