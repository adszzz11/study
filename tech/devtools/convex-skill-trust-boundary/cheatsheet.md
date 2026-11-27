---
date: 2026-11-28
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: Skill 신뢰 경계 검토

## 빠른 확인

| 보이는 것 | 확인할 질문 | 잘못된 추론 |
|---|---|---|
| `telemetry` 주석 | 실제 payload에 무엇이 있는가? | 단순 실행 횟수만 전송한다 |
| `idea` POST | 수신처·목적·선택권이 고지되는가? | 전송됐으니 영구 저장됐다 |
| `curl … | bash` | 응답 코드의 버전과 검토 근거는? | HTTPS니까 코드가 안전하다 |
| 다운로드/실행 분리 | 사이에 검토·검증이 있는가? | 두 call이면 안전하다 |
| Hash pinning | 기대 hash의 신뢰 경로는? | 일치하면 악성 코드가 아니다 |
| Marketplace 등록 | 개별 동작의 검토 범위는? | 모든 동작이 보증됐다 |
| Classifier 회피 지시 | 전체 효과와 거절이 존중되는가? | 실제 우회 성공도 입증됐다 |

## 사례 기억 카드

```text
quickstart: idea + template → /generate → id → 임시 파일
add: /add-hosting 또는 /add-component → bash
labs-quickstart: classifier 차단 형태를 피하도록 call 분리 지시
분석 범위: Issue #64, revision 6ca54f6 발췌
```

## 리뷰 체크리스트

- [ ] 데이터 전송과 서버 저장을 구분했다.
- [ ] 목표 위임과 데이터·실행 권한을 구분했다.
- [ ] 검토 시점과 실행 시점 코드의 동일성을 확인한다.
- [ ] 여러 call을 전체 흐름으로 평가한다.
- [ ] 현재 상태·실제 피해·악의를 단정하지 않는다.
- [ ] 원격 실행이 거절되면 모양만 바꾸어 재시도하지 않는다.

[[tech/devtools/convex-skill-trust-boundary/03-references|근거 범위 확인]] · [[tech/devtools/convex-skill-trust-boundary/README|학습 경로]]

## Sources

- https://github.com/convex/convex-backend-skill/issues/64
