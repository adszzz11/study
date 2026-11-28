---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 근거와 확인할 자료

## 원자료 상태

사용자 제공 dossier를 기반으로 작성했다. 원영상 URL, 모델명, 배포 파일, 평가 표는 제공되지 않았다. 아래 보충 링크로 영상의 정체나 결과를 대신 확정하지 않는다.

| 주장·단서 | 현재 상태 | 추가로 필요한 근거 |
|---|---|---|
| 54GB·3.6GB·5.9GB | 표기 등장 | 각 모델 식별자·파일 목록·측정 단위 |
| 세 가지 값 | 설명 등장 | 논문·알고리즘·적용 범위·scale |
| 코딩 성능 | 주제로 언급 | 문제·prompt·생성 설정·테스트·결과 |
| 노트북 실행 | 질문으로 등장 | 장치 사양·runtime 버전·실측 로그 |
| Apache 2.0 가중치 | 언급 | 공식 배포 페이지·해당 파일의 라이선스 |
| 문서 로컬 처리 | 클라우드와 대비 | 데이터 흐름·외부 통신 관찰·설정 |

## 보충 자료 읽는 법

- HumanEval: 실행 기반 평가의 구성과 판정 방법을 학습한다. 자체 소규모 테스트 결과를 공식 benchmark 점수로 부르지 않는다.
- llama.cpp: 실제 선택한 모델 형식과 하드웨어 지원 여부를 확인한다. 저장 용량에서 처리 속도를 역산하지 않는다.
- Apache License 2.0: 일반 라이선스 원문을 읽되, 대상 배포물에 적용되는지 별도로 확인한다.

## 기록 원칙

출처 URL·확인 날짜·모델 revision·파일 checksum을 남긴다. 미확인은 빈칸 대신 `미확인`으로 기록한다. 새 근거를 확보하면 관찰 결과와 해석을 구분해 갱신한다.

[[tech/ai/model-compression-coding-evaluation/README|학습 경로]]

## Sources

- 사용자 제공 dossier: 원영상 URL·모델 배포 URL이 제공되지 않음. 아래 링크는 보충 학습 자료이며 영상의 모델·수치를 입증하지 않는다.
- HumanEval 공식 저장소: https://github.com/openai/human-eval — 코드 생성 결과를 실행 테스트로 평가하는 참고 자료.
- llama.cpp 공식 저장소: https://github.com/ggml-org/llama.cpp — 로컬 inference runtime 조사 출발점. 대상 모델과의 호환성은 별도 확인.
- Apache License 2.0 원문: https://www.apache.org/licenses/LICENSE-2.0 — 개별 가중치에 적용되는지는 배포물에서 확인.
