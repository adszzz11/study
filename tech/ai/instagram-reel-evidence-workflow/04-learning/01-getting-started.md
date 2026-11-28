---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기 — 증거를 받았을 때

1. 제공받은 캡처·자막·전사본을 원본 그대로 보관하고, 전달 경로와 수신 시각을 기록한다.
2. 영상 파일이 있으면 hash와 기본 메타데이터를 먼저 얻는다.

```sh
shasum -a 256 reel.mp4
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height \
  -of default=noprint_wrappers=1 reel.mp4
ffmpeg -i reel.mp4 -vf fps=1 frames/frame-%03d.png
```

3. 증거 표를 만든다. `관찰`은 보이는/들리는 사실, `해석`은 검증 대기 주장으로 분리한다.

| ID | 위치 | 관찰 | 해석/검증 상태 |
| --- | --- | --- | --- |
| E-01 | 00:00–00:03 | 예: 화면에 보이는 정확한 문자열 | 공식 출처 확인 전에는 미확정 |

4. 자막 또는 전사본의 각 문장을 timestamp와 연결한다. OCR·ASR 오류, 편집된 구간, 들리지 않는 구간은 명시한다.
5. 제품명이나 URL이 확인된 뒤에만 공식 문서와 릴리스 노트로 주장 검증을 시작한다.

완료 후 [[tech/ai/instagram-reel-evidence-workflow/04-learning/02-deep-dive|Deep dive]]에서 evidence-to-claim 연결을 만든다.
