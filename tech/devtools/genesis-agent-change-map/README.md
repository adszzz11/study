---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# Genesis Map — Coding Agent 변경의 영향과 테스트 공백 시각화

> **한 줄 정의**: Genesis는 Git 코드베이스를 business flow map으로 표현하고, coding agent 변경의 영향 범위·테스트 검증 수준·잠재 위험을 코드 근거와 함께 보여주는 local CLI 및 agent skill이다.

## Overview

Agent의 diff 설명을 사용자 행동과 연결해 읽는 리뷰 보조 도구다. Guest checkout을 추가하며 payment retry, 재고 확보 시점, 무료배송 기준이 함께 바뀌면, 각각 중복 결제·마지막 재고 중복 판매·가격 정책 변화로 이어질 수 있다. Genesis는 이런 변경을 checkout flow 위에 배치한다.

- `map`: 현재 시스템의 business flow를 설명한다.
- `review <revision>`: 비교 revision 이후 변경과 테스트 근거를 보여준다.
- 산출물: `.genesis/out/latest/view.html`, `.genesis/out/latest/summary.md`.
- 핵심 질문: 테스트가 코드를 **실행**했는가를 넘어, 바뀐 동작의 오류를 **검출**할 수 있는가?

코드 인용은 CLI가 검증하지만 변경 의미와 위험은 agent가 해석한다. 테스트를 실행하거나 변경의 안전을 인증하는 도구는 아니다. Python의 parsing 지원과 다른 언어의 지원 수준도 구분해야 한다.

## Learning Path

- [ ] [[tech/devtools/genesis-agent-change-map/README|학습 진입점]] — 전체 목적과 적용 범위 확인
- [ ] [[tech/devtools/genesis-agent-change-map/01-overview|Overview]] — 문제, 특징, benchmark 한계 이해
- [ ] [[tech/devtools/genesis-agent-change-map/02-ecosystem|Ecosystem]] — diff·테스트 실행·static analysis와 역할 비교
- [ ] [[tech/devtools/genesis-agent-change-map/04-learning/01-getting-started|시작하기]] — 설치 확인과 첫 map/review 진행
- [ ] [[tech/devtools/genesis-agent-change-map/04-learning/02-deep-dive|심화 학습]] — 인용 검증과 test verdict를 코드로 대조
- [ ] [[tech/devtools/genesis-agent-change-map/05-projects|Projects]] — checkout 위험과 테스트 공백을 실습
- [ ] [[tech/devtools/genesis-agent-change-map/03-references|References]] — 근거와 미확인 사항 추적
- [ ] [[tech/devtools/genesis-agent-change-map/cheatsheet|Cheatsheet]] — 명령·판정·리뷰 체크리스트 빠르게 확인

## When To Use

- Agent 변경이 여러 사용자 경로에 미치는 영향을 리뷰할 때.
- 테스트가 통과해도 assertion이 변경 동작을 검증하는지 의심될 때.
- 코드 인용을 확인하며 PR에 붙일 리뷰 요약을 준비할 때.

## When Not To Use

- 테스트 실행, runtime coverage, 보안 검사 또는 안전 인증이 필요할 때 단독 수단으로 사용하지 않는다.
- Python 이외 언어에서 누락 branch까지 자동으로 표시된다고 기대하는 경우.
- Agent의 model 호출까지 모두 local이라는 조건이 필요한 경우. CLI의 local 동작과 agent의 데이터 처리는 별도 확인해야 한다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/genesis-agent-change-map/01-overview|Genesis의 business flow와 테스트 판정]]

기존 vault의 관련 tech 노트는 작업 공간에서 확인할 수 없어 임의 링크를 추가하지 않았다.

## Sources

- https://github.com/GenesisAgentInfra/genesis — 제공된 dossier의 GitHub 수집 본문 근거.
- https://raw.githubusercontent.com/GenesisAgentInfra/genesis/main/docs/install.md — 본문에서 안내한 설치 가이드. 내용은 별도 열람하지 않음.
