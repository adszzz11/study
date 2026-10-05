---
date: 2026-10-05
tags: [tech]
type: tech-tool-study
status: draft
---

# GoLive — References

[[tech/devtools/golive-skill/README|학습 진입점]]

## GoLive 공식 자료

1. [GitHub repository / README](https://github.com/mikehasa/golive-skill) — 설치, workflow, 사용 범위의 출발점
2. [Architecture](https://github.com/mikehasa/golive-skill/blob/main/docs/ARCHITECTURE.md) — Agent·CLI 경계와 local execution 구조
3. [Provider scope](https://github.com/mikehasa/golive-skill/blob/main/docs/PROVIDERS.md) — built-in provider와 guided flow 구분
4. [Trust, access and control](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md) — approval gate, credential, teardown의 안전 경계
5. [Validation scope and live-test evidence](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md) — 검증된 provider 조합과 미검증 범위
6. [GoLive skill source directory](https://github.com/mikehasa/golive-skill/tree/main/skills/golive) — Skill 지시문과 source layout 확인
7. [GoLive npm package](https://www.npmjs.com/package/golive) — 배포 package 정보와 설치 전 확인 지점

## 비교용 공식 자료

- [Vercel deployment documentation](https://vercel.com/docs/deployments/overview) — Git, CLI, API 등 Vercel deployment 방식
- [Pulumi IaC concepts](https://www.pulumi.com/docs/iac/concepts/) — desired-state IaC의 개념과 운영 모델

## 읽는 순서

1. README로 전제 조건과 기본 workflow를 파악한다.
2. Trust에서 변경 gate와 credential 보관 방식을 먼저 읽는다.
3. Providers와 Validation을 함께 읽어 “지원”과 “검증됨”을 구별한다.
4. 실제 적용 직전에는 해당 provider의 원문 문서·현재 비용·권한 요구사항도 다시 확인한다.

## Sources

- [GoLive GitHub repository](https://github.com/mikehasa/golive-skill)
- [GoLive Trust model](https://github.com/mikehasa/golive-skill/blob/main/docs/TRUST.md)
- [GoLive Validation](https://github.com/mikehasa/golive-skill/blob/main/docs/VALIDATION.md)
