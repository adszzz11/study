---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Remotion — Deep dive

[[tech/devtools/remotion/README|학습 진입점]] · 이전: [[tech/devtools/remotion/04-learning/01-getting-started|Getting started]] · 다음: [[tech/devtools/remotion/05-projects|Projects]]

## 1. Props와 metadata 해석

Composition의 데이터 흐름은 다음과 같다.

```text
defaultProps
    ↓ inputProps를 병합해 기본값 덮어쓰기
calculateMetadata({props, ...})
    ↓ 필요하면 props와 duration / fps / width / height 반환
최종 component props + 영상 설정
```

`calculateMetadata()`에서 비동기 조회와 동적 길이 계산을 수행할 수 있다. 입력 schema는 검증과 Studio의 편집 control 정의에 활용한다. 외부 입력의 런타임 검증을 TypeScript 타입 선언만으로 대신하지 않는다. [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering), [calculateMetadata](https://www.remotion.dev/docs/calculate-metadata)

입문 예제를 확장한 `src/Root.tsx`다. `seconds`를 JSON으로 받아 1~60초 범위에서 길이를 정한다. 아래 수동 검증은 원리를 보여주는 작은 예제이며, 입력이 커지면 공유 schema로 분리한다.

```tsx
import {Composition} from 'remotion';
import type {CalculateMetadataFunction} from 'remotion';
import {TitleCard} from './TitleCard';
import type {TitleCardProps} from './TitleCard';

type ReportProps = TitleCardProps & {seconds: number};
const FPS = 30;

const Report = ({title, accent}: ReportProps) => (
  <TitleCard title={title} accent={accent} />
);

const calculateMetadata: CalculateMetadataFunction<ReportProps> = ({props}) => {
  if (
    typeof props.title !== 'string' || props.title.trim().length === 0 ||
    typeof props.accent !== 'string' || !/^#[0-9a-f]{6}$/i.test(props.accent) ||
    typeof props.seconds !== 'number' || !Number.isFinite(props.seconds) ||
    props.seconds < 1 || props.seconds > 60
  ) {
    throw new Error('Invalid report props');
  }
  return {
    fps: FPS,
    durationInFrames: Math.round(props.seconds * FPS),
    props: {...props, title: props.title.trim()},
  };
};

export const RemotionRoot = () => (
  <Composition
    id="Report"
    component={Report}
    width={1920}
    height={1080}
    fps={FPS}
    durationInFrames={150}
    defaultProps={{title: 'Monthly report', accent: '#86efac', seconds: 5}}
    calculateMetadata={calculateMetadata}
  />
);
```

`props.json`에 `"seconds": 8`을 추가하고 id를 `Report`로 렌더링하면 240 frames가 된다. 음수·문자열 길이 입력은 에러가 나야 한다. 외부 API의 데이터가 매번 달라지면 재렌더 결과도 달라질 수 있으므로 렌더링에 사용한 입력 snapshot을 남긴다.

## 2. Sequence의 로컬 시간

```tsx
import {Sequence} from 'remotion';
import {TitleCard} from './TitleCard';

export const TwoScenes = () => (
  <>
    <Sequence from={0} durationInFrames={60}>
      <TitleCard title="Summary" accent="#7dd3fc" />
    </Sequence>
    <Sequence from={60} durationInFrames={90}>
      <TitleCard title="Results" accent="#86efac" />
    </Sequence>
  </>
);
```

이 component를 150 frames의 Composition에 등록한다고 가정한다. 두 번째 장면은 바깥 frame 60에서 자체 frame 0으로 시작하므로 입문 예제의 fade-in을 재사용한다. `Sequence`는 시간 배치와 표시 구간을 정하며 자동으로 장면 사이 crossfade를 만들지는 않는다. [Sequence](https://www.remotion.dev/docs/sequence)

## 3. 재현 가능한 frame 만들기

| 흔한 원인 | 적용할 원칙 |
|---|---|
| `Math.random()`에 따라 입자가 바뀜 | `random('particle-1')`처럼 고정 seed 사용 |
| wall-clock이나 timer 기반 motion | frame·fps에서 위치와 스타일 계산 |
| font 로딩 전 캡처 | `@remotion/fonts`의 `loadFont()` 등 로딩 완료를 기다리는 경로 사용 |
| 외부 데이터·이미지 변경 | 입력 snapshot과 asset 버전 보관 |
| 패키지 버전 혼합 | `remotion`과 모든 `@remotion/*`를 동일한 exact version으로 고정 |

고정 seed는 랜덤 값을 안정화하지만 OS·폰트·브라우저까지 자동으로 통일하지는 않는다. 동일 환경에서 대표 frame을 비교하고, 환경을 바꿨다면 새로 검증한다. [random](https://www.remotion.dev/docs/random), [loadFont](https://www.remotion.dev/docs/fonts-api/load-font), [Renderer](https://www.remotion.dev/docs/renderer)

## 4. Node.js 서버 export 흐름

```text
입력 검증 → render job 생성 → queue
    → bundle 또는 배포된 serveUrl 확보
    → selectComposition({serveUrl, id, inputProps})
    → renderMedia({serveUrl, composition, inputProps, ...})
    → 결과 저장 → 진행 상태 / 다운로드 제공
```

`selectComposition()`은 id에 해당하는 composition과 입력에 따른 metadata를 해석한다. `renderMedia()`에도 **동일한 inputProps**를 전달해야 내용과 길이 계산이 맞는다. `serveUrl`은 Remotion bundle의 로컬 경로나 배포 URL을 가리키며 일반 앱의 임의 페이지 URL과 구분한다. [selectComposition](https://www.remotion.dev/docs/renderer/select-composition), [renderMedia](https://www.remotion.dev/docs/renderer/render-media)

서비스 설계에서 추가할 항목은 다음과 같다. 아래는 framework가 모두 자동 제공한다는 뜻이 아니라 운영 설계 예시다.

- job 상태를 `queued → rendering → succeeded / failed`로 기록한다.
- 일시적인 asset 다운로드 실패와 잘못된 props를 구분해 재시도한다.
- 같은 job의 중복 요청이 결과 파일을 충돌시키지 않게 식별자를 둔다.
- job별 입력, 템플릿 버전, 처리 시간, 실패 원인을 남긴다.
- 비용은 render 시간뿐 아니라 대기 시간·저장·전송을 함께 측정한다.

## 5. Player와 client export 연결

Player에는 component, inputProps, fps, 크기, 길이를 넘긴다. 사용자가 props를 수정하면 preview가 바뀐다. Player 자체는 최종 파일을 만드는 renderer가 아니며, Composition의 `calculateMetadata()`가 Player에서 자동 실행된다고 가정해서도 안 된다. 동적 설정은 앱에서 계산하고 일치시킨다. [Player](https://www.remotion.dev/docs/player), [calculateMetadata](https://www.remotion.dev/docs/calculate-metadata)

`@remotion/web-renderer`는 component와 영상 설정을 직접 받아 브라우저에서 export한다. `v4.0.491`부터 stable이지만 기본 Canvas 재구성 경로에는 CSS 제약이 있다. 선택적인 HTML-in-canvas 경로의 제약은 별도로 확인한다. [Client-side rendering](https://www.remotion.dev/docs/client-side-rendering), [Limitations](https://www.remotion.dev/docs/client-side-rendering/limitations)

| 비교 항목 | 확인 방법 |
|---|---|
| 스타일 재현 | font, 줄바꿈, `perspective`, `object-position`이 있는 대표 frame 비교 |
| codec·container | 목표 브라우저에서 실제 파일 생성·재생 확인 |
| 외부 asset | URL 접근, CORS, 로딩 실패 조건 확인 |
| 성능 | 긴 영상·고해상도에서 메모리, 소요 시간, UI 반응 측정 |
| 설정 일치 | preview와 export에 같은 props·fps·길이·크기 전달 |

## 6. 심화 완료 조건

- [ ] `seconds: 8`로 8초 영상이 나오고 잘못된 입력은 실패한다.
- [ ] 두 번째 Sequence의 local frame과 전체 frame을 구분한다.
- [ ] font·seed·asset·패키지 버전을 고정한 대표 frame을 보관했다.
- [ ] preview, server export, client export 중 지원할 경로를 정했다.
- [ ] 운영 경로는 [[tech/devtools/remotion/02-ecosystem|인프라 비교]]와 실제 측정 결과로 선택했다.

## Sources

- [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering)
- [calculateMetadata](https://www.remotion.dev/docs/calculate-metadata)
- [Sequence](https://www.remotion.dev/docs/sequence)
- [random](https://www.remotion.dev/docs/random)
- [loadFont](https://www.remotion.dev/docs/fonts-api/load-font)
- [Renderer](https://www.remotion.dev/docs/renderer)
- [selectComposition](https://www.remotion.dev/docs/renderer/select-composition)
- [renderMedia](https://www.remotion.dev/docs/renderer/render-media)
- [Player](https://www.remotion.dev/docs/player)
- [Client-side rendering](https://www.remotion.dev/docs/client-side-rendering)
- [Client-side limitations](https://www.remotion.dev/docs/client-side-rendering/limitations)
- [서버 렌더링 비교](https://www.remotion.dev/docs/compare-ssr)
