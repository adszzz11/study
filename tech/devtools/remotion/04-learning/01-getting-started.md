---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Remotion — Getting started

[[tech/devtools/remotion/README|학습 진입점]] · 다음: [[tech/devtools/remotion/04-learning/02-deep-dive|Deep dive]]

## 목표와 준비

**문구와 색상을 JSON으로 바꿀 수 있는 5초 타이틀 영상을 MP4로 출력한다.** React component, TypeScript props, 기본 CSS를 알고 있다고 가정한다.

아래 파일과 명령은 **별도 실습 프로젝트**에서 사용한다. vault에는 학습 노트만 둔다. 예제는 공식 API를 바탕으로 작성했으며 이 노트 작성 과정에서 실제 영상 렌더링은 실행하지 않았다.

- Node.js와 npm을 준비한다. OS별 요구사항은 [공식 설치 문서](https://www.remotion.dev/docs/)에서 확인한다.
- `@latest`는 실행 시점에 따라 결과가 바뀐다. 생성된 `package.json`과 lockfile에 실제 버전을 기록한다.
- 조사 기준 `v4.0.522`. `remotion`과 설치된 모든 `@remotion/*`는 같은 정확한 버전을 사용한다. `^`나 `~`로 서로 다른 버전이 섞이지 않게 한다.

## 1. 프로젝트 생성

```bash
npx create-video@latest
# wizard에서 프로젝트 이름 my-video, Blank template, npm 선택
cd my-video
npm install
npm run dev
```

Studio가 열리면 프로젝트 생성에 성공한 것이다. wizard에서 다른 이름을 선택했다면 `cd` 대상도 바꾼다. 이 실습은 일반 Remotion template 기준이다. Next.js·React Router 앱 template은 Studio 실행 script가 다를 수 있다. [프로젝트 생성](https://www.remotion.dev/docs/)

## 2. 타이틀 component 작성

`src/TitleCard.tsx`를 작성한다. frame `0 → 20`에서 제목이 나타나고, 이후에는 그대로 유지된다.

```tsx
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
} from 'remotion';

export type TitleCardProps = {
  title: string;
  accent: string;
};

export const TitleCard = ({title, accent}: TitleCardProps) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#101827',
        color: accent,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 80,
        fontFamily: 'sans-serif',
      }}
    >
      <div style={{fontSize: 80, textAlign: 'center', opacity}}>
        {title}
      </div>
    </AbsoluteFill>
  );
};
```

`setTimeout()`이나 CSS animation의 경과 시간에 의존하지 않고 현재 frame에서 opacity를 계산한다. Studio에서 앞뒤로 seek해도 같은 frame은 같은 값을 낸다. [Animating properties](https://www.remotion.dev/docs/animating-properties)

## 3. Composition과 entry 등록

`src/Root.tsx`를 다음 내용으로 구성한다.

```tsx
import {Composition} from 'remotion';
import {TitleCard} from './TitleCard';

export const RemotionRoot = () => (
  <Composition
    id="TitleCard"
    component={TitleCard}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={150}
    defaultProps={{title: 'My first video', accent: '#7dd3fc'}}
  />
);
```

`src/index.ts`가 다음과 같이 root를 등록하는지 확인한다. 이미 존재하면 중복 등록하지 않는다.

```ts
import {registerRoot} from 'remotion';
import {RemotionRoot} from './Root';

registerRoot(RemotionRoot);
```

`150 / 30 = 5초`, 마지막 frame은 `149`다. Studio에서 `TitleCard`를 선택하고 frame `0`, `10`, `20`, `149`를 확인한다. [Fundamentals](https://www.remotion.dev/docs/the-fundamentals)

## 4. JSON으로 개인화하고 export

실습 프로젝트 루트에 `props.json`을 만든다.

```json
{
  "title": "이번 달 리포트",
  "accent": "#86efac"
}
```

프로젝트 루트에서 실행한다.

```bash
mkdir -p out
npx remotion render src/index.ts TitleCard out/title.mp4 --props=props.json --codec=h264
npx remotion still src/index.ts TitleCard out/title.png --props=props.json --frame=20
```

`--props`는 JSON 파일 경로를 받는다. 같은 component로 문구·색상만 다른 영상을 만들 수 있다. `still`은 특정 frame의 이미지를 뽑아 빠르게 확인할 때 유용하다. [CLI render](https://www.remotion.dev/docs/cli/render), [CLI still](https://www.remotion.dev/docs/cli/still)

## 5. 결과 확인

- [ ] MP4가 1920×1080, 30fps, 5초로 출력된다.
- [ ] 첫 frame의 제목은 보이지 않고, frame 20 이후에는 완전히 보인다.
- [ ] JSON 문구와 색상이 출력에 반영된다.
- [ ] 한글이 깨지지 않고 긴 제목이 영역 밖으로 넘치지 않는다.
- [ ] `out/title.png`와 Studio의 frame 20을 비교했다.

기본 `sans-serif`는 운영체제에 따라 달라질 수 있다. 같은 결과가 필요하면 한글 glyph를 포함하는 고정 font asset과 로딩 처리를 추가한다. 다음 노트에서 다룬다.

## 자주 막히는 지점

| 증상 | 먼저 확인할 것 |
|---|---|
| composition을 찾지 못함 | entry 경로, `registerRoot()`, id의 대소문자 |
| 5초가 아닌 길이 | `durationInFrames / fps` 계산 |
| props가 반영되지 않음 | 현재 작업 경로, JSON 문법, `--props` 경로 |
| 한글 또는 줄바꿈 차이 | font asset과 설치 환경, 글자 수·너비 |
| preview는 정상인데 export는 다름 | 사용한 렌더링 경로, 지원 CSS, asset 로딩 |

## Sources

- [프로젝트 생성](https://www.remotion.dev/docs/)
- [Fundamentals](https://www.remotion.dev/docs/the-fundamentals)
- [Animating properties](https://www.remotion.dev/docs/animating-properties)
- [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering)
- [Renderer — 버전 일치 안내](https://www.remotion.dev/docs/renderer)
- [CLI render](https://www.remotion.dev/docs/cli/render)
- [CLI still](https://www.remotion.dev/docs/cli/still)
- [loadFont](https://www.remotion.dev/docs/fonts-api/load-font)
