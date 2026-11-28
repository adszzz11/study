---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: QA 테스트 유형 비교

## 비교 범위

자료에 경쟁 제품이나 도구 생태계는 없다. 아래 항목은 같은 영상의 QA 테스트 유형이다. 하나를 선택하면 나머지를 제외하는 대안이 아니라, 분류 기준과 검증 초점이 다른 항목으로 읽는다.

| 테스트 | 자료에 제시된 내용 | Alpha/Beta와 비교할 축 |
|---|---|---|
| Alpha testing | 내부 참여자 역할 | 참여 주체 |
| Beta testing | 실제 사용자 역할 | 참여 주체 |
| Smoke testing | 새 빌드의 핵심 기능을 빠르게 확인 | 점검 대상·속도 |
| Regression testing | 변경 후 기존 기능 다시 점검 | 변경 영향·기존 기능 |
| Exploratory testing | 시나리오 없이 사용하며 버그 탐색 | 탐색 방식 |
| Acceptance testing | 고객·기획 기준에 따른 출시 준비 여부 확인 | 판단 기준·출시 준비 |
| Performance testing | 응답 속도 측정 | 측정 대상 |

## 확장하지 말아야 할 비교

영상에는 호환성, 사용 흐름, 접근성, 보안 점검도 등장하지만 Alpha/Beta 참여자에게 어떻게 배정하는지 설명하지 않는다. 마지막 화면의 sanity testing과 load testing은 요약에 구체 설명이 없어 세부 비교를 확장하지 않는다.

## 계획에 적용하기

**설계 제안:** 계획표에서 참여자 구분과 검증 목적을 서로 다른 열로 둔다. 예를 들어 실제 사용자의 응답 속도 관찰을 계획할 수 있지만, 이것은 영상에 제시된 운영 조합이 아니다. Beta 참여 사실 자체는 측정값이나 acceptance 기준 충족의 증거를 대신하지 않는다.

## 연결

[[tech/devtools/alpha-beta-participant-roles/01-overview|개념과 한계]] · [[tech/devtools/alpha-beta-participant-roles/05-projects|QA 계획표 프로젝트]] · [[tech/devtools/alpha-beta-participant-roles/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: QA 테스트 12종 소개 영상의 수집 요약. 원본 영상 제목·URL·게시자·게시일은 제공되지 않았다.
- 출처 URL: 미제공. 검증 가능한 URL을 임의로 만들어 기재하지 않는다.
- 이 노트의 근거 범위는 제공 요약에 한정되며, 실습·양식·운영 제안은 원본 영상의 지침이 아니다.
