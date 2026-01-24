---
date: 2026-01-24
tags:
  - tech
  - advanced
  - claude
  - prompt-engineering
parent: "[[README]]"
---

# Claude - 심화

> ⬅️ [[03-claude-code|이전: Claude Code]] | [[README|목차]]

---

## 1. 프롬프트 엔지니어링

### 기본 원칙

1. **명확성**: 구체적이고 명확한 지시
2. **구조화**: 단계별로 나누어 요청
3. **예시 제공**: Few-shot 학습 활용
4. **역할 부여**: 페르소나 설정

### 효과적인 프롬프트 구조

```markdown
# 역할
당신은 [역할]입니다.

# 컨텍스트
[배경 정보]

# 작업
[구체적인 요청]

# 형식
[출력 형식 지정]

# 제약
[제한 사항]
```

### Few-shot 예시

```markdown
다음 형식으로 코드 리뷰를 작성해주세요:

예시 1:
입력: `if (x == null) return;`
출력: `x == null` 대신 `x === null`을 사용하세요 (strict equality)

예시 2:
입력: `var name = "test";`
출력: `var` 대신 `const` 또는 `let`을 사용하세요

이제 다음 코드를 리뷰해주세요:
[코드]
```

---

## 2. 고급 기법

### Chain of Thought (CoT)

```markdown
다음 문제를 단계별로 생각하며 풀어주세요:

1. 먼저 문제를 분석하세요
2. 가능한 접근법을 나열하세요
3. 각 접근법의 장단점을 비교하세요
4. 최적의 방법을 선택하고 구현하세요

문제: [복잡한 문제]
```

### Self-Consistency

여러 번 생각하게 하고 가장 일관된 답변 선택

```markdown
이 문제에 대해 3가지 다른 관점에서 분석하고,
가장 합리적인 결론을 도출해주세요.
```

### Tree of Thoughts

```markdown
다음 문제를 해결하기 위한 의사결정 트리를 만들어주세요.
각 분기점에서 장단점을 평가하고 최적 경로를 선택하세요.
```

---

## 3. Claude Agent SDK

### 개요

프로그래밍 방식으로 Claude 에이전트를 구축하는 SDK

### 설치

```bash
pip install anthropic-agent-sdk
```

### 기본 에이전트

```python
from anthropic_agent import Agent, Tool

# 도구 정의
@Tool
def search_database(query: str) -> str:
    """데이터베이스 검색"""
    # 구현
    return results

# 에이전트 생성
agent = Agent(
    model="claude-sonnet-4-20250514",
    tools=[search_database],
    system="당신은 데이터 분석가입니다."
)

# 실행
response = agent.run("최근 매출 데이터 분석해줘")
```

### 멀티 에이전트

```python
from anthropic_agent import Agent, Swarm

researcher = Agent(name="researcher", ...)
writer = Agent(name="writer", ...)
reviewer = Agent(name="reviewer", ...)

swarm = Swarm(agents=[researcher, writer, reviewer])
result = swarm.run("기술 블로그 작성해줘")
```

---

## 4. 비교 분석

### Claude vs GPT-4 vs Gemini

| 비교 항목 | Claude | GPT-4 | Gemini |
|-----------|--------|-------|--------|
| 컨텍스트 | 200K | 128K | 1M |
| 코딩 | 우수 | 우수 | 양호 |
| 안전성 | 매우 높음 | 높음 | 높음 |
| 가격 | 중간 | 높음 | 낮음 |
| 한국어 | 우수 | 우수 | 양호 |

### 선택 가이드

```
코딩 작업이 많다?
├── Yes → Claude Sonnet / GPT-4
└── No
    └── 긴 문서 처리?
        ├── Yes → Claude / Gemini
        └── No  → 비용 고려하여 선택
```

---

## 5. 프로덕션 고려사항

### Rate Limiting

| Tier | RPM | TPM |
|------|-----|-----|
| Free | 5 | 20K |
| Tier 1 | 50 | 40K |
| Tier 2 | 1000 | 80K |
| Tier 4 | 4000 | 400K |

### 에러 핸들링

```python
import anthropic
from anthropic import RateLimitError, APIError

try:
    response = client.messages.create(...)
except RateLimitError:
    # 재시도 로직
    time.sleep(60)
except APIError as e:
    # 에러 로깅
    logger.error(f"API Error: {e}")
```

### 비용 최적화

- 짧은 프롬프트 사용
- 캐싱 활용 (Prompt Caching)
- 적절한 모델 선택 (Haiku for 단순 작업)
- max_tokens 적절히 설정

---

## 6. Prompt Caching

### 개념

반복되는 시스템 프롬프트를 캐싱하여 비용 절감

### 사용법

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "긴 시스템 프롬프트...",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[...]
)
```

### 효과

- 캐시 히트 시 입력 토큰 비용 90% 절감
- 응답 속도 향상

---

## 7. 추가 학습

### 추천 자료

- [ ] [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [ ] [Claude API Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [ ] [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

### 관련 기술

- [[study/tech/http/pre/api-design|API 설계]]
- LangChain
- LlamaIndex

---

## 시리즈 완료

> [!success] 축하합니다!
> Claude 시리즈를 완료했습니다.
>
> **복습 권장**:
> - [[01-basics|기초]] - 모델 특징 복습
> - [[02-api|API]] - 코드 재실습
> - [[03-claude-code|Claude Code]] - CLI 활용

---

## References

- [Anthropic Docs](https://docs.anthropic.com/)
- [Claude Agent SDK](https://github.com/anthropics/anthropic-agent-sdk)
- [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
