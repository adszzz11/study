---
date: 2026-09-20
tags: [tech]
type: tech-tool-study
status: draft
---

# Reel Tool Study 치트시트

> [[README|목차로 돌아가기]]

## 현재 상태

```text
shortcode: DddvxSdAIrG
topic: unknown
status: blocked by missing content artifact
do not: infer a tool from the URL alone
```

## 가장 필요한 입력

```text
영상 파일 > 핵심 화면 캡처 > 캡션 전문 > 기술명
```

## 5분 식별 체크리스트

- [ ] title frame을 읽는다.
- [ ] logo, domain, package name을 찾는다.
- [ ] caption과 overlay text를 분리해 전사한다.
- [ ] creator의 주장에 timestamp를 붙인다.
- [ ] official domain에서 기술명과 vendor를 대조한다.
- [ ] 확신이 없으면 `unknown`으로 둔다.

## Claim 검증

| 확인 대상 | 질문 |
|---|---|
| Feature | 어느 version/plan에서 지원하는가? |
| Performance | baseline과 측정 조건은 무엇인가? |
| Cost | 과금 단위와 제외 비용은 무엇인가? |
| Security | 데이터가 어디에 저장되고 얼마나 유지되는가? |
| Integration | 필요한 SDK, API, protocol은 무엇인가? |

## 판정값

```text
supported    공식 근거와 재현이 지지
qualified    조건을 붙이면 성립
contradicted 공식 근거 또는 재현과 충돌
unknown      근거 부족
```

## 기록 template

```markdown
- Claim:
- Timestamp:
- Exact wording:
- Official source:
- Version/date:
- Reproduction:
- Verdict:
- Caveat:
```

## Sources

- [원본 Instagram Reel](https://www.instagram.com/reel/DddvxSdAIrG/)
- 사용자 제공 dossier
