---
date: 2026-11-27
tags: [tech]
type: tech-tool-study
status: draft
---

# Cheatsheet

## 먼저 정할 다섯 가지

| 항목 | 기록 내용 |
|---|---|
| Query | 관찰 반응 / 원하는 반응 |
| Candidate | 실험 / compound / target |
| Relevance | 유사 / 반대 / 알려진 연결 |
| Context | 세포 유형·농도·시간·control |
| Output | 순위·실험 근거·불확실성 |

## 검색 흐름

```text
metadata 확인 → QC → signature 생성 → 조건 필터
→ baseline 벡터 비교 → Top-K → 근거·안정성 확인
```

- Cosine: `(q · x) / (||q|| ||x||)`; 0 벡터는 정의되지 않는다.
- 같은 방향 검색: cosine 내림차순. 반대 방향 검색: 목적을 명시하고 별도 평가.
- Scale·전처리는 결과에 영향을 준다. 전처리 fit은 학습 데이터에서만 수행.
- Score는 확률·효능·작용 강도가 아니다.

## 검토 체크리스트

- [ ] Cell-level을 single-cell로 단정하지 않았는가?
- [ ] Target·compound 매핑의 근거가 있는가?
- [ ] 결측을 추정해 채우지 않았는가?
- [ ] Replicate·identity 중복과 split 누수를 확인했는가?
- [ ] 실험 행과 후보 단위 평가를 구분했는가?
- [ ] Recall@K 등의 relevance 정의와 분모가 명확한가?
- [ ] Control·replicate 변경 시 순위 안정성을 확인했는가?
- [ ] 유사성·생물학적 관련성·인과 관계를 구분했는가?

## 확인 한계

실제 논문의 modality, 모델, 데이터셋, 도구, 성능, URL은 제공되지 않았다. 합성 실습은 검색 계산만 설명한다.

## 연결

[[tech/ai/perturbation-signature-retrieval/README|학습 지도]] · [[tech/ai/perturbation-signature-retrieval/03-references|근거 상태]] · [[tech/ai/perturbation-signature-retrieval/04-learning/01-getting-started|실행 예제]]

## Sources

- 사용자 제공 dossier: 영상 00:47에 주제의 논문 제목이 표시되었다는 설명. 영상 및 논문 URL은 제공되지 않아 기재할 수 없다.
- 아래 설계·실습은 dossier를 바탕으로 만든 학습용 제안이며, 원 논문의 구현 또는 검증 결과가 아니다.
