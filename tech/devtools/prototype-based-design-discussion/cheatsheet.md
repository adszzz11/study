---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 검토 흐름

```text
영역 선택 → 현재 상태·의도 기록 → 시스템 참조 대응
         → 속성표 검토 → 같은 상태의 전후 화면 비교 → 결과·보류 기록
```

위 흐름은 학습용 제안이다.

## 빠른 구분

| 질문 | 기록할 내용 |
|---|---|
| 어디인가? | 화면·영역·상태 |
| 무엇을 바꾸는가? | 구성·색상·텍스트 스타일·변수 |
| 왜 바꾸는가? | 변경 의도와 근거 |
| 기준이 있는가? | 참조 위치 또는 미확정 |
| 확인했는가? | 값 대응과 시각적 결과 각각 기록 |

## 명령 주의사항

```text
/apply-ds-to-prototype
```

자료에 등장한 문자열일 뿐, 공개 표준 명령이나 설치 가능한 도구로 확인되지 않았다. Figma URL의 역할, 실행 환경, API/plugin/MCP 사용, 파일 기록, 권한·승인·자동 적용 범위는 미상이다.

## 완료 전 체크

- [ ] 의견과 화면 위치가 연결되어 있다.
- [ ] 시각적 선호와 시스템 정합성을 구분했다.
- [ ] 현재 값·목표 참조·확인 결과가 있다.
- [ ] 전후 화면의 내용과 상태가 같다.
- [ ] 값 일치를 token binding 증거로 취급하지 않았다.
- [ ] 미확정 대응과 누락 가능성을 기록했다.
- [ ] interaction·접근성·사용성 개선을 화면만으로 단정하지 않았다.

## 기술스택 요약

- 사례 UI: MeetBook 예약 캘린더 프로토타입의 특정 영역 검토.
- 디자인 참조: Figma URL 입력, 역할과 연동 방식 미확인.
- 작업 인터페이스: 채팅의 `/apply-ds-to-prototype` 입력 장면.
- 검토 요소: 색상 코드·텍스트 스타일·디자인 변수 및 전후 화면.
- 구현 한계: framework·backend·API·자동 적용 범위·성능 미상.

[[tech/devtools/prototype-based-design-discussion/04-learning/01-getting-started|시작하기]] · [[tech/devtools/prototype-based-design-discussion/03-references|출처 상태]] · [[tech/devtools/prototype-based-design-discussion/README|학습 진입점]]

## Sources

- 사용자 제공 dossier: 짧은 영상의 수집 요약. 원본 영상 URL과 화면에 입력된 Figma URL은 제공되지 않았다. 원본을 직접 검증한 기록이 아니다.
- 보충 자료 URL: https://help.figma.com/ — Figma 공식 도움말 진입점. 개념을 추가 조사하기 위한 자료이며, 사례의 명령·연동 방식·정확성을 입증하는 출처는 아니다.
