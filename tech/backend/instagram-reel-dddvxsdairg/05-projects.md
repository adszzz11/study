---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 실전 프로젝트

> [[README|목차로 돌아가기]]

## 프로젝트 1: Capture-to-Note

Reel artifact를 받아 검증 가능한 Tool Study로 변환한다.

### 입력

- 화면 캡처, 영상 파일, caption 전문, 기술명 중 하나
- 원본 Reel URL

### 산출물

- 기술명·vendor·official URL
- timestamp가 포함된 핵심 claim 목록
- official docs 5개 이상의 source register
- 경쟁 또는 대안 tool 2개 비교
- 최소 실행 예제와 limitation
- 갱신된 `README.md` 및 학습 문서

### 작업 순서

- [ ] artifact의 provenance와 수집일을 기록한다.
- [ ] OCR/transcription 결과를 원본 frame과 대조한다.
- [ ] 기술명과 official domain을 확정한다.
- [ ] claim을 feature, performance, cost, security, integration으로 분류한다.
- [ ] official docs와 release notes로 검증한다.
- [ ] 재현 가능한 최소 예제를 작성한다.
- [ ] 각 claim을 `supported`, `qualified`, `contradicted`, `unknown`으로 판정한다.

## 프로젝트 2: Access Failure Log

콘텐츠 접근 실패를 재사용 가능한 진단 기록으로 만든다.

```yaml
attempt:
  source: instagram-reel
  method: unauthenticated-web | exact-search | embed | local-browser
  observed_at: YYYY-MM-DD
  result: success | empty | error
  error_code: null
  artifact_saved: false
  next_action: request-screenshot
```

성공하지 않은 요청도 반복 작업을 줄이는 증거다. 단, "검색 결과 없음"을 "콘텐츠가 존재하지 않음"으로 해석하지 않는다.

## Acceptance criteria

| 기준 | 통과 조건 |
|---|---|
| 식별 | tool과 vendor가 official source로 확인됨 |
| 정확성 | 영상 주장과 노트의 요약이 구분됨 |
| 최신성 | version/date가 각 주요 claim에 연결됨 |
| 재현성 | 명령, 환경, 기대 결과가 기록됨 |
| 안전성 | secret·개인정보·비공개 session이 포함되지 않음 |

## Sources

- [원본 Instagram Reel](https://www.instagram.com/reel/DddvxSdAIrG/)
- 사용자 제공 dossier

