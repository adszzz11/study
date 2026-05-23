# 4-1. Dify 셀프호스팅 (Mac mini)

> 시간 ~20분. 결과: localhost에서 Dify Studio 접속.

## 📌 컨테이너 구성

Dify Docker Compose가 띄우는 것:
- `api` — Python 백엔드
- `worker` — Celery 워커 (RAG 인덱싱)
- `web` — Next.js 프론트
- `nginx` — 리버스 프록시
- `db` (Postgres)
- `redis` (캐시·큐)
- `weaviate` — 벡터DB
- `sandbox` — 코드 실행 격리

총 7-8개 컨테이너. **메모리 4GB+ 권장**.

## 💻 셋업

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
cp .env.example .env

# 환경 변수 편집 (포트·시크릿)
vim .env
#   NGINX_PORT=80              # 기본
#   DB_PASSWORD=<랜덤>
#   REDIS_PASSWORD=<랜덤>
#   SECRET_KEY=$(openssl rand -hex 32)
#   ALLOW_REGISTRATION=false    # 외부 등록 차단
#   INIT_PASSWORD=<관리자 초기 비번>

docker compose up -d

# 헬스체크
docker compose ps
curl http://localhost/health
```

브라우저 `http://localhost` → 관리자 계정 생성.

## 🔑 첫 LLM 설정

대시보드 → Settings → Model Provider:
- OpenAI: API Key + base URL
- Anthropic: API Key
- Ollama: base URL `http://host.docker.internal:11434`
- Cohere (rerank용)

## 📦 첫 Knowledge Base

대시보드 → Knowledge → Create:
1. 문서 업로드 (PDF/DOCX/MD/TXT)
2. 청킹 모드 — Automatic 또는 Custom
3. 인덱싱 (백그라운드 worker가 처리)
4. Embedding 모델 선택

## ✅ 체크포인트
- [ ] `docker compose ps` 모든 컨테이너 healthy
- [ ] 관리자 로그인
- [ ] LLM Provider 등록 + 테스트 성공
- [ ] KB 1개 생성 + 문서 1개 인덱싱 완료

## ⚠️ 함정

| 증상 | 원인 |
|------|------|
| Weaviate OOM | RAM 4GB+ 필요. Mac mini 16GB 권장 |
| Nginx 80 충돌 | `.env`에서 `NGINX_PORT=8088` 같은 다른 포트 |
| Worker 인덱싱 멈춤 | `docker compose logs worker` 확인. embedding 키 |
| Mac에서 host.docker.internal | OrbStack/Docker Desktop 자동 지원, Linux는 extra_hosts |
| 외부 노출 위험 | 기본 0.0.0.0 — Tailscale로 격리 |

## 🛡️ 보안 기본
- `.env` chmod 600
- ALLOW_REGISTRATION=false
- Tailscale 안에서만 접근
- 정기 백업: `docker compose exec db pg_dump …`

## 🔗 다음 → [02-workflow.md](02-workflow.md)
