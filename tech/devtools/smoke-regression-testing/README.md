---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Smoke testing과 Regression testing의 목적과 적용 기준

> **한 줄 정의**: Smoke testing은 새 빌드의 핵심 기능을 빠르게 확인하고, Regression testing은 변경 후 기존 기능이 유지되는지 다시 점검하는 QA 테스트다.

## Overview

두 테스트는 실행 속도보다 **확인하려는 질문**으로 구분한다. Smoke testing은 “새 빌드의 핵심 기능이 동작하는가?”, Regression testing은 “변경 후 기존 기능이 유지되는가?”에 답한다. 같은 기능이 두 점검에 포함될 수 있다.

이 노트는 특정 도구의 사용법이 아닌 QA 목적과 대상 선정 기준을 학습하는 tool-study다. 언어·프레임워크·자동화 도구·CI/CD 구성은 자료에 명시되지 않았다. 실습과 실행 흐름은 정의에 근거한 설계 제안이다.

## Learning Path

- [ ] [[tech/devtools/smoke-regression-testing/01-overview|Overview: 정의와 특징]]
- [ ] [[tech/devtools/smoke-regression-testing/02-ecosystem|비교: QA 관점 구분]]
- [ ] [[tech/devtools/smoke-regression-testing/04-learning/01-getting-started|시작하기: 질문과 체크리스트]]
- [ ] [[tech/devtools/smoke-regression-testing/04-learning/02-deep-dive|심화: 범위와 결과 해석]]
- [ ] [[tech/devtools/smoke-regression-testing/05-projects|Projects: 실전 적용]]
- [ ] [[tech/devtools/smoke-regression-testing/03-references|References: 근거와 한계]]
- [ ] [[tech/devtools/smoke-regression-testing/cheatsheet|Cheatsheet: 빠른 판단]]

## When To Use

- 새 빌드에서 중요한 동작부터 빠르게 확인할 때 Smoke testing을 설계한다.
- 소프트웨어 변경 후 유지되어야 할 기존 동작을 다시 확인할 때 Regression testing을 설계한다.
- 결과 보고서에 검증 목적과 실제 범위를 구분해서 남길 때 두 관점을 함께 사용한다.

## When Not To Use

- Smoke 통과만으로 모든 기존 기능이 유지되었다고 판단하지 않는다.
- Regression testing을 항상 전체 기능의 전수 검사로 간주하지 않는다.
- 두 테스트의 통과를 성능·보안·접근성 검증의 근거로 사용하지 않는다.
- 고정된 실행 순서나 자동화 도구를 정하려는 경우 이 자료만으로 결정하지 않는다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/smoke-regression-testing/01-overview|Smoke / Regression의 핵심 개념]]

기존 vault의 관련 노트는 이 작업 공간에서 확인되지 않아 추가 링크를 만들지 않았다. 필수 MOC 링크의 대상 존재 여부는 실제 vault에서 확인해야 한다.

## Sources

- 사용자 제공 dossier: 영상 요약 및 시점 정보(00:10, 00:15). 원본 URL은 제공되지 않아 기재할 수 없다.
- 원본 영상의 제목·게시자·각 시점의 원문은 확인되지 않았다. 출처 URL을 추정하거나 다른 자료로 대체하지 않았다.
