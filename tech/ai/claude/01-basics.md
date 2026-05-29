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
| **Claude Opus 4.8** | 최신, SWE-Bench Pro 69.2%, 에이전틱 작업 강화 | 에이전틱 코딩, 금융 분석, 복잡한 추론 |
| **Claude Opus 4.7** | 1M context 표준가, 고해상도 비전, Task Budgets | 복잡한 분석, 코딩, 대용량 컨텍스트 |
| **Claude Sonnet 4.6** | 균형잡힌 성능, 1M context, extended thinking | 일반 업무, 코딩, 에이전틱 검색 |
| **Claude Haiku 4.5** | 빠른 속도, 저비용 | 단순 작업, 분류 |

> [!info] 2026-05-28 업데이트
> **Claude Opus 4.8** (`claude-opus-4-8`) 출시 — Opus 4.7과 동일 가격, Fast mode 3배 저렴, 2.5× 속도

> [!warning] Deprecation
> **Claude Haiku 3** (`claude-3-haiku-20240307`) 2026-04-19 에 retire 예정 → Claude Haiku 4.5로 마이그레이션 권장

### 🚨 Claude Mythos (2026-03-27 유출)

- Anthropic CMS 오류로 내부 자료가 외부에 노출되며 다음 모델 **"Claude Mythos"** (코드명 Capybara) 존재가 알려짐
- 현재 Claude 4.6 Opus 대비 프로그래밍/추론 작업에서 "dramatically" 성능 향상
- 특히 사이버보안 취약점 탐지에 탁월
- Opus 위의 **4번째 제품 티어**로 출시 예정, 초기에는 사이버보안 방어 목적 선별 고객에게만 제공
- 일반 공개 시점 미정

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

- ❌ 이미지 생성 불가
- ❌ 고급 모델일수록 비용 높음

### 업데이트 이력

| 날짜 | 내용 |
|------|------|
| 2026-03-27 | Claude Mythos 내부 자료 유출, Claude 4.6 모델 최대 output 128K 상향 |
| 2026-03-27 | Claude Haiku 3 deprecation 공지 (2026-04-19 retire) |

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
