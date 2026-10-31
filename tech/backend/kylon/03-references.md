---
date: 2026-10-22
tags: [tech]
type: tech-tool-study
status: draft
---

# Kylon References

> 제품 기능, integration 수, 가격, security certification 상태는 바뀔 수 있다. 도입·계약 전에는 아래 공식 원문을 다시 확인한다.

## Product and Getting Started

1. [Kylon 공식 제품 및 FAQ](https://kylon.io/) — 제품 범위, 대상 사용자, FAQ
2. [Pricing](https://kylon.io/pricing) — plan과 과금 확인
3. [Help Center](https://kylon.io/help) — 사용법과 platform 안내
4. [Kylon Agent / Web Bot Auth](https://kylon.io/bot) — agent·bot authentication

## Architecture and Operations

5. [How Kylon connects agents and tools](https://kylon.io/blog/how-kylon-connects-agents-and-tools) — CLI, Connection, App 기술 설명
6. [How Permissions Work in Kylon](https://kylon.io/blog/how-permissions-work-in-kylon) — permission 모델
7. [Approve an Agent’s action](https://kylon.io/help/approve-agent-actions) — approval card와 human-in-the-loop
8. [Run history](https://kylon.io/product/run-history) — workflow 실행 이력
9. [Secret vault and credential injection](https://kylon.io/product/credentials) — secret과 credential 사용

## Security and Legal

10. [Prompt-injection protection](https://kylon.io/help/prompt-injection-protection) — 위협 모델과 사용자 통제
11. [Privacy Policy](https://kylon.io/privacy) — 데이터 처리와 저장 위치 안내
12. [Terms of Service](https://kylon.io/terms) — 서비스 이용 약관

## Reading Order

처음에는 제품/FAQ → permissions → approval → prompt-injection protection → run history 순서로 읽는다. 기능 가능 여부만 확인하지 말고, 누가 어느 Connection을 쓰며 어떤 action을 사람이 승인하는지 함께 기록한다.

## Related Notes

- [[README|Kylon 학습 경로]]
- [[cheatsheet|운영 checklist]]
