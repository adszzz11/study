---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# What / Why / 특징

## What

React 시각 효과 컴포넌트는 UI에 표현을 더하기 위한 컴포넌트다. dossier는 React Bits의 Paper Crumple 미리보기와 3D 큐브 그리드 페이지를 다룬다. 큐브 그리드 페이지가 React Bits 소속인지는 확인되지 않았다.

## Why

영상의 배경 질문은 AI를 잘 활용하지만 미적 판단이 부족한 신입 디자이너에 관한 것이다. 도구 사용 능력만으로 전체 화면의 시각적 완성도와 사용성을 판단하기는 어렵다.

**매력적인 미리보기**와 **실제 화면에 적합한 효과**는 다른 판단 대상이다. 화면 레퍼런스에서 정보 위계와 맥락을 살핀 다음 효과 후보를 검토하는 방식을 학습 전략으로 제안한다.

## 특징과 증거 범위

| 항목 | 확인된 사실 | 단정하면 안 되는 사항 |
|---|---|---|
| Paper Crumple | React Bits 미리보기 등장 | 이름에서 유추한 동작, 입력, 속성, 종이 변형 알고리즘 |
| 3D 큐브 그리드 | 큐브의 그리드 형태를 설명하는 페이지 | WebGL·Three.js·CSS transforms·Canvas 사용 여부 |
| Copy prompt | Claude Code·Codex·ChatGPT 대상 메뉴 | 소스 코드 복사, 도구별 prompt 차이, 자동 설치·수정, 정확성 |

## 관찰 가능한 흐름과 아키텍처의 구분

```text
레퍼런스 탐색 → 효과 미리보기·설명 확인 → AI 도구 대상 prompt 복사
```

위 구조는 탐색 흐름이다. 컴포넌트 내부 아키텍처를 설명하지 않는다. React 버전, API, 상태 관리, 렌더링 엔진, 의존성, 배포 방식, 라이선스와 성능은 미확인으로 남긴다.

## 다음 학습

[[tech/devtools/react-visual-effects/04-learning/01-getting-started|관찰 기록부터 시작하기]] · [[tech/devtools/react-visual-effects/README|학습 안내]]

## Sources

- 제공된 dossier: 영상 수집 요약. 원본 영상·갤러리·컴포넌트 페이지 URL은 제공되지 않았다.
- React 공식 문서: https://react.dev/learn — 보충 학습 자료이며, dossier 속 효과의 구현을 입증하는 출처는 아니다.
