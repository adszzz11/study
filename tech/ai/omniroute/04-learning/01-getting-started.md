---
date: 2026-07-31
tags: [tech]
type: tech-tool-study
status: draft
---

# OmniRoute Getting Started

> [[../README|목차로 돌아가기]] · [[02-deep-dive|다음: Deep Dive]]

## 학습 목표

- local OmniRoute를 실행하고 dashboard와 `/v1` API를 확인한다.
- 최소 한 개의 provider connection을 만들고 `auto`로 첫 요청을 보낸다.
- OpenAI-compatible client의 `base_url`만 바꿔 호출한다.
- production 전에 credential encryption과 network exposure를 점검한다.

## 1. 설치 방식 선택

| 방식 | 적합한 경우 | 핵심 명령 |
|---|---|---|
| npm global | local 학습, CLI 사용 | `npm install -g omniroute` |
| Docker | runtime과 data volume 격리 | `docker run ... diegosouzapw/omniroute:latest` |
| source | code 탐색, contribution | `npm install && npm run dev` |

### npm으로 시작

```bash
npm install -g omniroute
omniroute
```

- Dashboard: `http://localhost:20128`
- API base URL: `http://localhost:20128/v1`

설치 직후 진단이 필요하면 CLI의 doctor 명령을 사용한다.

```bash
omniroute doctor
```

### Docker로 시작

```bash
docker run -d \
  --name omniroute \
  --restart unless-stopped \
  --stop-timeout 40 \
  -p 127.0.0.1:20128:20128 \
  -v omniroute-data:/app/data \
  diegosouzapw/omniroute:latest
```

`127.0.0.1` binding은 local 학습용 안전한 기본값이다. remote access가 필요하면 port를 무작정 public으로 열지 말고 TLS reverse proxy, dashboard auth, API key scope를 함께 설계한다. 재현 가능한 운영 환경에서는 `latest` 대신 검증한 image version을 pin한다.

## 2. Storage encryption 먼저 설정

OmniRoute는 credential을 SQLite에 저장한다. `STORAGE_ENCRYPTION_KEY`가 없으면 plaintext passthrough mode이므로 실제 account를 연결하기 전에 encryption key를 준비한다.

```bash
openssl rand -hex 32
```

생성 결과는 password manager나 secret manager에 보관하고 runtime의 `STORAGE_ENCRYPTION_KEY`로 주입한다. key 값을 shell history, source control, 이 노트에 붙여 넣지 않는다.

> [!WARNING]
> encryption key를 분실하면 암호화된 credential을 복구할 수 없을 수 있다. database backup과 key backup은 분리해 관리한다.

## 3. Provider 연결

1. Dashboard의 **Providers**로 이동한다.
2. 학습에 사용할 provider 하나를 선택한다.
3. 공식 API key 또는 OAuth flow로 connection을 만든다.
4. connection health와 사용 가능한 model을 확인한다.
5. Dashboard의 **Endpoints**에서 client용 API key를 발급·복사한다.

처음에는 account 하나와 model 하나로 direct call을 확인한 뒤 `auto`를 테스트한다. 여러 account를 한꺼번에 추가하면 authentication 실패와 routing 실패를 구분하기 어렵다.

## 4. API smoke test

### Model catalog

```bash
curl http://localhost:20128/v1/models \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY"
```

### Chat Completions

```bash
curl http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [
      {"role": "user", "content": "한 문장으로 OmniRoute를 설명해줘."}
    ]
  }'
```

### Streaming

```bash
curl --no-buffer http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/fast",
    "stream": true,
    "messages": [
      {"role": "user", "content": "짧은 테스트 응답을 생성해줘."}
    ]
  }'
```

## 5. OpenAI SDK 연결

client의 model SDK를 다시 작성하지 않고 `base_url`과 gateway API key를 바꾼다.

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key="YOUR_OMNIROUTE_KEY",
)

response = client.chat.completions.create(
    model="auto/coding",
    messages=[
        {"role": "user", "content": "Python binary search를 작성해줘."}
    ],
)

print(response.choices[0].message.content)
```

## 6. Routing 결과 관찰

completion response의 `X-OmniRoute-Decision` header는 strategy, provider alias, latency 정보를 제공한다. 여러 번 호출해 route가 어떻게 달라지는지 기록한다.

```bash
curl -i http://localhost:20128/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OMNIROUTE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto/cheap",
    "messages": [{"role": "user", "content": "ping"}]
  }'
```

관찰할 항목:

- HTTP status와 streaming 종료 여부
- `X-OmniRoute-Decision`
- 선택된 provider/model/connection
- input·output token과 추정 cost
- latency
- dashboard call log의 error와 fallback 기록

## 7. 첫 학습 실험

| 실험 | 변경 | 예상 관찰 |
|---|---|---|
| Balanced | `model: auto` | last-known-good 성향의 균형 route |
| Coding | `model: auto/coding` | coding 적합도를 더 중시 |
| Fast | `model: auto/fast` | latency weight 증가 |
| Cheap | `model: auto/cheap` | token cost weight 증가 |
| Offline | `model: auto/offline` | quota headroom 중시 |

같은 prompt를 각 variant로 5회 이상 호출하되, model quality 결론을 내리기보다 **routing decision과 실패 처리**가 policy 설명과 일치하는지 본다.

## 완료 체크리스트

- [ ] Dashboard와 `/v1/models`에 접속했다.
- [ ] `STORAGE_ENCRYPTION_KEY`를 secret으로 주입했다.
- [ ] provider connection 하나를 연결했다.
- [ ] direct model과 `auto` 호출을 각각 성공했다.
- [ ] streaming response를 확인했다.
- [ ] OpenAI SDK에서 `base_url`을 바꿔 호출했다.
- [ ] `X-OmniRoute-Decision`과 dashboard telemetry를 확인했다.
- [ ] 외부 provider 사용 시 prompt가 upstream으로 전달됨을 이해했다.

## Troubleshooting

| 증상 | 먼저 볼 것 |
|---|---|
| `/v1/models`가 비어 있음 | provider connection 상태, OAuth token, model catalog |
| `401` | Dashboard에서 발급한 endpoint key, `Bearer` header |
| `429` 반복 | account quota, reset window, 후보 connection 수 |
| streaming 중단 | client SSE 지원, proxy buffering, upstream 상태 |
| `auto`가 예상과 다른 target 선택 | candidate pool, health, quota, pricing, latency telemetry |
| 재시작 후 credential 문제 | volume mount, SQLite file, encryption key 일치 |

## Sources

- https://github.com/diegosouzapw/OmniRoute#-quick-start
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/API_REFERENCE.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/SECURITY.md
- https://github.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/guides/DOCKER_GUIDE.md
