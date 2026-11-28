---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# References와 근거 범위

## 주 자료

| 자료 | 쓰임 | 제한 |
|---|---|---|
| GitHub Issue #64 | 세 skill 발췌, 작성자 주장, 개선 제안 | 독립적인 실행 검증 아님 |
| Revision `6ca54f6` | 인용된 구현의 분석 범위 | 현재 HEAD와 동일하다고 볼 수 없음 |
| 연결된 skills catalog | 관련 탐색 경로 | 내용 미열람; 추가 근거로 사용하지 않음 |

## 주장별 확인 수준

- **발췌에서 확인:** `idea` 전송 payload, 응답 id 저장, remote response의 shell 실행, classifier 회피를 이유로 한 call 분리 지시.
- **작성자 관찰·평가:** 전송 고지 부재, marketplace 배포 설명, onboarding 의도에 대한 해석.
- **미확인:** 실제 서버 응답 코드, 원문 보관 여부와 기간, 실제 실행·피해, 특정 harness 우회 성공, 현재 수정 여부.

작성일은 2026-10-26이고 수집 화면에서는 Open이었다. 이 노트의 `date`는 작성일이며 이슈 상태의 재확인 날짜를 뜻하지 않는다.

## 후속 조사 질문

1. 현재 revision에서 관련 지시와 payload가 바뀌었는가?
2. 서버의 데이터 처리 고지와 거절 가능한 경로가 있는가?
3. 실행 script가 배포물에 포함되거나 검증 가능한 버전으로 고정되는가?
4. Maintainer의 공식 답변이나 수정 내역이 있는가?

이 질문들은 조사 제안이며 확인된 사실이 아니다.

[[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64
- https://thirtysix.github.io/awesome-agent-skills/#skills?q=convex — 이슈가 연결한 catalog, 미열람
