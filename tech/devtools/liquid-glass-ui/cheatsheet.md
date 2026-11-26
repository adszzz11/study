---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — 빠른 점검

## 확인 가능한 것과 불가능한 것

| 주장 | 근거 상태 |
|---|---|
| 반투명 패널을 사용한 음악 앱 목업 | dossier에 명시 |
| 보라색·파란색 구성 | dossier에 명시, 필수 색상으로 일반화 불가 |
| 배경과 콘텐츠를 연결하는 표면 | 설계 관점의 해석 |
| Blur·Refraction·Animation 적용 | 확인 불가 |
| 특정 기업 Design System·API 사용 | 확인 불가 |
| 성능·접근성·사용성 검증 완료 | 근거 없음 |

## 핵심 구분

- Transparency: 배경이 비치는 정도.
- Blur: 배경이 흐려지는 처리. Transparency만으로 적용 여부를 알 수 없다.
- Visual Layer: 표면과 콘텐츠의 시각적 관계. 소프트웨어 아키텍처와 구분한다.
- Observation / Interpretation / Hypothesis를 별도 기록한다.

## 실험 순서

1. 콘텐츠·기능·Layout을 고정한다.
2. 패널 Alpha만 바꾼다.
3. Color와 Surface를 분리한다.
4. 밝은·어두운·복잡한 배경으로 바꾼다.
5. Blur는 별도 옵션으로 비교한다.
6. 곡 정보, 재생 버튼, 선택 상태의 식별 결과를 남긴다.

## 구현 검토 질문

- 텍스트와 아이콘이 모든 배경에서 읽히는가?
- 패널 경계와 중요 콘텐츠가 드러나는가?
- 선택·비활성·재생 상태를 구분할 수 있는가?
- 패널이 늘어날 때 시각적 밀도가 과해지는가?
- 반투명 표면이 화면 이해에 기여하는가?

[[tech/devtools/liquid-glass-ui/03-references|근거 범위]] · [[tech/devtools/liquid-glass-ui/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 네 가지 UI 스타일을 제시한 영상에 관한 설명. 원본 URL은 제공되지 않아 기재할 수 없음.
- 원본 영상·코드·사용자 평가·성능 측정 자료는 직접 확인하지 못함. 실습과 검증 기준은 이 노트의 제안임.
