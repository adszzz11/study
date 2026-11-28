---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

| 목적 | 명령/기준 |
| --- | --- |
| 파일 동일성 | `shasum -a 256 reel.mp4` |
| 메타데이터 | `ffprobe -v error -show_format -show_streams reel.mp4` |
| frame 추출 | `ffmpeg -i reel.mp4 -vf fps=1 frames/%03d.png` |
| 증거 인용 | `E-ID + timestamp + frame/자막 줄` |
| 주장 상태 | `supported` / `contradicted` / `insufficient` |
| 주제 미확인 | `unknown — evidence required` |

## 발표 전 점검

- [ ] Reel URL만으로 영상 내용을 추론하지 않았는가?
- [ ] 자동 전사/OCR의 오류를 사람이 검토했는가?
- [ ] 제품 claim을 공식 URL로 재확인했는가?
- [ ] 민감한 원본·개인 정보를 public vault에 넣지 않았는가?

전체 흐름은 [[tech/ai/instagram-reel-evidence-workflow/README|README]]와 [[tech/ai/instagram-reel-evidence-workflow/03-references|References]]에서 다시 확인한다.
