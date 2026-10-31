---
date: 2026-10-27
tags: [tech]
type: tech-tool-study
status: draft
---

# .llm 파일들의 생성원리

> **한 줄 정의**: `.llm`은 LLM의 표준 모델 확장자가 아니며, 실제 Local LLM 모델은 보통 checkpoint를 `GGUF`, `safetensors`, `ONNX` 같은 runtime 친화적 artifact로 직렬화·변환해 만든다.

## Overview

이 노트는 “LLM 파일을 만든다”는 말을 파일명 변경이 아니라 **학습된 tensor와 실행 metadata를 특정 runtime이 읽는 binary artifact로 packaging하는 과정**으로 설명한다.

- Local LLM 배포의 대표 결과물은 `.gguf`다.
- 학습·fine-tuning 생태계에서는 `.safetensors`와 PyTorch `state_dict`가 흔하다.
- `.llm`은 공통 LLM format이 아니다. 공개 확장자 정보에서는 Second Life의 Linden Lab Mesh 용례로 알려져 있다.

## Learning Path

- [ ] [[01-overview|What/Why와 핵심 구성요소]]
- [ ] [[02-ecosystem|파일 형식과 quantization 생태계 비교]]
- [ ] [[03-references|공식 문서와 소스 코드 읽기 순서]]
- [ ] [[04-learning/01-getting-started|작은 모델을 GGUF로 변환해 보기]]
- [ ] [[04-learning/02-deep-dive|binary layout·quantization·보안 심화]]
- [ ] [[05-projects|실습 프로젝트]]
- [ ] [[cheatsheet|Cheatsheet]]

## When To Use

- 모델을 Local PC, CPU, Metal, 또는 제한된 GPU memory에서 실행할 때
- Hugging Face checkpoint를 llama.cpp 등의 runtime에 맞춰 배포할 때
- tokenizer·architecture·quantization이 결과 품질에 미치는 영향을 조사할 때

## When Not To Use

- 확장자만 바꾸어 모델을 변환하려는 경우: format conversion은 tensor mapping과 metadata 검증을 필요로 한다.
- 출처가 불명확한 PyTorch pickle checkpoint를 바로 load하려는 경우
- training 없이 단지 API 기반 LLM을 호출하려는 경우

## Related Notes

- [[MOCs/Index]]
- [[MOCs/AI]]
- [[tech/ai/mark-it-down/README|MarkItDown]]

## Sources

- https://github.com/ggml-org/ggml/blob/master/docs/gguf.md
- https://huggingface.co/docs/hub/gguf
- https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md
- https://github.com/huggingface/safetensors/blob/main/README.md
- https://fileinfo.com/extension/llm

## Q&A

**Q:** Claude나 Codex가 가장 이해하기 쉬운 파일 형식은 무엇인가?

**A:** Claude나 Codex에 내용을 읽히고 수정하게 하려면 UTF-8 `Markdown` 같은 plain-text 형식이 가장 적합하다. 구조가 필요하면 `JSON`·`YAML`·`CSV`처럼 text로 직접 검토할 수 있는 형식을 함께 쓴다. 반면 `GGUF`, `safetensors`, `ONNX`, `.pt`는 모델 runtime이나 framework가 읽는 binary artifact이므로, 에이전트가 그 내부 weight를 사람이 읽듯 이해하는 입력 형식으로 기대하면 안 된다. 이 파일들은 metadata나 변환 결과를 확인하는 대상이며, 설명·설정·tokenizer·평가 결과는 별도 text 파일로 제공하는 편이 좋다.
