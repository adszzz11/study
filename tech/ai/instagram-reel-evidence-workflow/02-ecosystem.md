---
date: 2026-11-10
tags: [tech]
type: tech-tool-study
status: draft
---

# Ecosystem — evidence extraction tools

| 단계 | 선택지 | 강점 | 주의점 |
| --- | --- | --- | --- |
| 영상 검사 | FFmpeg/ffprobe | codec·duration·frame 추출 | 콘텐츠 의미를 해석하지 않는다. |
| 음성 전사 | Whisper | 로컬 전사와 segment timestamp | 고유명사·다국어는 사람이 교정한다. |
| 화면 문자 | Tesseract OCR | frame의 UI·자막 텍스트화 | 작은 글자·모션 블러에 취약하다. |
| 문서 정규화 | MarkItDown | 검증용 공식 문서를 Markdown으로 수집 | 영상 자체를 검증하지 않는다. |
| provenance | W3C PROV / SHA-256 | artifact와 활동의 관계 표현 | hash만으로 출처의 진위를 보장하지 않는다. |

실무에서는 자동 추출 결과를 사실로 취급하지 말고, frame·timestamp와 함께 사람 검토를 통과시킨다. 비교 기준과 주장 검증 절차는 [[tech/ai/instagram-reel-evidence-workflow/04-learning/02-deep-dive|Deep dive]]를 따른다.
