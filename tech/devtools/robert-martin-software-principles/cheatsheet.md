---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet: 변경하기 전에 묻기

| 상황 | 질문 | 가능한 다음 행동 |
|---|---|---|
| 함수가 이해되지 않음 | 이름이 의도와 결과를 드러내는가? | 이름·제어 흐름 정리 |
| 모듈이 자주 바뀜 | 서로 다른 변경 이유가 섞였는가? | SRP 관점으로 책임 분리 |
| 조건 분기 반복 | 실제 반복되는 변화가 있는가? | OCP 관점으로 확장 지점 검토 |
| 구현 교체 후 장애 | 행동 계약이 유지되는가? | LSP 계약 테스트 |
| client가 불필요한 기능에 묶임 | 꼭 필요한 계약만 쓰는가? | ISP 관점으로 계약 축소 |
| 정책 테스트에 ORM 필수 | source dependency가 어디를 향하는가? | DIP, 내부 계약·외부 adapter |
| 테스트가 refactoring을 방해 | 내부 구조를 고정했는가? | 관찰 가능한 행동 중심으로 수정 |
| 계층마다 상용구 증가 | 경계가 실제 변경을 막는가? | 구조 축소·응집성 재검토 |

## Dependency Rule

```text
외부 세부사항 -> 내부 정책
runtime 호출 방향과 source-code dependency 방향은 다를 수 있다.
```

## TDD

**Red → Green → Refactor**: 실패하는 행동 테스트 → 최소 구현 → 행동 유지하며 구조 개선.

## 피할 오해

- SRP = 메서드 하나인 클래스: 아님. 변경 이유를 살핀다.
- DIP = 모든 클래스에 interface: 아님. 필요한 경계를 식별한다.
- Clean Architecture = 네 개 폴더: 아님. 실제 import·타입 의존을 확인한다.
- Unit test 통과 = 연동 보장: 아님. SQL·transaction·wiring은 별도 검증한다.
- 작은 함수 = 항상 좋은 코드: 아님. 응집성과 읽기 흐름도 본다.

## Review 체크리스트

- [ ] 응집성: 함께 바뀌는 코드가 가까운가?
- [ ] 결합도: 외부 기술 변경이 정책에 새어 들어오는가?
- [ ] 행동 계약: 대체 구현도 호출자 가정을 지키는가?
- [ ] Side effect: 계산과 I/O 경계를 설명할 수 있는가?
- [ ] Test boundary: 테스트가 보장하지 못하는 범위를 아는가?
- [ ] 비용: 경계가 줄인 변경 비용과 늘린 복잡성을 함께 기록했는가?

## Navigation

[[tech/devtools/robert-martin-software-principles/README|학습 경로로 돌아가기]]

## Sources

- 근거: 사용자 제공 dossier(공개 URL 미제공), 기존 지식에 기반한 개념 분석.
- 출처 URL: 제공된 URL 없음. 웹 검색 및 URL 열기를 수행하지 않았으며 URL을 임의로 생성하지 않았다.
- 직접 인용, 최신 동향, 정량적 생산성 효과, 프로젝트별 적용 성과는 검증하지 않았다. 해당 주장은 **확인 필요**다.
