---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: 비교 가능한 측정 준비

다음은 확인된 실험 결과가 아니라 학습용 실습안이다. 모델과 runtime이 미상이므로 특정 설치 명령이나 다운로드 파일을 지정하지 않는다.

## 1. 수치 대응 복원

| 표기 | 모델·revision | 파일 구성 | 표현 방식 | 측정 대상 |
|---|---|---|---|---|
| 약 54GB | 미확인 | 미확인 | 미확인 | 미확인 |
| 3.6GB | 미확인 | 미확인 | 미확인 | 미확인 |
| 5.9GB | 미확인 | 미확인 | 미확인 | 미확인 |

관계가 확인되기 전에는 압축률을 계산하지 않는다. 단일 가중치 파일·전체 다운로드·실행 중 최대 메모리를 별도 측정한다. GB/GiB도 기록한다.

## 2. 실행 조건 기록

```yaml
# 실습용 기록 양식: 실제 측정값으로 채운다.
model_id: unknown
revision: unknown
source_model_id: unknown
conversion: unknown
weight_files: []
license_url: unknown
hardware: unknown  # CPU, GPU, RAM/VRAM, OS
runtime_version: unknown
prompt_set_version: unknown
sampling: unknown  # temperature, top_p, seed 등 지원 설정
max_output_tokens: unknown
attempts_per_problem: unknown
```

## 3. 작은 평가 세트 작성

- 함수 구현: 빈 입력·정상 입력·중복값을 포함한다.
- 경계값 처리: 0, 음수, 최댓값 등 요구사항에 해당하는 조건을 테스트한다.
- 버그 수정: 재현 테스트와 기존 동작 회귀 테스트를 함께 준비한다.

예: `clamp(x, lo, hi)`는 `lo <= hi`일 때 범위를 벗어난 값을 경계로 제한한다. `lo > hi`는 `ValueError`로 정한다. 모델에는 함수 명세를 주고 평가 테스트는 별도 보관한다.

```python
# candidate는 생성 결과에서 가져온 함수. 분리된 실행 환경에서 실행한다.
assert candidate.clamp(5, 0, 10) == 5
assert candidate.clamp(-1, 0, 10) == 0
assert candidate.clamp(11, 0, 10) == 10
assert candidate.clamp(3, 3, 3) == 3
try:
    candidate.clamp(0, 2, 1)
except ValueError:
    pass
else:
    raise AssertionError('expected ValueError')
```

## 4. 첫 측정

호환성을 확인하고 짧은 입력으로 로딩·생성을 시도한다. 생성 코드는 timeout과 자원 제한을 둔 분리 환경에서 테스트한다. 같은 prompt·출력 한도·시도 횟수를 두 모델에 적용한다. 생성 실패와 테스트 실패를 모두 기록한다.

## 완료 체크

- [ ] 모델 쌍의 관계 또는 관계 미확인을 명시했다.
- [ ] 테스트와 성공 기준을 생성 전에 정했다.
- [ ] 장치·runtime·생성 설정을 기록했다.
- [ ] 파일 크기·최대 메모리·생성 시간을 구분했다.

[[tech/ai/model-compression-coding-evaluation/04-learning/02-deep-dive|심화 실험으로 이동]] · [[tech/ai/model-compression-coding-evaluation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 원영상 URL·모델 배포 URL이 제공되지 않음. 아래 링크는 보충 학습 자료이며 영상의 모델·수치를 입증하지 않는다.
- HumanEval 공식 저장소: https://github.com/openai/human-eval — 코드 생성 결과를 실행 테스트로 평가하는 참고 자료.
- llama.cpp 공식 저장소: https://github.com/ggml-org/llama.cpp — 로컬 inference runtime 조사 출발점. 대상 모델과의 호환성은 별도 확인.
- Apache License 2.0 원문: https://www.apache.org/licenses/LICENSE-2.0 — 개별 가중치에 적용되는지는 배포물에서 확인.
