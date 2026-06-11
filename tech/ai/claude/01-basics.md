# Claude 모델 개요

## 현재 모델 라인업 (2026-06-11 기준)

| 모델 ID | 설명 | 출시일 |
|---------|------|--------|
| `claude-fable-5` | Mythos-class, 일반 공개 최고 성능 모델 | 2026-06-09 |
| `claude-mythos-5` | Mythos-class, Project Glasswing 참가자 전용 | 2026-06-09 |
| `claude-opus-4-8` | 가장 강력한 GA 모델 (Fable 5 이전) | 2026-05-28 |
| `claude-opus-4-7` | 복잡한 추론·코딩에 최적 | 2026-04-16 |
| `claude-sonnet-4-6` | 속도와 성능의 균형 | 2026-02-17 |
| `claude-haiku-4-5` | 빠르고 경량 | 2025-10-15 |

---

## Claude Fable 5 & Mythos 5 (2026-06-09)

> 출처: https://platform.claude.com/docs/en/release-notes/overview

### 주요 특징

- **컨텍스트 윈도우**: 기본 1M 토큰 (최대 입력)
- **최대 출력**: 128k 토큰
- **Adaptive thinking**: 항상 활성화 (비활성화 불가)
- **Thinking display**: 기본값 `"omitted"` — 요약 보려면 `display: "summarized"` 설정

### 새 토크나이저 (Fable 5 / Mythos 5)

- Claude Opus 4.7에서 도입된 토크나이저 사용
- Opus 4.7 이전 모델 대비 **동일 텍스트가 약 30% 더 많은 토큰** 생성
- 마이그레이션 전 `model: "claude-fable-5"` 로 [Token Counting API](https://platform.claude.com/docs/en/build-with-claude/token-counting) 로 확인 필수

### Safety Classifiers & Refusal

```
stop_reason: "refusal"
```

- Fable 5는 요청 수신 시·응답 생성 중 safety classifier 실행
- 출력 생성 전 거부 시 **과금 없음**
- `fallbacks` 파라미터 (beta): 거부된 요청을 다른 모델로 재시도 (fallback 모델 요금 청구)
  - Claude API·Claude Platform on AWS에서 beta 지원
  - Message Batches API에서는 미지원

### stop_details.category 신규 값

| 값 | 설명 |
|----|------|
| `"cyber"` | 기존 — 사이버 공격 관련 거부 |
| `"bio"` | 기존 — 생물 무기 관련 거부 |
| `"reasoning_extraction"` | 신규 — 모델 출력 역공학/복제 시도 거부 |

> beta 헤더 불필요

### 주의사항

- `thinking: {"type": "disabled"}` **지원 안 함** → 400 에러
- manual extended thinking budget 및 assistant prefill **지원 안 함** → 400 에러
- 멀티턴 대화에서 thinking 블록은 **변경 없이 그대로 전달**해야 함
- **30일 데이터 보존 필수** — zero data retention에서 사용 불가

### 접근성

- `claude-fable-5`: 일반 공개 (GA)
- `claude-mythos-5`: Project Glasswing 초대 전용

---

## 모델 Deprecation 예정

| 모델 | 은퇴 예정일 |
|------|-----------|
| `claude-sonnet-4-20250514` | 2026-06-15 |
| `claude-opus-4-20250514` | 2026-06-15 |
| `claude-opus-4-1-20250805` | 2026-08-05 |

> 출처: https://platform.claude.com/docs/en/about-claude/model-deprecations
