---
date: 2026-11-26
tags: [tech]
type: tech-tool-study
status: draft
---

# SpatialCraft Cheatsheet

## 용어 빠른 참조

| 용어 | 기억할 의미 |
|---|---|
| Frozen model | 모델 파라미터 고정; 외부 지식은 변화 가능 |
| Orchestration | 도구 선택·호출 순서·출력 해석·다음 행동 연결 |
| Rollout | 하나의 task에 대한 실행 경로 |
| Experience | 동일 task의 경로 대조로 얻은 condition-action tactic |
| Skill | activation·termination condition을 갖춘 multi-step procedure |
| Skill-anchored Experience | 연결된 Skill 활성 중에 제공되는 전술 |
| Withholding | Experience를 무작위로 제외하여 결과 차이 관찰 |
| Contrastive Utility Score | task difficulty와 기여를 분리하려는 효용 추정 장치 |
| Consolidation | 일관된 positive utility의 Experience를 Skill에 통합 |

## 핵심 순환

```text
History → rollout 대조 → Experience → Skill 연결
        → withholding 평가 → 유용한 전술 통합
```

개념 요약이며 정확한 구현 순서의 명세는 아니다.

## 주장 경계

- **보고됨**: 5 benchmarks × 4 backbones의 20개 설정 모두 최고 accuracy.
- **미확인**: 정확도 수치·개선 폭·baseline 이름·통계적 유의성·비용.
- **미확인**: 설치법·API·Utility Score 수식·제외 확률·Skill 실행 형식.
- **실습 예시**: 좌표계 일치 전술과 대상 식별 → 계산 → 해석 절차.
- **피할 해석**: frozen = 시스템 불변, memory 증가 = 성능 보장, withholding = 엄밀한 개별 인과효과 보장.

## 실행 전 점검

- [ ] 같은 task 안에서 rollout을 비교했는가?
- [ ] 도구 오류와 운용 오류를 구분했는가?
- [ ] 전술의 적용 조건과 Skill 종료 조건이 명확한가?
- [ ] 통합 전후와 별도 task의 결과를 비교했는가?
- [ ] 정확도와 호출·비용을 함께 기록했는가?

## 연결

- [[tech/ai/spatialcraft-procedural-intelligence/README|학습 경로]]
- [[tech/ai/spatialcraft-procedural-intelligence/03-references|근거와 미확인 사항]]
- [[tech/ai/spatialcraft-procedural-intelligence/04-learning/02-deep-dive|평가 실습]]

## Sources

- https://arxiv.org/abs/2611.31475 — SpatialCraft 논문. 이 노트는 제공된 초록·서지 정보 dossier에 근거하며, 전문이나 공식 코드를 검증한 결과가 아니다.
