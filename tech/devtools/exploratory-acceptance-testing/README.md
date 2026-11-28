---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Exploratory testing과 Acceptance testing의 역할 및 상호 보완

> **한 줄 정의**: Exploratory testing은 정해진 시나리오 없이 제품을 사용하며 버그를 발견하고, Acceptance testing은 고객·기획 기준으로 출시 준비 여부를 확인하는 테스트다.

## Overview

제품 사용 중 **문제를 발견하는 질문**과 **출시 기준 충족을 판단하는 질문**을 분리한다. 두 방식은 경쟁 도구가 아니라 서로 다른 근거를 제공하는 QA 활동이다.

| 활동 | 핵심 질문 | 남길 근거 |
|---|---|---|
| Exploratory testing | 사용하면서 어떤 문제가 드러나는가? | 관찰한 문제와 발생 맥락 |
| Acceptance testing | 고객·기획 기준을 충족했는가? | 기준별 확인 결과 |

탐색에서 버그를 찾지 못했다고 출시 기준이 입증되지는 않는다. 기준을 충족했다고 모든 사용 상황의 문제가 배제되는 것도 아니다. 이 노트의 정의는 제공 dossier의 설명 범위를 따른다.

## Learning Path

- [ ] [[tech/devtools/exploratory-acceptance-testing/README|학습 진입점과 전체 경로]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/01-overview|Overview: What / Why / 특징]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/02-ecosystem|비교: QA 활동별 질문]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/03-references|References: 출처와 근거 한계]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/04-learning/01-getting-started|시작하기: 같은 기능에 두 질문 적용]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/04-learning/02-deep-dive|심화: 발견과 기준 연결]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/05-projects|Projects: 실전 적용]]
- [ ] [[tech/devtools/exploratory-acceptance-testing/cheatsheet|Cheatsheet: 빠른 점검]]

## When To Use

- 기능을 자유롭게 사용하며 예상하지 못한 문제를 발견하려 할 때 Exploratory testing을 적용한다.
- 고객·기획 기준을 근거로 출시 준비 상태를 검토할 때 Acceptance testing을 적용한다.
- 발견한 버그가 출시 판단에 미치는 영향을 설명해야 할 때 두 결과를 연결한다.

## When Not To Use

- Exploratory testing 결과만으로 출시 기준 충족을 확정하지 않는다.
- Acceptance testing 통과를 모든 사용 상황의 무결성 보증으로 사용하지 않는다.
- 실제 기준이 없다면 수행자의 추측으로 Acceptance testing 통과를 선언하지 않는다.
- 도구 선정·효율 순위·비용 추정에는 이 자료만으로 충분하지 않다.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/exploratory-acceptance-testing/02-ecosystem|관련 tech 노트: Smoke·Regression 등 QA 유형 비교]]

필수 MOC 링크는 대상 vault의 기존 관리 노트를 전제로 한다. 현재 작업 공간에는 해당 파일이 없으며, 관리 파일은 생성하거나 수정하지 않는다.

## Sources

- 사용자 제공 dossier: QA 테스트 유형 설명을 정리한 자료. 원본 영상 제목·URL·게시일은 제공되지 않았다.
- 추가 용어 확인용: ISTQB Glossary — https://glossary.istqb.org/ (원자료의 출처가 아니며, 이 노트의 원자료 주장에 대한 직접 인용으로 사용하지 않음).
