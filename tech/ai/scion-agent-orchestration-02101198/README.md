---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion — 이기종 AI Agent 팀의 협업과 실행을 위한 오케스트레이션 플랫폼

> **한 줄 정의**: Scion은 서로 다른 AI agent harness와 모델을 독립적인 실행 환경에 배치하고, 사람과 agent 사이의 작업 위임·통신·상태 관찰을 지원하는 Apache-2.0 오픈소스 orchestration 플랫폼이다.

## Overview

단일 coding agent의 응답 품질만으로 긴 프로젝트를 운영하기는 어렵다. Scion은 팀의 작업 소유권, context 공유, 도움 요청, 진행 상황 관찰을 다루는 기반 시설이다. Claude Code, Antigravity, Codex, OpenCode 같은 harness를 조합하고 templates·skills·instructions로 역할을 정의한다.

- **실행과 협업의 분리:** Harness는 작업을 수행하고, Hub와 Runtime Broker는 identity·dispatch·실행 환경을 관리한다.
- **협업 방식의 실험:** Shared directories, Git worktrees, separate clones를 선택하고 위임·메시지·관찰 경로를 구성한다.
- **운영 확장:** CLI 중심 사용에서 Workstation과 hosted Hub로 확장한다. 로컬에서도 agent는 Hub를 거친다.
- **성숙도:** 활발히 개발 중인 pre-1.0 프로젝트로 API와 configuration이 바뀔 수 있다. 공식 지원되는 Google 제품은 아니다.

## Learning Path

- [ ] [[tech/ai/scion-agent-orchestration-02101198/README|학습 지도 다시 보기]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/01-overview|Overview: 개념과 구조]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/02-ecosystem|Ecosystem: 대안과 조합]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/03-references|References: 자료와 검증 범위]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/04-learning/01-getting-started|시작하기: 단일 agent 실행]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/04-learning/02-deep-dive|심화: 팀 운영 설계]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/05-projects|Projects: 협업 실험]]
- [ ] [[tech/ai/scion-agent-orchestration-02101198/cheatsheet|Cheatsheet: 빠른 참조]]

권장 순서: 개념과 비교 → 단일 agent 실행 → 작은 팀 실험 → 운영 확장 검토. References와 Cheatsheet는 각 단계에서 함께 사용한다.

## When To Use

- 역할이 다른 agent에게 병렬 작업을 나누고 사람이 결과를 검토해야 할 때.
- Harness와 모델을 섞어 쓰면서 실행·통신·관찰 경로를 공통으로 관리할 때.
- 협업 instructions를 바꿔 가며 품질·비용·조정 시간을 실험할 때.

## When Not To Use

- 단일 harness로 끝낼 수 있는 짧고 단순한 작업.
- 안정적인 API와 configuration 계약 또는 공식 Google 제품 지원이 필수인 경우.
- 자동 merge·충돌 해결이나 검증된 sandbox 보안 수준을 전제해야 하는 경우. 제공 자료만으로 보장할 수 없다.
- 팀 생산성 향상이나 비용 절감의 정량적 효과를 이미 입증된 사실로 요구하는 경우.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/codex/README|Codex]] — Scion이 실행할 수 있는 개별 harness의 학습 노트.

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
