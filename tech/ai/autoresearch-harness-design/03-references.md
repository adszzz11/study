---
date: 2026-11-25
tags: [tech]
type: tech-tool-study
status: draft
---

# References: 근거 범위와 후속 확인

## 핵심 자료

| 자료 | URL | 이 노트에서의 용도 |
|---|---|---|
| arXiv abstract 페이지 | https://arxiv.org/abs/2611.28244 | 논문 식별 및 abstract 보고 결과의 원출처 |
| DOI | https://doi.org/10.48550/arXiv.2611.28244 | 같은 논문의 영구 식별자 |

논문명: *Demystifying the Autoresearch Harness: How Context and Skills Shape Self-Evolving Agents*.

작성 근거는 사용자가 제공한 abstract·서지 정보 dossier다. 두 URL은 같은 논문을 가리키며 독립적인 검증 자료 두 개가 아니다. 저자·본문·공식 저장소·설치 명령은 제공 자료로 확인되지 않아 보충하지 않았다.

## 근거를 분리해서 읽기

| 구분 | 예시 |
|---|---|
| Abstract 보고 | 여섯 setting에서 context folding 최상위; 선택적 삭제의 평균적 우위 |
| 해석 | 실패 조건을 다시 확인하는 접근성이 유용할 수 있음 |
| 실습 제안 | JSON schema, archive 기반 삭제 후보 관리, 반복 실험과 비용 계측 |
| 확인 불가 | 통계적 유의성, 정확한 알고리즘, 세부 budget, 재현 절차 |

## 원문·코드 확보 후 확인할 항목

- [ ] 논문 버전, benchmark subset과 model별 상세 결과.
- [ ] Context folding의 저장·조회·압축·복원 알고리즘.
- [ ] Baseline과 rolling summary의 token limit·prompt·갱신 규칙.
- [ ] 19.2%의 계산식과 각 setting의 평균·분산.
- [ ] 미사용 lesson의 정의, deletion threshold, 복구 정책.
- [ ] `fast₁`의 정의와 medal rate의 평가 절차.
- [ ] AIDE·OpenEvolve 버전과 inference budget 산정 방식.
- [ ] 실행 비용·hardware·wall-clock time 및 결합 ablation.

확인 전에는 프로젝트 예제를 MLEvolver의 공식 구현이나 재현이라고 부르지 않는다.

## Navigation

- [[tech/ai/autoresearch-harness-design/README|학습 진입점]]

## Sources

- https://arxiv.org/abs/2611.28244
- https://doi.org/10.48550/arXiv.2611.28244
