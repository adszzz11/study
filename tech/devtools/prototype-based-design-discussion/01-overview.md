---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

프로토타입은 시안을 보여주는 결과물이면서, 의견과 화면 위치를 연결하는 공통 기준이다. “전체적으로 수정”이라는 의견을 특정 영역의 구성·색상·텍스트 스타일처럼 확인할 수 있는 대상으로 좁힌다.

## Why

AI가 화면을 완성했다는 사실과 특정 디자인 시스템에 맞는다는 판단은 별개다. 화면 논의에서는 대상과 변경 의도를, 시스템 검토에서는 값과 참조 기준의 대응을 기록한다.

| 층위 | 질문 | 남길 근거 |
|---|---|---|
| 화면 | 어느 영역을 왜 바꾸는가? | 위치, 현재 상태, 변경 의도 |
| 시스템 | 어떤 기준과 대응하는가? | 현재 값, 참조값, 확인 결과 |

## 핵심 특징

1. **범위 고정:** 화면 전체 → 캘린더 영역 → 스타일 → 컴포넌트 또는 토큰 순으로 검토 대상을 좁힐 수 있다. 마지막 연결 구조가 실제 구현됐는지는 미상이다.
2. **명령과 참조 입력:** 채팅에 `/apply-ds-to-prototype`과 Figma URL을 넣는 장면이 등장한다.
3. **이중 검토:** 속성 비교표는 값의 대응을, 적용 전후 화면은 시각적 영향을 살피는 데 사용한다.
4. **개념 구분:** 디자인은 전체 구성과 결과, 컴포넌트는 재사용 UI 단위, 토큰은 스타일 의도를 이름 있는 값으로 관리하는 단위로 이해한다. 이 정의는 학습용 설명이다.

## 관찰된 흐름과 미확인 구현

```text
프로토타입 검토 → 명령 및 Figma URL 입력
                 → 스타일·변수 비교 → 적용 전후 화면 확인
```

위 흐름은 관찰된 인터페이스의 정리이며 software architecture가 아니다. 제품·실행 환경, URL의 역할, Figma API/plugin/MCP 사용 여부, 파일 직접 기록 여부, 자동 적용 범위와 승인 단계는 확인되지 않았다. 실제 token binding이나 component replacement를 수행했다고 단정하지 않는다.

## 읽기 연결

[[tech/devtools/prototype-based-design-discussion/02-ecosystem|비교]] · [[tech/devtools/prototype-based-design-discussion/04-learning/01-getting-started|시작하기]] · [[tech/devtools/prototype-based-design-discussion/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: 짧은 영상의 수집 요약. 원본 영상 URL과 화면에 입력된 Figma URL은 제공되지 않았다. 원본을 직접 검증한 기록이 아니다.
- 보충 자료 URL: https://help.figma.com/ — Figma 공식 도움말 진입점. 개념을 추가 조사하기 위한 자료이며, 사례의 명령·연동 방식·정확성을 입증하는 출처는 아니다.
