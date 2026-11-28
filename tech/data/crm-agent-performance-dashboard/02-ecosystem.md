---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: 통합형과 기능 분리형 비교

## 비교 범위

자료가 직접 언급한 비교 대상은 Obsidian뿐이다. 다른 경쟁 제품이나 시장 우위를 판단할 근거는 없다. 기능 분리형 접근은 분석을 위한 설계 대안이다.

| 비교 축 | Orbit Agents 소개 | Obsidian | 기능 분리형 접근 |
|---|---|---|---|
| 자료 내 위치 | 메모리·에이전트 운영 통합 시스템 | 영상에서 비교 대상으로 언급 | 설계 대안 |
| 메모리 | Knowledge Graph·Shared Memory 구상 | 구체적인 기능 비교 근거 부족 | 별도 메모리 계층 |
| CRM | 화면 소개 확인 | 자료에 관련 설명 없음 | 별도 CRM |
| 에이전트 성과 | 대시보드 소개 확인 | 자료에 관련 설명 없음 | 실행 로그·분석 화면 분리 |
| 조직 관리 | 부서별 에이전트 조직도 | 자료에 관련 설명 없음 | 역할·소속 모델 별도 설계 |
| 검토 과제 | 실제 연결·집계 검증 | 제공 자료만으로 비교 불가 | 식별자·동기화·집계 일관성 |

Obsidian 열의 ‘설명 없음’은 기능 부재를 의미하지 않는다.

## 선택 기준

- 통합형의 기대 가치: 여러 업무 맥락을 한곳에서 파악한다. 동일 고객과 실행 기록이 화면마다 일관되는지 확인해야 한다.
- 분리형의 설계 과제: 시스템별 ID 매핑, 동기화 지연, 재전송·중복 이벤트, 오류 복구를 명시해야 한다.
- 도입 검증: 같은 고객의 발굴 기록 → CRM 상태 → 접촉 기록 → 대시보드 수치를 따라가며 원본으로 검산한다.

가격, 확장성, 보안, 연동 목록, 성능은 자료에 없어 비교하지 않는다.

## Related Notes

- [[tech/data/crm-agent-performance-dashboard/README|학습 지도]]
- [[tech/data/crm-agent-performance-dashboard/04-learning/01-getting-started|설계 실습]]

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·영상 제목·게시일은 제공되지 않았다. 영상 시점은 dossier의 표기를 따른다.
- Obsidian 공식 도움말: https://help.obsidian.md/ — 비교 대상의 일반 학습용 참고이며 Orbit Agents의 기능이나 연동을 입증하는 출처가 아니다.
