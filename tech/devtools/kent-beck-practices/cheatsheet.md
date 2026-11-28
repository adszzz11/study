---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet — 작은 변경의 판단 기준

> **근거 범위:** 제공된 dossier는 수집 자료 없이 일반 지식으로 작성된 잠정 정리다. 인물의 기여·저술·개념의 정확한 표현은 확인 필요하다. 해석과 실습 제안은 Kent Beck의 직접적인 발언이나 권고가 아니다.

## Red–Green–Refactor

```text
Red      새 동작을 구체화 → 의도한 이유의 실패 확인
Green    해당 동작을 만족하는 작은 구현 → 전체 관련 테스트
Refactor 동작 유지 → 이름·중복·책임 개선 → 재검증
```

## 작업 체크리스트

- [ ] 이번 변경의 관찰 가능한 동작을 한 문장으로 설명한다.
- [ ] 환경 오류와 assertion 실패를 구분한다.
- [ ] 정상 사례뿐 아니라 경계·오류 사례를 검토한다.
- [ ] 구조 변경과 동작 변경의 의도를 구분한다.
- [ ] 테스트가 내부 구현을 불필요하게 고정하지 않는지 본다.
- [ ] DB·외부 API 등 실제 의존성 검증의 공백을 적는다.
- [ ] 보안·성능·migration·복구에 별도 검토가 필요한지 본다.

## 증상별 다음 행동

| 증상 | 다음 확인 |
|---|---|
| 테스트가 너무 느림 | unit과 integration 책임, 실행 병목 |
| Refactoring마다 테스트 수정 | 내부 호출·private 구조 결합 |
| mock 테스트만 통과 | 실제 계약·저장소 검증 |
| 통합 때 충돌 집중 | 변경 크기·통합 빈도·대기 |
| 테스트는 통과하지만 요구 불일치 | 사용자 예시·acceptance 기준 |

**기억할 한계:** 테스트 통과는 작성한 사례의 증거다. 작은 변경은 전체 시스템 검토를 대체하지 않는다. 위 내용은 학습용 정리이며 Beck의 직접 인용이 아니다.

[[tech/devtools/kent-beck-practices/04-learning/01-getting-started|실습]] · [[tech/devtools/kent-beck-practices/03-references|근거 확인]] · [[tech/devtools/kent-beck-practices/README|학습 경로]]

## Sources

- 제공된 dossier: URL 없음. 일반 지식 기반 잠정 정리이며 인용 가능한 수집 자료는 제공되지 않았다.
- 확인할 자료 후보: https://www.kentbeck.com/ — 인물·저술 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://martinfowler.com/bliki/TestDrivenDevelopment.html — TDD 개념 확인용. 이 노트 작성 시 원문 미검증.
- 확인할 자료 후보: https://refactoring.com/ — Refactoring 개념 확인용. 이 노트 작성 시 원문 미검증.
