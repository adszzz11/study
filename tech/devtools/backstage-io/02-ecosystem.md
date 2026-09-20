---
date: 2026-07-30
tags: [tech]
type: tech-tool-study
status: draft
---

# Backstage Ecosystem과 대안 비교

> [[README|목차로 돌아가기]] · [[01-overview|이전: Overview]] · [[03-references|다음: References]]

## 비교 전제

Internal Developer Portal 시장에서는 “기능 목록”보다 운영 모델이 더 큰 차이를 만든다.

- Backstage: 조직이 조립하고 운영하는 open-source framework
- Managed Backstage: Backstage 생태계를 유지하면서 hosting/operation 부담을 줄이는 방식
- Commercial IDP: vendor가 opinionated product와 integration을 제공하는 방식
- 조합형 stack: service catalog, docs, workflow 도구를 별도로 연결하는 방식

제품 기능과 가격은 자주 바뀌므로 실제 선정 시 최신 vendor documentation과 proof of concept로 재검증한다.

## 주요 선택지

| 선택지 | 형태 | 강점 | 주의점 | 잘 맞는 상황 |
|---|---|---|---|---|
| Backstage OSS | Open-source framework | 높은 customization, 큰 plugin ecosystem, data/control ownership | platform engineering과 지속 upgrade 필요 | 고유 workflow가 많고 전담 team이 있음 |
| Roadie | Managed Backstage | Backstage model/plugin 친화성, 운영 부담 감소 | SaaS 제약·비용·지원 plugin 확인 | Backstage를 원하지만 hosting 부담을 줄이고 싶음 |
| Spotify Portal for Backstage | Managed/enterprise Backstage offering | 원 제작자의 practices와 enterprise capabilities | commercial 조건과 OSS 경계 확인 | Spotify ecosystem과 managed path 선호 |
| Port | Commercial IDP | flexible software catalog, action/automation, 빠른 SaaS 도입 | vendor model과 pricing, customization 경계 | 빠른 time-to-value와 SaaS 운영 선호 |
| Cortex | Commercial IDP | service catalog, scorecards, engineering standards | vendor lock-in과 확장 모델 검토 | service maturity와 scorecard 중심 |
| OpsLevel | Commercial IDP | service ownership, maturity, standards | custom portal UX 범위 확인 | catalog governance와 scorecard 우선 |
| Atlassian Compass | Commercial developer experience platform | Atlassian/Jira ecosystem 결합 | ecosystem 의존성과 extension 범위 | Atlassian stack을 이미 표준화 |
| 직접 조합 | Custom stack | 작은 범위와 단순성, 필요한 기능만 선택 | 통합 UX와 ownership이 분산 | catalog/docs 요구가 제한적 |

## Backstage와 인접 도구

이 도구들은 대체재라기보다 plugin/integration 대상인 경우가 많다.

| 영역 | 예시 | Backstage와의 관계 |
|---|---|---|
| SCM | GitHub, GitLab, Bitbucket | entity discovery, source link, Scaffolder publish |
| CI/CD | GitHub Actions, Jenkins, Argo CD | entity page에 build/deploy 상태 노출, action trigger |
| Infrastructure | Kubernetes, Terraform, cloud | runtime/resource visibility와 provisioning action |
| Observability | Grafana, Datadog, Prometheus | dashboard, alert, SLO를 entity context에 연결 |
| Incident | PagerDuty, Opsgenie | on-call, incident와 runbook 접근 |
| Documentation | MkDocs, TechDocs | docs build/publish와 portal reader |
| Identity | GitHub, Google, Microsoft, Okta | sign-in, group/user ingestion, authorization identity |

Backstage가 이들 시스템의 source of truth를 빼앗기보다 링크와 metadata를 Catalog entity에 연결하는 것이 일반적이다.

## Build vs Buy 판단

| 질문 | Backstage OSS 쪽 신호 | Managed/Commercial 쪽 신호 |
|---|---|---|
| UX와 data model이 얼마나 고유한가? | 조직 고유 workflow가 핵심 | 표준 기능으로 대부분 충족 |
| 전담 team이 있는가? | product owner와 engineers가 지속 배정됨 | 운영 인력이 제한됨 |
| time-to-value는? | 단계적 pilot과 장기 투자가 가능 | 수주 내 adoption이 필요 |
| hosting/data 조건은? | 직접 통제 필요 | SaaS 허용 가능 |
| integration은? | custom/internal system 비중이 큼 | vendor connector로 대부분 해결 |
| upgrade 부담은? | 내부에서 감당 가능 | vendor support가 중요 |
| 비용 구조는? | engineering cost를 수용 | license가 더 예측 가능 |

단순한 “license 비용 vs 무료” 비교는 잘못된 결론을 만든다. OSS Backstage의 총비용에는 platform engineers, plugin maintenance, upgrades, infrastructure, security review와 user research가 포함된다.

## Backstage가 유리한 경우

- 내부 시스템과 workflow가 경쟁력의 일부여서 깊은 customization이 필요하다.
- portal을 장기적인 internal product로 운영할 역량이 있다.
- entity model과 source metadata를 직접 통제해야 한다.
- 조직의 React/TypeScript/Node.js 역량을 활용할 수 있다.
- vendor별 UI를 entity-centered experience로 재구성하려 한다.

## 상용 IDP가 유리한 경우

- ownership catalog, scorecard와 self-service의 표준 범위가 요구사항 대부분이다.
- 전담 개발 team보다 빠른 rollout과 vendor support가 중요하다.
- upgrade, hosting, plugin compatibility 운영을 외부화하고 싶다.
- procurement/security 조건에서 SaaS가 허용된다.

## Anti-pattern 비교

| Anti-pattern | 결과 | 대안 |
|---|---|---|
| 모든 plugin을 먼저 설치 | 복잡도와 maintenance만 증가 | user journey별 최소 plugin |
| Catalog를 CMDB dump로 사용 | stale metadata와 낮은 신뢰 | ownership과 source-of-truth 계약 |
| scorecard로 team을 처벌 | metadata gaming, adoption 저하 | 개선 경로와 자동화 연결 |
| template이 approval을 우회 | security/비용 사고 | permission, validation, audit |
| portal page view만 성공 지표로 사용 | 실제 developer outcome 불명 | time-to-find, task success, lead time |

## 평가용 PoC scorecard

각 항목을 1–5점으로 평가한다.

- [ ] 대표 service 20–50개의 ingestion과 ownership 정확도
- [ ] 검색으로 owner/runbook/dashboard를 찾는 시간
- [ ] golden path 1개의 완료율과 소요 시간
- [ ] permission과 audit 요구 충족
- [ ] custom integration 구현 난이도
- [ ] upgrade/운영 작업량
- [ ] developer 만족도와 재사용 의향
- [ ] 3년 TCO: license + engineering + infrastructure + support

## Sources

- [Backstage Documentation](https://backstage.io/docs/)
- [Backstage Plugin Marketplace](https://backstage.io/plugins/)
- [Backstage GitHub Repository](https://github.com/backstage/backstage)
- [Roadie](https://roadie.io/)
- [Port](https://www.getport.io/)
- [Cortex](https://www.cortex.io/)
- [OpsLevel](https://www.opslevel.com/)
- [Atlassian Compass](https://www.atlassian.com/software/compass)
- [Spotify Portal for Backstage](https://backstage.spotify.com/)

