---
date: 2026-10-21
tags: [tech]
type: tech-tool-study
status: draft
---

# Jcode — 참고자료

> [[README|목차로 돌아가기]] | [[04-learning/01-getting-started|다음: 시작하기]]

## Primary Sources

1. [Jcode 공식 홈페이지](https://jcode.sh/) — 제품 개요와 배포 채널
2. [Jcode Docs](https://jcode.sh/docs) — 설치, provider, MCP, remote 사용
3. [Jcode GitHub](https://github.com/1jehuang/jcode) — source, MIT License, 기능·benchmark 설명
4. [Commands 문서](https://jcode.sh/docs/commands) — memory, background task, command 흐름
5. [Releases](https://jcode.sh/releases) — version과 변경 이력
6. [TypeScript SDK](https://jcode.sh/sdk) — `launch()`, `connect()`, approval과 security model
7. [Jcode Desktop](https://jcode.sh/desktop) — desktop client 배포 정보
8. [Jcode Enterprise](https://jcode.sh/enterprise) — enterprise 배포·security review 안내

## Reading Order

1. Docs로 설치·provider·tool permission을 확인한다.
2. GitHub README와 release note로 현재 기능과 변경점을 대조한다.
3. Commands 문서로 verification, memory, background task의 동작을 확인한다.
4. SDK 문서로 automation의 권한·approval boundary를 확인한다.
5. 실제 repository에서 동일 task set으로 benchmark를 재현한다.

## Source Evaluation Note

공식 문서는 기능과 의도 파악의 1차 자료다. 반면 성능·RAM·startup 비교는 공급자 자체 측정값일 수 있으므로, hardware, OS, model, provider latency, repository 규모를 기록한 local evaluation으로 판단을 보완한다.

## Sources

- https://jcode.sh/
- https://jcode.sh/docs
- https://github.com/1jehuang/jcode
- https://jcode.sh/docs/commands
- https://jcode.sh/releases
- https://jcode.sh/sdk
