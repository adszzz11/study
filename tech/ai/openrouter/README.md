# OpenRouter 학습 가이드

> 500+ LLM 모델을 단일 API로 사용하는 통합 AI 게이트웨이

## 목차

### 기본 개념
- [[01-overview|개요]] - 핵심 개념, 장단점, 사용 사례
- [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
- [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티

### 실습 학습
- [[04-learning/01-quickstart|Quick Start]] - API 키 발급 및 첫 요청
- [[04-learning/02-models|모델 선택]] - 모델 선택 및 라우팅
- [[04-learning/03-openai-sdk|OpenAI SDK 사용]] - OpenAI SDK로 사용하기
- [[04-learning/04-routing-variants|라우팅 변형]] - :nitro, :floor 등
- [[04-learning/05-multimodal|멀티모달]] - 이미지, PDF 처리
- [[04-learning/06-cost-management|비용 관리]] - 비용 관리 및 BYOK

### 응용
- [[05-projects|실전 프로젝트]] - 프로젝트, Best Practices
- [[cheatsheet|치트시트]] - 빠른 참조

---

## Quick Start

### 1. API 키 발급
1. [openrouter.ai](https://openrouter.ai) 접속
2. Google/GitHub로 로그인
3. Keys 메뉴에서 API 키 생성
4. 크레딧 충전 (최소 $5)

### 2. 첫 API 호출

```python
import openai

client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."  # OpenRouter API 키
)

response = client.chat.completions.create(
    model="anthropic/claude-sonnet-4",
    messages=[{"role": "user", "content": "안녕하세요!"}]
)

print(response.choices[0].message.content)
```

### 3. curl로 테스트

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "anthropic/claude-sonnet-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 학습 플랜

### Week 1: 기초 (3-4시간)
| 일차 | 주제 | 학습 내용 |
|-----|------|----------|
| Day 1 | 개요 이해 | OpenRouter란?, 장단점, 사용 사례 |
| Day 2 | 환경 설정 | 계정 생성, API 키 발급, 첫 요청 |
| Day 3 | 모델 탐색 | 주요 모델 비교, 모델 선택 기준 |

### Week 2: 핵심 기능 (4-5시간)
| 일차 | 주제 | 학습 내용 |
|-----|------|----------|
| Day 4 | OpenAI SDK | baseURL 변경, 기존 코드 마이그레이션 |
| Day 5 | 라우팅 변형 | :nitro, :floor, :free, :thinking |
| Day 6 | 멀티모달 | 이미지 분석, PDF 처리 |
| Day 7 | 비용 관리 | 가격 비교, BYOK 설정 |

### Week 3: 실전 적용 (5-6시간)
| 일차 | 주제 | 학습 내용 |
|-----|------|----------|
| Day 8-9 | 미니 프로젝트 | 챗봇 만들기, 폴백 구현 |
| Day 10 | 최적화 | 비용 최적화, 모델 라우팅 전략 |

---

## 핵심 포인트

```
OpenRouter = LLM 라우터 + 마켓플레이스

특징:
- 500+ 모델 단일 API
- OpenAI API 100% 호환
- 자동 폴백/로드밸런싱
- 라우팅 변형 (속도/비용/무료)
- BYOK 지원 (5% 수수료)
```

---

## 관련 노트

- [[LLM-기초]]
- [[OpenAI-API]]
- [[LangChain]]
