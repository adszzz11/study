---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# AI Agent 대시보드의 지표와 진행 상태 표시

> **한 줄 정의**: AI Agent의 구성과 작업 현황을 노드, 수치 패널, 진행 막대로 표현하는 인터페이스로, 표시된 상태와 실제 실행 성과의 연결 여부가 신뢰도를 좌우한다.

## Overview

영상 두 시점에는 중앙 JEV와 주변 Agent 노드, 지표 패널, 진행 막대가 나타나며 배치와 값이 달라진다. 이는 화면 변화의 관찰이지 실제 업무 완료의 증거는 아니다. “JEV와 Claude를 결합한 37개 AI Agent 팀이 회사 전체를 운영한다”는 홍보 주장은 실제 실행 기록이나 산출물로 검증되지 않았다.

이 노트는 특정 제품 사용법보다 **State·Metric·Progress를 근거와 함께 읽고 설계하는 방법**을 다룬다. 제품명, API, 설치 방법과 성능은 자료만으로 확정할 수 없다.

## Learning Path

- [ ] [[tech/devtools/agent-dashboard-progress/01-overview|Overview]]: 관찰과 주장, 검증 공백을 구분한다.
- [ ] [[tech/devtools/agent-dashboard-progress/02-ecosystem|비교]]: 화면 표현과 검증 가능한 설계를 비교한다.
- [ ] [[tech/devtools/agent-dashboard-progress/03-references|References]]: 출처 범위와 추가 확인 항목을 살핀다.
- [ ] [[tech/devtools/agent-dashboard-progress/04-learning/01-getting-started|시작하기]]: 작은 작업 목록에서 상태와 진행률을 계산한다.
- [ ] [[tech/devtools/agent-dashboard-progress/04-learning/02-deep-dive|심화 학습]]: 이벤트·재시도·동적 분모·데이터 지연을 다룬다.
- [ ] [[tech/devtools/agent-dashboard-progress/05-projects|프로젝트]]: 근거를 조회할 수 있는 대시보드를 만든다.
- [ ] [[tech/devtools/agent-dashboard-progress/cheatsheet|Cheatsheet]]: 검증 질문과 계산 기준을 빠르게 확인한다.

## When To Use

- Multi-agent 화면에서 활동량과 검증된 성과를 구분할 때.
- 운영 대시보드의 지표 정의, 진행률, 근거 로그를 설계할 때.
- 시연 영상의 주장과 실제로 관찰 가능한 사실을 분리할 때.

## When Not To Use

- JEV·Claude의 연동 API나 특정 제품 설치법이 필요할 때.
- 37개 Agent의 실재, 회사 운영 능력, 성능 우위를 입증하려 할 때.
- 이 자료만으로 frontend·backend·database·통신 방식을 선택하려 할 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/agent-dashboard-progress/01-overview|Agent 대시보드의 상태·지표 개념]]

필수 MOC 링크는 vault 통합을 위한 참조다. 현재 작업 폴더에는 MOC가 없어 대상 존재 여부는 확인하지 못했다.

## Sources

- 사용자 제공 dossier: 영상 00:00·00:05 장면 요약. 원본 URL은 제공되지 않아 기재할 수 없다.
- 아래 실습·모델·설계 제안은 학습용이며 영상에서 확인된 구현을 뜻하지 않는다.
