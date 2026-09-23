---
date: 2026-09-23
tags: [tech]
type: tech-tool-study
status: draft
---

# OpenCut — Getting Started

[[tech/devtools/opencut/README|학습 진입점]] · 다음: [[tech/devtools/opencut/04-learning/02-deep-dive|Deep dive]]

## 목표

classic editor에서 15–30초 길이의 짧은 영상을 만들며 `import → timeline → trim/split → text/caption → export` loop를 한 번 완주한다. 실습 시작점은 [opencut.app](https://opencut.app/)이다.

## 준비물

- 짧은 video clip 2개와 image 또는 logo 1개
- BGM 또는 voice clip 1개
- 표시할 문구 1–2개
- 출력 비율 하나: 예를 들어 Shorts/Reels용 세로 canvas

민감한 원본은 먼저 더미 asset으로 실습한다. 웹 editor의 실제 저장·처리 범위는 도입 환경에서 별도로 검증한다.

## 기본 편집 loop

1. **Import** — media를 불러오고 preview에서 재생 가능 여부를 확인한다.
2. **Timeline 배치** — 주 clip을 첫 track에 넣고, BGM·text·image를 필요한 시점의 별도 track에 둔다.
3. **Trim / split** — 시작·끝 handle로 불필요한 구간을 줄이고, 장면 전환점에서 clip을 split한다.
4. **Text / caption** — 읽기 쉬운 크기와 contrast로 제목 또는 caption을 넣는다. transcript file이 있다면 import 기반 caption 생성을 시험한다.
5. **Preview** — 전체를 재생하며 audio level, timing, safe area, text readability를 확인한다.
6. **Export** — output을 내보내고 대상 플랫폼에서 재생해 aspect ratio·audio sync·caption clipping을 검토한다.

## 검수 체크리스트

- [ ] 첫 1–2초에 핵심 message가 보인다.
- [ ] 자막이 mobile safe area와 겹치지 않는다.
- [ ] clip 경계에 의도하지 않은 blank frame 또는 audio pop이 없다.
- [ ] BGM이 narration/text 이해를 방해하지 않는다.
- [ ] export 결과가 preview와 시간·비율·가독성 면에서 일치한다.

## 작은 실습: 3장면 short

| 구간 | 구성 | 확인점 |
|---|---|---|
| 0–3초 | hook text + 주 clip | 제목 대비와 첫 frame |
| 3–12초 | 문제/과정 clip + caption | cut timing과 caption line break |
| 12–18초 | 결과 clip + CTA | logo·safe area·audio fade |

완성 파일만 남기지 말고, 사용한 input·canvas size·export 결과를 기록한다. 동일한 template을 반복할 때 비교 기준이 된다.

## Sources

- [Live classic editor](https://opencut.app/)
- [OpenCut classic repository](https://github.com/OpenCut-app/opencut-classic)
- [v0.3.0 release](https://github.com/OpenCut-app/OpenCut/releases/tag/v0.3.0)
