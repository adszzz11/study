---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage References

> [[README|목차로 돌아가기]] · [[02-ecosystem|이전: Ecosystem]] · [[04-learning/01-getting-started|다음: Getting Started]]

## 읽는 순서

### 1. 방향과 mental model

| 자료 | 확인할 내용 |
|---|---|
| [What is Backstage?](https://backstage.io/docs/overview/what-is-backstage/) | portal/framework의 목적과 core features |
| [Technical Overview](https://backstage.io/docs/overview/technical-overview/) | Catalog, Templates, TechDocs, Search, plugins |
| [Architecture Overview](https://backstage.io/docs/overview/architecture-overview/) | frontend/backend/data 경계 |
| [CNCF Project Page](https://www.cncf.io/projects/backstage/) | governance와 CNCF maturity |

### 2. 첫 app과 configuration

| 자료 | 확인할 내용 |
|---|---|
| [Standalone Installation](https://backstage.io/docs/getting-started/) | `create-app`, prerequisites, local SQLite demo |
| [Configuration](https://backstage.io/docs/conf/) | `app-config*.yaml`, visibility, environment substitution |
| [Configuring Plugins](https://backstage.io/docs/getting-started/configure-app-with-plugins/) | new frontend system의 plugin 설치 |
| [Deployment](https://backstage.io/docs/golden-path/deployment/) | Docker, Kubernetes와 production 고려사항 |

### 3. Software Catalog

| 자료 | 확인할 내용 |
|---|---|
| [Catalog Overview](https://backstage.io/docs/features/software-catalog/) | metadata와 ownership model |
| [Descriptor Format](https://backstage.io/docs/features/software-catalog/descriptor-format/) | entity envelope과 kind별 `spec` |
| [System Model](https://backstage.io/docs/features/software-catalog/system-model/) | Domain/System/Component/API/Resource 관계 |
| [Entity References](https://backstage.io/docs/features/software-catalog/references/) | `kind:namespace/name`과 축약형 |
| [Catalog Configuration](https://backstage.io/docs/features/software-catalog/configuration/) | locations, rules와 processing |
| [Catalog API](https://backstage.io/docs/features/software-catalog/software-catalog-api/) | entity query와 client integration |
| [External Integrations](https://backstage.io/docs/integrations/) | GitHub/GitLab 등 SCM 연결 |

### 4. Self-service와 documentation

| 자료 | 확인할 내용 |
|---|---|
| [Software Templates](https://backstage.io/docs/features/software-templates/) | Scaffolder 개념과 `/create` |
| [Writing Templates](https://backstage.io/docs/features/software-templates/writing-templates/) | parameters, steps, output |
| [Built-in Actions](https://backstage.io/docs/features/software-templates/builtin-actions/) | 설치된 action ID와 input |
| [Writing Custom Actions](https://backstage.io/docs/features/software-templates/writing-custom-actions/) | 외부 시스템 연동 action |
| [TechDocs Overview](https://backstage.io/docs/features/techdocs/) | docs-like-code 흐름 |
| [TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture/) | basic과 recommended deployment |

### 5. Extension과 운영

| 자료 | 확인할 내용 |
|---|---|
| [Backend System](https://backstage.io/docs/backend-system/) | plugins, modules, services, extension points |
| [Frontend System](https://backstage.io/docs/frontend-system/) | extensions와 app composition |
| [Search](https://backstage.io/docs/features/search/) | searchable content와 engine |
| [Search Architecture](https://backstage.io/docs/features/search/architecture/) | collator, index와 query 구조 |
| [Authentication](https://backstage.io/docs/auth/) | auth provider와 identity |
| [Permissions Overview](https://backstage.io/docs/permissions/overview/) | policy, decision, enforcement |
| [Observability](https://backstage.io/docs/observability/) | logs, metrics와 tracing |

### 6. Release와 security

| 자료 | 확인할 내용 |
|---|---|
| [GitHub Releases](https://github.com/backstage/backstage/releases) | stable/next release와 changelog |
| [Versioning Policy](https://backstage.io/docs/overview/versioning-policy/) | umbrella와 package version 차이, skew |
| [Backstage Upgrade Helper](https://backstage.github.io/upgrade-helper/) | 생성 app의 version별 변경 diff |
| [Security Overview](https://backstage.io/docs/overview/security/) | integrator의 security responsibility |
| [Threat Model](https://backstage.io/docs/overview/threat-model/) | trust boundary와 주요 위협 |
| [GitHub Security Advisories](https://github.com/backstage/backstage/security/advisories) | 공개 vulnerability와 조치 |

## Version snapshot

| 항목 | 조사 기준 상태 |
|---|---|
| 조사일 | 2026-07-30 |
| Latest stable | `v1.53.1` (2026-07-29) |
| Next line | `v1.54.0-next.*` |
| Main cadence | 월간 |
| Next cadence | 주간 |
| Umbrella SemVer | strict SemVer 아님; minor에도 breaking change 가능 |
| CNCF stage | Incubating |

> [!tip] 기록 원칙
> 이 표는 시점 snapshot이다. 실제 install/upgrade 전에는 Releases, Versioning Policy, 생성 app의 `package.json` engines와 Upgrade Helper를 다시 확인한다.

## Community 탐색

- [Plugin Marketplace](https://backstage.io/plugins/) — plugin 후보 탐색
- [Backstage Community](https://backstage.io/community/) — community channel과 events
- [GitHub Discussions](https://github.com/backstage/backstage/discussions) — 설계 질문과 사례
- [Backstage adopters](https://github.com/backstage/backstage/blob/master/ADOPTERS.md) — 공개 adopter 목록

Community plugin은 최소한 다음을 평가한다.

- 최근 release/commit과 maintainer activity
- 사용하는 frontend system과 backend system
- Backstage target release compatibility
- permission framework integration
- secret 취급과 외부 API scope
- database migration과 operational footprint
- license와 vulnerability response

## Source 검증 checklist

- [ ] 블로그보다 공식 docs와 repository changelog를 우선한다.
- [ ] version/date가 있는 주장은 release page에서 확인한다.
- [ ] old frontend/backend 문서와 current system 문서를 구분한다.
- [ ] example config의 secret을 그대로 commit하지 않는다.
- [ ] plugin README의 compatible package range를 확인한다.
- [ ] architecture recommendation과 local demo default를 혼동하지 않는다.

## Sources

- [Backstage Documentation](https://backstage.io/docs/)
- [Backstage GitHub](https://github.com/backstage/backstage)
- [Backstage GitHub Releases](https://github.com/backstage/backstage/releases)
- [Release & Versioning Policy](https://backstage.io/docs/overview/versioning-policy/)
- [Backstage Upgrade Helper](https://backstage.github.io/upgrade-helper/)
- [CNCF Backstage Project Page](https://www.cncf.io/projects/backstage/)

