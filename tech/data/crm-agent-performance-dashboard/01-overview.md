---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

CRM은 고객 관계를 정리하고, 에이전트 성과 대시보드는 에이전트의 활동과 결과를 살피는 접점이다. Orbit Agents 소개 자료는 이를 공유 메모리·사전 구성 에이전트·조직도와 함께 배치한다.

## Why

에이전트가 **무엇을 기억하는가**와 **무엇을 수행했는가**를 업무 관리에 연결하려는 구상이다. Lead Finder와 Email Outreach Agent의 역할은 고객 발굴에서 접촉으로 이어지는 구성을 시사한다. 화면의 공존만으로 실제 연동이나 업무 효과를 입증할 수는 없다.

## 핵심 특징과 해석의 경계

| 구성 | 자료에서 소개된 내용 | 단정할 수 없는 내용 |
|---|---|---|
| Knowledge Graph | 파일·출력물·엔터티를 연결된 노드로 표시 | CRM·실행 이력과 같은 저장소 사용 |
| Shared Memory | Claude·Codex 등 여러 클라이언트 연결 구상 | 실제 연결 성공, 동기화·충돌 처리 |
| 사전 구성 에이전트 | Lead Finder, Email Outreach Agent | 자동 인계, CRM 자동 등록, 응답 반영 |
| CRM·대시보드 | 00:48 CRM, 00:53 성과 화면 소개 | 지표 계산식, 데이터 정확성, 성과 개선 |
| 조직도 | Content·Marketing·Research 아래 에이전트 배치 | 권한, 승인, 작업 지휘 체계 구현 |

## 검토용 아키텍처

```text
Lead 발견 → CRM 기록 → Outreach 활동 → 고객 반응 → 성과 집계
                  ↘ 고객·에이전트·실행 ID로 근거 연결 ↗
```

위 흐름은 dossier를 바탕으로 만든 설계 모형이며 확인된 제품 실행 과정이 아니다. 실제 구현을 평가할 때는 안정적인 ID, 변경 이력, 기간·중복 제거 규칙, 공동 기여 배분, 원본 조회 기능을 확인한다.

## 성과의 다섯 계층

| 계층 | 설계용 지표 예시 | 해석 주의 |
|---|---|---|
| 실행 | 시도·완료·실패 | 실행 완료 ≠ 업무 성공 |
| 산출물 | 발굴 Lead·생성 메시지 | 양만으로 품질 판단 불가 |
| 고객 활동 | 실제 접촉·응답 | 생성과 발송을 구분 |
| 업무 결과 | 유효 Lead·후속 단계 진입 | 고객 관계의 진전을 확인 |
| 운영 효율 | 시간·검토 부담·비용 | 성과에 든 자원도 비교 |

이 지표들은 실습 제안이며 Orbit Agents의 제공 기능으로 확인되지 않았다.

## Related Notes

- [[tech/data/crm-agent-performance-dashboard/README|학습 지도]]
- [[tech/data/crm-agent-performance-dashboard/04-learning/01-getting-started|설계 실습]]

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·영상 제목·게시일은 제공되지 않았다. 영상 시점은 dossier의 표기를 따른다.
- Obsidian 공식 도움말: https://help.obsidian.md/ — 비교 대상의 일반 학습용 참고이며 Orbit Agents의 기능이나 연동을 입증하는 출처가 아니다.
