---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Alpha/Beta testing의 참여자 구분과 QA 역할 설계

> **한 줄 정의**: Alpha/Beta testing은 제공 자료에서 내부 참여자 중심의 Alpha testing과 실제 사용자 중심의 Beta testing으로 참여 주체를 구분하는 QA 테스트다.

## Overview

이 학습 노트는 특정 제품이나 Framework가 아닌 QA 참여자 역할 구분을 다룬다. 자료가 설명하는 핵심은 **누가 참여하는가**이며, 기능·성능·출시 준비 여부 같은 **무엇을 확인하는가**는 별도로 기록해야 한다.

- **자료에 명시:** Alpha는 내부 참여자, Beta는 실제 사용자 중심이다.
- **분석 틀:** 참여자 축과 검증 목적 축을 분리해 계획과 결과를 해석한다.
- **미확인:** 수행 순서, 환경, 공개 범위, 모집 방식, 규모, 완료 기준, 자동화 도구.
- **적용 제안:** 참여 사실, 관찰 결과, acceptance 기준 충족 여부를 서로 다른 항목으로 남긴다.

## Learning Path

- [ ] [[tech/devtools/alpha-beta-participant-roles/01-overview|Overview]] — 정의와 근거의 경계 파악
- [ ] [[tech/devtools/alpha-beta-participant-roles/02-ecosystem|QA 유형 비교]] — 분류 축과 검증 초점 비교
- [ ] [[tech/devtools/alpha-beta-participant-roles/03-references|References]] — 출처와 미확인 항목 점검
- [ ] [[tech/devtools/alpha-beta-participant-roles/04-learning/01-getting-started|시작하기]] — 참여자·목적·결과 분리 기록
- [ ] [[tech/devtools/alpha-beta-participant-roles/04-learning/02-deep-dive|심화 학습]] — 경계 사례와 출시 판단 검토
- [ ] [[tech/devtools/alpha-beta-participant-roles/05-projects|적용 프로젝트]] — QA 계획표와 비교 실습 수행
- [ ] [[tech/devtools/alpha-beta-participant-roles/cheatsheet|Cheatsheet]] — 기록 전후 빠른 점검

## When To Use

- QA 계획에서 내부 참여자와 실제 사용자의 역할을 명확히 기록할 때.
- “Beta 완료” 같은 요약에서 검증 범위와 근거가 빠졌는지 검토할 때.
- 참여자 관점의 차이와 수행 조건의 차이를 나누어 분석할 때.

## When Not To Use

- 이 자료만으로 모집 인원, 공개 방식, 테스트 환경이나 출시 일정을 확정하려는 경우.
- Alpha/Beta 수행 사실만으로 보안·성능·핵심 기능 검증을 모두 완료 처리하려는 경우.
- 실제 사용자 참여를 acceptance 기준 충족 또는 출시 승인으로 대신하려는 경우.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/alpha-beta-participant-roles/02-ecosystem|QA 테스트 분류 축과 검증 초점 비교]] — 함께 읽을 관련 tech 노트.

## Sources

- 사용자 제공 dossier: QA 테스트 12종 소개 영상의 수집 요약. 원본 영상 제목·URL·게시자·게시일은 제공되지 않았다.
- 출처 URL: 미제공. 검증 가능한 URL을 임의로 만들어 기재하지 않는다.
- 이 노트의 근거 범위는 제공 요약에 한정되며, 실습·양식·운영 제안은 원본 영상의 지침이 아니다.
