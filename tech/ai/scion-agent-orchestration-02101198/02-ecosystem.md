---
date: 2026-11-29
tags: [tech]
type: tech-tool-study
status: draft
---

# Scion Ecosystem과 선택 기준

## 비교 범위

제공 dossier에는 경쟁 orchestration 제품의 상세 기능·성능 자료가 없다. 아래 표는 구성 요소와 접근 방식의 관계를 비교하며 제품 간 우열이나 benchmark를 주장하지 않는다.

| 대상·접근 방식 | 담당 문제 | Scion과의 관계 | 선택 기준 |
|---|---|---|---|
| Claude Code, Antigravity, Codex, OpenCode | 개별 agent의 작업 수행 | 실행 대상 harness | 단일 harness로 충분한가? |
| Scion 기반 agent 팀 | 복수 identity·실행·통신·관찰 | 분석 대상 | 병렬화 이익이 조정 비용보다 큰가? |
| GitHub Issues, Linear, Farmtable, Beads | 작업 추적 | Architecture companion | 작업 상태의 기준을 어디에 둘 것인가? |
| Shared directories | 파일·노트·산출물 교환 | 공유 기반 | 동시 수정·산출물 위치 규칙이 있는가? |
| Specialized memory systems | 추가 memory 기능 | 외부 확장 | 필요한 기억의 수명·검색·갱신 방식은 무엇인가? |
| Skill Bank·외부 registries | Skills 배포·버전·resolution | 전문성 재사용 | 검증된 skill 버전을 어떻게 유지하는가? |
| A2A bridge | 다른 agent system 연결 | 상호 연결 경계 | 필요한 호환 범위를 실제로 확인했는가? |

## Workspace 선택

아래 장단점은 공유 방식에서 도출한 설계적 해석이다.

| 방식 | 적합한 상황 | 팀이 정할 규칙 |
|---|---|---|
| Shared directories | 노트와 산출물을 빠르게 교환 | 파일별 작성자·동시 수정 조정 |
| Git worktrees | 변경을 분리하고 검토 후 통합 | Branch 소유권·review·통합 담당 |
| Separate clones | 저장소 복사본을 분리 | 결과 전달·동기화·통합 절차 |

어느 방식도 자료만으로 자동 merge, 충돌 해결, transaction 수준의 파일 접근 제어를 보장하지 않는다.

## 도입 판단 순서

1. 단일 harness로 작업을 수행해 baseline을 남긴다.
2. 독립적인 작업 두 개로 나눌 수 있는지 확인한다.
3. 작은 팀으로 결과 품질, 전체 시간, 사람의 개입, 사용 비용을 측정한다.
4. 이익이 관찰되면 hosted 운영과 외부 task tracking·memory 연동을 검토한다.

Task tracker와 Hub에 같은 상태를 기록한다면 어느 쪽이 기준인지 명시한다. 도구를 추가한다고 작업 소유권과 완료 기준이 자동으로 정해지지는 않는다.

## Navigation

- [[tech/ai/scion-agent-orchestration-02101198/README|Scion 학습 진입점]]

## Sources

- https://github.com/GoogleCloudPlatform/scion — README 및 제공된 dossier의 프로젝트 설명.
