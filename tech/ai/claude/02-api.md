# Claude API 변경사항

> 출처: https://platform.claude.com/docs/en/release-notes/overview

---

## 2026-06-09 업데이트

### Adaptive Thinking (Fable 5 / Mythos 5)

- Fable 5와 Mythos 5에서 adaptive thinking은 유일한 thinking 모드
- `thinking: {"type": "disabled"}` → **400 에러**
- `thinking.display` 기본값: `"omitted"` (Opus 4.8, Opus 4.7, Mythos Preview와 동일)
  - 요약 수신: `display: "summarized"` 설정
  - raw chain of thought는 절대 반환 안 됨

```python
# Fable 5 올바른 사용 예
response = client.messages.create(
    model="claude-fable-5",
    max_tokens=4096,
    thinking={"type": "adaptive", "display": "summarized"},
    messages=[{"role": "user", "content": "..."}]
)
```

### Refusal 처리 & Fallbacks (Beta)

```python
# fallbacks 파라미터 (beta)
response = client.messages.create(
    model="claude-fable-5",
    max_tokens=1024,
    fallbacks=[{"model": "claude-opus-4-8"}],  # beta
    messages=[{"role": "user", "content": "..."}]
)

# 거부 감지
if response.stop_reason == "refusal":
    category = response.stop_details.category  # "cyber", "bio", "reasoning_extraction"
    explanation = response.stop_details.explanation
```

- 출력 전 거부 시 **과금 없음**
- `fallbacks`: Message Batches API 미지원

### Claude Managed Agents 업데이트

#### 1. Scheduled Deployments

- cron 스케줄로 세션 자동 실행 가능
- 별도 스케줄러 없이 배포 가능
- 참고: https://platform.claude.com/docs/en/managed-agents/scheduled-deployments

#### 2. Vault 환경 변수 자격증명

- `env_var` 타입 자격증명 추가 — CLI, SDK 등 환경변수 인증 서비스에 시크릿 주입
- 참고: https://platform.claude.com/docs/en/managed-agents/vaults

#### 3. Webhook session_thread_id

- `session.thread_*` 이벤트에 `session_thread_id` 필드 추가
- 멀티 에이전트 스레드 추적 가능

---

## 2026-06-05 업데이트

- `claude-opus-4-1-20250805` deprecation 발표 → 2026-08-05 은퇴

---

## 2026-06-02 업데이트

### Advisor Tool max_tokens

- advisor tool 정의에 `tools[].max_tokens` 설정 가능
- advisor 모델의 응답 길이 제한 → 레이턴시·비용 절감
- 참고: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool

### Refusal 과금 정책 변경

- `stop_reason: "refusal"` 이고 출력이 없으면 **과금 없음** (GA)

---

## 데이터 보존 요구사항

| 모델 | 최소 보존 기간 |
|------|-------------|
| `claude-fable-5` | 30일 (zero data retention 불가) |
| 기타 모델 | 일반 정책 적용 |
