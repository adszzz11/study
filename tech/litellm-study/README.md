# LiteLLM 학습 가이드

> 100+ LLM 프로바이더를 단일 API로 통합하는 오픈소스 게이트웨이

## 목차

1. [[01-overview|개요]] - 핵심 개념, 장단점, 사용 사례
2. [[02-ecosystem|에코시스템]] - 관련 기술, 비교, 트렌드
3. [[03-references|참고 자료]] - 공식 문서, 학습 자료, 커뮤니티
4. 학습 자료
   - [[04-learning/01-python-sdk|Python SDK 기본 사용]]
   - [[04-learning/02-proxy-server|프록시 서버 설정]]
   - [[04-learning/03-config-yaml|config.yaml 작성법]]
   - [[04-learning/04-providers|100+ 프로바이더 연결]]
   - [[04-learning/05-load-balancing|로드 밸런싱과 폴백]]
   - [[04-learning/06-budget-tracking|예산 관리와 모니터링]]
5. [[05-projects|실전 프로젝트]] - 프로젝트 예제, Best Practices
6. [[cheatsheet|치트시트]] - 빠른 참조

---

## Quick Start

### 1. 설치

```bash
pip install litellm
```

### 2. Python SDK로 바로 사용

```python
from litellm import completion
import os

os.environ["OPENAI_API_KEY"] = "your-api-key"

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "안녕하세요!"}]
)
print(response.choices[0].message.content)
```

### 3. 프록시 서버 실행

```bash
# 단일 모델로 빠르게 시작
litellm --model gpt-4o

# config 파일로 시작
litellm --config config.yaml
```

### 4. Docker로 실행

```bash
docker run -e OPENAI_API_KEY=your-key -p 4000:4000 ghcr.io/berriai/litellm:main-latest
```

---

## 학습 플랜

### 1주차: 기초 (예상 시간: 4-6시간)
- [ ] LiteLLM 개념 이해 ([[01-overview]])
- [ ] Python SDK 기본 사용법 익히기 ([[04-learning/01-python-sdk]])
- [ ] 여러 프로바이더 연결 테스트 ([[04-learning/04-providers]])

### 2주차: 프록시 서버 (예상 시간: 4-6시간)
- [ ] 프록시 서버 로컬 실행 ([[04-learning/02-proxy-server]])
- [ ] config.yaml 작성법 익히기 ([[04-learning/03-config-yaml]])
- [ ] 로드 밸런싱 설정 ([[04-learning/05-load-balancing]])

### 3주차: 운영 및 프로젝트 (예상 시간: 6-8시간)
- [ ] 예산 관리 및 모니터링 ([[04-learning/06-budget-tracking]])
- [ ] 실전 프로젝트 적용 ([[05-projects]])
- [ ] Docker 배포 실습

---

## 핵심 포인트

| 항목 | 설명 |
|------|------|
| 저장소 | [github.com/BerriAI/litellm](https://github.com/BerriAI/litellm) |
| 문서 | [docs.litellm.ai](https://docs.litellm.ai) |
| 지원 프로바이더 | 100+ (OpenAI, Anthropic, Azure, Bedrock, Ollama 등) |
| API 형식 | OpenAI 호환 |
| 사용 방식 | Python SDK / Proxy Server |
| 월간 다운로드 | 47만+ |

---

## 왜 LiteLLM인가?

```
┌─────────────────────────────────────────────────────────────┐
│                      Your Application                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        LiteLLM                               │
│  - 통합 API 인터페이스                                        │
│  - 자동 폴백 & 로드 밸런싱                                    │
│  - 비용 추적 & 예산 관리                                      │
│  - 가상 키 관리                                               │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────┬──────────┼──────────┬─────────┐
        ▼         ▼          ▼          ▼         ▼
    ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
    │OpenAI │ │Claude │ │Azure  │ │Bedrock│ │Ollama │
    └───────┘ └───────┘ └───────┘ └───────┘ └───────┘
```

---

## 학습 전 준비사항

- Python 3.8+ 설치
- 최소 1개 이상의 LLM API 키 (OpenAI, Anthropic 등)
- Docker (선택사항, 프록시 서버 배포 시)
- 터미널/명령줄 기본 사용법

---

## 관련 학습 자료

- [[../python/README|Python 기초]]
- [[../docker/README|Docker 기초]]
