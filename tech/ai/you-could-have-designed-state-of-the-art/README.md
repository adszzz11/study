---
date: 2026-06-18
tags:
  - tech
  - ai
  - transformer
  - positional-encoding
  - rope
status: learning
type: tech-tool-study
---

# You could have designed state of the art positional encoding

> **한 줄 정의**: Transformer의 `positional encoding`은 permutation-equivariant한 self-attention에 token 순서와 거리 정보를 주입하는 메커니즘이며, 현대 LLM에서는 `RoPE`와 RoPE scaling 변형이 사실상 표준 축이다.

## 개요

Hugging Face 글 [You could have designed state of the art positional encoding](https://huggingface.co/blog/designing-positional-encoding)은 positional encoding을 “외워야 하는 공식”이 아니라 직접 설계해 볼 수 있는 문제로 풀어낸다.

출발점은 간단하다. Self-attention은 token sequence를 보지만, positional signal이 없으면 같은 token이 서로 다른 위치에 있을 때 둘을 안정적으로 구분하기 어렵다. 그래서 글은 다음 순서로 개선한다.

- `integer encoding`: 위치 번호를 직접 더한다.
- `binary encoding`: 값 범위와 uniqueness를 개선한다.
- `sinusoidal positional encoding`: smooth하고 deterministic한 encoding을 만든다.
- `relative position`: absolute index보다 token 간 거리 관계에 집중한다.
- `RoPE`: `Q`와 `K`를 position-dependent rotation으로 회전시켜 dot product 안에 relative position을 넣는다.
- `nD RoPE`: image, video, audio처럼 다차원 좌표계로 확장한다.

```text
No position
  -> absolute additive position
  -> smooth sinusoidal position
  -> relative distance in attention
  -> rotary Q/K position
  -> RoPE scaling and nD extensions
```

---

## 학습 경로

### 1단계: 문제의식 잡기

- [ ] [[01-overview|개요]] 읽기 - self-attention이 왜 위치를 모르는지 이해
- [ ] `permutation equivariance`, `absolute position`, `relative position` 구분
- [ ] 같은 token이 다른 위치에 있을 때 attention output이 왜 같아질 수 있는지 설명해 보기

### 2단계: positional encoding 계보 비교

- [ ] [[02-ecosystem|생태계/비교]]에서 learned absolute, sinusoidal, relative, ALiBi, RoPE 비교
- [ ] `embedding에 더하는 방식`과 `attention score/QK에 넣는 방식` 구분
- [ ] [[study/tech/ai/ai-ecosystem]] 안에서 LLM architecture component로 위치시키기

### 3단계: 원문과 핵심 논문 확인

- [ ] [[03-references|참고자료]]에서 Hugging Face 원문, Transformer, RoFormer, ALiBi, RoPE scaling 논문 확인
- [ ] RoPE가 `absolute position tracking`과 `relative relationship modeling`을 동시에 하는 이유 정리
- [ ] 2026년 RoPE 한계 연구의 키워드: aliasing, base, precision, locality bias

### 4단계: 직접 구현하며 이해

- [ ] [[04-learning/01-getting-started|시작하기]] - sinusoidal PE와 RoPE의 최소 구현
- [ ] [[04-learning/02-deep-dive|심화]] - RoPE dot product, scaling, nD extension, long-context failure mode
- [ ] `rotate_half`, `cos/sin cache`, `position_ids`가 실제 구현에서 하는 역할 확인

### 5단계: 실전 적용

- [ ] [[05-projects|실전 프로젝트]] - PE 시각화, RoPE scaling 실험, nD RoPE toy ViT 만들기
- [ ] [[cheatsheet|치트시트]] - 공식, 선택 기준, 구현 체크리스트 빠른 참조

---

## 파일 구조

```text
you-could-have-designed-state-of-the-art/
├── README.md
├── 01-overview.md
├── 02-ecosystem.md
├── 03-references.md
├── 04-learning/
│   ├── 01-getting-started.md
│   └── 02-deep-dive.md
├── 05-projects.md
└── cheatsheet.md
```

## 바로가기

| 단계 | 파일 | 설명 |
|------|------|------|
| 개요 | [[01-overview]] | What/Why, 핵심 특징, 설계 흐름 |
| 비교 | [[02-ecosystem]] | positional encoding 방식별 장단점 |
| 참고자료 | [[03-references]] | 원문, 논문, 문서, 추가 읽을거리 |
| 시작하기 | [[04-learning/01-getting-started]] | sinusoidal PE와 RoPE 최소 구현 |
| 심화 | [[04-learning/02-deep-dive]] | RoPE 수식, scaling, long context 이슈 |
| 프로젝트 | [[05-projects]] | 실험 과제와 구현 아이디어 |
| 치트시트 | [[cheatsheet]] | 공식/선택 기준/주의점 요약 |

---

## 관련 노트

- [[study/tech/ai/ai-ecosystem]] - Transformer/LLM 구성요소를 AI 생태계 안에서 배치
- [[study/tech/ai/litellm]] - long-context model을 provider/router 관점에서 선택할 때 연결
- [[study/tech/ai/model-context-protocol-mcp]] - 긴 context를 tool/resource와 어떻게 분리할지 비교
- [[study/tech/ai/llm-wiki-study]] - 긴 문서/노트 처리에서 context window와 retrieval 설계 연결

---

**생성일**: 2026-06-18  
**상태**: 학습 중
