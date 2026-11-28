---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem: QA 활동별 비교

## 비교 관점

자료에는 벤더·프레임워크 생태계가 없다. 아래는 함께 소개된 QA 유형의 역할 비교다. 같은 기능에 여러 유형을 적용할 수 있으며, 표의 배열은 실행 순서가 아니다.

| 유형 | 자료에서 설명한 역할 | 비교 초점 |
|---|---|---|
| Exploratory testing | 시나리오 없이 사용하며 버그 발견 | 사용을 통한 발견 |
| Acceptance testing | 고객·기획 기준으로 출시 준비 확인 | 기준 충족 판단 |
| Smoke testing | 새 빌드 핵심 기능을 빠르게 확인 | 새 빌드의 핵심 상태 |
| Regression testing | 변경 후 기존 기능 재점검 | 변경의 영향 |
| Alpha/Beta testing | 내부 참여자와 실제 사용자 구분 | 참여자 |
| Performance testing | 응답 속도 측정 | 속도 |
| 기기·브라우저 호환성 점검 | 환경 간 호환성 확인 | 실행 환경 |
| 사용 흐름 점검 | 혼란 없는 흐름 확인 | 사용의 명확성 |
| 접근성 점검 | 스크린 리더·큰 글자 지원 확인 | 접근성 지원 |
| 보안 점검 | 권한 우회·정보 유출 점검 | 권한·정보 보호 |
| Sanity testing / Load testing | 전체 목록에 포함 | 구체 설명이 없어 상세 비교 불가 |

## 측정과 판단 연결

응답 속도를 측정한 사실만으로 출시 기준 충족을 선언할 수 없다. 실제 기준과 측정 조건·결과를 대조해야 Acceptance testing의 판단 근거가 된다. 이는 정의를 적용한 해석이며 원자료에는 구체적인 속도 기준이 없다.

- 관찰: 특정 환경에서 응답 시간이 측정되었다.
- 기준 확인: 고객·기획의 실제 허용 기준과 조건을 확보했는가?
- 판단: 해당 기준과 결과를 대조해 충족 여부를 설명한다.

## 연결

[[tech/devtools/exploratory-acceptance-testing/01-overview|핵심 개념]] · [[tech/devtools/exploratory-acceptance-testing/05-projects|변경 후 QA 질문 분리 프로젝트]] · [[tech/devtools/exploratory-acceptance-testing/README|학습 경로]]

## Sources

- 사용자 제공 dossier: QA 테스트 유형 설명을 정리한 자료. 원본 영상 제목·URL·게시일은 제공되지 않았다.
- 추가 용어 확인용: ISTQB Glossary — https://glossary.istqb.org/ (원자료의 출처가 아니며, 이 노트의 원자료 주장에 대한 직접 인용으로 사용하지 않음).
