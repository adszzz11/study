---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Overview: What / Why / 특징

## What

모델 압축은 저장·표현 비용을 줄이는 접근이다. 파라미터 수 감소와 파라미터당 표현 비용 감소는 구분해야 한다. 코딩 평가는 생성 코드가 요구사항과 실행 테스트를 충족하는지 측정한다.

## Why

파일 크기, 기능적 품질, 실행 가능성은 서로 다른 질문이다. 작은 파일이 실행 중 작은 메모리만 사용한다거나 올바른 코드를 생성한다는 보장은 없다. 문법적으로 유효한 코드 → 실행되는 코드 → 요구사항을 충족하는 코드도 다른 수준이다.

## 핵심 특징

### 파라미터 수와 저장 비용

```text
가중치 저장 비용 ≈ 파라미터 수 × 파라미터당 표현 비용 + 부가 정보
```

이는 분석 틀이며 영상 수치를 재현한 공식이 아니다. 파일에는 scale·메타데이터 등이 포함될 수 있으며, 전체 다운로드에는 다른 파일도 포함될 수 있다.

### 세 가지 값과 ternary representation

세 값이라는 설명은 ternary representation을 조사할 단서다. 실제 세 값, 전체/부분 적용, 학습 중/학습 후 적용, 저장 표현과 연산 표현의 일치 여부, scale 필요성은 미확인이다. 특정 quantization 구현의 성능을 영상에 귀속하지 않는다.

### 저장과 실행의 분리

```text
모델 파일 식별 → runtime 호환성 → 로딩 → 고정 입력 생성
→ 코드 테스트 → 메모리·시간·성공률 비교
```

이 흐름은 제안한 검증 절차다. 확인된 구현 아키텍처가 아니다. 장치·runtime·입출력 길이가 없으면 노트북 실행 여부를 확정할 수 없다.

### 가중치 공개와 처리 경로

Apache 2.0 가중치 공개가 언급되지만 대상 모델·배포 파일·라이선스 원문 연결은 없다. 학습 데이터·학습 코드 공개 여부까지 추론할 수 없다. 가중치 접근, runtime 실행, 회사 문서의 외부 전송 여부를 각각 확인한다.

## 다음 학습

[[tech/ai/model-compression-coding-evaluation/02-ecosystem|접근과 배포 선택 비교]] · [[tech/ai/model-compression-coding-evaluation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 원영상 URL·모델 배포 URL이 제공되지 않음. 아래 링크는 보충 학습 자료이며 영상의 모델·수치를 입증하지 않는다.
- HumanEval 공식 저장소: https://github.com/openai/human-eval — 코드 생성 결과를 실행 테스트로 평가하는 참고 자료.
- llama.cpp 공식 저장소: https://github.com/ggml-org/llama.cpp — 로컬 inference runtime 조사 출발점. 대상 모델과의 호환성은 별도 확인.
- Apache License 2.0 원문: https://www.apache.org/licenses/LICENSE-2.0 — 개별 가중치에 적용되는지는 배포물에서 확인.
