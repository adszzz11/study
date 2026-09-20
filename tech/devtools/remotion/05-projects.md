---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Remotion — Projects

[[tech/devtools/remotion/README|학습 진입점]] · 빠른 참조: [[tech/devtools/remotion/cheatsheet|Cheatsheet]]

## 프로젝트 진행 원칙

아래는 공식 기능을 조합한 **학습용 프로젝트 제안**이다. 실습 코드와 render 결과는 별도 저장소에서 관리하고, 이 vault에는 설계·측정·회고를 기록한다. 첫 프로젝트를 완료한 뒤 다음 단계로 확장한다.

## 1. 개인화 타이틀 영상

**목표:** 동일한 디자인으로 제목·색상이 다른 5초 영상 3개를 만든다.

| 항목 | 내용 |
|---|---|
| 선수 학습 | [[tech/devtools/remotion/04-learning/01-getting-started|Getting started]] |
| 입력 | 고객별 `title`, `accent` JSON |
| 구현 | 하나의 TitleCard + JSON별 CLI render |
| 산출물 | MP4 3개, 대표 frame PNG, 입력 JSON |
| 완료 기준 | 길이·해상도 동일, 입력별 문구·색상 반영, 긴 제목도 읽힘 |

- [ ] 기본 제목, 긴 한글 제목, 숫자·영문 혼합 제목을 비교한다.
- [ ] template 수정 한 번으로 출력 3개가 함께 바뀌는지 확인한다.
- [ ] 편집 시간과 render 시간을 구분해 기록한다.

## 2. 데이터 기반 월간 리포트

**목표:** 보고할 지표 개수에 따라 장면과 길이가 달라지는 영상을 만든다.

```json
{
  "period": "2026-08",
  "metrics": [
    {"label": "완료 작업", "value": 42},
    {"label": "문서 작성", "value": 18}
  ]
}
```

- intro, 지표 카드, outro를 별도 component로 만든다.
- 예시 설계: intro 60 frames + 지표당 90 frames + outro 30 frames.
- `calculateMetadata()`에서 `60 + metrics.length * 90 + 30`으로 길이를 계산한다.
- 지표 배열이 비어 있으면 안내 장면을 보여줄지, 입력 에러로 처리할지 명시한다.
- 입력 snapshot과 동일한 font asset으로 재렌더 결과를 비교한다.

**완료 기준:** 30fps에서 지표 2개는 270 frames, 즉 9초다. 지표 개수 변경이 길이에 반영되고, Sequence 경계에 의도하지 않은 공백이 없어야 한다. 마지막 frame은 `durationInFrames - 1`이다.

## 3. Preview와 export를 갖춘 작은 편집 앱

**목표:** 문구·색상 입력 UI와 Player를 연결하고, export 버튼으로 파일을 생성한다.

1. 입력 상태를 하나로 관리해 Player와 export에 동일하게 전달한다.
2. 해상도·fps·길이 계산을 공유한다.
3. server 또는 client export 중 하나를 먼저 구현한다.
4. render 진행 상태, 완료 다운로드, 실패 시 재시도 UI를 만든다.
5. 대표 입력으로 preview와 출력 frame을 비교한다.

**완료 기준:** 수정한 문구가 파일에 반영되고, export를 중복 클릭하거나 실패했을 때 상태가 명확해야 한다. 브라우저 export를 선택했다면 지원 브라우저와 사용 CSS 범위를 결과 기록에 포함한다. 고급 편집 기능으로 확대할 때 Editor Starter를 비교한다.

## 4. 렌더링 경로 측정 실험

**목표:** 동일한 템플릿으로 Local/서버, Lambda, Browser 중 도입 가능한 경로를 측정한다. Cloud 환경 사용은 별도 실습 환경에서 진행한다.

| 조건 | 고정할 값 |
|---|---|
| 콘텐츠 | 동일 입력·미디어·font·template 버전 |
| 출력 | 해상도, fps, 영상 길이, codec |
| 부하 | 단일 요청과 서비스에서 예상하는 동시 요청 |
| 실행 환경 | CPU·메모리·브라우저·지역·패키지 버전 |
| 관찰 | queue 대기, render 시간, 실패율, 메모리, 비용 |

cold start와 warm 실행을 구분하고 반복 측정의 중앙값과 범위를 남긴다. 브라우저와 서버의 지원 codec이 다르면 설정 차이도 기록한다. 공식 Lambda 권장과 자체 측정 결과를 구분한다.

## 회고 질문

- 수작업 편집에서 어떤 부분이 실제로 줄었는가?
- component 재사용이 쉬웠던 장면과 어려웠던 장면은 무엇인가?
- preview와 export의 차이는 어느 단계에서 발견했는가?
- 처리량 확대에 가장 먼저 걸린 제약은 CPU, I/O, 메모리, queue 중 무엇인가?

## Sources

- [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering)
- [calculateMetadata](https://www.remotion.dev/docs/calculate-metadata)
- [Sequence](https://www.remotion.dev/docs/sequence)
- [Player](https://www.remotion.dev/docs/player)
- [Client-side rendering](https://www.remotion.dev/docs/client-side-rendering)
- [Client-side limitations](https://www.remotion.dev/docs/client-side-rendering/limitations)
- [서버 렌더링 비교](https://www.remotion.dev/docs/compare-ssr)
- [공식 Blog — Editor Starter](https://www.remotion.dev/blog)
