---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 웹 디자인 레퍼런스와 Codex·Claude Code 연계 활용

> **한 줄 정의**: 웹 디자인 예시를 살펴보고 관련 내용을 Codex 또는 Claude Code에 전달하는 활용 방식으로, 수집 자료에서는 전달 대상과 구현 절차까지 확인되지는 않는다.

## Overview

이 tool-study는 디자인 참고 자료를 개발 도구의 입력으로 전환하는 과정을 다룬다. dossier에는 threeui의 디자인 예시와 Codex 또는 Claude Code에 붙여넣는 안내가 등장한다. 실제 복사 원문, prompt, 실행 환경과 구현 결과는 제시되지 않았다.

- **관찰 사실**: 키보드·책·꽃·타일 구체 예시, 버튼과 책 형태 에셋 카드, 애니메이션 배경 언급.
- **해석**: 디자인 탐색 결과를 개발 입력으로 연결하는 흐름.
- **후속 과제**: 입력 → 요구사항 → 환경 → 검증의 연결을 실제 기록으로 확보하기.

`threeui`라는 이름이나 타일 구체의 외형만으로 Three.js 등 특정 graphics library를 추론하지 않는다. 코드 제공, export, 라이선스, framework와 dependencies도 미확인이다.

## Learning Path

아래 순서로 읽고 체크한다. 실습 단계는 영상의 재현 절차가 아니라 정보 공백을 확인하기 위한 제안이다.

- [ ] [[tech/devtools/codex-claude-design-workflow/README|학습 진입점]] — 전체 범위와 근거의 한계 확인
- [ ] [[tech/devtools/codex-claude-design-workflow/01-overview|Overview]] — What/Why와 확인 수준 구분
- [ ] [[tech/devtools/codex-claude-design-workflow/02-ecosystem|Ecosystem]] — 세 대상의 역할과 비교 조건 파악
- [ ] [[tech/devtools/codex-claude-design-workflow/03-references|References]] — 출처와 추가 확보 자료 점검
- [ ] [[tech/devtools/codex-claude-design-workflow/04-learning/01-getting-started|시작하기]] — 관찰 기록과 전달 명세 작성
- [ ] [[tech/devtools/codex-claude-design-workflow/04-learning/02-deep-dive|심화 학습]] — 입력 확보 후 재현 및 비교 설계
- [ ] [[tech/devtools/codex-claude-design-workflow/05-projects|Projects]] — 명세·재현·비교 산출물 만들기
- [ ] [[tech/devtools/codex-claude-design-workflow/cheatsheet|Cheatsheet]] — 실행 전 체크와 기록 양식 참조

## When To Use

- 디자인 참고를 구현 요구사항으로 정리할 때.
- 실제 복사 내용과 요청문을 분리해 재현 가능한 기록을 만들 때.
- 동일한 조건에서 Codex·Claude Code의 결과와 수동 수정 부담을 비교하려 할 때.

## When Not To Use

- 이 자료만으로 특정 framework, 코드 export 또는 라이선스를 확정하려 할 때.
- 영상과 동일한 결과를 즉시 재현하거나 두 도구의 성능 우열을 판단하려 할 때.
- 원본 시각 자료 없이 정확한 외형 복제를 완료 기준으로 삼을 때.

## Related Notes

- [[MOCs/Index]]
- [[MOCs/Devtools]]
- [[tech/devtools/codex-claude-design-workflow/01-overview|디자인 참고 자료를 개발 입력으로 전환하는 기준]]

현재 작업 공간에는 기존 vault 파일이 없어 위 두 필수 MOC의 존재를 확인하지 못했다. MOC 생성·수정·등록은 이 작업에 포함하지 않는다.

## Sources

- https://threeui.com/browse — dossier에 기재된 디자인 참고 경로. 이 노트에서는 사이트 기능을 직접 검증하지 않았다.
- 사용자 제공 dossier — 영상 관찰 내용을 정리한 2차 자료. 영상 원본 URL과 Codex·Claude Code 공식 문서 URL은 제공되지 않았다.
