---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Usability·Accessibility·Security testing의 점검 대상과 경계

> **한 줄 정의**: Usability testing은 혼란 없는 사용 흐름을, Accessibility testing은 스크린 리더·큰 글자 지원을, Security testing은 권한 우회·정보 유출 가능성을 점검한다.

## Overview

기능이 작동해도 사용자가 흐름을 이해하지 못하거나, 접근 지원 조건에서 이용하지 못하거나, 허용되지 않은 정보에 접근할 수 있다. 세 테스트는 같은 기능을 서로 다른 판단 축으로 살핀다.

| 관점 | 핵심 질문 | 자료의 경계 |
|---|---|---|
| Usability | 사용 중 어디서 혼란을 겪는가? | 사용자 집단·측정 기준 미제공 |
| Accessibility | 스크린 리더·큰 글자 조건에서도 이용 가능한가? | 접근성 전체 범위를 열거한 것은 아님 |
| Security | 권한 우회·정보 유출이 가능한가? | 공격 기법·검사 도구 미제공 |

이 노트는 devtools 분류의 QA 학습 주제다. 특정 제품·프레임워크·버전·표준을 소개하는 문서는 아니다.

## Learning Path

- [ ] [[tech/devtools/usability-accessibility-security-testing/01-overview|Overview]] — 정의와 판단 축 익히기
- [ ] [[tech/devtools/usability-accessibility-security-testing/02-ecosystem|Ecosystem 비교]] — 다른 QA 테스트와 경계 구분
- [ ] [[tech/devtools/usability-accessibility-security-testing/03-references|References]] — 근거의 범위와 공백 확인
- [ ] [[tech/devtools/usability-accessibility-security-testing/04-learning/01-getting-started|시작하기]] — 같은 기능을 세 관점으로 점검
- [ ] [[tech/devtools/usability-accessibility-security-testing/04-learning/02-deep-dive|심화 학습]] — 관찰·추정·통과 조건 분리
- [ ] [[tech/devtools/usability-accessibility-security-testing/05-projects|Projects]] — 점검표와 변경 전후 비교 작성
- [ ] [[tech/devtools/usability-accessibility-security-testing/cheatsheet|Cheatsheet]] — 현장 질문 빠르게 확인

## When To Use

- 기본 기능 확인 이후 사용 흐름·접근 지원·보안의 누락을 찾을 때.
- 동일 화면의 결함을 관점별로 설명하고 수정 후 재점검할 때.
- QA 학습에서 Smoke·Regression과 세 테스트의 관계를 구분할 때.

## When Not To Use

- 접근성 준수 인증이나 보안 감사의 완전한 기준으로 사용하지 않는다.
- 구체적인 자동화 도구 선택, 정량 합격 기준, 공격 기법을 결정하는 유일한 근거로 사용하지 않는다.
- 세 관점 중 하나의 통과로 다른 관점까지 통과했다고 판단하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/usability-accessibility-security-testing/01-overview|세 테스트의 정의와 판단 축]] — 같은 주제의 tech 개요 노트

## Sources

- 사용자 제공 dossier: QA 영상 요약을 바탕으로 한 수집 자료. 원본 URL·영상 제목·발행일이 제공되지 않아 출처 URL을 기재할 수 없다.
- 아래 설명은 해당 자료의 범위에 한정한다. 실습 절차와 기록 양식은 자료에서 도출한 학습용 제안이며 영상의 공식 절차가 아니다.
