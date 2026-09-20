---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Agent Reach — Getting started

[[tech/devtools/agent-reach/README|목차]] · [[tech/devtools/agent-reach/04-learning/02-deep-dive|다음: Deep dive]]

## 목표와 전제

공개 URL 하나를 읽고 **환경 진단 결과와 실제 콘텐츠 결과를 구분**하는 것이 첫 목표다. 아래는 2026-09-09의 `main` 문서를 기준으로 작성한 실습안이며, 이 노트 작성 중 설치·인증·호출을 실행한 것은 아니다.

- Python 3.10 이상과 `pipx`가 준비된 개인 실습 환경을 사용한다.
- CLI를 호출할 수 있는 Agent 또는 terminal에서 진행한다.
- 설치 파일·credentials·임시 출력은 공개 vault 밖에 둔다.
- 시작할 때는 Web 한 경로만 확인하고, 필요한 플랫폼을 점진적으로 추가한다.

## 1. 설치 대상 구분

| 목적 | 설치 대상 | 주의점 |
|---|---|---|
| 배포 버전 재현 | v1.5.0 tag | 현재 `main` 전용 옵션을 그대로 적용하지 않음 |
| 이 노트의 현재 동작 학습 | `main` 또는 해당 commit SHA | 이동하는 branch이므로 날짜·SHA를 함께 기록 |

다음 두 명령은 **대안**이다. 한 가지를 선택한다. 패키지 설치는 환경에 파일과 의존성을 추가한다.

```bash
# 배포 버전 학습용
pipx install https://github.com/Panniantong/Agent-Reach/archive/refs/tags/v1.5.0.zip

# 현재 main 학습용: 실행 시점에 내용이 달라질 수 있음
pipx install https://github.com/Panniantong/Agent-Reach/archive/main.zip
```

재현성이 중요하면 archive URL의 `main` 대신 조사한 commit SHA를 사용한다. package version 문자열만으로 release와 이후 `main`을 구분할 수 있다고 가정하지 않는다. 설치 후에는 항상 해당 버전의 도움말부터 읽는다.

```bash
agent-reach --help
agent-reach install --help
agent-reach doctor --help
```

## 2. 현재 main에서 점검과 설치 나누기

```bash
# 현재 main: 기본은 의존성·설정 점검
agent-reach install --env=auto

# 현재 main: system 모드가 수행할 작업 미리 보기
agent-reach install --env=auto --dry-run
```

기본 `install`의 check-only 설명은 **Agent Reach 패키지가 설치된 뒤 실행하는 이 명령**에 관한 것이다. 앞 단계 `pipx install`까지 read-only라는 뜻은 아니다. 현재 `--safe`는 check-only 동작의 호환 옵션이다.

아래 명령은 필요한 변경을 확인한 뒤 개인 실습 환경에서 선택적으로 수행한다. `--system`은 외부 도구 설치·설정 쓰기를 허용하는 현재 `main`의 명시적 옵션이다.

```bash
agent-reach install --env=auto --system
```

근거: [현재 설치 가이드](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md). v1.5.0 재현 환경에서는 tag의 문서와 도움말을 따른다.

## 3. 진단 읽기

```bash
agent-reach doctor
agent-reach doctor --json
```

| 필드 | 읽는 방법 |
|---|---|
| `status` | `ok`, `warn`, `off`, `error` 등 channel 진단 상태 |
| `message` | 설치·설정·실시간 검증 제한을 설명하는 핵심 근거 |
| `tier` | 설정 난이도·요구 조건 분류이며 성공률 점수가 아님 |
| `backends` | 선언된 backend 후보 목록 |
| `active_backend` | 진단에서 선택된 backend; `null`의 이유는 message 확인 |

Twitter는 도구와 credentials가 있어도 live 인증 검증을 생략해 `warn`일 수 있다. 반대로 `ok`라도 특정 URL의 내용이 반환되는지는 따로 확인한다. [doctor](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py), [Twitter 구현](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/twitter.py)

## 4. 공개 URL 하나 읽기

Web channel의 실제 읽기 경로를 직접 호출한다. 아래 URL은 공개 예제 페이지다. 요청은 Jina Reader로 전달된다.

```bash
curl --fail --show-error --location   'https://r.jina.ai/https://example.com'
```

성공 여부는 다음 순서로 판단한다.

1. HTTP 오류나 연결 실패가 없는지 확인한다.
2. 출력이 비어 있지 않은지 확인한다.
3. 예제 페이지의 본문이 있는지 확인한다. 로그인·차단 안내문만 있으면 본문 읽기 성공으로 기록하지 않는다.
4. 대상 URL, 사용 backend, 확인 시각, 관찰한 결과를 남긴다.

이 명령의 성공은 Jina 경로의 한 번의 검증이다. 다른 소셜 channel이나 Agent의 skill 로딩까지 검증한 결과는 아니다.

## 5. Agent에서 연결 확인

Agent가 자신의 skill 탐색 경로에서 Agent Reach의 `SKILL.md`를 발견하는지 확인한다. 공식 설치 문서의 특정 host 경로가 모든 Agent에 공통인 것은 아니다.

```text
Agent Reach skill을 사용해 https://example.com 의 본문을 읽어라.
실제 사용한 upstream 도구와 비어 있지 않은 본문 확보 여부를 보고하라.
결과에 없는 내용을 보충하지 말고, 실패하면 오류와 미검증 범위를 기록하라.
```

## 완료 기준

- [ ] 설치한 tag 또는 commit과 upstream 버전을 기록했다.
- [ ] `doctor`의 status·message·active_backend를 함께 해석했다.
- [ ] 실제 공개 URL에서 관련 본문을 확인했다.
- [ ] Agent를 사용하는 경우 skill 발견과 직접 도구 호출을 확인했다.
- [ ] 공개 노트에 credentials나 개인 응답 원문이 포함되지 않았다.

## Sources

- [Install guide](https://github.com/Panniantong/Agent-Reach/blob/main/docs/install.md)
- [Python 요구 버전·패키지](https://github.com/Panniantong/Agent-Reach/blob/main/pyproject.toml)
- [v1.5.0 release](https://github.com/Panniantong/Agent-Reach/releases/tag/v1.5.0)
- [SKILL.md](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/skill/SKILL.md)
- [doctor](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/doctor.py)
- [Twitter channel](https://github.com/Panniantong/Agent-Reach/blob/main/agent_reach/channels/twitter.py)
