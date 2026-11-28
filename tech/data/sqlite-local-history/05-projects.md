---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Projects: 로컬 기록 저장 적용

아래는 dossier에서 착안한 실습 제안이다. 제품 구현이나 실제 저장 schema를 설명하지 않는다.

## 1. 로컬 받아쓰기 기록함

- 입력: 음성 인식으로 생성된 텍스트. 처음에는 샘플 텍스트로 대체한다.
- 저장: 사용자가 확정한 기록을 로컬 SQLite에 보관한다.
- 화면: 기록 목록과 선택한 기록의 본문을 표시한다.
- 완료 기준: 앱 재실행 후 조회, 중복 저장 정책, 삭제 결과를 확인한다.

인식 정확도보다 **한 번의 받아쓰기가 어떤 기록으로 남는가**를 먼저 명확히 한다. 구현 출발점은 [[tech/data/sqlite-local-history/04-learning/01-getting-started|최소 기록 모델]]이다.

## 2. 저장 정책 비교 실험

같은 받아쓰기의 중간 결과 시퀀스를 준비하고 전체 revision 저장과 최종 결과만 저장하는 두 DB를 만든다.

| 관찰 항목 | 기록 방법 |
|---|---|
| 기록량 | 행 수와 본문 총 길이, DB 파일 크기 측정 |
| 이해하기 쉬운 정도 | 같은 세션의 최종본을 찾는 절차 기록 |
| 수정 이력 | 이전 문장과 수정 순서를 복원할 수 있는지 확인 |
| 재시도 | 같은 요청 반복 시 중복 발생 여부 확인 |

완료 기준은 두 정책의 관찰값과 선택 이유를 표로 설명하는 것이다. 파일 크기는 페이지 할당 등의 영향도 받으므로 행 수와 함께 본다. 어느 정책이 Sokki의 실제 동작인지는 판단하지 않는다.

## 3. 화자 정보를 포함한 회의 기록 모델

Damso의 소개에서 착안해 다음 개념 모델을 설계한다.

```text
meeting 1 ── N utterance N ── 1 speaker_profile
meeting: 녹음 전 확인 상태
utterance: 발화 순서, 텍스트, 필요 시 시작·종료 시각
speaker_profile: 누적 화자 식별 정보
```

- 녹음 전 사용자 확인을 별도 상태로 두고, 동의 전 녹음이 시작되지 않는 흐름을 설계한다.
- 발화와 화자 프로필의 보관·삭제 정책을 각각 정한다.
- 완료 기준: 회의별 발화 조회, 화자별 구분, 확인 거절 시 녹음 시작 방지 흐름을 검증한다.

이는 Damso의 실제 저장 기술이나 schema를 재현하는 프로젝트가 아니다.

## 관련 노트

[[tech/data/sqlite-local-history/02-ecosystem|제품 비교의 한계]] · [[tech/data/sqlite-local-history/04-learning/02-deep-dive|정책 검토]] · [[tech/data/sqlite-local-history/README|학습 경로]]

## Sources

- 제공 dossier의 프로젝트 제안과 Damso 소개, 원자료 URL 미제공.
- SQL 구현 보충: https://www.sqlite.org/lang.html
