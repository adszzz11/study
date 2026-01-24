---
date: 2026-01-24
tags:
  - tech
  - basics
  - claude
  - ai
parent: "[[README]]"
---

# Claude - 기초

> ⬅️ [[README|목차로 돌아가기]] | ➡️ [[02-api|다음: API]]

---

## 1. What - 개념 정의

> **한 줄 정의**: Anthropic이 Constitutional AI 방식으로 훈련한 대화형 AI 모델

### 핵심 개념

- **Constitutional AI**: 헌법(원칙)에 기반한 AI 훈련 방식
- **RLHF (Reinforcement Learning from Human Feedback)**: 인간 피드백 기반 강화학습
- **Context Window**: 한 번에 처리 가능한 토큰 수

### Claude 모델 종류

| 모델 | 특징 | 용도 |
|------|------|------|
| **Claude Opus 4.5** | 최고 성능, 깊은 사고 | 복잡한 분석, 코딩 |
| **Claude Sonnet 4** | 균형잡힌 성능 | 일반 업무, 코딩 |
| **Claude Haiku 3.5** | 빠른 속도, 저비용 | 단순 작업, 분류 |

### 주요 용어

| 용어 | 설명 |
|------|------|
| Token | 텍스트의 최소 처리 단위 (약 4글자 = 1토큰) |
| Context Window | 입력+출력 합계 토큰 한도 (200K tokens) |
| Temperature | 응답의 무작위성 (0=결정적, 1=창의적) |
| System Prompt | AI의 역할/행동을 정의하는 지시문 |

---

## 2. Why - 등장 배경

### Anthropic 설립 배경

- OpenAI 출신 연구원들이 2021년 설립
- AI 안전성 연구에 중점
- "안전하고 유익한 AI" 개발 목표

### 해결하려는 문제

- AI의 유해한 출력 방지
- 편향성 감소
- 투명하고 예측 가능한 AI 행동

### Constitutional AI vs 기존 방식

| 문제     | 기존 RLHF   | Constitutional AI |
| ------ | --------- | ----------------- |
| 학습 데이터 | 인간 라벨러 의존 | 원칙 기반 자기 개선       |
| 확장성    | 비용 높음     | 자동화 가능            |
| 일관성    | 라벨러마다 다름  | 원칙 기반 일관성         |

---

## 3. 핵심 특징

### 장점

- ✅ 긴 컨텍스트 (200K tokens)
- ✅ 뛰어난 코딩 능력
- ✅ 안전성 및 윤리적 가드레일
- ✅ 정확한 지시 따르기
- ✅ 한국어 지원 우수

### 단점

- ❌ 실시간 정보 접근 불가 (학습 데이터 기준)
- ❌ 이미지 생성 불가
- ❌ 인터넷 검색 제한적

---

## 4. Constitutional AI 원리

### 작동 방식

```
1. 초기 모델이 응답 생성
   ↓
2. 원칙(Constitution)에 따라 자기 비평
   ↓
3. 비평 기반으로 응답 수정
   ↓
4. 수정된 데이터로 재학습
```

### 주요 원칙 예시

- 유해한 내용 생성하지 않기
- 정직하게 답변하기
- 불확실할 때 인정하기
- 편향 없이 균형잡힌 시각 제공

---

## 다음 단계

> [!tip] 다음으로
> 기초 개념을 이해했다면 [[02-api|Claude API]]로 넘어가세요.

---

## References

- [Anthropic 공식 사이트](https://www.anthropic.com/)
- [Claude 모델 비교](https://www.anthropic.com/claude)
- [Constitutional AI 논문](https://arxiv.org/abs/2212.08073)
