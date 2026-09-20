---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# 시작하기: Reel에서 기술 주제 식별하기

> [[../README|목차로 돌아가기]] | [[02-deep-dive|다음: 심화]]

## 목표

원본을 볼 수 없는 상태에서 추측하지 않고, 최소 artifact로 기술명과 핵심 claim을 식별한다.

## 1. 입력 artifact 확보

우선순위는 다음과 같다.

1. 영상 파일
2. 주요 장면 화면 캡처
3. caption 전문
4. 언급된 기술명

화면 캡처를 받을 때는 가능하면 다음 장면을 포함한다.

- 첫 title frame
- tool 이름 또는 logo가 보이는 frame
- code/API/UI가 보이는 frame
- 결과와 성능 수치가 보이는 frame
- 마지막 CTA 또는 caption

## 2. 관찰과 해석 분리

```markdown
## Observation
- 화면에 보이는 정확한 문자열:
- 보이는 URL/domain:
- code identifier:
- UI label:

## Interpretation
- 추정 tool:
- confidence: low | medium | high
- 대안 후보:
- 확인에 필요한 공식 source:
```

`Observation`에는 보이는 사실만, `Interpretation`에는 후보와 confidence를 기록한다.

## 3. 기술명 확정

동명이인 package와 unofficial fork를 피하기 위해 세 항목 이상을 맞춘다.

- 제품명 또는 repository 이름
- vendor/organization
- official domain
- package name
- logo 또는 UI

## 4. Claim 목록 만들기

| Claim ID | 영상 주장 | 유형 | 검증 상태 |
|---|---|---|---|
| C1 | 미확인 | feature | blocked |
| C2 | 미확인 | performance | blocked |
| C3 | 미확인 | integration | blocked |

## 완료 조건

- [ ] 기술명과 vendor를 식별했다.
- [ ] Reel의 핵심 claim을 원문 의미를 보존해 적었다.
- [ ] 관찰과 해석을 분리했다.
- [ ] official URL을 하나 이상 찾았다.
- [ ] [[02-deep-dive]]로 검증을 이어갈 수 있다.

## Sources

- [원본 Instagram Reel](https://www.instagram.com/reel/DddvxSdAIrG/)
- 사용자 제공 dossier

