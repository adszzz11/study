---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage

> **한 줄 정의**: Backstage는 Software Catalog를 중심으로 문서·템플릿·인프라 도구를 통합해 조직 맞춤형 Internal Developer Portal(IDP)을 만드는 Apache-2.0 open-source TypeScript framework다.

## Overview

Backstage는 Spotify가 tooling fragmentation과 service ownership 문제를 해결하기 위해 만들고 CNCF에 기부한 developer portal framework다. 기존 CI/CD, Kubernetes, observability 도구를 대체하지 않고 그 위에 discovery, metadata, documentation, self-service UX를 제공한다.

```text
SCM · Cloud · Kubernetes · 조직 directory
                    ↓ ingestion
          Software Catalog / Entity Graph
                    ↓
       Catalog UI · Search · TechDocs · Plugins
                    ↓
      Software Templates · Golden Paths · Actions
```

핵심 구성 요소는 다음과 같다.

| 영역 | 역할 |
|---|---|
| Software Catalog | service, API, resource, owner, dependency를 entity graph로 관리 |
| Software Templates | 승인된 기본값을 넣은 self-service workflow와 golden path 제공 |
| TechDocs | repository의 Markdown을 portal에서 읽는 docs-like-code |
| Search | Catalog, TechDocs와 plugin content를 통합 검색 |
| Plugins | 사내·외부 도구를 frontend/backend extension으로 통합 |
| Permission framework | plugin action과 resource에 조직의 authorization policy 적용 |

> [!warning] 제품이 아니라 framework
> OSS Backstage는 설치 즉시 완성되는 portal이 아니다. Platform Team이 product owner이자 integrator가 되어 catalog model, plugin, UX, authorization, upgrade와 운영 정책을 계속 관리해야 한다.

조사 기준은 2026-07-30이다. 최신 stable release는 `v1.53.1`(2026-07-29), 다음 release line은 `v1.54.0-next.*`다. umbrella release는 strict SemVer가 아니므로 minor upgrade에도 breaking change가 포함될 수 있다.

## Learning Path

- [ ] [[01-overview|1. What / Why / 핵심 특징]] — Backstage가 해결하는 문제와 architecture 이해
- [ ] [[02-ecosystem|2. Ecosystem과 대안 비교]] — Port, Cortex, OpsLevel, Compass, Roadie와 build-vs-buy 판단
- [ ] [[03-references|3. 공식 참고자료]] — 도입·구현·운영 단계별 문서 지도
- [ ] [[04-learning/01-getting-started|4. Getting Started]] — local app 생성, Catalog entity 등록, 첫 검증
- [ ] [[04-learning/02-deep-dive|5. Deep Dive]] — ingestion, plugins, production, security, upgrades
- [ ] [[05-projects|6. 실전 Projects]] — 작은 pilot에서 production IDP까지 단계적 설계
- [ ] [[cheatsheet|7. Cheatsheet]] — entity YAML, config, 명령과 운영 체크 빠른 참조

## When To Use

- service/API/resource가 많아 owner, lifecycle, dependency를 찾기 어렵다.
- GitHub, CI/CD, Kubernetes, observability, incident, security 도구가 여러 UI에 흩어져 있다.
- 신규 service마다 repository, pipeline, IaC, monitoring을 반복 조립한다.
- architecture, runbook, onboarding 문서를 code와 함께 관리하려 한다.
- 조직 고유 workflow와 UI가 필요하고 plugin을 개발·운영할 Platform Team이 있다.
- golden path를 강제 규정이 아니라 편리한 self-service 경험으로 제공하려 한다.

## When Not To Use

- 단순한 service directory나 정적 문서 사이트 하나면 충분하다.
- portal을 제품으로 지속 운영할 team, budget, product ownership이 없다.
- 즉시 사용할 완제품, vendor support, prebuilt integration이 최우선이다.
- Catalog metadata를 소유 team이 갱신할 유인과 governance가 없다.
- 기존 도구를 실제 orchestration/control plane으로 대체하려 한다.
- 사용자 문제 검증 없이 “portal 도입” 자체를 목표로 삼고 있다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[../../infra/kubernetes/README|Kubernetes]] — Backstage가 상태를 보여 주고 배포될 수 있는 infrastructure
- [[../git/github-repo-merge|GitHub repository merge]] — Catalog ingestion과 Scaffolder publish 대상 SCM workflow

## Sources

- [What is Backstage?](https://backstage.io/docs/overview/what-is-backstage/)
- [Backstage GitHub repository](https://github.com/backstage/backstage)
- [Backstage GitHub Releases](https://github.com/backstage/backstage/releases)
- [Release & Versioning Policy](https://backstage.io/docs/overview/versioning-policy/)
- [CNCF Backstage Project Page](https://www.cncf.io/projects/backstage/)
- [Architecture Overview](https://backstage.io/docs/overview/architecture-overview/)
- [Software Catalog](https://backstage.io/docs/features/software-catalog/)
- [Software Templates](https://backstage.io/docs/features/software-templates/)
- [TechDocs Architecture](https://backstage.io/docs/features/techdocs/architecture/)

