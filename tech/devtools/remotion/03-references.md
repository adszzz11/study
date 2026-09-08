---
date: 2026-09-09
tags: [tech]
type: tech-tool-study
status: draft
---

# Remotion — References

[[tech/devtools/remotion/README|학습 진입점]] · 다음: [[tech/devtools/remotion/04-learning/01-getting-started|Getting started]]

## 읽는 순서

| 단계 | 공식 자료 | 읽고 답할 질문 |
|---|---|---|
| 1 | [설치](https://www.remotion.dev/docs/) | 프로젝트 생성과 Studio 시작 방법은? |
| 2 | [Fundamentals](https://www.remotion.dev/docs/the-fundamentals) | frame과 Composition의 관계는? |
| 3 | [Animating properties](https://www.remotion.dev/docs/animating-properties) · [Sequence](https://www.remotion.dev/docs/sequence) | 장면과 motion을 어떻게 분리하는가? |
| 4 | [Parameterized videos](https://www.remotion.dev/docs/parameterized-rendering) | 외부 데이터를 어떻게 전달·변환하는가? |
| 5 | [calculateMetadata](https://www.remotion.dev/docs/calculate-metadata) | 내용에 따라 길이를 어떻게 바꾸는가? |
| 6 | [Render](https://www.remotion.dev/docs/render) · [Renderer](https://www.remotion.dev/docs/renderer) | CLI와 서버 export는 어떻게 연결되는가? |
| 7 | [Player](https://www.remotion.dev/docs/player) | 앱 안에 preview를 어떻게 넣는가? |
| 8 | [Client-side rendering](https://www.remotion.dev/docs/client-side-rendering) · [Limitations](https://www.remotion.dev/docs/client-side-rendering/limitations) | 브라우저 export에 어떤 제약이 있는가? |

## 구현 중 찾아볼 자료

- CLI: [render](https://www.remotion.dev/docs/cli/render), [still](https://www.remotion.dev/docs/cli/still)
- 서버 API: [selectComposition](https://www.remotion.dev/docs/renderer/select-composition), [renderMedia](https://www.remotion.dev/docs/renderer/render-media)
- 재현성: [random](https://www.remotion.dev/docs/random), [loadFont](https://www.remotion.dev/docs/fonts-api/load-font)
- 운영 선택: [Server-side rendering 비교](https://www.remotion.dev/docs/compare-ssr)
- agent 활용: [Agent Skills](https://www.remotion.dev/docs/ai/skills)

## 오래된 자료를 읽는 기준

조사일은 **2026-09-09**, 확인한 release는 **v4.0.522**다. 다음 세 가지를 먼저 확인한다.

1. 예제의 `remotion`과 `@remotion/*` 버전이 서로 같은가? 재현 시 정확한 버전과 lockfile을 보관한다.
2. Media Parser를 신규 구현에 사용하고 있는가? 공식 phase-out 안내와 Mediabunny 전환 문서를 대조한다.
3. Player preview를 export로 설명하거나 client export가 모든 CSS를 지원한다고 가정하는가? 렌더링 경로와 제약 문서로 확인한다.

제공 dossier의 마지막 생태계 문장은 중간에서 끝나므로, 이 노트의 생태계 정리는 공식 Player·설치·Blog·Agent Skills 문서로 보완했다. Media Parser의 `2026-02-01` deprecated 날짜는 공식 Mediabunny 전환 공지의 후속 note로 확인했다. 같은 글에 남은 초기 발표 문장과 후속 상태 안내를 구분해 읽는다.

## 업데이트할 때

- [ ] Release에서 현재 버전과 변경 내용을 확인한다.
- [ ] server/client 양쪽의 API·지원 범위가 달라졌는지 본다.
- [ ] 대표 frame과 실제 MP4를 다시 비교한다.
- [ ] 공식 사실과 자체 성능 측정·설계 판단을 구분해 기록한다.

## Sources

- [공식 Documentation](https://www.remotion.dev/docs/)
- [공식 Blog](https://www.remotion.dev/blog)
- [GitHub Releases](https://github.com/remotion-dev/remotion/releases)
- [v4.0.522](https://github.com/remotion-dev/remotion/releases/tag/v4.0.522)
- [Renderer — 패키지 버전 일치 안내](https://www.remotion.dev/docs/renderer)
- [Mediabunny 전환 공지](https://www.remotion.dev/blog/mediabunny)
- [Media Parser — phase-out 안내](https://www.remotion.dev/docs/media-parser)
- [Client-side limitations](https://www.remotion.dev/docs/client-side-rendering/limitations)
