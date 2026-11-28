---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

threeui는 수집 자료에서 웹 디자인 예시를 접하는 지점으로 등장한다. `threeui.com/browse` 화면에는 버튼과 책 형태의 에셋 카드가 보이며, 영상은 애니메이션 배경도 언급한다. 이후 Codex 또는 Claude Code에 무언가를 붙여넣는 활용을 안내한다.

이 관찰은 실제 복사 대상이나 입력 형식을 알려주지 않는다. 따라서 이 흐름을 image-to-code, component 복제 또는 code import로 단정할 수 없다.

## Why

시각적 참고만으로는 구현자가 형태·배치·상호작용과 실행 조건을 결정해야 한다. 참고 자료를 구현 가능한 입력으로 바꾸려면 무엇을 전달했고 어떤 결과를 원하는지 구체화해야 한다. 이것이 이 노트의 분석 관점이며, 영상에서 효과가 입증된 workflow라는 뜻은 아니다.

## 특징과 단계별 경계

| 단계 | 확인된 내용 | 미확인 내용 |
|---|---|---|
| 디자인 탐색 | threeui 소개와 다양한 예시 | 검색·필터, 상세 정보 |
| 화면 요소 | 버튼과 책 형태 카드 | 제공 파일·코드·데이터 |
| 동적 표현 | 애니메이션 배경 언급 | 구현 방식·라이브러리·실행 조건 |
| 도구 전달 | Codex 또는 Claude Code에 붙여넣기 안내 | 복사 대상·입력 형식·실제 prompt |
| 구현·검증 | 제공 자료로 확인 불가 | 결과·작동 여부·수정 과정 |

**핵심 경계는 보이는 디자인과 전달되는 정보 사이에 있다.** 카드의 노출은 source code, 이미지, component 또는 prompt 제공을 입증하지 않는다. 타일 구체라는 표현도 3D rendering 사용의 증거가 아니다.

## 재현성 분석 기준

| 축 | 기록할 내용 |
|---|---|
| 입력 | 실제 복사 원문과 형식, 출처 |
| 요구사항 | 구현할 형태·배치·상호작용과 기대 결과 |
| 환경 | 기존 프로젝트, 실행 방법, 확인된 dependencies |
| 검증 | 시각·동작 요구 충족 여부와 수정 내역 |

위 표는 학습용 분석 기준이며 확인된 제품 기능 목록이 아니다.

## 다음 단계

[[tech/devtools/codex-claude-design-workflow/02-ecosystem|역할 비교]] → [[tech/devtools/codex-claude-design-workflow/04-learning/01-getting-started|관찰과 명세 실습]] · [[tech/devtools/codex-claude-design-workflow/README|학습 경로]]

## Sources

- https://threeui.com/browse — dossier에 기재된 디자인 참고 경로. 이 노트에서는 사이트 기능을 직접 검증하지 않았다.
- 사용자 제공 dossier — 영상 관찰 내용을 정리한 2차 자료. 영상 원본 URL과 Codex·Claude Code 공식 문서 URL은 제공되지 않았다.
