# 4-4. Claude / Gemini 라우팅 (LiteLLM)

## 🌉 LiteLLM 게이트웨이 패턴

OpenAI Agents SDK는 OpenAI API만 직접 지원. 다른 LLM은 LiteLLM proxy로 가운데에 둠.

```bash
pip install litellm
litellm --model anthropic/claude-opus-4-7 --port 4000
```

또는 config 파일:
```yaml
# litellm-config.yaml
model_list:
  - model_name: claude-opus
    litellm_params:
      model: anthropic/claude-opus-4-7
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-2.0-pro
```

```bash
litellm --config litellm-config.yaml --port 4000
```

## 🔌 Agency Swarm에 연결

```python
import openai

# OpenAI 호환 endpoint를 LiteLLM proxy로
openai.base_url = "http://localhost:4000/v1"
openai.api_key = "anything"

class Developer(Agent):
    def __init__(self):
        super().__init__(
            name="Developer",
            model="claude-opus",   # LiteLLM에 등록된 이름
            ...
        )
```

## 🎯 직원별 다른 모델

```python
CEO(model="claude-opus-4-7")              # 비싼 모델로 통합 응대
Developer(model="claude-sonnet-4-6")       # 중간
VA(model="ollama/qwen2.5:14b")             # 로컬, 비용 0
```

## 💰 비용 통제

LiteLLM에서:
- 사용량 한도 설정
- 모델별 fallback (Opus 실패 시 Sonnet)
- caching (같은 prompt 캐싱)

→ Paperclip 예산과 결합하면 이중 통제.

## ✅ 체크포인트
- [ ] LiteLLM proxy 동작
- [ ] Agency Swarm 직원이 Claude 응답 받음
- [ ] 직원별 다른 모델 라우팅
- [ ] LiteLLM 로그에서 사용량 확인

## 🔗 본 vault 내
- [[study/tech/ai/litellm]] — LiteLLM 깊이
- 다음 → [../05-projects.md](../05-projects.md)
