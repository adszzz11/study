---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: CRM·Agent 성과 검토

## 증거 경계

| 수준 | 기억할 내용 |
|---|---|
| 소개 확인 | CRM 00:48, 성과 대시보드 00:53, 그래프·에이전트·조직도 |
| 구상 | Claude·Codex 등 여러 클라이언트의 Shared Memory |
| 미확인 | 실제 연동·계산식·정확성·업무 성과·구현 스택 |
| 설계 제안 | 아래 모델·지표·검산 절차 |

## 최소 모델

```text
Agent 1 ─ N Run 1 ─ N Activity N ─ 1 Lead
Outcome ─ Lead + 근거 Activity
Contribution ─ Outcome + Agent + weight
```

## 혼동하지 말 것

- Run 완료 ≠ 업무 성공.
- 메시지 생성 ≠ 실제 발송 ≠ 고객 도달.
- 발송 건수 ≠ 고유 접촉 고객 수.
- 개인 관여 건수 합 ≠ 팀 결과 수.
- 조직 소속 ≠ 작업 기여 ≠ 승인 권한.
- 그래프 표시 ≠ 동일 저장소·실제 동기화 입증.

## 지표 계약 체크

`기간 · 시간대 · cohort · 분자 · 분모 · 응답 창 · 중복 키 · 실패 처리 · 확정 시점 · 원본 ID`

응답률 예시: **접촉 cohort 중 7일 이내 응답한 고유 고객 / 해당 cohort의 고유 접촉 고객**. 분모가 0이면 N/A, 창이 닫히지 않았으면 잠정치다.

## 빠른 검산

1. 수치에서 고객·결과 목록을 연다.
2. Activity → Run → Agent 및 원본 이벤트를 찾는다.
3. 외부 이벤트 ID로 중복을 제거한다.
4. 공동 결과와 부서 이동 규칙을 확인한다.
5. 같은 계약으로 재계산한다.

## Related Notes

- [[tech/data/crm-agent-performance-dashboard/README|학습 지도]]
- [[tech/data/crm-agent-performance-dashboard/04-learning/01-getting-started|설계 실습]]

## Sources

- 사용자 제공 dossier: Orbit Agents 소개 영상의 수집 요약. 원본 URL·영상 제목·게시일은 제공되지 않았다. 영상 시점은 dossier의 표기를 따른다.
- Obsidian 공식 도움말: https://help.obsidian.md/ — 비교 대상의 일반 학습용 참고이며 Orbit Agents의 기능이나 연동을 입증하는 출처가 아니다.
