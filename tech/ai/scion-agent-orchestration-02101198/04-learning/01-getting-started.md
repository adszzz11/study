---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion 시작하기

## 목표와 준비

목표는 Workstation을 올리고 연습용 repository에서 단일 agent의 작업 결과를 사람이 확인하는 것이다. 처음부터 병렬 팀을 만들지 않는다.

- Docker, Podman 또는 Apple Container 등 사용할 runtime의 설치·가동 상태를 확인한다.
- 사용할 harness·model과 필요한 인증 방식을 선택한다. Credentials는 공개 노트에 기록하지 않는다.
- 작고 되돌릴 수 있는 연습용 Git repository를 준비한다.
- 설치할 release와 해당 문서의 요구사항을 확인한다. Source build는 설치 가이드의 Go·Node.js 조건에 따른다.

## 1. 설치와 Workstation 시작

다음은 작성 시 README에 안내된 Homebrew 경로다. Community tap과 기본 image registry를 확인하고 사용한다.

```sh
brew tap homebrew-scion/scion
brew install homebrew-scion/scion/scion
scion server start
```

Onboarding은 `http://127.0.0.1:8080/onboarding`에서 runtime 감지, identity, container image, 첫 workspace 구성을 안내한다. README는 이 배포가 `ghcr.io/homebrew-scion`을 기본 image registry로 사용하고 Telegram broker plugin도 설치한다고 설명한다.

Source build를 택한다면 설치 가이드를 먼저 읽는다. README의 `make all`은 web frontend를 빌드해 binary에 포함하는 경로다.

## 2. Project 초기화와 첫 Agent

아래 `my-project`는 준비한 연습용 repository 경로로 바꾼다. 명령은 사용자가 실행할 실습 예제이며 이 노트에서 실행한 결과가 아니다.

```sh
cd my-project
scion init
scion start my-agent "저장소 구조를 읽고 개선 제안 3개를 보고하라. 소스 파일은 수정하지 마라."
```

Onboarding은 machine initialization을 처리하지만 repository마다 `scion init`은 필요하다. 수동 machine 설정을 사용하더라도 Hub 실행을 생략하지 않는다.

## 3. 결과 확인

- Web UI와 logs에서 agent 시작·진행·완료 또는 도움 요청 상태를 확인한다.
- 지원되는 interactive harness라면 `scion attach`를 사용한다. Agent 선택 인자 등 정확한 문법은 설치 버전의 help에서 확인한다.
- 최종 보고가 repository 내용에 근거하는지 확인하고 `git diff`로 의도하지 않은 변경이 없는지 살핀다.
- 종료·정리 명령도 해당 버전의 CLI help에서 확인하고 실습 agent와 runtime 자원을 정리한다.

## 완료 기준

- [ ] CLI → Hub → 실행 환경의 관계를 설명할 수 있다.
- [ ] 선택한 harness·runtime·인증 방식을 기록했다.
- [ ] 단일 agent 보고와 실제 repository를 대조했다.
- [ ] 실습 자원의 종료·정리 상태를 확인했다.

## 문제를 좁히는 순서

| 증상 | 먼저 확인할 항목 |
|---|---|
| Onboarding에 접속 불가 | Server 로그·로컬 주소·포트 사용 상태 |
| Agent 시작 실패 | Hub 연결·runtime 상태·image 준비·harness 인증 |
| Project 연결 문제 | 실행 디렉터리·repository별 init 여부 |
| Attach 불가 | Agent 실행 상태·interactive harness 지원·tmux session |

다음은 [[tech/ai/scion-agent-orchestration-02101198/04-learning/02-deep-dive|작은 팀의 역할과 공유 방식 설계]]다.

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
