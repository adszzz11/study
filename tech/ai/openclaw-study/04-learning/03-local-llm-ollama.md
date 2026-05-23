# 4-3. Ollama 로컬 LLM을 OpenClaw 백엔드로 붙이기

> 시간 ~20분. 결과: API 비용 0원, 인터넷 안 끊겨도 동작하는 Llama/Qwen 기반 비서.

## 📌 핵심 개념

OpenClaw는 LLM 호출을 **OpenAI 호환 API**로 추상화한다. Ollama가 같은 인터페이스를 제공하므로 그냥 base URL만 바꿔주면 동작한다.

```
OpenClaw ──HTTP──► OpenAI-compatible endpoint
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
         OpenAI Cloud         Ollama (localhost:11434)
         (api.openai.com)     (M4 Pro에서 직접 추론)
```

### 언제 로컬 모델이 좋고, 언제 클라우드가 좋은가

| 작업 | 추천 |
|------|------|
| 가벼운 분류·요약 | 로컬 (Llama 3.2 8B) |
| 단순 라우팅·tool 선택 | 로컬 (8B로 충분) |
| 긴 문서 분석·복잡 코드 | 클라우드 (Claude Opus 4.7) |
| 프라이버시 민감 데이터 | 로컬 강제 |
| 실시간 응답성 | 로컬 (35-80 t/s) |
| 최신 지식 필요 | 클라우드 (cutoff 신선) |

## 💻 셋업

### 1. Ollama 모델 풀

[01-mac-mini-setup.md](01-mac-mini-setup.md)에서 Ollama 설치는 끝났다고 가정.

```bash
# 추천 풀
ollama pull llama3.2:8b          # 빠름, 일반 대화
ollama pull qwen2.5:14b          # 균형, 코딩까지
ollama pull qwen2.5-coder:14b    # 코드 특화
ollama pull mxbai-embed-large    # 임베딩 (RAG용)

# (선택) M4 Pro 48GB 이상
ollama pull llama3.3:70b-instruct-q3_K_M  # 무겁지만 GPT-4 mini급

# 동작 확인
ollama list
ollama run llama3.2:8b "한 줄로 자기소개해"
```

### 2. Ollama를 외부에서 접근 가능하게

기본은 127.0.0.1 바인딩. Docker 컨테이너에서 접근하려면 호스트 전체 바인딩 필요.

**Mac (Homebrew 서비스)**:

```bash
# 환경변수로 설정
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"

# Ollama 재시작
brew services restart ollama

# 또는 인터랙티브하게
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

> Tailnet 안에서만 외부 접근하기. 절대 인터넷에 직접 노출 금지. ([04-remote-and-hardening.md](04-remote-and-hardening.md))

### 3. OpenClaw .env에 Ollama 설정

```bash
# ~/openclaw/.env (추가)
OLLAMA_BASE_URL=http://host.docker.internal:11434
OPENCLAW_DEFAULT_MODEL=ollama/qwen2.5:14b
# 또는 일부 에이전트만 로컬로
```

`docker-compose.yml`에 (Linux 호스트인 경우):

```yaml
services:
  openclaw:
    extra_hosts:
      - "host.docker.internal:host-gateway"
```

### 4. config.yaml에서 모델 라우팅

```yaml
# ~/openclaw/.openclaw/config.yaml
models:
  local-fast:
    provider: ollama
    base_url: http://host.docker.internal:11434
    model: llama3.2:8b
  local-quality:
    provider: ollama
    base_url: http://host.docker.internal:11434
    model: qwen2.5:14b
  cloud-premium:
    provider: anthropic
    model: claude-opus-4-7

agents:
  default:
    # 단순 요청은 로컬, 복잡한 건 클라우드
    router:
      simple_classifier: local-fast
      default: local-quality
      escalation: cloud-premium
```

### 5. 재시작 + 테스트

```bash
docker compose restart openclaw

# 응답 시간 비교
time curl -s http://localhost:8080/api/chat -d '{
  "agent": "default",
  "message": "Hello"
}' | jq -r .reply
```

텔레그램에서 한 번 더 물어봐서 응답 속도/품질 비교.

## 🧪 벤치마크 (Mac mini M4 Pro 48GB 기준 — 참고치)

| 모델 | 컨텍스트 | TTFT | 토큰/s | 메모리 |
|------|---------|------|--------|--------|
| llama3.2:8b Q4 | 8K | 0.3s | 75 | 5GB |
| qwen2.5:14b Q4 | 16K | 0.5s | 45 | 9GB |
| qwen2.5-coder:14b | 16K | 0.5s | 42 | 9GB |
| llama3.3:70b Q3 | 8K | 2.1s | 7 | 30GB |
| MLX(Apple) llama3.2:8b | 8K | 0.2s | 95 | 5GB |

**팁**: Ollama 대신 `mlx-lm`(Apple 공식 MLX)를 쓰면 Apple Silicon에서 10-20% 더 빠름. 다만 OpenAI 호환 API는 wrapper 별도 필요.

## ✅ 체크포인트

- [ ] 호스트에서 `curl http://localhost:11434/api/tags` → 모델 리스트 응답
- [ ] 컨테이너 내부에서 `docker compose exec openclaw curl http://host.docker.internal:11434/api/tags` → 응답
- [ ] 텔레그램 첫 메시지 응답 시간이 5초 이내
- [ ] `Activity Monitor`에서 GPU 사용량 올라감 (메탈 가속 확인)

## ⚠️ 흔한 실수

| 증상 | 원인·해결 |
|------|----------|
| 컨테이너에서 host로 못 붙음 | `OLLAMA_HOST=0.0.0.0` 설정 + 재시작 |
| 모델 응답이 갑자기 끊김 | 컨텍스트 한도 초과. `num_ctx` 늘리거나 더 작은 모델로 |
| GPU 안 쓰고 CPU만 씀 | Ollama 최신 버전 + macOS 14+ 필요. `ollama --version` 확인 |
| 메모리 swap 폭주 | 모델 크기 + 다른 워크로드 > RAM. `ollama ps`로 로드된 모델 확인 후 `ollama stop` |
| Tool calling 결과 이상 | Llama 3.2/3.3은 tool calling 지원, Qwen 2.5는 잘됨. 그 외 모델은 한계 있음 |
| 한국어 품질 낮음 | `qwen2.5` 계열이 한국어 가장 잘됨. `gemma3` 도 검토 |

## 🧠 한국어 응답 품질 (체감 기준)

| 모델 | 한국어 자연스러움 | 문법 정확도 |
|------|----------|----------|
| qwen2.5:14b | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| llama3.3:70b | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| llama3.2:8b | ⭐⭐⭐ | ⭐⭐⭐ |
| gemma3:9b | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| claude-opus-4-7 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 💡 하이브리드 패턴 추천

> "단순한 건 로컬, 어려운 건 Claude"

```yaml
# config.yaml
agents:
  family:
    model: local-fast       # 가족 봇은 비용 0원
  work:
    model: cloud-premium    # 업무 봇은 Claude
  research:
    model: local-quality    # 평소엔 로컬
    escalate_when: "사용자가 '깊이 분석' 같은 키워드 사용"
    escalate_to: cloud-premium
```

비용 절감 효과: **월 메시지 5,000건 가정 → 로컬만 쓸 때 $0, 하이브리드 시 $10-20, 풀 클라우드 시 $50-100**.

## 🔗 다음 단계

- Tailscale로 외부에서 봇 접근 + 보안 강화 → [04-remote-and-hardening.md](04-remote-and-hardening.md)

## 참고

- [Ollama on Mac: Apple Silicon Setup Guide](https://localaimaster.com/blog/mac-local-ai-setup)
- [MLX-Powered Ollama on Apple Silicon](https://aiindigo.com/blog/mlx-powered-ollama-on-apple-silicon-a-deep-dive-into-local-ai-deployment)
- [ToolHalla: Best Local LLMs for Mac Mini M4 in 2026](https://toolhalla.ai/blog/best-local-llms-mac-mini-m4-2026)
