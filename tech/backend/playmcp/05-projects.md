---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# PlayMCP Projects

## 1. 개인 일상 Agent

카카오맵 장소 탐색, 톡캘린더 일정 조회, 나와의 채팅방 알림을 조합한다.

- 첫 milestone: 장소와 일정만 읽어 충돌 후보를 반환한다.
- write 단계: 발송 전 대상·시간·본문을 보여주고 confirmation을 요구한다.

## 2. 국내 생활 정보 Agent

지자체 API 또는 공공데이터를 `search_waste_rules`, `search_public_facilities`, `search_local_events` Tool로 감싼다.

- 지역·날짜를 필수 schema로 제한한다.
- source URL과 갱신 시각을 응답에 포함한다.
- API 장애 시 추측하지 않고 데이터 갱신 실패를 명시한다.

## 3. 커머스·콘텐츠 추천 Agent

사용자 조건을 입력받아 카카오 서비스 또는 자체 catalog를 조회하고 추천 근거와 링크를 반환한다.

- ranking 이유와 필터 조건을 결과에 포함한다.
- 구매·주문은 추천 Tool과 분리하고 별도 confirmation을 둔다.

## 4. 운영 자동화 Agent

채용공고·가격·공고문 변화를 주기적으로 탐색한 뒤 조건 충족 시 알림을 보낸다. OpenClaw 연동은 이런 agent 운영 시나리오의 연결 지점이 될 수 있다.

- baseline snapshot과 change diff를 저장한다.
- 중복 알림 방지를 위한 idempotency key를 둔다.
- 알림 대상과 빈도를 사용자가 해제할 수 있게 한다.

## 5. Kakao Tools 배포형 서비스

작고 안전한 task 단위 Tool을 PlayMCP에 등록해 카카오톡 사용자에게 노출되는 경로를 목표로 한다. 2026년 AGENTIC PLAYER 10은 이 Kakao Tools/PlayMCP 배포 모델을 활용한 사례다.

## Sources

- [카카오 — AGENTIC PLAYER 10](https://www.kakaocorp.com/page/detail/12059)
- [카카오 — OpenClaw 연동](https://www.kakaocorp.com/page/detail/12012)
- [카카오 — PlayMCP 베타 오픈](https://www.kakaocorp.com/page/detail/11674)
