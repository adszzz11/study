---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 최소 연결 실습

## 목표와 전제

읽기 전용 backend 하나를 등록하고 Virtual Server를 통해 tool 목록과 호출 결과를 확인한다. 아래는 실습 절차 설계이며 실행 완료 기록이 아니다. 설치 명령·인증 endpoint·payload 전체는 선택 버전의 원문으로 확인한다.

- Python ≥ 3.11이 필요하다.
- 제공 자료는 production arm64 미지원을 명시하고 Apple Silicon에 Rosetta 또는 PyPI 설치를 안내한다. 현재 버전의 지원 상태를 먼저 확인한다.
- PyPI·OCI·Kubernetes 중 하나를 선택한다. 첫 실습에서는 backend와 Gateway를 최소 구성으로 유지한다.
- Compose는 기본적으로 GHCR pre-built image를 사용한다. Gateway image local build는 CI가 생성하는 hermetic wheel closure가 필요하다고 설명된다.

## 1. 버전과 설정 고정

선택 release/tag 또는 commit SHA, OS/architecture, Python 버전, 배포 방법을 기록한다. 다음은 shell에서 필수 secret을 준비하는 예시이며 Gateway를 설치하거나 실행하지 않는다.

```sh
# 각 명령은 독립적인 random secret을 생성한다. 값을 노트·Git에 저장하지 않는다.
export JWT_SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
export AUTH_ENCRYPTION_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
```

실제 secret 형식·길이는 선택 버전 문서에서 확인한다. Container를 사용할 경우 shell 변수 설정만으로 전달된다고 가정하지 말고 해당 실행 방식의 환경변수 주입을 설정한다. 지속 운영에서는 secret을 안전하게 보관하고 재시작 시 유지한다.

## 2. Gateway와 backend 준비

1. 원문 README의 선택 배포 절차로 Gateway를 시작한다.
2. Client → Gateway 인증을 구성한다.
3. 읽기 전용 test MCP server 또는 REST endpoint 하나를 준비한다.
4. Gateway → upstream credential을 별도로 구성한다.
5. Tool catalog에서 등록 결과, tool ID, schema와 설명을 확인한다.

실제 credential, 개인 데이터, 변경 작업이 가능한 production tool은 첫 실습에서 사용하지 않는다.

## 3. Virtual Server 구성

Catalog에서 확인한 실제 tool ID를 `associated_tools`에 선택하고 server를 만든다. 다음은 개념 메모로, 완전한 API request body가 아니다.

```text
associated_tools: [<catalog에서 확인한 tool ID>]
client endpoint: <gateway-base-url>/servers/<실제 server UUID>/mcp
```

Client의 transport와 MCP protocol version 호환성을 각각 확인한 뒤 접속한다. UUID나 tool ID를 임의로 만들어 넣지 않는다.

## 4. 완료 기준

- [ ] 의도한 tool만 client 목록에 보인다.
- [ ] 정상 입력의 결과가 backend 직접 호출과 의미상 일치한다.
- [ ] 잘못된 입력은 예상한 오류로 처리된다.
- [ ] 인증 없는 요청과 잘못된 credential의 동작을 기록했다.
- [ ] Gateway 및 upstream 로그로 요청 성공·실패 위치를 확인했다.
- [ ] 설정과 결과를 secret 없이 기록했다.

Tool 목록을 제한한 결과만으로 권한 격리가 검증되었다고 결론 내리지 않는다.

## 이어 읽기

[[tech/ai/mcp-context-forge-fe0ea4a7/04-learning/02-deep-dive|Deep Dive]] · [[tech/ai/mcp-context-forge-fe0ea4a7/cheatsheet|Cheatsheet]] · [[tech/ai/mcp-context-forge-fe0ea4a7/README|학습경로]]

## Sources

- https://github.com/IBM/mcp-context-forge — 제공된 repository 발췌 dossier의 원 출처.
- https://github.com/IBM/mcp-context-forge/blob/main/README.md — 설치·기능·배포 설명의 확인 지점. `main`은 변경될 수 있다.

> 근거는 제공된 dossier다. 저장소의 현재 상태, 명령 실행, 성능 및 보안은 직접 검증하지 않았다. 버전·수치·지원 범위는 발췌 시점의 프로젝트 설명이다.
