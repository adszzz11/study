---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage Getting Started

> [[../README|목차로 돌아가기]] · [[../03-references|이전: References]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

이 실습의 목표는 production deployment가 아니라 다음 end-to-end loop를 확인하는 것이다.

1. local Backstage app 실행
2. `catalog-info.yaml` entity 등록
3. owner와 relation 확인
4. TechDocs annotation과 plugin surface 탐색
5. production 전환 시 바꿔야 할 항목 식별

## Prerequisites

공식 standalone guide의 현재 요구사항을 먼저 확인한다.

- Unix-like environment: Linux, macOS 또는 WSL
- 생성 app의 `package.json` `engines.node`에 맞는 Node.js Active LTS
- Yarn/npm 기본 사용법
- GNU-like build tools
- 최소 6 GB memory와 충분한 disk
- Git과 접근 가능한 SCM account

> [!warning] Version pinning
> `@latest`는 학습 시작에는 편하지만 재현 가능한 team setup에는 부적합하다. 조사 시점 stable은 `v1.53.1`이나 `create-app` package version과 umbrella release version은 같은 개념이 아니다. 실제 실행 전 Releases와 공식 guide를 확인하고 생성 명령/version을 작업 기록에 남긴다.

## 1. App 생성과 실행

```bash
npx @backstage/create-app@latest
# prompt 예: my-backstage-app

cd my-backstage-app
yarn start
```

생성되는 핵심 구조는 다음과 같다.

```text
my-backstage-app/
├── app-config.yaml
├── app-config.local.yaml
├── catalog-info.yaml
├── package.json
└── packages/
    ├── app/       # React frontend
    └── backend/   # Node.js backend
```

브라우저에서 기본 app을 열고 Catalog, Create, Docs, Search 메뉴가 동작하는지 확인한다. local demo는 in-memory SQLite와 demo content를 사용할 수 있으며 production-ready 상태가 아니다.

### 첫 검증

- [ ] frontend와 backend가 error 없이 시작한다.
- [ ] Catalog 목록과 entity page를 열 수 있다.
- [ ] backend initialization log에서 core plugins를 확인한다.
- [ ] generated app의 Node/Yarn version을 기록한다.
- [ ] secret이 들어갈 `app-config.local.yaml`의 Git 추적 여부를 확인한다.

## 2. 첫 Catalog entity 작성

학습용 repository root에 `catalog-info.yaml`을 둔다.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: hello-service
  title: Hello Service
  description: Backstage 학습용 HTTP service
  tags:
    - typescript
  annotations:
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: experimental
  owner: group:default/platform
  system: learning-platform
  providesApis:
    - hello-api
```

같은 파일에 YAML document separator로 관련 entity를 추가할 수 있다.

```yaml
---
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: hello-api
  description: Hello Service의 HTTP API
spec:
  type: openapi
  lifecycle: experimental
  owner: group:default/platform
  system: learning-platform
  definition: |
    openapi: 3.0.0
    info:
      title: Hello API
      version: 1.0.0
    paths: {}
```

### Reference 읽기

- canonical: `component:default/hello-service`
- kind 생략이 허용되는 field의 예: `hello-service`
- namespace 생략: `component:hello-service`
- fully qualified owner: `group:default/platform`

축약형은 문맥에 따라 default kind가 다를 수 있다. shared automation과 debugging에서는 fully qualified reference가 더 명확하다.

## 3. Entity 등록

방법 A: UI의 Catalog import flow에 raw file URL을 입력한다.

방법 B: `app-config.yaml`에 location을 선언한다.

```yaml
catalog:
  locations:
    - type: url
      target: https://github.com/acme/hello-service/blob/main/catalog-info.yaml
```

private repository는 해당 SCM integration과 credential이 필요하다.

```yaml
integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}
```

```bash
export GITHUB_TOKEN='<short-lived-token>'
yarn start
```

> [!danger] Secret 관리
> token을 `app-config.yaml`, entity annotation, template skeleton 또는 Git history에 넣지 않는다. local environment variable 또는 조직의 secret manager를 사용하고 최소 scope를 부여한다.

### Entity 확인

- [ ] `hello-service`가 Catalog에 표시된다.
- [ ] owner reference가 실제 `Group` entity로 resolve된다.
- [ ] `providesApis` relation으로 `hello-api`가 연결된다.
- [ ] source location과 edit link가 올바르다.
- [ ] YAML 오류 시 Catalog processing error를 읽을 수 있다.

owner가 unresolved라면 먼저 조직 data를 ingestion하거나 학습용 `Group` entity를 만든다.

```yaml
apiVersion: backstage.io/v1alpha1
kind: Group
metadata:
  name: platform
spec:
  type: team
  children: []
```

## 4. TechDocs 최소 구성

repository에 다음 파일을 추가한다.

```text
hello-service/
├── catalog-info.yaml
├── mkdocs.yml
└── docs/
    └── index.md
```

```yaml
# mkdocs.yml
site_name: Hello Service
nav:
  - Home: index.md
plugins:
  - techdocs-core
```

```markdown
# Hello Service

## Ownership

Platform Team이 소유한다.

## Runbook

1. health endpoint를 확인한다.
2. 최근 deployment와 error dashboard를 확인한다.
```

entity의 `backstage.io/techdocs-ref: dir:.` annotation과 Docs tab을 확인한다. local build 성공은 production architecture가 완성되었다는 뜻이 아니다. production에서는 [[02-deep-dive#TechDocs production path|CI build + object storage]]로 전환한다.

## 5. 첫 Template 읽기

기본 app의 `/create`에서 template을 열고 다음 구조를 찾는다.

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: service-template
  title: Create a service
spec:
  owner: group:default/platform
  type: service
  parameters:
    - title: Service metadata
      required: [name, owner]
      properties:
        name:
          title: Name
          type: string
        owner:
          title: Owner
          type: string
  steps:
    - id: fetch
      name: Fetch skeleton
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
  output:
    text:
      - title: Result
        content: Created `${{ parameters.name }}`
```

실행 전에 installed action 목록, input schema, permission과 side effect를 확인한다. custom action ID는 expression parsing 문제를 피하도록 camelCase를 사용한다.

## 6. Production gap 기록

| Local evaluation | Production에서 필요한 결정 |
|---|---|
| SQLite/demo data | managed PostgreSQL, backup, migration |
| guest/demo sign-in | auth provider, resolver, session과 identity |
| broad/default access | permission policy와 plugin enforcement |
| manual Catalog location | SCM discovery/provider, ownership governance |
| local TechDocs build/storage | CI publisher와 object storage |
| single process | Docker/Kubernetes, replicas, health, autoscaling |
| local secret/env | secret manager, rotation, least privilege |
| default logs | metrics, traces, structured logs와 alert |
| `latest` install | pinned versions와 upgrade cadence |

## 완료 기준

- [ ] app을 재시작해도 실습 절차를 재현할 수 있다.
- [ ] Component, API와 Group relation을 설명할 수 있다.
- [ ] ingestion error를 Catalog UI/log에서 찾을 수 있다.
- [ ] local default와 production recommendation의 차이를 설명할 수 있다.
- [ ] 다음 pilot에서 검증할 user journey 하나를 정의했다.

## Sources

- [Standalone Installation](https://backstage.io/docs/getting-started/)
- [Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Descriptor Format](https://backstage.io/docs/features/software-catalog/descriptor-format/)
- [Entity References](https://backstage.io/docs/features/software-catalog/references/)
- [GitHub Integration](https://backstage.io/docs/integrations/github/locations/)
- [TechDocs](https://backstage.io/docs/features/techdocs/)
- [Software Templates](https://backstage.io/docs/features/software-templates/)
- [Writing Templates](https://backstage.io/docs/features/software-templates/writing-templates/)

